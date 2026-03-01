#!/usr/bin/env python3
"""
MuJoCo + mink  ·  Month 1 Baseline: Rigid-Body Dual-Arm Pick, Contact-Aware Handover, and Place
"""

from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np
from loop_rate_limiters import RateLimiter
import mink

# ─────────────────────────────────────────────────────────────────────────────
# Paths & world geometry
# ─────────────────────────────────────────────────────────────────────────────

_HERE       = Path(__file__).parent
_MODEL_PATH = _HERE / "franka_emika_panda" / "dual_panda_scene.xml"

CUBE_WORLD_POS    = np.array([0.08, -0.35, 0.285])
CUBE_HALF         = 0.025
HANDOVER_POS      = np.array([0.00, -0.28, 0.52])
LIFT_HEIGHT       = 0.22
GRIP_OFFSET_R     = 0.04
CONTACT_THRESHOLD = 0.010
TABLE_TOP         = 0.285

# ─────────────────────────────────────────────────────────────────────────────
# Control constants
# ─────────────────────────────────────────────────────────────────────────────

GRIPPER_OPEN   = 255.0
GRIPPER_CLOSED = 0.0

LEFT_CTRL  = slice(0, 7)
LEFT_GRIP  = 7
LEFT_QPOS  = slice(0, 7)
RIGHT_CTRL = slice(8, 15)
RIGHT_GRIP = 15
RIGHT_QPOS = slice(9, 16)

DEFAULT_DAMPING = 1e-3
CARRY_DAMPING   = 5e-2
DEFAULT_POS_THR = 0.010
DEFAULT_ORI_THR = 0.15
DEFAULT_TIMEOUT = 18.0


# ─────────────────────────────────────────────────────────────────────────────
# Arm context — bundles all per-arm identity into a single object
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ArmContext:
    """Everything needed to command one arm while freezing the other."""
    model: object
    data: object
    cfg: object
    site_id: int
    mocap_id: int
    mocap_name: str
    ctrl_slice: slice
    qpos_slice: slice
    grip_index: int
    frozen_ctrl: slice
    frozen_grip: int
    rate: object
    viewer: object
    frozen_vals: np.ndarray = field(default_factory=lambda: np.zeros(7))
    frozen_grip_val: float = GRIPPER_OPEN


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


def snapshot_joints(data):
    """Return (left_joints, right_joints) copies of current joint positions."""
    return data.qpos[LEFT_QPOS].copy(), data.qpos[RIGHT_QPOS].copy()


# ─────────────────────────────────────────────────────────────────────────────
# Trajectory interpolation
# ─────────────────────────────────────────────────────────────────────────────

def minimum_jerk(t):
    """Minimum-jerk profile: zero velocity and acceleration at endpoints."""
    return 10 * t**3 - 15 * t**4 + 6 * t**5


def quat_slerp(q0, q1, t):
    """Spherical linear interpolation between two quaternions."""
    q0 = q0 / np.linalg.norm(q0)
    q1 = q1 / np.linalg.norm(q1)
    dot = np.dot(q0, q1)
    if dot < 0:
        q1 = -q1
        dot = -dot
    if dot > 0.9995:
        result = q0 + t * (q1 - q0)
        return result / np.linalg.norm(result)
    theta = np.arccos(np.clip(dot, -1, 1))
    sin_theta = np.sin(theta)
    return (np.sin((1 - t) * theta) / sin_theta) * q0 + \
           (np.sin(t * theta) / sin_theta) * q1


# ─────────────────────────────────────────────────────────────────────────────
# Motion primitives
# ─────────────────────────────────────────────────────────────────────────────

