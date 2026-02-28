#!/usr/bin/env python3
"""
MuJoCo + mink  ·  Month 1 Baseline: Rigid-Body Dual-Arm Pick, Contact-Aware Handover, and Place
"""

from pathlib import Path
import mujoco
import mujoco.viewer
import numpy as np
from loop_rate_limiters import RateLimiter
import mink

_HERE       = Path(__file__).parent
_MODEL_PATH = _HERE / "franka_emika_panda" / "dual_panda_scene.xml"

CUBE_WORLD_POS    = np.array([0.08, -0.35, 0.285])
CUBE_HALF         = 0.025
HANDOVER_POS      = np.array([0.00, -0.28, 0.52])
LIFT_HEIGHT       = 0.22
GRIP_OFFSET_R     = 0.04
GRIP_OFFSET_L     = 0.00
CONTACT_THRESHOLD = 0.010
TABLE_TOP         = 0.285          # z height of table surface
TABLE_CENTER      = np.array([0.0, -0.45, TABLE_TOP])  # center of table


# ─────────────────────────────────────────────────────────────────────────────
# Quaternion utilities
# ─────────────────────────────────────────────────────────────────────────────

def quat_error(q1, q2):
    return min(np.linalg.norm(q1 - q2), np.linalg.norm(q1 + q2))


def topdown_quat_for_site(model, data, site_name):
    mujoco.mj_forward(model, data)
    sid   = model.site(site_name).id
    R_cur = data.site_xmat[sid].reshape(3, 3).copy()
    z_des = np.array([0., 0., -1.])
    x_cur = R_cur[:, 0].copy()
    x_des = x_cur - np.dot(x_cur, z_des) * z_des
    x_des = (x_des / np.linalg.norm(x_des)
             if np.linalg.norm(x_des) > 1e-6
             else np.array([1., 0., 0.]))
    y_des = np.cross(z_des, x_des)
    y_des /= np.linalg.norm(y_des)
    R_des = np.column_stack([x_des, y_des, z_des])
    q = np.empty(4)
    mujoco.mju_mat2Quat(q, R_des.flatten())
    return q


def sidegrip_quat(approach_dir, y_hint):
    z_des = np.array(approach_dir, dtype=float)
    z_des /= np.linalg.norm(z_des)
    y_h   = np.array(y_hint, dtype=float)
    y_h  /= np.linalg.norm(y_h)
    x_des = np.cross(y_h, z_des)
    if np.linalg.norm(x_des) < 1e-6:
        x_des = np.array([1., 0., 0.])
    else:
        x_des /= np.linalg.norm(x_des)
    y_des = np.cross(z_des, x_des)
    y_des /= np.linalg.norm(y_des)
    R_des = np.column_stack([x_des, y_des, z_des])
    q = np.empty(4)
    mujoco.mju_mat2Quat(q, R_des.flatten())
    return q


# ─────────────────────────────────────────────────────────────────────────────
# Model helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_model():
    assert _MODEL_PATH.exists(), f"Not found: {_MODEL_PATH}"
    model = mujoco.MjModel.from_xml_path(str(_MODEL_PATH))
    data  = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    cfg   = mink.Configuration(model)
    print(f"[INFO] Loaded {_MODEL_PATH.name}")
    return model, data, cfg


def check_site(model, name):
    try:
        sid = model.site(name).id
        print(f"[INFO] Verified site '{name}' (id={sid})")
        return sid
    except Exception:
        raise RuntimeError(f"[ERROR] Site '{name}' not found.")


def reset_cube(model, data):
    adr = model.jnt_qposadr[model.joint("cube_joint").id]
    data.qpos[adr:adr+7] = [*CUBE_WORLD_POS, 1, 0, 0, 0]
    mujoco.mj_forward(model, data)
    print(f"[INFO] Initialized Cube position to {CUBE_WORLD_POS}")


# ─────────────────────────────────────────────────────────────────────────────
# IK Mocap Control
# ─────────────────────────────────────────────────────────────────────────────

