# Master's Thesis Proposal

## Title

**Safe Dual-Arm Cable Routing with Deformable Linear Objects: Hierarchical Planning and Contact-Aware Control Barrier Functions**

---

## Table of Contents

1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
   - [Problem Statement](#21-problem-statement)
   - [Objectives](#22-objectives)
3. [Related Work](#3-related-work)
4. [Methodology](#4-methodology)
   - [MuJoCo Simulation and Adapted DER Model](#41-mujoco-simulation-and-adapted-der-model)
   - [Level 1: Global Motion Planner](#42-level-1-global-motion-planner-jitdit)
   - [Level 2: Local Controller](#43-level-2-local-controller-mpc--mode-switching-cbf)
   - [Stress Testing](#44-stress-testing)
5. [Tools & Technologies](#5-tools--technologies)
6. [References](#7-references)

---

## 1. Abstract

The manipulation of deformable linear objects (DLOs), such as cables, is a crucial step in industrial manufacturing. Unlike rigid bodies, routing a DLO through constrained environments using dual-arm manipulation introduces severe motion planning challenges. A robust system must handle three distinct safety aspects simultaneously: \
(1) Arm–arm self-collision \
(2) Arm/cable environment collision \
(3) Contact-aware fixture interaction (distinguishing necessary, desired clip insertions from unintended collisions) \
Currently, no existing framework integrates all three capabilities into a unified, computationally scalable system.

This thesis proposes a novel hierarchical collision-avoidance framework for dual-arm cable routing in simulation. The architecture utilizes a global planner extending advanced, highdimensional planners such as Just-in-Time (JIT) or Direction Informed Trees (DIT*) to compute DLO-aware coarse paths efficiently. This global path is tracked by a local controller featuring Model Predictive Control (MPC) wrapped in a Control Barrier Function (CBF) safety filter. Crucially, CBF employs a mode-switching mechanism driven by forcebased contact estimation to allow safe interactions with fixtures while rigorously preventing other collisions. Built purely on the MuJoCo API utilizing the adapted Discrete Elastic Rods (DER) cable model, this CPU-efficient, minimal-middleware prototype serves as a highly scalable validation testbed with a clear path to future real-robot deployment.

**Keywords**: Dual-Arm Manipulation, Deformable Linear Objects (DLO), Hierarchical Collision Avoidance, Just-in-Time Informed Trees (JIT), Control Barrier Functions (CBF), Mode-Switching, Contact-Aware Safety, MuJoCo.

## 2. Introduction

### 2.1 Problem Statement

Routing cables through environmental fixtures requires precise dual-arm coordination to maintain proper tension and guide the infinite-dimensional DLO. Traditional motion planners struggle in this domain due to the massive configuration space (14-DoF for two Franka Panda arms plus the DLO state).

To ensure safety without relying on computationally prohibitive full-physics rollouts, the system must navigate a complex collision landscape. It must definitively avoid arm–arm self-collisions and arm/cable environment collisions. However, because the task explicitly requires the DLO to touch and snap into routing clips, the system cannot treat all environmental contacts as failures. The core problem is creating a hierarchical architecture that merges fast global pathfinding with a local safety layer capable of contact-aware collision avoidance (distinguishing good clip insertions from bad collisions).

### 2.2 Objectives

The primary objective is to design a hierarchical collision-avoidance framework for dual-arm cable routing in simulation, utilizing realistic DLO models and scalable planners, with a clear path to real-robot deployment. Specific objectives include:

1. **Simulation Layer**: Build a clean, minimal-middleware research prototype directly around the MuJoCo API using the adapted DER model to simulate realistic cable bending, twisting, and sagging without requiring GPU acceleration.
2. **Global Planning (Level 1)**: Implement a DLO-aware global planner using DIT* or JIT style algorithms to significantly reduce planning time in the 14-DoF + DLO space, using a catenary-aware cost function.
3. **Local Control & Safety (Level 2)**: Develop an MPC local controller wrapped with a CBF QP to track the global path while strictly enforcing four safety constraints: arm–arm, arm–environment, cable–environment, and DLO overstretch limits.
4. **Contact-Aware Interaction**: Integrate mode-switching logic into the CBF, allowing the system to temporarily relax specific environmental collision constraints during force-validated clip insertions.

## 3. Related Work

Recent DLO manipulation studies strongly advocate for hierarchical systems consisting of a global planner for coarse motion and a local controller for responsive shaping. Yu et al. (2023) utilized this exact architecture, employing MPC with artificial potential fields to achieve whole-body obstacle avoidance during dual-arm manipulation.

However, standard global planners like RRT scale poorly in such high-dimensional spaces. Recent TUM-AIR group developments, specifically Direction Informed Trees (DIT*) and Justin-Time Informed Trees (JIT), drastically reduce global planning times by minimizing unnecessary collision checks. This thesis seeks to extend these planners, which are currently focused on rigid objects, to include DLO-inclusive collision checking.

For local safety, Control Barrier Functions (CBFs) provide mathematical guarantees for collision avoidance. Furthermore, Zhu et al. (2019) and Chen et al. (2023, 2024) have demonstrated that explicitly exploiting environmental contacts and utilizing forcedependent state estimation is vital for complex shaping tasks. This project unifies these concepts, utilizing mode-switching CBFs to merge guaranteed collision avoidance with necessary fixture interaction.

## 4. Methodology

To ensure maximum CPU performance and match state-of-the-art simulation-first pipelines (such as DLOplanning2), the initial framework will bypass heavy middleware (ROS 2/MoveIt 2) and interface directly with MuJoCo via Python/C++.

### 4.1 MuJoCo Simulation and Adapted DER Model

The environment will feature a dual arm `bi-frankapanda.xml` MJCF base. The cable will be simulated using the `qj25/adapteddlomuj` Discrete Elastic Rods (DER) implementation. This approach replaces native MuJoCo composite objects, offering vastly superior bending/twisting mechanics critical for accurate collision checking during routing.

### 4.2 Level 1: Global Motion Planner (DIT* or JIT)

The global layer will generate a coarse, collision-free path.

- **Algorithm Base**: The system will use the TUM group's DIT* implementation (already validated on dual-arm cable routing tasks) or the DLOplanning2 CBiRRT as a baseline, upgrading to JIT if the source is available.
- **Collision & Cost**: During sampling, MuJoCo's native contact geometry (capsules and spheres) will be used to check the 14-DoF arms, the DER cable geometry, and fixtures. A catenary-aware cost function will penalize states where the predicted DLO sag approaches obstacles.

### 4.3 Level 2: Local Controller (MPC + Mode-Switching CBF)

The local controller will follow the coarse path while reacting to dynamic states. The baseline will use MPC (similar to Yu et al.), upgraded with a CBF Quadratic Program (QP) safety filter.

- **Safety Constraints**: The CBF will use MuJoCo's geometric distance queries to enforce four constraints:
  - $h_{arm-arm} \ge 0$
  - $h_{arm-env} \ge 0$
  - $h_{cable-env} \ge 0$
  - ...and a tension limit to prevent cable snapping.
- **Mode-Switching via Contact Estimation**: To achieve contact-aware fixture interaction, the system will monitor simulated end-effector force-torque sensors. Upon detecting a defined Contact Establishment Indicator (CEI) signature near a routing clip, the CBF will switch modes locally relaxing the $h_{arm/cable-env}$ constraint for that specific fixture to permit insertion.

### 4.4 Stress Testing

To prove the robustness of the CBF safety filter over open-loop planning, the local controller will be stressed by injecting fast dynamic motions and introducing simulated dynamic obstacles into the workspace, monitoring for any failure in the three core safety aspects.

## 5. Tools & Technologies

- **Physics Simulator**: MuJoCo 3.x (*direct Python/C++ API; bypassing ROS for Phase 1*)
- **Robot Models**: Dual Franka Emika Panda (*vikashplus/frankasim*)
- **Cable Physics Model**: Adapted Discrete Elastic Rods (DER) via `qj25/adapteddlomuj`
- **Kinematics**: Pinocchio / `mink` IK library
- **Optimization**: OSQP or qpOASES (for the CBF-QP)
- **Hardware Sync**: ROS Integration for seamless future real-world deployment and hardware synchronization

## 7. References

- Yin, H., Varava, A., & Kragic, D. (2021). "Modeling, learning, perception, and control methods for deformable object manipulation." **Science Robotics**, 6(54).
- Zhu, J., et al. (2019). "Robotic manipulation planning for shaping deformable linear objects with environmental contacts." **IEEE Robotics and Automation Letters**.
- McConachie, D., et al. (2020). "Manipulating deformable objects by interleaving prediction, planning, and control." **The International Journal of Robotics Research**.
- Yu, M., et al. (2023). "A coarse-to-fine framework for dual-arm manipulation of deformable linear objects with whole-body obstacle avoidance." **2023 IEEE International Conference on Robotics and Automation (ICRA)**.
- Chen, K., Bing, Z., et al. (2023). "Contact-aware Shaping and Maintenance of Deformable Linear Objects With Fixtures." **2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)**.
- Chen, K., et al. (2024). "Real-time Contact State Estimation in Shape Control of Deformable Linear Objects under Small Environmental Constraints." **ICRA**.
- Zhang, L., et al. (2025). "Direction Informed Trees (DIT*): Optimal Path Planning via Direction Filter and Direction Cost Heuristic." **arXiv preprint** arXiv:2508.19168.
- Cai, K., Zhang, L., et al. (2026). "Just in time Informed Trees: Manipulability-Aware Asymptotically Optimized Motion Planning." **arXiv preprint** arXiv:2601.19972.
- Zeng, Q., et al. (2023). "Accurate Simulation and Parameter Identification of Deformable Linear Objects in MuJoCo." **arXiv preprint** arXiv:2310.00911.
- Laha, R., et al. (2024). "Safe Multi-Robotic Arm Interaction via 3D Convex Shapes." **arXiv preprint** arXiv:2503.11791.
- Grandia, F., et al. (2021). "Safety-Critical Model Predictive Control with Discrete-Time Control Barrier Functions." **American Control Conference (ACC)**.
