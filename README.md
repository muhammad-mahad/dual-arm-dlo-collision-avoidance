# Safe Dual-Arm Cable Routing with Deformable Linear Objects

A demonstration of dual-arm bimanual manipulation acting as the computational testbed for my Master's thesis on **hierarchical planning and contact-aware Control Barrier Functions (CBFs)** using two Franka Emika Panda robots in the MuJoCo physics simulator.

![Demo Screenshot](docs/figures/demo_screenshot.png)
<br>
![Demo Animation](media/demo_preview.gif)

## Features

- **Dual Franka Emika Panda arms** performing coordinated pick-and-handover in MuJoCo
- **Constrained differential inverse kinematics** (`mink`) providing highly accurate real-time local collision avoidance and safety margins
- **Distance-threshold sensing capabilities** allowing contact-aware handover via MuJoCo spatial sites
- **Zero-jump smooth motion interpolation** for millimeter-scale carrying and exact payload placement
- **Freeze-based gripper isolation**, safely managing asymmetric active/frozen control across the 14-DoF workspace

## Technical Stack

| Component | Technology |
|---|---|
| Physics Engine | MuJoCo 3.x |
| Robot Model | Franka Emika Panda (7-DoF) × 2 |
| IK Solver & Kinematics| `mink` (differential IK with QP) / Pinocchio |
| Local Controller & Safety | MPC wrapped in a Control Barrier Function (CBF-QP) (Phase 3) |
| Global Motion Planner | TUM's Direction Informed Trees (DIT*) or Just-in-Time (JIT) (Phase 4) |
| Cable Physics Model | Adapted Discrete Elastic Rods (DER) via `qj25/adapteddlomuj` |
| Optimization Algorithms | OSQP or qpOASES |
| Language | Python 3 / C++ |

## Collision Avoidance Details

While the system's baseline leverages purely constrained differential IK for margin safety across the configuration space, the full architecture aggressively expands to a strict **Control Barrier Function (CBF)** safety filter integrated deeply with contact-estimation logic.

The hierarchical approach enforces four exact geometric safety constraints:

- **Arm-to-arm avoidance**: Prevents self-collision between left and right arms ($h_{arm-arm} \ge 0$)
- **Arm-to-environment avoidance**: Each arm rigidly avoids workspace boundaries ($h_{arm-env} \ge 0$)
- **Cable-to-environment avoidance**: Ensure the Deformable Linear Object avoids snagging ($h_{cable-env} \ge 0$)
- **Overstretch Limits**: DLO tension scaling to prevent cable snapping

Crucially, the system utilizes force-simulated **Contact Establishment Indicators (CEI)** to achieve *mode-switching*. This permits the framework to temporarily relax environmental collision constraints during force-validated clip insertions, distinguishing intended clip snaps from bad collisions.

This approach incorporates concepts heavily proposed in:

- Yu, M., et al. (2023). "A coarse-to-fine framework for dual-arm manipulation of deformable linear objects with whole-body obstacle avoidance." **ICRA**.
- Chen, K., Bing, Z., et al. (2023). "Contact-aware Shaping and Maintenance of Deformable Linear Objects With Fixtures." **IROS**.
- Zhu, J., et al. (2019). "Robotic manipulation planning for shaping deformable linear objects with environmental contacts." **IEEE Robotics and Automation Letters**.

## Installation

```bash
git clone https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git
cd dual-arm-dlo-collision-avoidance

# If on Linux / macOS
chmod +x setup_env.sh
./setup_env.sh
source venv/bin/activate
```

*(If on Windows, simply double-click or run `setup_env.bat`, then run `venv\Scripts\activate.bat`)*

## Usage

```bash
cd simulation
python demo_pick_cube.py
```

## Next Steps

This project timeline corresponds precisely with my **Master's thesis** roadmap:

1. **Phase 1: Rigid-Body Baseline (Completed)**: MuJoCo dual-arm initial setup using direct Python/C++ API.
2. **Phase 2: DLO Integration**: Adopt `qj25/adapteddlomuj` Discrete Elastic Rods pipeline.
3. **Phase 3: CBF Safety Layer**: MPC local controller enforcing the absolute safety barriers and distances.
4. **Phase 4: Global Planner Integration**: Applying modified JIT/DIT algorithms tailored exclusively for infinite-dimensional DLO shapes.
5. **Phase 5: Contact-Aware Fixture Routing**: Implement force-driven mode-switching to allow clip insertions without invalidating constraint checks.

*(See the `ROADMAP.md` tracking document for an explicit monthly breakdown.)*

## Author

**Muhammad Mahad**