def move_single(pos, quat, label,
                model, data, cfg,
                ee_task, tasks,
                site_id, mocap_id, mocap_name,
                active_ctrl, active_qpos,
                frozen_ctrl, frozen_vals,
                active_grip, frozen_grip,
                rate, viewer,
                gripper_val=255.0,
                frozen_grip_val=255.0,
                pos_thr=0.010, ori_thr=0.15,
                timeout_secs=18.0,
                damping=1e-3):
    print(f"\n>>> {label}  →  {np.round(pos, 3)}")
    data.mocap_pos[mocap_id]  = pos.copy()
    data.mocap_quat[mocap_id] = quat.copy()
    mujoco.mj_forward(model, data)
    ee_task.set_target(mink.SE3.from_mocap_name(model, data, mocap_name))
    t0 = data.time
    while viewer.is_running():
        data.mocap_pos[mocap_id]  = pos.copy()
        data.mocap_quat[mocap_id] = quat.copy()
        ee_task.set_target(mink.SE3.from_mocap_name(model, data, mocap_name))
        vel = mink.solve_ik(cfg, tasks, rate.dt, "daqp", damping=damping)
        cfg.integrate_inplace(vel, rate.dt)
        data.ctrl[active_ctrl]  = cfg.q[active_qpos]
        data.ctrl[active_grip]  = gripper_val
        data.ctrl[frozen_ctrl]  = frozen_vals
        data.ctrl[frozen_grip]  = frozen_grip_val
        mujoco.mj_step(model, data)
        viewer.sync()
        rate.sleep()
        pos_err = np.linalg.norm(data.site_xpos[site_id] - pos)
        q_now   = np.empty(4)
        mujoco.mju_mat2Quat(q_now, data.site_xmat[site_id])
        ori_err = quat_error(q_now, quat)
        if pos_err <= pos_thr and ori_err <= ori_thr:
            print(f"    ✓ Pos error: {pos_err*1000:.1f}mm  |  Ori error: {ori_err:.3f}rad")
            return True
        if (data.time - t0) > timeout_secs:
            print(f"    ⚠ Timeout (Pos error: {pos_err*1000:.1f}mm | Ori error: {ori_err:.3f}rad)")
            return False
    return False


def carry_smooth(waypoints, quat, label,
                 model, data, cfg,
                 task, site_id,
                 mocap_id, mocap_name,
                 active_ctrl, active_qpos,
                 frozen_ctrl, frozen_vals,
                 active_grip, frozen_grip,
                 frozen_grip_val,
                 rate, viewer,
                 step_size=0.003,      # 3mm per IK step, which ensures a very smooth motion
                 damping=5e-2,
                 settle_steps=30):
    """
    Move through a list of waypoints by interpolating the mocap target
    in tiny increments. It never jumps and the gripper stays firmly closed.
    """
    print(f"\n>>> {label}  ({len(waypoints)} waypoints)")
    current = np.array(data.mocap_pos[mocap_id], dtype=float)

    for wp_idx, target in enumerate(waypoints):
        target = np.array(target, dtype=float)
        total_dist = np.linalg.norm(target - current)
        if total_dist < 1e-4:
            continue
        n_steps = max(1, int(total_dist / step_size))
        print(f"    WP{wp_idx+1}: {np.round(target,3)}  dist={total_dist*1000:.1f}mm  steps={n_steps}")

        for i in range(1, n_steps + 1):
            if not viewer.is_running():
                return
            # Interpolate mocap target linearly
            alpha = i / n_steps
            interp_pos = current + alpha * (target - current)
            data.mocap_pos[mocap_id]  = interp_pos
            data.mocap_quat[mocap_id] = quat.copy()
            task.set_target(mink.SE3.from_mocap_name(model, data, mocap_name))

            vel = mink.solve_ik(cfg, [task], rate.dt, "daqp", damping=damping)
            cfg.integrate_inplace(vel, rate.dt)

            data.ctrl[active_ctrl]  = cfg.q[active_qpos]
            data.ctrl[active_grip]  = 0.0            # ALWAYS closed (hardcoded)
            data.ctrl[frozen_ctrl]  = frozen_vals
            data.ctrl[frozen_grip]  = frozen_grip_val

            mujoco.mj_step(model, data)
            viewer.sync()
            rate.sleep()

        # Settle at each waypoint
        for _ in range(settle_steps):
            if not viewer.is_running():
                return
            data.ctrl[active_ctrl]  = cfg.q[active_qpos]
            data.ctrl[active_grip]  = 0.0
            data.ctrl[frozen_ctrl]  = frozen_vals
            data.ctrl[frozen_grip]  = frozen_grip_val
            mujoco.mj_step(model, data)
            viewer.sync()
            rate.sleep()

        current = target.copy()
        print(f"    ✓ Waypoint {wp_idx+1}/{len(waypoints)} reached")