def move_single(ctx, pos, quat, label, ee_task, tasks,
                gripper_val=GRIPPER_OPEN,
                pos_thr=DEFAULT_POS_THR, ori_thr=DEFAULT_ORI_THR,
                timeout_secs=DEFAULT_TIMEOUT, damping=DEFAULT_DAMPING):
    """Move the active arm to a target pose while freezing the other arm."""
    print(f"\n>>> {label}  ->  {np.round(pos, 3)}")
    ctx.data.mocap_pos[ctx.mocap_id]  = pos.copy()
    ctx.data.mocap_quat[ctx.mocap_id] = quat.copy()
    mujoco.mj_forward(ctx.model, ctx.data)
    ee_task.set_target(mink.SE3.from_mocap_name(ctx.model, ctx.data, ctx.mocap_name))
    t0 = ctx.data.time

    while ctx.viewer.is_running():
        ctx.data.mocap_pos[ctx.mocap_id]  = pos.copy()
        ctx.data.mocap_quat[ctx.mocap_id] = quat.copy()
        ee_task.set_target(mink.SE3.from_mocap_name(ctx.model, ctx.data, ctx.mocap_name))

        vel = mink.solve_ik(ctx.cfg, tasks, ctx.rate.dt, "daqp", damping=damping)
        ctx.cfg.integrate_inplace(vel, ctx.rate.dt)

        ctx.data.ctrl[ctx.ctrl_slice]  = ctx.cfg.q[ctx.qpos_slice]
        ctx.data.ctrl[ctx.grip_index]  = gripper_val
        ctx.data.ctrl[ctx.frozen_ctrl] = ctx.frozen_vals
        ctx.data.ctrl[ctx.frozen_grip] = ctx.frozen_grip_val

        mujoco.mj_step(ctx.model, ctx.data)
        # Reinforce frozen gripper after physics step (prevents solver drift)
        ctx.data.ctrl[ctx.frozen_grip] = ctx.frozen_grip_val
        ctx.viewer.sync()
        ctx.rate.sleep()

        pos_err = np.linalg.norm(ctx.data.site_xpos[ctx.site_id] - pos)
        q_now   = np.empty(4)
        mujoco.mju_mat2Quat(q_now, ctx.data.site_xmat[ctx.site_id])
        ori_err = quat_error(q_now, quat)

        if pos_err <= pos_thr and ori_err <= ori_thr:
            print(f"    done  Pos: {pos_err*1000:.1f}mm | Ori: {ori_err:.3f}rad")
            return True
        if (ctx.data.time - t0) > timeout_secs:
            print(f"    timeout  Pos: {pos_err*1000:.1f}mm | Ori: {ori_err:.3f}rad")
            return False
    return False


