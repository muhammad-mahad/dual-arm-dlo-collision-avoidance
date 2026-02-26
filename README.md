# Dual-Arm DLO Collision Avoidance

### M.Sc. Thesis Simulation — Robotics & AI, NUST

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![MuJoCo](https://img.shields.io/badge/MuJoCo-3.x-green)](https://github.com/google-deepmind/mujoco)
[![mink](https://img.shields.io/badge/IK-mink-orange)](https://github.com/kevinzakka/mink)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> **Thesis title:** Hierarchical Collision Avoidance for Dual-Arm Cable Routing —  
> Integrating DLO-Aware Global Planning with Mode-Switching Control Barrier Functions

---

## Demo

![Demo Preview](media/demo_preview.gif)

> Two Franka Emika Panda arms performing autonomous pick-up, contact-aware  
> handover, and smooth millimeter-scale placement in MuJoCo.

📹 **Full demo video:** [Insert YouTube / Drive link]

---

## Overview

This repository contains the simulation foundation for my M.Sc. thesis on  
**hierarchical collision avoidance for dual-arm cable routing**.

The current phase implements a complete rigid-body baseline:

- ✅ Autonomous pick-up from table (right arm, top-down grasp)
- ✅ Contact-aware handover using distance-threshold sensing
- ✅ Smooth, millimeter-scale trajectory interpolation (no joint trajectory pre-computation)
- ✅ Continuous task-space control via **mink differential IK**
- ✅ Freeze-and-freeze gripper isolation to prevent grip loss

The thesis roadmap extends this testbed to **deformable cable manipulation**  
with a full hierarchical planner + CBF safety filter (see [ROADMAP.md](ROADMAP.md)).

---

## Thesis Context

This simulation is developed as part of my M.Sc. thesis in **Robotics and AI** at  
the National University of Sciences and Technology (NUST), Pakistan, under the  
supervision of [Dr. Karam Dad Kallu](https://smme.nust.edu.pk/faculty/karam-dad-1/).

The thesis is directly aligned with the TUM-AIR group's research on  
[contact-aware DLO shaping (IROS 2023)](https://www.youtube.com/watch?v=RUvGRpoiYyQ)  
and the [KI.FABRIK cable routing initiative](https://kifabrik.mirmi.tum.de/solutions/assembly-of-flexible-parts/).

📄 [Read the full thesis proposal](docs/thesis_proposal.md)

---

## Technology Stack

| Component | Choice |
|---|---|
| Physics Engine | MuJoCo 3.x |
| Robot Model | 2× Franka Emika Panda |
| IK Solver | [mink](https://github.com/kevinzakka/mink) (differential IK) |
| DLO Model (planned) | Adapted Discrete Elastic Rods ([adapteddlomuj](https://github.com/qj25/adapteddlomuj)) |
| CBF Solver (planned) | OSQP |
| Language | Python 3.10+ |

---

## Installation

### Prerequisites

- Python 3.10+
- Git

---

### Option 1 — Automated Setup (Recommended)

Clone the repository and run the setup script for your platform. It will automatically create the virtual environment and install all dependencies from `requirements.txt`.

**Linux / macOS**

```bash
git clone https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git
cd dual-arm-dlo-collision-avoidance
chmod +x setup_env.sh
./setup_env.sh
```

**Windows**

```bat
git clone https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git
cd dual-arm-dlo-collision-avoidance
setup_env.bat
```

---

### Option 2 — Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git
cd dual-arm-dlo-collision-avoidance

# 2. Create and activate virtual environment
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt
```

---

### Verify Installation

After either option, confirm everything is working:

```bash
python -c "import mujoco; import mink; from loop_rate_limiters import RateLimiter; import numpy; print('All imports OK')"
```

---

### Run the Demo

```bash
cd simulation
python demo_pick_cube.py
```

A MuJoCo viewer window will open and the 18-phase dual-arm pick-handover-place sequence will begin automatically.

---

## Demo Phases

| Phase | Description |
|---|---|
| P0–P2 | Right arm approaches and grasps cube (top-down orientation) |
| P3 | Right gripper closes — firm grasp established |
| P4–P5 | Right arm lifts cube, wrist reorients to side-grip, moves to handover position |
| P6–P8 | Left arm approaches with contact sensing (distance threshold: 10 mm) |
| P9–P10 | Synchronized clamping — both grippers close, right gripper opens (handover complete) |
| P11a–P11b | Left arm moves sideways at constant height, then lifts (prevents inertial slip) |
| P12 | Right arm retreats — left arm fully frozen at current joint state |
| P13–P15 | Left carry via smooth 1 mm waypoint interpolation to table center |
| P16–P17 | Cube settles on table, left gripper opens |
| P18 | Left arm retreats |

---

## Project Roadmap

See [ROADMAP.md](ROADMAP.md) for the complete thesis implementation plan.

| Phase | Status | Description |
|---|---|---|
| Phase 1: Rigid-body baseline | ✅ Complete | Current repo — pick, handover, place |
| Phase 2: DLO integration | 🔲 Planned | Replace cube with DER cable model |
| Phase 3: CBF safety layer | 🔲 Planned | Arm-arm, arm-env, cable-env, tension constraints |
| Phase 4: Global planner | 🔲 Planned | DIT*/JIT* with DLO-aware collision checker |
| Phase 5: Contact-aware routing | 🔲 Planned | Mode-switching CBF via CEI for fixture insertion |

---

## References

1. Chen, K. et al. — *Contact-aware Shaping and Maintenance of DLOs with Fixtures*, IROS 2023
2. Chen, K. et al. — *Real-time Contact State Estimation for DLOs*, ICRA 2024
3. Yu, M. et al. — *Coarse-to-Fine Framework for Dual-Arm DLO Manipulation*, ICRA 2023
4. Zhang, L. et al. — *Direction Informed Trees (DIT\*)*, arXiv 2025
5. Cai, K. & Zhang, L. et al. — *Just-in-Time Informed Trees (JIT\*)*, arXiv 2026

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Contact

**[Muhammad Mahad]**  
M.Sc. Candidate, Robotics & AI — NUST, Pakistan  
[LinkedIn](https://www.linkedin.com/in/muhammad-mahad/) | [Email](mailto:mmahad.rime24smme@student.nust.edu.pk)
