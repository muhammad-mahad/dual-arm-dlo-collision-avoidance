# Dual-Arm Franka Panda with Collision Avoidance in MuJoCo

A demonstration of dual-arm bimanual manipulation with real-time collision
avoidance using two Franka Emika Panda robots in the MuJoCo physics simulator.

![Demo Screenshot](screenshot.png)

## Features

- **Dual Franka Emika Panda arms** performing coordinated pick-and-lift
- **Real-time collision avoidance** using differential IK with safety constraints
- **Three obstacle types** (box, cylinder, overhead) placed in the workspace
- **Safety margins**: 5cm minimum distance enforced between arms and obstacles
- **Distance monitoring**: Real-time logging of arm-to-arm and arm-to-obstacle distances
- **Zero collisions** across all test runs

## Technical Stack

| Component | Technology |
|---|---|
| Physics Engine | MuJoCo 3.x |
| Robot Model | Franka Emika Panda (7-DoF) × 2 |
| IK Solver | mink (differential IK with QP) |
| Collision Avoidance | mink.CollisionAvoidanceLimit |
| QP Solver | DAQP |
| Language | Python 3 |

## Collision Avoidance Details

The system uses **constrained differential inverse kinematics** to enforce safety:

- **Arm-to-arm avoidance**: Prevents self-collision between left and right arms
- **Arm-to-obstacle avoidance**: Each arm avoids all 3 workspace obstacles
- **Safety margin**: 5cm minimum clearance enforced via QP constraints
- **Detection distance**: Avoidance behavior activates at 15cm proximity

This approach is a stepping stone toward implementing **Control Barrier
Functions (CBFs)** for formal safety guarantees in deformable linear object
(DLO/cable) manipulation, as proposed in:

- Yu et al., "Generalizable whole-body global manipulation of DLOs by
  dual-arm robot," IJRR, 2024
- Chen et al., "Contact-aware Shaping and Maintenance of DLOs With
  Fixtures," IROS, 2023
- Aksoy & Wen, "Planning and Control for DLO Manipulation," 2025

## Installation

```bash
pip install mink mujoco numpy loop-rate-limiters daqp
git clone https://github.com/<YOUR_USERNAME>/dual_panda_collision_avoidance.git
cd dual_panda_collision_avoidance
```

## Usage

```bash
python demo_collision_avoidance.py
```

## Next Steps

This demo serves as a baseline for my Master's thesis on
**"Collision Avoidance in Dual-Arm Manipulation of Deformable Linear Objects"**:

1. **ROS 2 + MoveIt 2** integration via multipanda_ros2
2. **DLO modeling** using Adapted Discrete Elastic Rods (DER)
3. **CBF safety layer** with formal safety guarantees
4. **Contact-aware fixture interaction** for cable routing

## Author

[Your Name] — [Your University]