def carry_smooth(ctx, waypoints, quat, label, task,
                 quat_end=None, step_size=0.003,
                 damping=CARRY_DAMPING, settle_steps=30):
    """Move through waypoints using minimum-jerk interpolation.
    Gripper stays closed throughout for stable carrying.

    If quat_end is given, orientation is smoothly SLERPed from quat to
    quat_end over the entire trajectory — this allows safe mid-carry
    reorientation without abrupt contact changes."""
    print(f"\n>>> {label}  ({len(waypoints)} waypoints)")

    # Start from actual EE position to prevent backward jumps
    current = np.array(ctx.data.site_xpos[ctx.site_id], dtype=float)
    ctx.data.mocap_pos[ctx.mocap_id] = current.copy()

    # Pre-compute cumulative segment distances for global SLERP progress
    seg_dists = []
    prev = current.copy()
    for wp in waypoints:
        d = np.linalg.norm(np.array(wp, dtype=float) - prev)
        seg_dists.append(d)
        prev = np.array(wp, dtype=float)
    total_path = sum(seg_dists)
    cumulative = 0.0

    for wp_idx, target in enumerate(waypoints):
        target = np.array(target, dtype=float)
        total_dist = np.linalg.norm(target - current)
        if total_dist < 1e-4:
            cumulative += seg_dists[wp_idx]
            continue
        n_steps = max(1, int(total_dist / step_size))
        print(f"    WP{wp_idx+1}: {np.round(target,3)}  "
              f"dist={total_dist*1000:.1f}mm  steps={n_steps}")

        for i in range(1, n_steps + 1):
            if not ctx.viewer.is_running():
                return
            alpha = minimum_jerk(i / n_steps)
            interp_pos = current + alpha * (target - current)

            # Compute orientation: fixed or SLERPed
            if quat_end is not None and total_path > 1e-4:
                global_t = (cumulative + alpha * total_dist) / total_path
                interp_quat = quat_slerp(quat, quat_end, global_t)
            else:
                interp_quat = quat.copy()

            ctx.data.mocap_pos[ctx.mocap_id]  = interp_pos
            ctx.data.mocap_quat[ctx.mocap_id] = interp_quat
            task.set_target(mink.SE3.from_mocap_name(ctx.model, ctx.data, ctx.mocap_name))

            vel = mink.solve_ik(ctx.cfg, [task], ctx.rate.dt, "daqp", damping=damping)
            ctx.cfg.integrate_inplace(vel, ctx.rate.dt)

            ctx.data.ctrl[ctx.ctrl_slice]  = ctx.cfg.q[ctx.qpos_slice]
            ctx.data.ctrl[ctx.grip_index]  = GRIPPER_CLOSED
            ctx.data.ctrl[ctx.frozen_ctrl] = ctx.frozen_vals
            ctx.data.ctrl[ctx.frozen_grip] = ctx.frozen_grip_val

            mujoco.mj_step(ctx.model, ctx.data)
            ctx.viewer.sync()
            ctx.rate.sleep()

        # Settle at waypoint with final orientation
        final_quat = quat_slerp(quat, quat_end, (cumulative + total_dist) / total_path) \
                     if quat_end is not None and total_path > 1e-4 else quat
        for _ in range(settle_steps):
            if not ctx.viewer.is_running():
                return
            ctx.data.mocap_quat[ctx.mocap_id] = final_quat
            ctx.data.ctrl[ctx.ctrl_slice]  = ctx.cfg.q[ctx.qpos_slice]
            ctx.data.ctrl[ctx.grip_index]  = GRIPPER_CLOSED
            ctx.data.ctrl[ctx.frozen_ctrl] = ctx.frozen_vals
            ctx.data.ctrl[ctx.frozen_grip] = ctx.frozen_grip_val
            mujoco.mj_step(ctx.model, ctx.data)
            ctx.viewer.sync()
            ctx.rate.sleep()

        cumulative += total_dist
        current = target.copy()
        print(f"    done  WP {wp_idx+1}/{len(waypoints)}")


def actuate_grippers(model, data, rate, viewer,
                     left_joints, right_joints,
                     left_grip, right_grip,
                     steps=160, label=""):
    """Run physics with fixed joint positions and specified gripper values."""
    if label:
        print(f"\n>>> {label}")
    for _ in range(steps):
        if not viewer.is_running():
            break
        data.ctrl[LEFT_CTRL]  = left_joints
        data.ctrl[LEFT_GRIP]  = left_grip
        data.ctrl[RIGHT_CTRL] = right_joints
        data.ctrl[RIGHT_GRIP] = right_grip
        mujoco.mj_step(model, data)
        viewer.sync()
        rate.sleep()
    if label:
        print("    done")


def settle(model, data, rate, viewer, lq, rq,
           left_grip=GRIPPER_CLOSED, right_grip=GRIPPER_CLOSED,
           steps=120, label=""):
    """Hold both arms frozen for N physics steps to let contacts stabilize."""
    if label:
        print(f"\n>>> {label}")
    for _ in range(steps):
        if not viewer.is_running():
            break
        data.ctrl[LEFT_CTRL]  = lq
        data.ctrl[LEFT_GRIP]  = left_grip
        data.ctrl[RIGHT_CTRL] = rq
        data.ctrl[RIGHT_GRIP] = right_grip
        mujoco.mj_step(model, data)
        viewer.sync()
        rate.sleep()
    if label:
        print(f"    done  ({steps} steps)")


