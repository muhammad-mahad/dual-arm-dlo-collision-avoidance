# Safe Dual-Arm Cable Routing with Deformable Linear Objects: Hierarchical Planning and Contact-Aware Control Barrier Functions

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Official repository:** [https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git](https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git)

A demonstration of dual-arm bimanual manipulation acting as the computational testbed for my Master's thesis on **Collision Avoidance in Dual-Arm Manipulation of Deformable Linear Objects (DLOs)** in the MuJoCo physics simulator.

![Demo Screenshot](docs/figures/demo_screenshot.png)
![Demo Animation](media/demo_preview.gif)

## Features

- **Dual Franka Emika Panda arms** performing coordinated pick-and-lift via precise simulation.
- **Real-time collision avoidance and kinematics** using constrained differential IK (`mink`).
- **Contact-aware handover** via distance-threshold sensing using MuJoCo sites.
- **Smooth motion interpolation** for millimeter-scale carrying and precise placement without violating physics bounds.
- **Freeze-based gripper isolation**, accurately managing asymmetric active/frozen control across the 14-DoF setup.
- **Zero collisions** during execution.

## Technical Stack

| Component | Technology |
|---|---|
| Physics Engine | MuJoCo 3.x |
| Robot Model | Franka Emika Panda (7-DoF) × 2 |
| Cable Physics Model | Adapted Discrete Elastic Rods (DER) via `qj25/adapteddlomuj` (Phase 2) |
| IK Solver / Kinematics | `mink` (differential IK with QP) / Pinocchio |
| Local Control | MPC with Control Barrier Functions (CBF-QP) (Phase 3) |
| Global Planner | TUM's Direction Informed Trees (DIT*) / Just-in-Time (JIT) (Phase 4) |
| Language | Python 3 / C++ |

## Collision Avoidance & Safety Constraints Details

The final system architecture relies heavily on local safety wrappers. Currently using constrained differential inverse kinematics to enforce basic safety bounds, the framework is advancing towards strict **Control Barrier Functions (CBFs)** implementation:

- $h_{arm-arm} \ge 0$: Prevent self-collision between the arms.
- $h_{arm-env} \ge 0$: Each arm safely avoids workspace obstacles.
- $h_{cable-env} \ge 0$: Ensure the DLO avoids unintentional snags.
- **Tension Limits**: Overstretch prevention limits.
- **Mode-Switching via Contact Estimation**: The system achieves contact-aware fixture interaction by monitoring simulated end-effector force-torque sensors and recognizing Contact Establishment Indicators (CEI), temporarily relaxing constraints to allow intended clip insertions.

This approach draws foundational methodology from:

- Yu et al. (2023). "A coarse-to-fine framework for dual-arm manipulation of deformable linear objects with whole-body obstacle avoidance." **ICRA**.
- Chen, K., Bing, Z., et al. (2023). "Contact-aware Shaping and Maintenance of Deformable Linear Objects With Fixtures." **IROS**.

## Installation

You have two choices for setting up the workspace. **Python 3.10+** is strictly required.

### Automatic Installation (Recommended)

**Linux / macOS**

```bash
chmod +x setup_env.sh
./setup_env.sh
source venv/bin/activate
```

**Windows** (Run from Command Prompt)

```cmd
setup_env.bat
venv\Scripts\activate.bat
```

### Manual Installation

```bash
git clone https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git
cd dual-arm-dlo-collision-avoidance
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

## Usage

```bash
cd simulation
python demo_pick_cube.py
```

## Roadmap & Next Steps

This repository is actively progressing through a 6-month timeline corresponding to the `ROADMAP.md` tracking plan:

1. **Phase 1: Rigid-Body Baseline (Completed)**: MuJoCo dual-arm environment setup via direct API.
2. **Phase 2: DLO & Planner Integration**: Integrate `qj25/adapteddlomuj` Discrete Elastic Rods (DER) cable model.
3. **Phase 3: CBF Safety Layer**: MPC local controller for path tracking with 4 core CBF constraints via OSQP.
4. **Phase 4: Global Planner Integration**: DIT*/JIT* algorithm adaptation for DLOs with catenary-aware cost functions.
5. **Phase 5: Contact-Aware Fixture Routing**: Mode-switching CBF utilizing Contact Establishment Indicators (CEI) to relax constraints at routing clip contact zones.

---
**Muhammad Mahad**
*(For full details, please refer to the `docs/thesis_proposal.md` document.)*