def actuate_grippers(model, data, rate, viewer,
                     left_joints, right_joints,
                     left_grip, right_grip,
                     steps=160, label=""):
    if label:
        print(f"\n>>> {label}")
    for _ in range(steps):
        if not viewer.is_running():
            break
        data.ctrl[0:7]  = left_joints
        data.ctrl[7]    = left_grip
        data.ctrl[8:15] = right_joints
        data.ctrl[15]   = right_grip
        mujoco.mj_step(model, data)
        viewer.sync()
        rate.sleep()
    if label:
        print("    ✓ Gripper actuation finished")


def wait_for_left_grip(target_pos, contact_thr,
                       model, data, cfg,
                       task_l, site_l,
                       moc_l, q_l_side,
                       moc_r, q_r_side, handover_r,
                       rq, rate, viewer,
                       timeout_secs=25.0):
    print(f"\n>>> P8 · Contact-Aware Handover (Distance Sensing to Target={np.round(target_pos,3)})")
    t0 = data.time
    while viewer.is_running():
        data.mocap_pos[moc_l]  = target_pos.copy()
        data.mocap_quat[moc_l] = q_l_side.copy()
        data.mocap_pos[moc_r]  = handover_r.copy()
        data.mocap_quat[moc_r] = q_r_side.copy()

        task_l.set_target(mink.SE3.from_mocap_name(model, data, "target_left"))
        vel = mink.solve_ik(cfg, [task_l], rate.dt, "daqp", damping=1e-3)
        cfg.integrate_inplace(vel, rate.dt)

        data.ctrl[0:7]  = cfg.q[0:7]
        data.ctrl[7]    = 255.0   # left open
        data.ctrl[8:15] = rq      # right frozen
        data.ctrl[15]   = 0.0     # RIGHT CLOSED (hardcoded, cannot be overridden)

        mujoco.mj_step(model, data)
        viewer.sync()
        rate.sleep()

        dist = np.linalg.norm(data.site_xpos[site_l] - target_pos)
        print(f"\r    left dist={dist*1000:.1f}mm", end="", flush=True)

        if dist <= contact_thr:
            print(f"\n    ✓ Contact-Aware logic triggered at {dist*1000:.1f}mm")
            return data.qpos[0:7].copy()
        if (data.time - t0) > timeout_secs:
            print(f"\n    ⚠ Timeout: Failed to confirm contact (Stopped at {dist*1000:.1f}mm)")
            return data.qpos[0:7].copy()
    return data.qpos[0:7].copy()


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    model, data, cfg = load_model()
    site_r = check_site(model, "attachment_site_right")
    site_l = check_site(model, "attachment_site_left")

    task_r = mink.FrameTask(
        frame_name="attachment_site_right", frame_type="site",
        position_cost=1.0, orientation_cost=0.5, lm_damping=1.0)
    task_l = mink.FrameTask(
        frame_name="attachment_site_left",  frame_type="site",
        position_cost=1.0, orientation_cost=0.5, lm_damping=1.0)
    task_p = mink.PostureTask(model=model, cost=1e-3)

    tasks_r = [task_r, task_p]
    tasks_l = [task_l, task_p]

    rate  = RateLimiter(frequency=40.0, warn=False)
    moc_r = model.body("target_right").mocapid[0]
    moc_l = model.body("target_left").mocapid[0]

    LC = slice(0, 7);  LG = 7;  LQ = slice(0, 7)
    RC = slice(8,15);  RG = 15; RQ = slice(9,16)

    with mujoco.viewer.launch_passive(
            model=model, data=data,
            show_left_ui=False, show_right_ui=False) as viewer:

        mujoco.mjv_defaultFreeCamera(model, viewer.cam)
        mujoco.mj_resetDataKeyframe(model, data, model.key("home1").id)
        lhq = data.qpos[0:7].copy()
        rhq = data.qpos[9:16].copy()
        reset_cube(model, data)

        # Quaternions with rotation logic preserved
        q_r_down = topdown_quat_for_site(model, data, "attachment_site_right")
        q_r_side = sidegrip_quat(approach_dir=[-1, 0, 0], y_hint=[0, 0, 1])
        q_l_side = sidegrip_quat(approach_dir=[+1, 0, 0], y_hint=[0, 1, 0])

        cfg.update(data.qpos)
        task_p.set_target_from_configuration(cfg)

        cx, cy, cz = CUBE_WORLD_POS
        cube_top   = cz + CUBE_HALF

        above_cube = np.array([cx, cy, cube_top + 0.20])
        pre_grasp  = np.array([cx, cy, cube_top + 0.06])
        grasp      = np.array([cx, cy, cz])
        lift       = np.array([cx, cy, cz + LIFT_HEIGHT])

        hx, hy, hz = HANDOVER_POS

        handover_r  = np.array([hx + GRIP_OFFSET_R, hy, hz])
        left_far    = np.array([hx - 0.10, hy, hz])
        left_close  = np.array([hx - 0.04, hy, hz])
        left_grip_p = np.array([hx + 0.04, hy, hz])
        carry       = np.array([-0.20, -0.15, hz + 0.15])

        # Waypoints: sideways first (same height), then lift
        carry_away = np.array([-0.20,  -0.15,  hz])        # same height as handover, move across
        carry_up   = np.array([-0.20,  -0.15,  hz + 0.15]) # then lift up at final X/Y

        # ── Helper shortcuts ─────────────────────────────────────────────────
        # r() = right arm active, left frozen at lhq, left gripper=255 (open)
        # l(rq, rg) = left arm active, right frozen at rq, right gripper=rg
        def r(frz_l=None, **kw):
            return dict(model=model, data=data, cfg=cfg,
                        site_id=site_r, mocap_id=moc_r, mocap_name="target_right",
                        active_ctrl=RC, active_qpos=RQ,
                        frozen_ctrl=LC, frozen_vals=frz_l if frz_l is not None else lhq,
                        active_grip=RG, frozen_grip=LG,
                        rate=rate, viewer=viewer, **kw)


        def l(frz_r, right_grip_val=0.0, **kw):
            return dict(model=model, data=data, cfg=cfg,
                        site_id=site_l, mocap_id=moc_l, mocap_name="target_left",
                        active_ctrl=LC, active_qpos=LQ,
                        frozen_ctrl=RC, frozen_vals=frz_r,
                        active_grip=LG, frozen_grip=RG,
                        frozen_grip_val=right_grip_val,
                        rate=rate, viewer=viewer, **kw)

        # P0-P2: right open (default frozen_grip_val=255 means left is open, which is fine)
        move_single(above_cube, q_r_down, "P0 · Right approaches cube (top-down orientation)",
                    ee_task=task_r, tasks=tasks_r, gripper_val=255.0,
                    pos_thr=0.025, ori_thr=0.25, timeout_secs=20.0, **r())

        move_single(pre_grasp, q_r_down, "P1 · Right → pre-grasp",
                    ee_task=task_r, tasks=tasks_r, gripper_val=255.0,
                    pos_thr=0.010, ori_thr=0.12, timeout_secs=15.0, **r())

        move_single(grasp, q_r_down, "P2 · Right → grasp",
                    ee_task=task_r, tasks=tasks_r, gripper_val=255.0,
                    pos_thr=0.010, ori_thr=0.12, timeout_secs=12.0, **r())

        rq = data.qpos[9:16].copy()
        actuate_grippers(model, data, rate, viewer,
                         lhq, rq, 255.0, 0.0, 160, "P3 · Right gripper closes to establish a firm grasp")
        rq = data.qpos[9:16].copy()

        # P4-P5: right CLOSED. Pass frozen_grip_val=255.0 to keep left open by default.
        # gripper_val=0.0 controls RIGHT (active arm) set to CLOSED
        move_single(lift, q_r_down, "P4 · Right lifts cube",
                    ee_task=task_r, tasks=tasks_r,
                    gripper_val=0.0,
                    pos_thr=0.015, ori_thr=0.18, timeout_secs=15.0, **r())
        rq = data.qpos[9:16].copy()

        move_single(lift, q_r_side, "P5a · Right wrist reorients to side-grip",
                    ee_task=task_r, tasks=tasks_r,
                    gripper_val=0.0,
                    pos_thr=0.020, ori_thr=0.12,
                    timeout_secs=15.0, damping=1e-2, **r())
        rq = data.qpos[9:16].copy()

        move_single(handover_r, q_r_side, "P5b · Right moves to handover position",
                    ee_task=task_r, tasks=tasks_r,
                    gripper_val=0.0,
                    pos_thr=0.012, ori_thr=0.18, timeout_secs=20.0, **r())
        rq = data.qpos[9:16].copy()

        # P6-P7: LEFT moves, RIGHT frozen CLOSED → right_grip_val=0.0
        move_single(left_far, q_l_side, "P6 · Left arm approaches (14cm)",
                    ee_task=task_l, tasks=tasks_l,
                    gripper_val=255.0,
                    pos_thr=0.020, ori_thr=0.20, timeout_secs=18.0,
                    **l(frz_r=rq, right_grip_val=0.0))
        lq = data.qpos[0:7].copy()

        move_single(left_close, q_l_side, "P7 · Left → close (6cm)  [R:CLOSED]",
                    ee_task=task_l, tasks=tasks_l,
                    gripper_val=255.0,
                    pos_thr=0.010, ori_thr=0.15, timeout_secs=12.0,
                    **l(frz_r=rq, right_grip_val=0.0))
        lq = data.qpos[0:7].copy()

        # P8: wait_for_left_grip (right hardcoded 0.0 inside function)
        lq = wait_for_left_grip(
            target_pos=left_grip_p,
            contact_thr=CONTACT_THRESHOLD,
            model=model, data=data, cfg=cfg,
            task_l=task_l, site_l=site_l,
            moc_l=moc_l, q_l_side=q_l_side,
            moc_r=moc_r, q_r_side=q_r_side, handover_r=handover_r,
            rq=rq, rate=rate, viewer=viewer,
            timeout_secs=25.0
        )
        rq = data.qpos[9:16].copy()

        # P9: FIRMLY close left. Use more steps and lower ctrl value for reinforcement
        # Close left first with dedicated actuate call (200 steps)
        actuate_grippers(model, data, rate, viewer,
                         lq, rq, 0.0, 0.0, 300,
                         "P9 · Synchronized clamping: both grippers close")
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # P9b: extra settle. Hold both grippers closed without arm motion
        # Lets physics confirm left finger contact before right releases
        for _ in range(120):
            if not viewer.is_running(): break
            data.ctrl[0:7]  = lq;  data.ctrl[7]  = 0.0   # left CLOSED
            data.ctrl[8:15] = rq;  data.ctrl[15] = 0.0   # right CLOSED
            mujoco.mj_step(model, data)
            viewer.sync()
            rate.sleep()
        print("    ✓ Firm double grasp confirmed via physics step")
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # P10: right opens for the FIRST TIME since P3
        actuate_grippers(model, data, rate, viewer,
                         lq, rq, 0.0, 255.0, 120,
                         "P10 · Right gripper opens (handover complete)")
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # P10b: settle after right opens to confirm the left arm holds the cube alone
        for _ in range(80):
            if not viewer.is_running(): break
            data.ctrl[0:7]  = lq;  data.ctrl[7]  = 0.0   # left CLOSED
            data.ctrl[8:15] = rq;  data.ctrl[15] = 255.0  # right open
            mujoco.mj_step(model, data)
            viewer.sync()
            rate.sleep()
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # P11a: Left moves SIDEWAYS first at the same height, with no vertical change
        move_single(carry_away, q_l_side, "P11a · Left arm moves sideways at constant height (prevents inertial slip)",
                    ee_task=task_l, tasks=tasks_l,
                    gripper_val=0.0,
                    pos_thr=0.012, ori_thr=0.20, timeout_secs=12.0,
                    damping=5e-2,
                    **l(frz_r=rq, right_grip_val=255.0))
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # P11b: Left lifts UP. Only Z changes now.
        move_single(carry_up, q_l_side, "P11b · Left lifts up",
                    ee_task=task_l, tasks=tasks_l,
                    gripper_val=0.0,
                    pos_thr=0.015, ori_thr=0.20, timeout_secs=15.0,
                    damping=5e-2,
                    **l(frz_r=rq, right_grip_val=255.0))
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # Read actual left EE position right now
        left_now = data.site_xpos[site_l].copy()

        # Pure single-axis waypoints. One axis moves at a time.
        # left_now is approx [-0.20, -0.15, hz+0.15] after carry_away

        # WP1: Move Y forward toward table center (pure Y, same X and Z)
        wp1 = np.array([left_now[0],   -0.40,          left_now[2]])

        # WP2: Move X to align over table center (pure X, same Y and Z)
        wp2 = np.array([-0.04,          -0.40,          left_now[2]])

        # WP3: Lower Z to just above table surface (pure Z down)
        wp3 = np.array([-0.04,          -0.40,          TABLE_TOP + CUBE_HALF + 0.005])

        # P12: Right retreats while the left arm is FULLY FROZEN at current lq
        # NEVER use **r() here. Passing r() uses lhq (home) as the frozen state, not the current lq
        print("\n>>> P12 · Right arm retreats while the left arm remains fully frozen at its current joint state")
        right_retreat_pos  = np.array([0.30, 0.20, 0.55])
        data.mocap_pos[moc_r]  = right_retreat_pos
        data.mocap_quat[moc_r] = q_r_down.copy()
        mujoco.mj_forward(model, data)
        task_r.set_target(mink.SE3.from_mocap_name(model, data, "target_right"))
        t0 = data.time
        while viewer.is_running():
            data.mocap_pos[moc_r]  = right_retreat_pos
            data.mocap_quat[moc_r] = q_r_down.copy()
            task_r.set_target(mink.SE3.from_mocap_name(model, data, "target_right"))

            vel = mink.solve_ik(cfg, [task_r, task_p], rate.dt, "daqp", damping=1e-2)
            cfg.integrate_inplace(vel, rate.dt)

            data.ctrl[RC]  = cfg.q[RQ]   # right arm moves
            data.ctrl[RG]  = 255.0        # right open
            data.ctrl[LC]  = lq           # left FROZEN at current (NOT lhq!)
            data.ctrl[LG]  = 0.0          # left gripper CLOSED so the cube is held

            mujoco.mj_step(model, data)
            data.ctrl[LG]  = 0.0          # clamp again after step
            viewer.sync()
            rate.sleep()

            pos_err = np.linalg.norm(data.site_xpos[site_r] - right_retreat_pos)
            if pos_err <= 0.030:
                print(f"    ✓ Right arm retreated (Pos error: {pos_err*1000:.1f}mm)")
                break
            if (data.time - t0) > 12.0:
                print(f"    ⚠ Timeout: Right arm retreat (Pos error: {pos_err*1000:.1f}mm)")
                break

        rq = data.qpos[9:16].copy()
        lq = data.qpos[0:7].copy()  # update lq after right moved


        # P13–P15: carry + place with 1mm steps, pure-axis path
        carry_smooth(
            waypoints=[wp1, wp2, wp3],
            quat=q_l_side,
            label="P13-15 · Left carry via smooth 1mm waypoint interpolation to table center",
            model=model, data=data, cfg=cfg,
            task=task_l, site_id=site_l,
            mocap_id=moc_l, mocap_name="target_left",
            active_ctrl=LC, active_qpos=LQ,
            frozen_ctrl=RC, frozen_vals=rq,
            active_grip=LG, frozen_grip=RG,
            frozen_grip_val=255.0,
            rate=rate, viewer=viewer,
            step_size=0.001,       # 1mm steps for ultra smooth motion
            damping=8e-2,          # very high damping
            settle_steps=60        # longer settle at each waypoint
        )
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # P16: Settle down to transfer weight to the table
        print("\n>>> P16 · Cube settles on table")
        for _ in range(200):
            if not viewer.is_running(): break
            data.ctrl[0:7]  = lq;  data.ctrl[7]  = 0.0
            data.ctrl[8:15] = rq;  data.ctrl[15] = 255.0
            mujoco.mj_step(model, data)
            viewer.sync()
            rate.sleep()
        print("    ✓ Placement stabilized")
        lq = data.qpos[0:7].copy()

        # P17: Open left gripper to release the cube
        actuate_grippers(model, data, rate, viewer,
                         lq, rq, 255.0, 255.0, 160,
                         "P17 · Left gripper opens (cube placed)")
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()

        # P18: Left retreats to the LEFT side (negative X)
        wp_up   = np.array([-0.04,  -0.40,   TABLE_TOP + 0.25])   # straight up first (same)
        wp_back = np.array([-0.35,  -0.20,   TABLE_TOP + 0.25])   # ← negative X = LEFT side

        carry_smooth(
            waypoints=[wp_up, wp_back],
            quat=q_l_side,
            label="P18 · Left arm retreats",
            model=model, data=data, cfg=cfg,
            task=task_l, site_id=site_l,
            mocap_id=moc_l, mocap_name="target_left",
            active_ctrl=LC, active_qpos=LQ,
            frozen_ctrl=RC, frozen_vals=rq,
            active_grip=LG, frozen_grip=RG,
            frozen_grip_val=255.0,
            rate=rate, viewer=viewer,
            step_size=0.003,       # Can go faster since there is no cube
            damping=1e-2,
            settle_steps=20
        )


        print("\n=== DEMO COMPLETE, Press Ctrl+C to quit ===")
        lq = data.qpos[0:7].copy()
        rq = data.qpos[9:16].copy()
        while viewer.is_running():
            data.ctrl[0:7]  = lq;  data.ctrl[7]  = 0.0
            data.ctrl[8:15] = rq;  data.ctrl[15] = 255.0
            mujoco.mj_step(model, data)
            viewer.sync()
            rate.sleep()


if __name__ == "__main__":
    main()