def wait_for_left_grip(ctx, target_pos, contact_thr,
                       task_l, q_l_side,
                       moc_r, q_r_side, handover_r, rq,
                       timeout_secs=25.0):
    """Drive the left arm toward target_pos until distance <= contact_thr."""
    print(f"\n>>> P8 - Contact-Aware Handover (target={np.round(target_pos,3)})")
    t0 = ctx.data.time

    while ctx.viewer.is_running():
        ctx.data.mocap_pos[ctx.mocap_id]  = target_pos.copy()
        ctx.data.mocap_quat[ctx.mocap_id] = q_l_side.copy()
        ctx.data.mocap_pos[moc_r]         = handover_r.copy()
        ctx.data.mocap_quat[moc_r]        = q_r_side.copy()

        task_l.set_target(mink.SE3.from_mocap_name(ctx.model, ctx.data, "target_left"))
        vel = mink.solve_ik(ctx.cfg, [task_l], ctx.rate.dt, "daqp", damping=DEFAULT_DAMPING)
        ctx.cfg.integrate_inplace(vel, ctx.rate.dt)

        ctx.data.ctrl[LEFT_CTRL]  = ctx.cfg.q[LEFT_QPOS]
        ctx.data.ctrl[LEFT_GRIP]  = GRIPPER_OPEN
        ctx.data.ctrl[RIGHT_CTRL] = rq
        ctx.data.ctrl[RIGHT_GRIP] = GRIPPER_CLOSED

        mujoco.mj_step(ctx.model, ctx.data)
        ctx.viewer.sync()
        ctx.rate.sleep()

        dist = np.linalg.norm(ctx.data.site_xpos[ctx.site_id] - target_pos)
        print(f"\r    left dist={dist*1000:.1f}mm", end="", flush=True)

        if dist <= contact_thr:
            print(f"\n    done  Contact at {dist*1000:.1f}mm")
            return ctx.data.qpos[LEFT_QPOS].copy()
        if (ctx.data.time - t0) > timeout_secs:
            print(f"\n    timeout  Stopped at {dist*1000:.1f}mm")
            return ctx.data.qpos[LEFT_QPOS].copy()
    return ctx.data.qpos[LEFT_QPOS].copy()


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
        frame_name="attachment_site_left", frame_type="site",
        position_cost=1.0, orientation_cost=0.5, lm_damping=1.0)
    task_p = mink.PostureTask(model=model, cost=1e-3)

    tasks_r = [task_r, task_p]
    tasks_l = [task_l, task_p]

    rate  = RateLimiter(frequency=40.0, warn=False)
    moc_r = model.body("target_right").mocapid[0]
    moc_l = model.body("target_left").mocapid[0]

    # ── ArmContext factories ──────────────────────────────────────────────

    def right_ctx(frozen_vals=None, frozen_grip_val=GRIPPER_OPEN):
        return ArmContext(
            model=model, data=data, cfg=cfg,
            site_id=site_r, mocap_id=moc_r, mocap_name="target_right",
            ctrl_slice=RIGHT_CTRL, qpos_slice=RIGHT_QPOS, grip_index=RIGHT_GRIP,
            frozen_ctrl=LEFT_CTRL, frozen_grip=LEFT_GRIP,
            rate=rate, viewer=viewer,
            frozen_vals=frozen_vals if frozen_vals is not None else lhq,
            frozen_grip_val=frozen_grip_val,
        )

    def left_ctx(frozen_vals, frozen_grip_val=GRIPPER_CLOSED):
        return ArmContext(
            model=model, data=data, cfg=cfg,
            site_id=site_l, mocap_id=moc_l, mocap_name="target_left",
            ctrl_slice=LEFT_CTRL, qpos_slice=LEFT_QPOS, grip_index=LEFT_GRIP,
            frozen_ctrl=RIGHT_CTRL, frozen_grip=RIGHT_GRIP,
            rate=rate, viewer=viewer,
            frozen_vals=frozen_vals,
            frozen_grip_val=frozen_grip_val,
        )

    # ── Viewer launch & wait for SPACE ────────────────────────────────────

    start_sim = False
    def key_callback(keycode):
        nonlocal start_sim
        if chr(keycode) == ' ':
            start_sim = True

    with mujoco.viewer.launch_passive(
            model=model, data=data,
            key_callback=key_callback,
            show_left_ui=False, show_right_ui=False) as viewer:

        mujoco.mjv_defaultFreeCamera(model, viewer.cam)
        mujoco.mj_resetDataKeyframe(model, data, model.key("home1").id)
        lhq = data.qpos[LEFT_QPOS].copy()
        rhq = data.qpos[RIGHT_QPOS].copy()
        mujoco.mj_forward(model, data)
        left_home_pos  = data.site_xpos[site_l].copy()
        right_home_pos = data.site_xpos[site_r].copy()
        reset_cube(model, data)

        viewer.sync()
        print("\n" + "="*50)
        print("  Simulation Ready")
        print("  1. Reposition/Resize window for recording")
        print("  2. Press SPACE within the viewer to start")
        print("="*50 + "\n")

        while viewer.is_running() and not start_sim:
            viewer.sync()
            rate.sleep()

        # ── Quaternions ───────────────────────────────────────────────────

        q_r_down = topdown_quat_for_site(model, data, "attachment_site_right")
        q_r_side = sidegrip_quat(approach_dir=[-1, 0, 0], y_hint=[0, 0, 1])
        q_l_side = sidegrip_quat(approach_dir=[+1, 0, 0], y_hint=[0, 1, 0])

        cfg.update(data.qpos)
        task_p.set_target_from_configuration(cfg)

        # ── Target positions ──────────────────────────────────────────────

        cx, cy, cz = CUBE_WORLD_POS
        cube_top   = cz + CUBE_HALF

        above_cube = np.array([cx, cy, cube_top + 0.20])
        pre_grasp  = np.array([cx, cy, cube_top + 0.06])
        grasp      = np.array([cx, cy, cz])
        lift       = np.array([cx, cy, cz + LIFT_HEIGHT])

        hx, hy, hz = HANDOVER_POS

        handover_r     = np.array([hx + GRIP_OFFSET_R, hy, hz])
        left_far       = np.array([hx - 0.10, hy, hz])
        left_close     = np.array([hx - 0.04, hy, hz])
        left_grip_p    = np.array([hx + 0.04, hy, hz])
        carry_away     = np.array([-0.20, -0.15, hz])
        carry_up       = np.array([-0.20, -0.15, hz + 0.15])
        right_retreat  = np.array([0.30, 0.20, 0.55])
        above_place    = np.array([-0.04, -0.40, cube_top + 0.20])
        place_pos      = np.array([-0.04, -0.35, TABLE_TOP + 0.012])

        # ── Phase execution ───────────────────────────────────────────────

        lq, rq = lhq.copy(), data.qpos[RIGHT_QPOS].copy()

        def pick_cube():
            """P0-P3: Right arm picks up the cube."""
            nonlocal lq, rq
            ctx = right_ctx()

            move_single(ctx, above_cube, q_r_down,
                        "P0 - Right approaches cube",
                        ee_task=task_r, tasks=tasks_r,
                        pos_thr=0.025, ori_thr=0.25, timeout_secs=20.0)

            move_single(ctx, pre_grasp, q_r_down,
                        "P1 - Right at pre-grasp",
                        ee_task=task_r, tasks=tasks_r,
                        pos_thr=0.010, ori_thr=0.12, timeout_secs=15.0)

            move_single(ctx, grasp, q_r_down,
                        "P2 - Right at grasp position",
                        ee_task=task_r, tasks=tasks_r,
                        pos_thr=0.010, ori_thr=0.12, timeout_secs=12.0)

            _, rq = snapshot_joints(data)
            actuate_grippers(model, data, rate, viewer,
                             lhq, rq, GRIPPER_OPEN, GRIPPER_CLOSED,
                             160, "P3 - Right gripper closes")
            lq, rq = snapshot_joints(data)

        def lift_and_handover():
            """P4-P10b: Lift, reorient, handover to left arm."""
            nonlocal lq, rq

            # P4: Lift cube
            ctx = right_ctx()
            move_single(ctx, lift, q_r_down,
                        "P4 - Right lifts cube",
                        ee_task=task_r, tasks=tasks_r,
                        gripper_val=GRIPPER_CLOSED,
                        pos_thr=0.015, ori_thr=0.18, timeout_secs=15.0)
            lq, rq = snapshot_joints(data)

            # P5a: Reorient wrist to side-grip
            move_single(right_ctx(), lift, q_r_side,
                        "P5a - Right reorients to side-grip",
                        ee_task=task_r, tasks=tasks_r,
                        gripper_val=GRIPPER_CLOSED,
                        pos_thr=0.020, ori_thr=0.12,
                        timeout_secs=15.0, damping=1e-2)
            lq, rq = snapshot_joints(data)

            # P5b: Move to handover position
            move_single(right_ctx(), handover_r, q_r_side,
                        "P5b - Right at handover position",
                        ee_task=task_r, tasks=tasks_r,
                        gripper_val=GRIPPER_CLOSED,
                        pos_thr=0.012, ori_thr=0.18, timeout_secs=20.0)
            lq, rq = snapshot_joints(data)

            # P6: Left arm far approach
            move_single(left_ctx(rq), left_far, q_l_side,
                        "P6 - Left arm approaches (14cm)",
                        ee_task=task_l, tasks=tasks_l,
                        pos_thr=0.020, ori_thr=0.20, timeout_secs=18.0)
            lq, rq = snapshot_joints(data)

            # P7: Left arm close approach
            move_single(left_ctx(rq), left_close, q_l_side,
                        "P7 - Left at close position (6cm)",
                        ee_task=task_l, tasks=tasks_l,
                        pos_thr=0.010, ori_thr=0.15, timeout_secs=12.0)
            lq, rq = snapshot_joints(data)

            # P8: Contact-aware grip transfer
            lq = wait_for_left_grip(
                left_ctx(rq), left_grip_p, CONTACT_THRESHOLD,
                task_l, q_l_side,
                moc_r, q_r_side, handover_r, rq,
                timeout_secs=25.0)
            _, rq = snapshot_joints(data)

            # P9: Both grippers close
            actuate_grippers(model, data, rate, viewer,
                             lq, rq, GRIPPER_CLOSED, GRIPPER_CLOSED,
                             300, "P9 - Synchronized clamping")
            lq, rq = snapshot_joints(data)

            # P9b: Settle to confirm firm double grasp
            settle(model, data, rate, viewer, lq, rq,
                   GRIPPER_CLOSED, GRIPPER_CLOSED,
                   120, "P9b - Firm double grasp confirmed")
            lq, rq = snapshot_joints(data)

            # P10a: Right gripper opens — handover complete
            actuate_grippers(model, data, rate, viewer,
                             lq, rq, GRIPPER_CLOSED, GRIPPER_OPEN,
                             120, "P10a - Right gripper opens (handover complete)")
            lq, rq = snapshot_joints(data)

            # P10b: Settle to confirm left holds cube alone
            print("\n>>> P10b - Left holds cube alone")
            settle(model, data, rate, viewer, lq, rq,
                   GRIPPER_CLOSED, GRIPPER_OPEN, 80)
            print("    done")
            lq, rq = snapshot_joints(data)

        def carry_and_place():
            """P11-P17: Left carries cube to table and places it."""
            nonlocal lq, rq

            # P11a: Pull back to create safe distance from right arm
            left_now = data.site_xpos[site_l].copy()
            pullback = np.array([left_now[0] - 0.08, left_now[1], left_now[2]])
            move_single(left_ctx(rq, GRIPPER_OPEN), pullback, q_l_side,
                        "P11a - Left pulls back from right arm",
                        ee_task=task_l, tasks=tasks_l,
                        gripper_val=GRIPPER_CLOSED,
                        pos_thr=0.012, ori_thr=0.20,
                        timeout_secs=8.0, damping=CARRY_DAMPING)
            lq, rq = snapshot_joints(data)

            # P11b: Smooth single move away from handover (diagonal)
            carry_smooth(left_ctx(rq, GRIPPER_OPEN),
                         waypoints=[carry_up],
                         quat=q_l_side,
                         label="P11b - Left moves away from handover",
                         task=task_l,
                         step_size=0.002, damping=CARRY_DAMPING, settle_steps=40)
            lq, rq = snapshot_joints(data)

            # P12: Right retreats while left holds the cube
            move_single(right_ctx(frozen_vals=lq, frozen_grip_val=GRIPPER_CLOSED),
                        right_retreat, q_r_down,
                        "P12 - Right arm retreats",
                        ee_task=task_r, tasks=tasks_r,
                        gripper_val=GRIPPER_OPEN,
                        pos_thr=0.030, ori_thr=0.30,
                        timeout_secs=12.0, damping=1e-2)
            lq, rq = snapshot_joints(data)

            # P13: Smooth diagonal carry to above placement position
            # Orientation SLERPs gradually from side-grip to top-down over
            # hundreds of steps, keeping the cube secure throughout.
            q_l_down = topdown_quat_for_site(model, data, "attachment_site_left")
            carry_smooth(left_ctx(rq, GRIPPER_OPEN),
                         waypoints=[above_place],
                         quat=q_l_side, quat_end=q_l_down,
                         label="P13 - Left carries cube above table",
                         task=task_l,
                         step_size=0.001, damping=8e-2, settle_steps=40)
            lq, rq = snapshot_joints(data)

            # P14: Lower to final placement (mirrors grasp height)
            move_single(left_ctx(rq, GRIPPER_OPEN), place_pos, q_l_down,
                        "P14 - Left places cube on table",
                        ee_task=task_l, tasks=tasks_l,
                        gripper_val=GRIPPER_CLOSED,
                        pos_thr=0.010, ori_thr=0.12, timeout_secs=12.0)
            lq, rq = snapshot_joints(data)

            # P15: Settle on table
            settle(model, data, rate, viewer, lq, rq,
                   GRIPPER_CLOSED, GRIPPER_OPEN,
                   200, "P15 - Cube settles on table")
            lq, rq = snapshot_joints(data)

            # P17: Release cube
            actuate_grippers(model, data, rate, viewer,
                             lq, rq, GRIPPER_OPEN, GRIPPER_OPEN,
                             160, "P17 - Left gripper opens (cube placed)")
            lq, rq = snapshot_joints(data)

        def retreat():
            """P18: Both arms return to home positions."""
            nonlocal lq, rq

            # P18a: Pull back horizontally to clear the cube, then rise
            left_now = data.site_xpos[site_l].copy()
            away_pos  = np.array([left_now[0] - 0.08, left_now[1], left_now[2]])
            clear_pos = np.array([left_now[0] - 0.08, left_now[1], TABLE_TOP + 0.35])
            q_l_down = topdown_quat_for_site(model, data, "attachment_site_left")
            move_single(left_ctx(rq, GRIPPER_OPEN), away_pos, q_l_down,
                        "P18a - Left pulls away from cube",
                        ee_task=task_l, tasks=tasks_l,
                        pos_thr=0.012, ori_thr=0.20,
                        timeout_secs=8.0, damping=1e-2)
            lq, rq = snapshot_joints(data)

            # P18b: Left arm returns to home position
            move_single(left_ctx(rq, GRIPPER_OPEN), left_home_pos, q_l_down,
                        "P18b - Left arm returns to home",
                        ee_task=task_l, tasks=tasks_l,
                        pos_thr=0.020, ori_thr=0.25,
                        timeout_secs=15.0, damping=1e-2)
            lq, rq = snapshot_joints(data)

            # P19: Right arm returns to home position
            move_single(right_ctx(frozen_vals=lq, frozen_grip_val=GRIPPER_OPEN),
                        right_home_pos, q_r_down,
                        "P19 - Right arm returns to home",
                        ee_task=task_r, tasks=tasks_r,
                        pos_thr=0.020, ori_thr=0.25,
                        timeout_secs=15.0, damping=1e-2)
            lq, rq = snapshot_joints(data)

        # ── Run all phases ────────────────────────────────────────────────

        pick_cube()
        lift_and_handover()
        carry_and_place()
        retreat()

        # Hold final pose
        print("\n=== DEMO COMPLETE, Press Ctrl+C to quit ===")
        lq, rq = snapshot_joints(data)
        while viewer.is_running():
            data.ctrl[LEFT_CTRL]  = lq
            data.ctrl[LEFT_GRIP]  = GRIPPER_OPEN
            data.ctrl[RIGHT_CTRL] = rq
            data.ctrl[RIGHT_GRIP] = GRIPPER_OPEN
            mujoco.mj_step(model, data)
            viewer.sync()
            rate.sleep()


if __name__ == "__main__":
    main()
