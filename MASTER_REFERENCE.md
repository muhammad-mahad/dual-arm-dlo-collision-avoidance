# Master Literature Reference: AIC Challenge + Thesis

All papers, repos, surveys, and research gaps consolidated from all source files. No implementation plans -- literature only.

---

## PART A: THESIS LITERATURE (Dual-Arm DLO Manipulation with Collision Avoidance)

Organized by the five thesis pipeline steps.

---

### Step 1: DLO State Estimation & Perception

#### 1.1 Real-Time Tracking Under Occlusion

**TrackDLO: Tracking Deformable Linear Objects Under Occlusion with Motion Coherence**
- Authors: Jingyi Xiang, Holly Dinkel, Harry Zhao, Naixiang Gao, Brian Coltin, Trey Smith, Timothy Bretl
- Venue: IEEE RA-L, Vol. 8, No. 10, pp. 6179-6186, 2023; Presented at ICRA 2024 (finalist for best paper award)
- DOI: 10.1109/LRA.2023.3303710
- Link: [doi.org/10.1109/LRA.2023.3303710](https://doi.org/10.1109/LRA.2023.3303710)
- Code: [github.com/RMDLO/trackdlo](https://github.com/RMDLO/trackdlo)
- What it does: Vision-only real-time DLO tracking from RGB-D sequences. Uses Motion Coherence Theory to handle tip, mid-section, and self-occlusion. No markers, no physics model required.
- Relevance: Go-to baseline for DLO perception in constrained environments. During cable routing around fixtures, DLO will be frequently occluded.
- Limitations: Does not incorporate contact forces from fixtures; degrades with severe full-body occlusion.

**GraphDLO: Graph-Based Neural Dynamics for DLO Trajectory Prediction**
- Authors: Holly Dinkel, Muhammad Zahid, Bhumsitt Pramuanpornsatid, Brian Coltin, Trey Smith, Florian Pokorny, Timothy Bretl
- Venue: Published 2025 (RMDLO lab)
- Link: [florianpokorny.com/static/publications/dinkel2025a.pdf](https://florianpokorny.com/static/publications/dinkel2025a.pdf)
- What it does: GNN trained on 300-hour dataset to predict future DLO trajectories under prehensile and non-prehensile interactions; predicts up to 10-step ahead.
- Relevance: Enables predictive collision checking -- knowing where cable will be before the robot gets there.

#### 1.2 Online Parameter Estimation

**Deformable Linear Objects Manipulation With Online Model Parameters Estimation**
- Authors: Alessio Caporali, Piotr Kicki, Kevin Galassi, Riccardo Zanella, Krzysztof Walas, Gianluca Palli
- Venue: IEEE RA-L, 2024
- Code: [github.com/lar-unibo/dlo_manipulation_online_params](https://github.com/lar-unibo/dlo_manipulation_online_params)
- Link: [researchgate.net/publication/377640143](https://www.researchgate.net/publication/377640143_Deformable_Linear_Objects_Manipulation_with_Online_Model_Parameters_Estimation)
- What it does: Neural network mimic of DLO dynamics conditioned on material parameters. Simultaneously estimates model parameters online via gradient-based optimization while performing shape control.
- Relevance: Key enabler for generalizing collision avoidance framework to different cable types without re-training.

#### 1.3 Real-Time Segmentation

**RT-DLO: Real-Time Deformable Linear Objects Instance Segmentation**
- Authors: Alessio Caporali et al. (University of Bologna)
- Venue: IEEE RA-L / IEEE Trans. Industrial Informatics, 2023
- Code: [github.com/lar-unibo/RT-DLO](https://github.com/lar-unibo/RT-DLO)
- Link: [doi.org/10.1109/LRA.2023.3266070](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10045806)
- What it does: >30 FPS instance segmentation of DLOs using skeleton-based graph approach on semantic masks. No assumptions about background or number of DLOs.
- Relevance: 2D perception front-end for dual-arm camera system.

#### 1.4 Comprehensive Survey

**Robotic Perception and Manipulation of Deformable Linear Objects: A Survey**
- Authors: Caporali, Galassi, et al. (University of Bologna)
- Venue: International Journal of Robotics Research (IJRR), first published online March 27, 2026
- Link: [doi.org/10.1177/02783649251329748](https://journals.sagepub.com/doi/epdf/10.1177/02783649261432253)
- Impact: IJRR is top robotics journal (IF ~9). Most up-to-date comprehensive DLO survey. Primary reference anchor.

#### 1.5 Additional Perception & Estimation

**UniStateDLO: Unified Generative State Estimation and Tracking of DLOs Under Occlusion**
- Authors: Lv, Yu et al.
- Venue: arXiv 2512.17764, Dec 2025 (preprint)
- Link: [arxiv.org/abs/2512.17764](https://arxiv.org/abs/2512.17764)
- What it does: Diffusion-model-based DLO state estimation under occlusion. Provides uncertainty estimates.
- Relevance: Uncertainty can feed into probabilistic collision constraints (Gap 3).

**GNN Topology Representation Learning for Deformable Multi-Linear Objects Dual-Arm Robotic Manipulation**
- Authors: Caporali et al. (University of Bologna)
- Venue: IEEE T-ASE, 2025
- Link: [doi.org/10.1109/TASE.2025.3562231](https://doi.org/10.1109/TASE.2025.3562231)
- What it does: GNN-based topology representation for multi-DLO manipulation in dual-arm settings.

**Interactive Perception for Deformable Object Manipulation**
- Authors: Weng et al.
- Venue: IEEE RA-L, 2024
- Link: [arxiv.org/abs/2403.05177](https://arxiv.org/abs/2403.05177)
- What it does: Interactive perception framework for deformable object manipulation.

**SPiD: Self-supervised Physics-Informed Manipulation of Deformable Linear Objects**
- Authors: Long et al.
- Venue: arXiv preprint, Feb 2026
- Link: [arxiv.org/abs/2602.03623](https://arxiv.org/abs/2602.03623)
- What it does: Self-supervised physics-informed DLO manipulation approach.

**Learning DLO Dynamics from a Single Trajectory**
- Authors: Mamedov, Geist, Viljoen, Trimpe, Swevers (RWTH Aachen / KU Leuven)
- Venue: IEEE Robotics and Automation Letters, Vol. 10, No. 7, 2025 — DOI: 10.1109/LRA.2025.3577421
- Link: [doi.org/10.1109/LRA.2025.3577421](https://doi.org/10.1109/LRA.2025.3577421)
- What it does: Physics-structured Gaussian Process model that learns accurate DLO dynamics from a single demonstration trajectory. Directly addresses the data scarcity problem for cable routing with new fixture layouts. Open-source code available.

**A Physics-Informed Neural Network Framework for Real-Time Model Predictive Shape Manipulation of DLOs**
- Venue: IEEE, 2026
- Link: [ieeexplore.ieee.org/document/11317980](https://ieeexplore.ieee.org/document/11317980/)
- What it does: PINN framework for real-time MPC-based shape manipulation of DLOs.

**Accurate Simulation and Parameter Identification of DLOs using Discrete Elastic Rods in MuJoCo**
- Authors: Qj25 / Chen et al.
- Venue: 2025
- Link: [arxiv.org/abs/2310.00911](https://arxiv.org/abs/2310.00911)
- Code: [github.com/qj25/der_mujoco](https://github.com/qj25/der_mujoco) and [github.com/qj25/adapteddlo_muj](https://github.com/qj25/adapteddlo_muj)
- What it does: DER-based cable simulation and parameter identification in MuJoCo. Thesis foundation.

**Robotic Manipulation of Deformable Linear Objects via Multiview Visual Tracking**
- What it does: Multiview visual tracking approach for DLO manipulation.
- Code: [lar-unibo/DLO_MultiView_Tracking](https://github.com/lar-unibo/DLO_MultiView_Tracking) (Cosserat rod multiview tracking)

#### 1.6 Additional Perception Papers (NEW)

**DLO3DS: Deformable Linear Objects 3D Shape Estimation and Tracking**
- Authors: Caporali, Galassi et al. (University of Bologna)
- Venue: IEEE Robotics and Automation Letters, Vol. 8, 2023
- Link: [doi.org/10.1109/LRA.2023.3273518](https://doi.org/10.1109/LRA.2023.3273518)
- What it does: Estimates 3D DLO shape from multiple 2D views using B-spline fitting and multi-view stereo. Achieves mean shape error of 0.82 mm — sufficient for precision cable routing. Compatible with standard ROS setups.
- Relevance: Provides high-accuracy 3D shape estimation without depth sensors, directly applicable to industrial setups where depth sensors are impractical near fixtures.

**3D Understanding of Deformable Linear Objects: Datasets and Transferability**
- Authors: Zagar et al.
- Venue: IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), 2025
- Link: [arxiv.org/abs/2310.08904](https://arxiv.org/abs/2310.08904)
- What it does: First published benchmark dataset for DLO 3D shape understanding. Studies transferability of learned models across different cable types and lighting conditions. Enables standardized performance comparisons for Stage 1 evaluation.
- Relevance: Directly usable for evaluating the DLO state estimator against prior methods on a standardized benchmark.

**A Robust Deformable Linear Object Perception Pipeline in 3D**
- Authors: Sun et al.
- Venue: IEEE Robotics and Automation Letters, 2023/2024
- Link: [doi.org/10.1109/LRA.2023.3337695](https://doi.org/10.1109/LRA.2023.3337695)
- What it does: Full perception pipeline covering detection, segmentation, and 3D reconstruction from RGB-D images. Explicitly addresses crossing and overlapping cable configurations arising in cable-routing tasks with fixtures.
- Relevance: Complementary to TrackDLO for handling complex multi-cable configurations in industrial setups.

**Recognizing and Picking Up Deformable Linear Objects Based on Graph Neural Networks**
- Authors: Shi & Yamakawa et al. (University of Tokyo)
- Venue: Journal of Robotics and Mechatronics (Fuji Technology Press), Vol. 37, No. 2, April 2025
- Link: [doi.org/10.20965/jrm.2025.p0335](https://doi.org/10.20965/jrm.2025.p0335)
- What it does: Graph-based representation for simultaneous classification and grasp-point estimation of DLOs in cluttered scenes. Particularly valuable for initializing dual-arm grasp prior to routing.
- Relevance: Pre-manipulation perception for identifying correct grasp points on industrial cables before routing begins.

**Multi-View, Model-Based Visual Tracking of Deformable Linear Objects During Robotic Manipulation**
- Authors: Caporali, Palli et al. (University of Bologna)
- Venue: RMDO Workshop at ICRA 2025 (spotlight); journal submission to IEEE RA-L in progress
- Link: [deformable-workshop.github.io/icra2025/spotlight/02_05_09_Caporali_multi.pdf](https://deformable-workshop.github.io/icra2025/spotlight/02_05_09_Caporali_multi.pdf)
- What it does: Tracks DLO 3D shape from multiple standard 2D cameras (no depth sensors) using model-based optimization. Unlike TrackDLO, works with cheaper standard cameras — directly relevant for industrial setups where depth sensors are impractical near fixtures.
- Relevance: Multi-view tracker for TUM dual-arm cable routing setup where depth sensors may be occluded by robot arms during fixture mounting phases. Monitor for formal RA-L publication.

#### Step 1 Summary

| Paper | Venue | Year | Code | Key Contribution |
|-------|-------|------|------|-----------------|
| TrackDLO | IEEE RA-L / ICRA 2024 | 2023 | Yes | Real-time tracking under occlusion |
| GraphDLO | RMDLO lab | 2025 | -- | GNN trajectory prediction, 10-step ahead |
| DLO Online Param Est. | IEEE RA-L | 2024 | Yes | Online material adaptation |
| RT-DLO | IEEE RA-L | 2023 | Yes | Real-time segmentation >30fps |
| DLO Survey | IJRR | 2026 | -- | Full state-of-the-art survey |
| UniStateDLO | arXiv | 2025 | -- | Diffusion-based under occlusion |
| Caporali GNN Topology | IEEE T-ASE | 2025 | -- | Multi-DLO dual-arm GNN |
| Weng et al. | 2024 | 2024 | -- | Interactive perception for DLO |
| SPiD (Long et al.) | 2026 | 2026 | -- | Self-supervised physics-informed |
| Mamedov et al. | IEEE RA-L | 2025 | Yes | Single-trajectory GP dynamics learning |
| PINN for DLO MPC | 2026 | 2026 | -- | Physics-informed NN for shape MPC |
| Qj25/Chen DER MuJoCo | 2025 | 2025 | Yes | DER simulation in MuJoCo |
| Multiview DLO Tracking | -- | -- | Yes | Multiview visual tracking |
| DLO3DS (Caporali et al.) | IEEE RA-L | 2023 | -- | 3D shape from multi-view, 0.82mm error |
| Zagar et al. | WACV | 2025 | Partial | Benchmark for 3D DLO understanding + transfer |
| Sun et al. | IEEE RA-L | 2024 | -- | Robust 3D perception pipeline, crossings |
| Sakuma et al. | JRM | 2025 | -- | GNN-based DLO recognition and grasp |
| Caporali Multi-View | ICRA Workshop / RA-L (under review) | 2025 | -- | Multi-view model-based tracking, no depth |

---

### Step 2: DLO Modeling

#### 2.1 Data-Driven: Neural Networks & GNNs

**Time-Series Data-Driven 3D Shape Control of DLOs Using a Dual-Arm Robot With Dynamic Model Updating**
- Authors: Jiyoung Choi, Micheale Haileslassie Gebrezgiher, Donggun Lee, Ayoung Hong
- Venue: IEEE RA-L, Vol. 11, No. 3, pp. 2849-2856, March 2026
- DOI: 10.1109/LRA.2026.3655208
- Link: [doi.org/10.1109/LRA.2026.3655208](https://doi.org/10.1109/LRA.2026.3655208)
- Simulation: CoppeliaSim V-REP; two heterogeneous arms (UR5e + RB5-850); ROS2
- What it does: Bi-LSTM network on time-series data for DLO future state prediction. MPC with online residual learning (MPCOLI) and interpolation for varying cable configurations. 3x faster than chain-like baselines (RMSE 0.71 cm at horizon 1).
- Relevance: Most current (2026) dual-arm DLO control paper. Online update mechanism is template for adaptive models when cable deforms around fixtures. Simulator setup (UR5e + CoppeliaSim + ROS2) is direct template.
- **Research Gap (explicit in paper):** "While the proposed approach demonstrated reliable cable manipulation under controlled, obstacle-free conditions, its applicability to more realistic settings remains limited." -- Direct thesis gap.

**Shape Control of Elastic Deformable Linear Objects for Robotic Cable Assembly**
- Authors: Bin Cao, Xizhe Zang, Xuehe Zhang, Zhuo Chen, Shouqiang Li, Jie Zhao
- Venue: Advanced Intelligent Systems, Vol. 6, No. 7, 2024
- Link: [doi.org/10.1002/aisy.202300835](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202300835)
- What it does: GNN global model with visual feedback for 3D shape control. IPOPT interior-point solver for MPC. Validated on aircraft assembly.

**Offline-Online Learning with GNN for Cable Manipulation**
- Authors: C. Wang et al.
- Venue: IEEE RA-L, Vol. 7, No. 2, pp. 5544-5551, April 2022 (referenced in 2024-2026 works)
- Link: [10.1109/LRA.2022.3158376](https://ieeexplore.ieee.org/document/9732674)
- Code: github.com/Mingrui-Yu/shape_control_DLO_2 (Yu et al. T-RO version)

#### 2.2 Additional Data-Driven Models

**Rearranging Deformable Linear Objects for Implicit Goals with Self-Supervised Planning and Control**
- Authors: Huo et al.
- Venue: Advanced Intelligent Systems, 2024
- Link: [doi.org/10.1002/aisy.202400330](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aisy.202400330)
- What it does: Self-supervised planning and control for DLO rearrangement toward implicit goals.

#### 2.3 Data-Driven: Adaptive Online Learning

**Global Model Learning for Large Deformation Control of Elastic DLOs: An Efficient and Adaptive Approach**
- Authors: Mingrui Yu, Kangchen Lv, Hanzhong Zhong, Shiji Song, Xiang Li
- Venue: IEEE T-RO, Vol. 39, No. 1, pp. 417-436, Feb 2023
- Link: [10.1109/TRO.2022.3200546](https://ieeexplore.ieee.org/document/9888782)
- Code: [github.com/Mingrui-Yu/shape_control_DLO_2](https://github.com/Mingrui-Yu/shape_control_DLO_2)
- What it does: Coupled offline-online neural network for global deformation model. Lyapunov-stable controller. Handles untrained DLOs via online adaptation. 24 tasks with different DLOs in real world.
- Relevance: Gold-standard model learning baseline.

#### 2.3 Physics-Based: Cosserat / Strain-Based Dynamics

**Controlling Deformable Objects with Nonnegligible Dynamics: A Shape-Regulation Approach to End-Point Positioning**
- Authors: Sebastien Tiburzio, Tomas Coleman, Daniel Feliu-Talegon, Cosimo Della Santina (TU Delft + DLR)
- Venue: IEEE T-RO, Vol. 41, pp. 6213-6228, 2025
- Link: [10.1109/TRO.2025.3620806](https://ieeexplore.ieee.org/document/11202387)
- What it does: Strain-based functional parameterization for DLO dynamics with nonnegligible inertial effects. Fully model-based with analytically proven closed-loop stability. Validated on 6 cables.
- Relevance: Addresses key limitation of quasi-static assumptions in most DLO controllers. Critical for high-speed cable routing.

**Robotic Co-Manipulation of Deformable Linear Objects for Large Deformation Tasks**
- Authors: Almaghout, Cherubini, Klimchik
- Venue: Robotics and Autonomous Systems, Vol. 175, Art. 104652, 2024
- Link: [doi.org/10.1016/j.robot.2024.104652](https://doi.org/10.1016/j.robot.2024.104652)
- What it does: ISG (Intermediary Shapes Generation) algorithm with optimization-based controller for dual-arm large deformation tasks. No extensive modeling or training. Handles opposite-concavity shape changes.
- Relevance: Computationally lightweight alternative for global planning in dual-arm setup.

#### 2.4 FEM-Based (Dual-Arm)

**Dual-Arm Shaping of Soft Objects in 3D Based on Visual Servoing and Online FEM Simulations**
- Authors: Celia Saghour, David Navarro-Alarcon, Philippe Fraisse, Andrea Cherubini
- Venue: IJRR, Vol. 44, Issue 7, first published December 10, 2024
- DOI: 10.1177/02783649241301076
- Link: [doi.org/10.1177/02783649241301076](https://doi.org/10.1177/02783649241301076)
- What it does: Combines data-based learning of robot action-to-deformation mapping with online FEM simulations to estimate full shape from visual features (PCA). Continuously corrects deformed mesh before updating interaction matrix.
- Relevance: Shows FEM in real-time for dual-arm -- potential integration with collision checking using predicted mesh.

#### 2.5 Additional Modeling Papers (NEW)

**GA-Net: Learning Graph Dynamics with Interaction Effects Propagation for Deformable Linear Objects Shape Control**
- Venue: IEEE Transactions on Automation Science and Engineering (T-ASE), January 2025 — DOI: 10.1109/TASE.2025.3429XXX (IEEE Xplore: 10845081)
- Project page: [parkergu.github.io/work_dlo](https://parkergu.github.io/work_dlo)
- Link: [ieeexplore.ieee.org/document/10845081](https://ieeexplore.ieee.org/document/10845081)
- What it does: Graph Neural Network with attention mechanism (GA-Net) that learns local interaction effects between neighboring DLO particles and propagates them globally. Achieves 14.14% better prediction accuracy than the previous best baseline (IN-BiLSTM). Validated in simulation and real-world across multiple DLO types. Coupled with MPC for shape control.
- Relevance: State-of-the-art published learning-based DLO dynamics model. Generalizes to unseen DLOs without retraining — critical for multi-cable industrial setup. Directly usable as prediction model inside Stage 4 MPC controller.
- Gap exposed: GA-Net MPC has no safety layer — thesis adds CBF safety filter on top of this exact MPC formulation.

**Parametric Modeling of Deformable Linear Objects for Robotic Outfitting and Maintenance of Space Systems**
- Authors: Quartaro, Pöhlmann et al.
- Venue: Frontiers in Robotics and AI, 2025
- Link: [pubmed.ncbi.nlm.nih.gov/40799461](https://pmc.ncbi.nlm.nih.gov/articles/PMC12340519/)
- What it does: Energy-based DLO model accounting for non-zero bend equilibrium (important for pre-bent cables in industry). Parameter estimation validated on UR10e robot. Directly applicable to modeling industrial cable types with complex resting shapes.
- Relevance: Extends standard straight-equilibrium models to cables with pre-formed shapes — common in automotive wire harness routing.

**Online Iterative Learning Enhanced Sim-to-Real Transfer for Efficient Deformable Object Manipulation**
- Authors: Chen et al. (different from TUM Chen)
- Venue: Machine Intelligence Research (Springer), Vol. 22, No. 4, pp. 696–712, 2025
- Link: [doi.org/10.1007/s11633-025-1566-0](https://link.springer.com/article/10.1007/s11633-025-1566-0)
- What it does: Iterative Parameter Projection (IPP) method that eliminates need for large-scale training data and demonstrates superior performance over LQR, SMC, and MPC baselines on real deformable manipulation. Published online iterative learning approach for adapting DLO models to real-robot deployment.
- Relevance: Sim-to-real transfer methodology directly applicable for adapting DLO models to real-robot deployment (Gap 5 of thesis).

#### Step 2 Summary

| Paper | Venue | Year | Code | Model Type |
|-------|-------|------|------|-----------|
| Choi et al. | IEEE RA-L | 2026 | -- | bi-LSTM + MPC + online |
| Cao et al. | Adv. Intell. Syst. | 2024 | -- | GNN + MPC |
| Wang et al. | IEEE RA-L | 2022 | Yes | GNN offline-online |
| Yu et al. | IEEE T-RO | 2023 | Yes | Neural + adaptive |
| Tiburzio et al. | IEEE T-RO | 2025 | -- | Cosserat strain dynamics |
| Almaghout et al. | RAS | 2024 | -- | ISG optimization |
| Saghour et al. | IJRR | 2024/2025 | -- | FEM visual servoing |
| GA-Net | IEEE T-ASE | 2025 | Partial | GNN attention, 14% better, multi-contact |
| Quartaro et al. | Frontiers Robotics AI | 2025 | -- | Non-zero bend equilibrium param. estim. |
| Online Iter. Learning (Chen) | Machine Intelligence Research | 2025 | -- | IPP sim-to-real, outperforms MPC/LQR |

---

### Step 3: Global Motion Planning

#### 3.1 Whole-Body Dual-Arm DLO Planning

**Generalizable Whole-Body Global Manipulation of Deformable Linear Objects by Dual-Arm Robot in 3-D Constrained Environments**
- Authors: Mingrui Yu, Kangchen Lv, Changhao Wang, Masayoshi Tomizuka, Yun-Hui Liu, Xiang Li
- Venue: IJRR, 2024
- Link: [doi.org/10.1177/02783649241276886](dl.acm.org/doi/10.1177/02783649241276886)
- Code: [github.com/Mingrui-Yu/DLO_planning_2](https://github.com/Mingrui-Yu/DLO_planning_2) (C++ + ROS Noetic + Unity simulator)
- What it does: Whole-body planning treating both robot arms and DLO as unified state. Energy-based DLO model for coarse planning plus local closed-loop correction. Handles 3D environments with obstacles, fixtures, joint limits.
- Relevance: **Most complete published system closest to thesis target.** Extend by adding explicit inter-robot, robot-DLO, and DLO-environment collision avoidance constraints into planner.
- Gap: Uses simplified energy model for DLO, leading to planning errors corrected by local controller. Tighter integration of learned model would improve robustness.

**Multi-Stage Cable Routing Through Hierarchical Imitation Learning**
- Authors: Jianlan Luo, Charles Xu, Xinyang Geng, et al.
- Venue: IEEE T-RO, 2024, DOI: 10.1109/tro.2024.3353075
- Link: [doi.org/10.1109/tro.2024.3353075](https://doi.org/10.1109/tro.2024.3353075)
- What it does: Hierarchical IL (high-level sequencing + low-level motor control) for routing cables through clips. Vision-based policies from demonstrations.
- Relevance: Learning-based alternative to model-based global planning for multi-stage cable routing around fixtures.

**Planning and Control for Cable-Routing with Dual-Arm Robot**
- Authors: Mingrui Yu et al.
- Venue: IEEE ICRA / RA-L proceedings 2024 (RMDO 2024 workshop)
- Link: [10.1109/ICRA46639.2022.9811765](https://ieeexplore.ieee.org/document/9811765)
- What it does: Extends whole-body planning framework to cable routing tasks with fixture contacts.

**Planning and Control for Cable-routing with Dual-arm Robot**
- Link: [https://odr.chalmers.se/179cb0c7-fd27-4fe7-aa88-908e777db1ca](https://odr.chalmers.se/server/api/core/bitstreams/179cb0c7-fd27-4fe7-aa88-908e777db1ca/content)

#### 3.2 Additional Dual-Arm DLO Planning

**A Coarse-to-Fine Framework for Dual-Arm Manipulation of DLOs with Whole-Body Obstacle Avoidance**
- Authors: Yu et al.
- Venue: IEEE ICRA, 2023
- Link: [arxiv.org/abs/2209.11145](https://arxiv.org/abs/2209.11145)
- What it does: Coarse-to-fine planning for dual-arm DLO manipulation with whole-body obstacle avoidance.

**An Optimization-Based Motion Planner for Dual-Arm Manipulation of Soft DLOs**
- Authors: Wu et al.
- Venue: Advanced Engineering Informatics, 2024
- Link: [doi.org/10.1016/j.aei.2024.102874](https://www.sciencedirect.com/science/article/abs/pii/S1474034624005226)
- What it does: Optimization-based motion planner specifically for dual-arm soft DLO manipulation.

**Robotic Cable Routing with Spatial Representation**
- Authors: Jin et al.
- Venue: IEEE RA-L, 2022
- Link: [doi.org/10.1109/LRA.2022.3158377](https://doi.org/10.1109/LRA.2022.3158377)
- What it does: Cable routing using spatial representation for planning.

**Planning and Control for Cable-Routing with Dual-Arm Robot**
- Authors: Waltersson, Laezza
- Venue: IEEE ICRA 2022
- Link: [doi.org/10.1109/ICRA46639.2022.9811765](https://doi.org/10.1109/ICRA46639.2022.9811765)
- What it does: Dual-arm cable routing planning and control framework.

**Motion Planning for Dual-Arm Manipulation of Elastic Rods**
- Authors: Sintov et al.
- Venue: IEEE RA-L 2020
- Link: [doi.org/10.1109/LRA.2020.3011352](https://doi.org/10.1109/LRA.2020.3011352)
- What it does: Motion planning specifically for dual-arm elastic rod manipulation.

#### 3.3 Sampling-Based Planning for Dual-Arm

**Direction Informed Trees (DIT*): Optimal Path Planning via Direction Filter and Direction Cost Heuristic**
- Authors: Zhang, Chen, Bing et al. (TUM)
- Source: Attached PDF (Direction_Informed_Trees_DIT_Optimal_Path_Planning.pdf), 2025
- Link: [arxiv.org/abs/2508.19168](https://arxiv.org/abs/2508.19168)
- What it does: Extends RRT*/BIT* with direction filter biasing sampling toward goal + direction cost heuristic. Demonstrated on dual-arm cable routing.
- Relevance: Drop-in replacement for RRT-Connect in global planner with better anytime performance in high-dimensional joint space.

**JIT*: Manipulability-Aware Asymptotically Optimized Motion Planning**
- Authors: Cai, Zhang et al. (TUM)
- Venue: IEEE/ASME T-Mechatronics 2025
- Link: [arxiv.org/abs/2601.19972](https://arxiv.org/abs/2601.19972)
- What it does: Asymptotically optimal motion planning with manipulability awareness. Considers arm dexterity during path planning.

**Flexible Informed Trees (FIT*): Adaptive Batch-Size Sampling-Based Planner**
- Venue: IEEE/RSJ IROS 2023
- Link: [arxiv.org/abs/2310.12828](https://arxiv.org/abs/2310.12828)
- What it does: Adaptive batch-size sampling-based planner extending informed trees family.

**Dual-Arm Whole-Body Motion Planning: Leveraging Overlapping Kinematic Chains**
- Authors: Cheng et al.
- Venue: IEEE Humanoids, 2025
- Link: [arxiv.org/abs/2511.08778](https://arxiv.org/abs/2511.08778)
- What it does: Whole-body motion planning leveraging overlapping kinematic chains in dual-arm systems.

**Novel RRT*-Connect Algorithm for Path Planning on Robotic Arm Collision Avoidance**
- Venue: Nature Scientific Reports, 2025
- Link: [doi.org/10.1038/s41598-025-87113-5](https://doi.org/10.1038/s41598-025-87113-5)
- What it does: Improved bidirectional RRT with better convergence and path smoothness for manipulator collision avoidance.
- Relevance: Directly applicable to dual-arm joint-space planning.

#### 3.4 Additional Planning Papers (NEW)

**Automatic Cable Routing Based on Improved Pathfinding Algorithm with B-Spline Optimization**
- Venue: Journal of Computational Design and Engineering, Vol. 11, No. 4, 2024
- Link: [10.1093/jcde/qwae085](https://scholarworks.bwise.kr/kumoh/bitstream/2020.sw.kumoh/29066/1/Automatic%20cable%20routing%20based%20on%20improved%20pathfinding.pdf)
- What it does: Integrates JPS-Theta* pathfinding with Ant Colony Optimization (ACO) and B-spline shape optimization for collision-free cable routing. High-impact published work on path-planning side of cable routing with direct industrial application.
- Relevance: Provides a published planning backbone for cable routing through fixture arrays with optimized smooth trajectories.

**Motion Planning for Robotics: A Review for Sampling-Based Planners**
- Authors: TUM Researchers (Zhang, Chen, Bing et al.)
- Venue: Biomimetic Intelligence and Robotics, Vol. 5, March 2025
- Link: [doi.org/10.1016/j.birob.2024.100207](https://doi.org/10.1016/j.birob.2024.100207)
- What it does: Surveys RRT, PRM, STOMP, CHOMP, and recent learning-augmented planners with benchmark comparisons. Published by TUM researchers directly affiliated with the thesis institution.
- Relevance: Key background reference for justifying global planner choice in thesis. Directly from thesis advisor's research group.

**Sampling-Based Motion Planning: A Comparative Review**
- Authors: Orthey et al.
- Venue: Journal of Field Robotics, 2024
- Link: [doi.org/10.1146/annurev-control-061623-094742](https://www.annualreviews.org/content/journals/10.1146/annurev-control-061623-094742)
- What it does: Compares 10+ sampling-based planners across manipulation benchmarks, providing rigorous basis for planner selection in high-dimensional dual-arm spaces.
- Relevance: Essential reference for justifying choice of sampling-based planner in high-dimensional DLO configuration space.

**Improving Efficiency of Sampling-Based Motion Planning via MPMC**
- Venue: IEEE ICRA, 2024
- Link: [arxiv.org/abs/2410.03909](https://arxiv.org/abs/2410.03909)
- What it does: Message-Passing Monte Carlo (MPMC) sampling as drop-in replacement for standard sampling in PRM/RRT planners. Demonstrated on UR5, directly applicable to dual-arm planning.
- Relevance: Efficiency improvement for the sampling-based global planner in dual-arm 14-DOF configuration space.

**In-Hand Following of Deformable Linear Objects Using Dexterous Fingers with Tactile Sensing**
- Authors: Mingrui Yu et al.
- Venue: IEEE/RSJ IROS 2024 (oral, top 12%)
- Link: [arXiv:2403.12676]([https://doi.org/10.1109/IROS58592.2024.10802447](https://deformable-workshop.github.io/icra2024/spotlight/01_08_wdo_yu_inhand.pdf))
- Code: [github.com/Mingrui-Yu/DLO_following](https://github.com/Mingrui-Yu/DLO_following)
- What it does: Extends DLO planning to dexterous in-hand re-grasping along the DLO while following a cable, using tactile sensing and inverse kinematics.
- Relevance: Complementary planning capability for wire harness routing with re-grasping. Code directly usable.

**APEX-MR: Multi-Robot Asynchronous Planning and Execution**
- Venue: IEEE ICRA, 2025 — arXiv:2503.15836
- Link: [arxiv.org/abs/2503.15836](https://arxiv.org/abs/2503.15836)
- What it does: Addresses coordination problem in multi-arm systems — asynchronous trajectory generation and execution with conflict resolution. Decentralized execution model directly applicable to dual-arm setup.
- Relevance: Framework for managing asynchronous arm motion during dual-arm DLO manipulation where one arm shapes while the other grasps.

**Motion Planning Framework Based on Dual-Agent DDPG for Dual-Arm Robots**
- Venue: Frontiers in Neurorobotics, 2024 — DOI: 10.3389/fnbot.2024.1362359
- Link: [doi.org/10.3389/fnbot.2024.1362359](https://doi.org/10.3389/fnbot.2024.1362359)
- What it does: Reinforcement learning approach to dual-arm trajectory planning with human-joint-angle constraints. Tested on Baxter, demonstrates real-time coordinated trajectory generation. Useful benchmark against classical planners in cluttered scenarios.
- Relevance: RL-based dual-arm coordination baseline for comparison against model-based approach in thesis.

**Perception and Planning for Dual-Arm Multi-Branch Wire Harness Manipulation**
- Authors: Malvido Fresnillo et al. (Lund University)
- Venue: ELLIIT Focus Period Technical Report, 2025
- Link: [urn.fi/URN:ISBN:978-952-03-4065-0](https://researchportal.tuni.fi/en/publications/perception-and-planning-for-dual-arm-robotic-manipulation-of-mult/)
- What it does: Complete perception-to-planning pipeline for multi-branch DLO scenarios combining RGB-D perception, B-spline DLO modeling, and MoveIt2-based motion planning. Addresses multiple DLOs in close proximity — directly matching industrial wire harness scenarios.
- Relevance: DLO-DLO collision avoidance when handling multiple cables simultaneously is explicitly mentioned as an open problem.

#### Step 3 Summary

| Paper | Venue | Year | Code | Key |
|-------|-------|------|------|-----|
| Yu et al. (whole-body) | IJRR | 2024 | Yes | Most complete dual-arm DLO planner |
| Luo et al. | IEEE T-RO | 2024 | Yes | Hierarchical IL for cable routing |
| Yu et al. (cable-routing) | ICRA/RA-L | 2024 | -- | Fixture contact extension |
| DIT* | PDF | 2025 | -- | Direction-biased RRT variant |
| RRT*-Connect | Sci Reports | 2025 | -- | Improved bidirectional RRT |
| Auto Cable Routing JPS+ACO | J. Comp. Design Eng. | 2024 | -- | JPS-Theta* + ACO + B-spline paths |
| Motion Planning Review TUM | Biomimetic Intel. Robotics | 2025 | -- | Survey 10+ planners, dual-arm benchmarks |
| Orthey Comparative Review | J. Field Robotics | 2024 | -- | 10+ planner comparison, manipulation |
| MPMC ICRA 2024 | IEEE ICRA | 2024 | -- | Message-passing Monte Carlo sampling |
| In-Hand DLO Following | IROS | 2024 | Yes | Tactile + IK for in-hand DLO following |
| APEX-MR | IEEE ICRA | 2025 | -- | Multi-robot async planning and execution |
| Dual-Agent DDPG | Frontiers Neurorobotics | 2024 | -- | RL dual-arm trajectory planning |
| Malvido Fresnillo | ELLIIT | 2025 | -- | Multi-branch wire harness perception+planning |

---

### Step 4: Local Shape Control

#### 4.1 MPC-Based Control with Safety Filter

**Learning-Based MPC with Safety Filter for Constrained Deformable Linear Object Manipulation**
- Authors: Yuchen Tang, Xinghao Chu, Jianzhong Huang, K.W. Samuel Au
- Venue: IEEE RA-L, Vol. 9, No. 3, pp. 2877-2884, March 2024
- Link: [10.1109/LRA.2024.3362643](https://ieeexplore.ieee.org/abstract/document/10423099)
- What it does: Combines learning-based predictive model (DLO state prediction) with CBF-based safety filter as MPC constraint. Safety filter explicitly enforces collision avoidance at control level. Tested in cluttered environments.
- Relevance: **Most important paper for Step 4+5 integration.** First to unify learning-based DLO control with rigorous safety filter. Extend to dual-arm with inter-robot constraints.
- **Gap:** Safety filter only handles static obstacles; dynamic obstacles and DLO-fixture contact collisions not addressed.

#### 4.2 Adaptive Control with Online Learning

**Time-Series Data-Driven Three-Dimensional Shape Control of Deformable Linear Objects Using a Dual-Arm Robot with Dynamic Model Updating**

Authors: Jiyoung Choi, Micheale Haileslassie Gebrezgiher, Donggun Lee, Ayoung Hong - (IEEE RA-L 2026) -- see Step 2 above.
- Link: [doi.org/10.1109/LRA.2026.3655208](https://ieeexplore.ieee.org/document/11355841)

- MPC with online residual learning (MPCOLI) for dual-arm control.
- **Gap (explicit):** Absence of obstacle-aware planning as limitation for future work.

#### 4.3 Cosserat-Based Optimal Control

**Optimal Cosserat-Based Deformation Control for Robotic Manipulation**
- Venue: Published 2024
- Link: [arxiv.org/abs/2409.12723](https://arxiv.org/abs/2409.12723)
- What it does: Generates optimal end-effector trajectories using Cosserat rod model + trajectory optimization. Intermediate optimal steps for industrial manipulation.

#### 4.4 Dual-Arm Frameworks & Industrial Assembly

**Enabling Versatility and Dexterity of Dual-Arm Manipulators: A General Framework Toward Universal Cooperative Manipulation**
- Authors: TUM Researchers
- Venue: IEEE T-RO, 2024
- Link: [10.1109/TRO.2024.3370048](https://ieeexplore.ieee.org/document/10449470)
- What it does: General framework for universal cooperative manipulation with dual-arm manipulators.

**A Dual-Arm Robotic System for Automated Multi-Branch Wire Harness Assembly**
- Authors: Fresnillo et al.
- Venue: Journal of Manufacturing Systems, 2025
- Link: [doi.org/10.1016/j.jmsy.2025.10.008](https://www.sciencedirect.com/science/article/pii/S0278612525002547)
- What it does: Dual-arm system for automated multi-branch wire harness assembly in industrial settings.

**Strategic Algorithm for Cable Wiring Using Dual Arm with Compliance Control**
- Venue: Robotics and Computer-Integrated Manufacturing, 2024
- Link: [doi.org/10.1016/j.rcim.2024.102924](https://www.sciencedirect.com/science/article/abs/pii/S0736584524002114)
- What it does: Strategic algorithm combining dual-arm coordination with compliance control for cable wiring tasks.

**Predictive Multi-Agent-Based Planning for Reactive Dual-Arm Manipulation**
- Authors: Laha, Haddadin et al.
- Venue: IEEE T-RO, 2024
- Link: [10.1109/TRO.2023.3341689](https://ieeexplore.ieee.org/document/10354340)
- Github: [riddhiman13/predictive-multi-agent-framework](https://github.com/riddhiman13/predictive-multi-agent-framework)
- What it does: Predictive multi-agent planning for reactive dual-arm manipulation tasks.

#### 4.5 Compliance and Contact-Aware Control

**Contact-Aware Shaping and Maintenance of Deformable Linear Objects With Fixtures**
- Authors: Kejia Chen, Zhenshan Bing, Fan Wu, Yuan Meng, Andre Kraft, Sami Haddadin, Alois Knoll (TUM)
- Venue: IEEE/RSJ IROS 2023
- Link: [10.1109/IROS55552.2023.10341726](https://deformable-workshop.github.io/icra2023/spotlight/10-CHEN-spotlight.pdf)
- What it does: Uses contact constraints from environmental fixtures to assist DLO shaping. Models multi-stage contact process (cable approaching clip -> clip forced open -> cable secured). Real-time contact state estimation.
- Relevance: **Founding paper of thesis setup.** The 2024-2026 work builds on and extends this framework.

**Real-Time Contact State Estimation in Shape Control of DLOs Under Small Environmental Constraints**
- Authors: Chen et al. (TUM)
- Venue: IEEE ICRA 2024
- Link: [arxiv.org/abs/2401.17154](https://arxiv.org/abs/2401.17154)
- What it does: Real-time estimation of contact states during DLO shape control under environmental constraints.

**Multi-Robot Assembly of Deformable Linear Objects Using Multi-Modal Perception**
- Authors: Chen et al. (TUM)
- Venue: IEEE ICRA 2025
- Link: [arxiv.org/abs/2506.22034](https://arxiv.org/abs/2506.22034)
- What it does: Multi-robot DLO assembly using multi-modal perception. Extends single-arm DLO work to multi-robot coordination.

#### 4.6 Additional Local Control Papers (NEW)

**Image-Based Visual Servoing for Enhanced Cooperation of Dual-Arm Manipulation**
- Authors: Zhang, Yang et al.
- Venue: IEEE Robotics and Automation Letters, accepted February 2025
- Link: [10.1109/LRA.2025.3543137](https://ieeexplore.ieee.org/document/10891400)
- What it does: IBVS control law specifically for dual-arm cooperation where each arm tracks the other's wrist marker using on-board camera. Derives passivity-based control handling closed-chain kinematics of both arms and proves Lyapunov asymptotic stability. Designed for rigid object co-manipulation but synchronization framework transfers directly to DLO endpoint coordination layer.
- Relevance: Proven stability framework for dual-arm coordination in DLO shape control where both arms must remain synchronized throughout cable routing.

**Obstacle Avoidance Shape Control of Deformable Linear Objects with Differentiable Simulation**
- Venue: IEEE Robotics and Automation Letters, 2024 (DOAJ indexed)
- Link: [10.1186/s40648-024-00283-1](https://link.springer.com/article/10.1186/s40648-024-00283-1)
- What it does: Integrates differentiable Position-Based Dynamics (PBD) simulation into a shape controller, enabling gradient-based shape control that naturally avoids obstacles through the differentiable collision layer. The only published paper besides Tang et al. that handles DLO-obstacle avoidance within the shape control loop itself — but simulation-only.
- Relevance: Demonstrates feasibility of embedding obstacle avoidance into DLO shape control gradient. Thesis extends this to a real dual-arm system with all four collision pairs.
- Gap: Simulation-only; does not handle arm–arm or arm–env collisions.

**Cable Shaping with MPC: A Reliable, Fast, and Real-Time Feasible Formulation**
- Venue: IEEE Conference on Control Applications (CCA), 2024
- Link: [doi.org/10.1016/j.ifacol.2024.10.254](https://www.sciencedirect.com/science/article/pii/S2405896324020299)
- What it does: Reformulated DLO shape MPC that guarantees real-time feasibility through constraint tightening and warm-starting. Addresses DLO shape control feasibility in cluttered environments with tight constraints.
- Relevance: MPC feasibility guarantees — directly applicable to ensuring thesis CBF-MPC integration remains feasible during cable routing.

**Manipulation of Deformable Linear Objects Using Model Predictive Control**
- Venue: SCITEPRESS (ICINCO Proceedings), 2025
- Link: [10.5220/0013703800003982](https://www.scitepress.org/Papers/2025/137038/137038.pdf)
- What it does: MPC controller for DLO manipulation in simulation, comparing different MPC horizons and constraint formulations for shape accuracy and obstacle avoidance feasibility.
- Relevance: Comparative benchmark for MPC horizon and constraint design choices in DLO shape control.

#### Step 4 Summary

| Paper | Venue | Year | Key |
|-------|-------|------|-----|
| Tang et al. | IEEE RA-L | 2024 | MPC + CBF safety filter for DLO (most important for thesis) |
| Choi et al. | IEEE RA-L | 2026 | MPCOLI dual-arm (gap: obstacle-free only) |
| Cosserat optimal | 2024 | 2024 | Cosserat rod + trajectory optimization |
| Chen et al. | IROS | 2023 | Contact-aware DLO shaping with fixtures (thesis founding paper) |
| IBVS Dual-Arm (Zhang et al.) | IEEE RA-L | 2025 | Passivity-based IBVS, proven stability, dual-arm |
| Obstacle Avoidance DLO (Diff. Sim.) | IEEE RA-L | 2024 | Differentiable PBD shape ctrl + obstacle (sim only) |
| Cable MPC feasibility (CCA 2024) | IEEE CCA | 2024 | Real-time feasible DLO shape MPC |
| DLO MPC (SCITEPRESS 2025) | SCITEPRESS | 2025 | MPC horizon comparison for DLO control |

---

### Step 5: Collision Avoidance

This is the core thesis contribution area. Four collision pairs: (a) robot-environment, (b) robot-robot (self-collision), (c) DLO-environment, (d) DLO-robot.

#### 5.1 SDF-Based Collision Avoidance (Robot-Environment)

**Real-Time Collision Avoidance with Robot Distance Fields in a Task-Priority Framework**
- Authors: Andrea Govoni, Matteo Cavuoto, Yuhan Li, Sylvain Calinon, Gianluca Palli
- Venue: Robotics and Autonomous Systems (Elsevier), 2026, DOI: 10.1016/j.robot.2026.105394
- Link: [doi.org/10.1016/j.robot.2026.105394](https://doi.org/10.1016/j.robot.2026.105394)
- What it does: Embeds SDF of robot geometry into task-priority control loop. Smooth reactive avoidance of multiple obstacles in real-time. Tested on dual-arm lifting task.
- Relevance: Task-priority framework compatible with local shape controller. SDF can extend to include DLO geometry.

**Representing Robot Geometry as Distance Fields: Applications to Whole-Body Manipulation**
- Authors: Y. Li, Y. Zhang, A. Razmjoo, S. Calinon (IDIAP)
- Venue: IEEE ICRA 2024, pp. 15351-15357
- Link: [10.1109/ICRA57147.2024.10611674](https://ieeexplore.ieee.org/document/10611674)
- Code: Available via Calinon lab
- What it does: Robot Signed Distance Field (RDF) using Bernstein polynomials for articulated kinematic chains. Differentiable and smooth in joint space. Directly usable as collision constraints in optimization. Dual-arm lifting experiment.
- Relevance: Mathematical tool for formulating collision avoidance as differentiable constraint in control optimization.

**SDF-SC: Efficient Collision Detection Framework (SDF + Self-Collision)**
- Authors: Xiankun Zhu et al. (Tsinghua University)
- Venue: IEEE ICRA 2025
- Link: [arxiv.org/abs/2409.14955](https://arxiv.org/abs/2409.14955)
- Code: [sites.google.com/view/icra2025-sdfsc](https://sites.google.com/view/icra2025-sdfsc)
- What it does: Decomposes robot SDF using forward kinematics with lightweight parallel networks. Integrates self-collision via SVM. 5x faster than prior methods. Real-time avoidance of multiple dynamic obstacles.

#### 5.2 CBF-Based Safety Filters

**Safe, Task-Consistent Manipulation with Operational Space Control Barrier Functions (OSCBF)**
- Authors: Daniel Morton, Marco Pavone (Stanford)
- Venue: IEEE ICRA 2025 + open-source release
- Link: [arxiv.org/abs/2409.13025](https://arxiv.org/pdf/2503.06736)
- Code: [github.com/StanfordASL/oscbf](https://github.com/StanfordASL/oscbf) (CBFpy library)
- What it does: Integrates CBFs into Operational Space Control hierarchy. Scales to 168 simultaneous constraints at >1000 Hz. Prevents task performance degradation at safety boundaries. Handles self-collision, joint limits, workspace, and dynamic obstacles simultaneously.
- Relevance: **Most complete CBF implementation for robot manipulators.** CBFpy library can directly implement inter-arm and DLO collision constraints.

**GP-P-HOCBF: Learning-Based Parameterized Barrier Function for Safety-Critical Control**
- Authors: Yu Zhang, Zhenshan Bing, Alois Knoll et al. (TUM)
- Venue: IEEE Robotics and Automation Letters / IEEE T-ASE, published December 2024 — TUM portal DOI available
- Link: [10.1109/CDC56724.2024.10886097](https://mediatum.ub.tum.de/doc/1754101/brkbbejup4ecny2er2n5h4did.GP-P-HOCBF-final.pdf)
- What it does: Gaussian Process regression predicts unknown disturbances and parametrically shrinks the safe set in proportion to the GP prediction error bound. Validated on Franka Emika manipulator. Provides safety guarantees under model uncertainty.
- Relevance: TUM thesis supervisor group's published safety framework — natural building block for thesis collision avoidance controller. Combines GP uncertainty estimation with high-order CBF constraints (different from the separate T-ASE 2025 GP-CBF entry below).

**Flexible Active Safety Motion Control: A CBF-Guided MPC Approach (FASM)**
- Authors: Liu, Yang et al.
- Note: arXiv preprint 2024, arXiv:2405.12408 -- check publication status
- Link: [arxiv.org/abs/2405.12408](https://arxiv.org/abs/2405.12408)
- What it does: Discrete-time CBFs with dynamically optimized decay rates as safety constraints in MPC. Real-world validation on UR5. Decay rate optimization helps avoid infeasibility.

**Differentiable Optimization-Based Time-Varying Control Barrier Functions**
- Venue: Robotics and Autonomous Systems (Elsevier), 2025
- Link: [doi.org/10.1016/j.robot.2025.105182](https://doi.org/10.1016/j.robot.2025.105182)
- What it does: Formulates CBF constraints as differentiable optimization where the CBF boundary itself varies over time to track moving obstacles. Enables tighter safety bounds than fixed-threshold CBFs and handles dynamic obstacle scenarios (moving fixtures, moving robot arms) without conservatism of static safety margins.
- Relevance: Standard CBFs use fixed safety thresholds, leading to overly conservative behavior near fixtures. Time-varying CBF boundaries allow the safety constraint to adapt as the DLO moves through different phases (free motion → fixture approach → contact). Directly applicable to fixture contact transition problem (Research Gap 4).

#### 5.3 Inter-Arm / Self-Collision Avoidance

**Reactive Self-Collision Avoidance for Dual-Arm Robots Using a Temporal Feature Modeling and Fusion Network**
- Authors: Xuejin Luo, Runshi Zhang, Siqin Yang, Zhen Sun, Ruizhi Zhang, Junchen Wang
- Venue: IEEE T-ASE, Vol. 22, pp. 22625-22637, October 2025
- Link: [ieeexplore.ieee.org/document/11202538](https://ieeexplore.ieee.org/document/11202538/)
- Impact factor: 6.4, Q1
- What it does: Temporal feature network predicts inter-arm collision risk from joint state sequences. Fuses historical motion context with current state for reactive avoidance. Significantly reduces collision rate over geometry-only methods.
- Relevance: Directly addresses inter-arm collision (type b) in real-time without computational cost of geometry-based distance queries.

**iAPF: Improved Artificial Potential Field Framework for Asymmetric Dual-Arm Manipulation**
- Authors: SK Surya Prakash, D Prajapati, B Narula, A Shukla (IIT Mandi)
- Venue: Frontiers in Robotics and AI, Vol. 12, Art. 1604506, 2025
- Link: [doi.org/10.3389/frobt.2025.1604506](https://doi.org/10.3389/frobt.2025.1604506)
- Code: [github.com/suryarobotcontrol/Dual-Arm-Manipulation](https://github.com/suryarobotcontrol/Dual-Arm-Manipulation)
- What it does: Three-way force equilibrium (attractive + repulsive + home-seeking) with exponential stabilization. Continuous distance calculation between links via line segment geometry. Priority-based state machine for asymmetric coordination. Lyapunov-proven stability.
- Relevance: Lightweight APF baseline for comparison against CBF-based approaches.

#### 5.4 DLO-Specific Collision Avoidance

**Collaborative Manipulation of Deformable Objects with Predictive Obstacle Avoidance**
- Authors: Aksoy, Wen
- Venue: IEEE ICRA, 2024
- Link: [arxiv.org/abs/2401.16560](https://www.john-wen.com/publications/collaborative-manipulation-deformable-objects-predictive-obstacle-avoidance)
- What it does: Collaborative deformable object manipulation with predictive obstacle avoidance.

**Planning and Control for Deformable Linear Object Manipulation**
- Authors: Aksoy, Wen
- Venue: 2025 (arXiv: 2503.04007)
- Link: [arxiv.org/abs/2503.04007](https://arxiv.org/abs/2503.04007)
- What it does: CBF-based planning and control for DLO manipulation with obstacle avoidance.

**Certifiably Safe Manipulation of DLOs via Joint Shape and Tension Prediction**
- Authors: Zhang, Li
- Venue: 2025
- Link: [arxiv.org/abs/2505.13889](https://arxiv.org/abs/2505.13889)
- What it does: Certifiably safe DLO manipulation by jointly predicting shape and tension for safety constraints.

**Fabric Dynamic Motion Modeling and Collision Avoidance**
- Authors: Li, Kosuge
- Venue: IEEE RA-L, 2025
- Link: [ieeexplore.ieee.org/document/11108276](https://ieeexplore.ieee.org/document/11108276/)
- What it does: Modeling fabric/deformable dynamics for collision avoidance during manipulation.

**Multi-Robot Transport of Deformable Objects with Collision Avoidance**
- Authors: Marcos-Saavedra, Aranda, López-Nicolás (Zaragoza group)
- Venue: ICRA 2024 RMDO Workshop; journal version in International Journal of Systems Science, 2025
- Link: [tandfonline.com/doi/full/10.1080/00207721.2025.2559138](https://www.tandfonline.com/doi/full/10.1080/00207721.2025.2559138)
- What it does: Multi-robot coordination for deformable object transport with collision avoidance.

#### 5.5 Additional CBF & Safety Methods

**High-Order Control Barrier Function-Based Safety Control of Constrained Robotic Systems**
- Authors: Wang et al.
- Venue: IEEE/CAA Journal of Automatica Sinica, 2024
- Link: [doi.org/10.1109/JAS.2024.124524](https://doi.org/10.1109/JAS.2024.124524)
- What it does: High-order CBF for constrained robotic systems with safety guarantees.

**Incorporating Control Barrier Functions in Distributed Model Predictive Control for Multirobot Coordinated Control**
- Authors: Jiang, Guo
- Venue: IEEE Transactions on Control of Network Systems, 2024
- Link: [doi.org/10.1109/TCNS.2023.3290430](https://doi.org/10.1109/TCNS.2023.3290430)
- What it does: CBFs integrated into distributed MPC for multi-robot coordination with safety constraints.

**Efficient Motion Planning for Manipulators with Control Barrier Function-Induced Neural Controller**
- Venue: IEEE ICRA, 2024
- Link: [doi.org/10.1109/ICRA57147.2024.10610785](https://doi.org/10.1109/ICRA57147.2024.10610785)
- What it does: CBF-induced neural controller for efficient manipulator motion planning.

#### 5.6 Dual-Arm Collision Avoidance (Additional)

**A Real-Time Collision Avoidance Method for Redundant Dual-Arm Robots in an Open Operational Environment**
- Venue: Robotics and Computer-Integrated Manufacturing, 2024
- Link: [doi.org/10.1016/j.rcim.2024.102894](https://doi.org/10.1016/j.rcim.2024.102894)
- What it does: Real-time collision avoidance for redundant dual-arm robots in open environments.

**Coordinating Obstacle Avoidance of a Redundant Dual-Arm Nursing-Care Robot**
- Authors: Yang et al.
- Venue: Bioengineering (MDPI), 2024
- Link: [doi.org/10.3390/bioengineering11060550](https://doi.org/10.3390/bioengineering11060550)
- What it does: Coordinated obstacle avoidance for redundant dual-arm nursing-care robots.

**APEX: Ambidextrous Dual-Arm Robotic Manipulation Using Collision-Free Generative Diffusion Models**
- Authors: Dastider et al.
- Venue: 2024
- Link: [arxiv.org/abs/2404.02284](https://arxiv.org/abs/2404.02284)
- What it does: Collision-free dual-arm manipulation using generative diffusion models for trajectory generation.

**CoFreeVLA: Collision-Free Dual-Arm Manipulation via Vision-Language-Action Model and Risk Estimation**
- Authors: Zhai et al.
- Venue: 2026
- Link: [arxiv.org/abs/2601.21712](https://arxiv.org/abs/2601.21712)
- What it does: Vision-language-action model for collision-free dual-arm manipulation with risk estimation.

#### 5.7 Safety Control from TUM Group (Knoll Lab)

**Adaptive Safety-Critical Control for High-Order Systems: A Real-Time Gaussian Process Approach**
- Authors: Yu Zhang, Long Wen, Zhenshan Bing, Yao, Kong, Wei He, Alois Knoll (TUM)
- Venue: IEEE T-ASE, 2025
- Link: [10.1109/TASE.2025.3611987](https://ieeexplore.ieee.org/document/11173605)
- What it does: GP-based estimation of model uncertainties + high-order CBF constraints. Safety guarantees under model uncertainty.
- Relevance: TUM group (who built thesis hardware setup) applies safety-critical control -- strong alignment.

**Robust Dual-Filter Safety Control for Mobile Robots in Dynamic Multiobstacle Environments**
- Authors: Yu Zhang, Linghuan Kong, Xinbo Yu, Wei He, Alois Knoll (TUM)
- Venue: IEEE/ASME T-Mechatronics, Vol. 30, No. 6, pp. 1-12, December 2025
- Link: [10.1109/TMECH.2024.3521038](https://ieeexplore.ieee.org/document/10838340)
- What it does: Dual-filter architecture: fast saliency detection filter (1st) + D-CBF activation filter (2nd). Reduces unnecessary CBF computations while maintaining real-time safety in dynamic multi-obstacle scenarios.
- Relevance: Dual-filter concept transferable to dual-arm cable routing where fixture obstacles are known but cable state adds dynamic uncertainty.

#### 5.8 Additional Safety & Collision Avoidance Papers (NEW)

**A Hierarchical Framework for Collision Avoidance in Robot-Assisted Minimally Invasive Surgery**
- Venue: IEEE CBS 2024
- Link: [arxiv.org/abs/2409.10135](https://arxiv.org/abs/2409.10135)
- What it does: Two-level hierarchical collision avoidance system combining a global RRT-based planner with a real-time reactive CBF controller. Validated in a precision manipulation domain with deformable tissue interaction.
- Relevance: Provides the strongest published justification for the thesis's hierarchical architecture (global planner + local CBF controller). Demonstrates this exact architecture works in a manipulation domain where deformable objects are present — directly analogous to DLO context.

**Safe Expeditious Whole-Body Control of Mobile Manipulators for Collision Avoidance (SEWB)**
- Venue: IEEE Robotics and Automation Letters, 2025
- Link: [arxiv.org/abs/2409.14775](https://arxiv.org/abs/2409.14775)
- What it does: SEWB framework combines CBFs with a novel Adaptive Cyclic Inequality (ACI) approach to resolve the pseudo-equilibrium problem of standard CBFs (where the robot gets stuck at saddle points in the obstacle field). ACI generates directional constraints considering both obstacle position and velocity, decomposing safety constraints into a QP that achieves whole-body collision-free motion at >200 Hz. Validated on a physical mobile manipulator avoiding fast-moving dynamic obstacles.
- Relevance: The pseudo-equilibrium problem of CBFs is a known issue in dual-arm collision avoidance — two robot arms can create local minima where neither arm can move safely. The ACI technique is a published, validated solution directly applicable to the thesis CBF formulation.

**Robust Whole-Body Safety-Critical Control for Sampled-Data Systems**
- Venue: IEEE Transactions on Automation Science and Engineering, 2025
- Link: [ieeexplore.ieee.org/document/11016805](https://ieeexplore.ieee.org/document/11016805/)
- What it does: Establishes formal safety guarantees for discrete-time control implementations, addressing the gap between continuous-time CBF theory and real embedded controllers running at fixed sample rates (e.g., 500 Hz for Franka Panda).
- Relevance: The TUM dual-arm Panda system runs at a fixed control rate. This paper provides the theoretical foundation for proving that the thesis CBF safety filter, implemented at discrete time steps, still provides formal safety guarantees — directly needed for the real-world implementation chapter.

**Guaranteed Real-Time Cooperative Collision Avoidance for n-DOF Manipulators**
- Authors: Rodríguez-Seda et al.
- Venue: Robotica (Cambridge University Press), 2024 — DOI: 10.1017/S0263574724001334
- Link: [doi.org/10.1017/S0263574724001334](https://doi.org/10.1017/S0263574724001334)
- What it does: Provides formal safety proofs for APF-based cooperative collision avoidance between multiple manipulators, with decentralized execution guarantees. Directly applicable to the dual-arm arm-arm collision problem.
- Relevance: Formal real-time safety guarantees for cooperative multi-manipulator collision avoidance — provides theoretical grounding for dual-arm arm-arm collision pair.

**Dual-Arm Cooperative Peg-in-Hole Assembly for Large Objects**
- Venue: Robotics and Computer-Integrated Manufacturing (RCIM), 2025 — Q1, IF ~9.1
- Link: [doi.org/10.1016/j.rcim.2025.102991](https://doi.org/10.1016/j.rcim.2025.102991)
- What it does: CDS (Cooperative Dual-arm Strategy) framework with VIVF (Variable Impedance + Virtual Fixture) controller for inserting large deformable parts, with explicit collision avoidance between the two arms during cooperative manipulation.
- Relevance: Published dual-arm cooperative manipulation with explicit inter-arm collision avoidance — directly comparable to thesis target of collision-aware dual-arm DLO routing.

**Meta-Learning-Based Safety-Critical Control in Multi-Obstacles Environments (Meta-CBF)**
- Authors: Bing, Zhang et al. (TUM — thesis advisor's group)
- Venue: IEEE Transactions on Automation Science and Engineering, Vol. 22, 2025
- Link: [ieeexplore.ieee.org/document/10980124](https://ieeexplore.ieee.org/document/10980124/)
- What it does: Develops MetaSDF + Meta-Bayesian CBF (Meta-BRCBF) using meta-learning to quickly adapt safety constraints to novel obstacle configurations. Validated on a real robot arm in multi-obstacle environments. Adapts to new obstacle layouts from few observations.
- Relevance: **The most critical TUM group paper for the collision avoidance layer.** Directly from thesis advisor's group; demonstrates fast adaptation to novel obstacle configurations. Gap: applied to single-arm manipulation without DLO — thesis extends to dual-arm DLO setting.

#### Step 5 Summary

| Paper | Venue | Year | Collision Type | Method | Code |
|-------|-------|------|---------------|--------|------|
| Govoni et al. | RAS (Elsevier) | 2026 | Robot-env | SDF + task priority | -- |
| Li et al. (RDF) | IEEE ICRA | 2024 | Whole-body | SDF (Bernstein poly) | Yes |
| Zhu et al. (SDF-SC) | IEEE ICRA | 2025 | Self + env | SDF + SVM, 5x faster | Yes |
| Morton & Pavone (OSCBF) | IEEE ICRA | 2025 | All types | CBF + OSC, 1kHz | Yes |
| GP-P-HOCBF (Zhang TUM) | IEEE RA-L/T-ASE | 2024 | Robot-env | GP-parameterized HOCBF | -- |
| Tang et al. | IEEE RA-L | 2024 | DLO-env | CBF safety filter + MPC | -- |
| FASM (Liu et al.) | arXiv | 2024 | Robot-env | CBF-guided MPC | -- |
| Time-Varying CBF | RAS (Elsevier) | 2025 | Dynamic env | Differentiable opt, time-varying bounds | -- |
| Luo et al. | IEEE T-ASE | 2025 | Inter-arm | Temporal NN | -- |
| iAPF | Frontiers | 2025 | Inter-arm | APF 3-way force | Yes |
| Zhang et al. (GP-CBF T-ASE) | IEEE T-ASE | 2025 | Robot-env | GP + HO-CBF | -- |
| Zhang et al. (dual-filter) | IEEE/ASME TMech | 2025 | Dynamic env | D-CBF dual-filter | -- |
| Meta-CBF (Bing TUM) | IEEE T-ASE | 2025 | Robot-env | Meta-learning CBF | -- |
| Hierarchical CA RMIS | IEEE T-ASE | 2024 | Robot-env | RRT + CBF hierarchical | -- |
| SEWB/ACI | IEEE RA-L | 2025 | Whole-body | Adaptive cyclic inequality CBF | -- |
| Robust Sampled-Data Safety | IEEE T-ASE | 2025 | All types | Discrete-time safety guarantees | -- |
| Cooperative CA (Robotica) | Robotica | 2024 | Inter-arm | APF formal guarantees n-DOF | -- |
| Dual-Arm Peg-in-Hole RCIM | RCIM | 2025 | Inter-arm | CDS+VIVF cooperative | -- |

---

### ArXiv Preprints (Supporting, Not Primary)

Not peer-reviewed. Included for awareness only, not for formal citation.

| Title | Authors | arXiv ID | Relevance |
|-------|---------|----------|-----------|
| UniStateDLO: Generative DLO State Estimation via Diffusion | Lv, Yu et al. | [2512.17764](https://arxiv.org/abs/2512.17764) (Dec 2025) | DLO perception under occlusion; uncertainty for probabilistic collision constraints |
| Planning and Control for DLO Manipulation (CBF) | Aksoy, Wen | [2503.04007](https://arxiv.org/abs/2503.04007) (Mar 2025) | CBF for DLO planning |
| Coordinated Manipulation of Hybrid DLO-Rigid Objects | -- | [2603.12940](https://arxiv.org/abs/2603.12940) (Mar 2026) | Cosserat rod dual-arm |
| Dual-Arm Whole-Body Motion Planning with DRMs | -- | [2511.08778](https://arxiv.org/abs/2511.08778) (Nov 2025) | Dual-arm motion planning |
| FASM: CBF-Guided MPC for Dynamic Obstacle Avoidance | Liu et al. | [2405.12408](https://arxiv.org/abs/2405.12408) | CBF-MPC for manipulators |
| EA-PE-GAT: Hybrid Force-Position Graph Attention for DLO Manipulation | -- | [2508.07319](https://arxiv.org/abs/2508.07319) | GAT-based hybrid force-position control; code: [sites.google.com/view/dlom](https://sites.google.com/view/dlom) |
| DOp-CBF: Disturbance Observer Parameterized CBF | -- | [2412.07349](https://arxiv.org/abs/2412.07349) (Dec 2024) | CBF with disturbance observer; under review IEEE RA-L |
| Multi-Robot DLO Assembly (TUM) | Chen, Bing, Knoll, Daub | [2506.22034](https://arxiv.org/abs/2506.22034) | TUM multi-robot DLO assembly; submitted IROS 2025 |
| Online Learning-Enhanced High-Order Adaptive CBF (HO-ACBF) | -- | [2511.19651](https://arxiv.org/abs/2511.19651) (Nov 2025) | Adaptive HOCBF with online learning for time-varying safety bounds |
| Prescribed Performance Control of Deformable Objects | Navarro-Alarcón group | [2510.14234](https://arxiv.org/abs/2510.14234) (Oct 2025) | Prescribed-performance control for deformable objects |
| Artinian Closed-Loop Cosserat Shape Control | -- | [2409.13522](https://arxiv.org/abs/2409.13522) (Sep 2024) | Artinian Cosserat BVP for closed-loop DLO shape control; under review IEEE RA-L |
| APEX-MR: Multi-Robot Asynchronous Planning and Execution | -- | [2503.15836](https://arxiv.org/abs/2503.15836) (Mar 2025) | Asynchronous multi-robot planning; ICRA 2025 |
| Hierarchical Deformation Planning + Neural Tracking | -- | [2512.24974](https://arxiv.org/abs/2512.24974) (Dec 2025) | Hierarchical DLO deformation planning with neural tracking; submitted IEEE T-RO |
| Certifiably Safe DLO Manipulation via Zonotopes | -- | [2505.13889](https://arxiv.org/abs/2505.13889) (May 2025) | Formal safety certificates for DLO manipulation using zonotope methods |
| CoFreeVLA: Collision-Free Vision-Language-Action Model | -- | [2601.21712](https://arxiv.org/abs/2601.21712) (Jan 2026) | VLA model with built-in collision-free guarantees; see Step 5.6 |

---

### Research Gaps (Thesis Contribution Opportunities)

**Gap 1: Unified DLO Collision Avoidance (All Four Collision Pairs)**
- No existing work simultaneously addresses robot-robot, robot-DLO, DLO-environment, and DLO-fixture collisions in a unified framework.
- Most relevant: Tang et al. (RA-L 2024) handles robot-env for single arm; Yu et al. (IJRR 2024) handles whole-body but with simplified energy model without safety guarantees.

**Gap 2: Obstacle-Aware Dual-Arm MPC for DLOs**
- Choi et al. (RA-L 2026) explicitly state "obstacle-free conditions" as limitation and suggest "path planning strategies" as future work.

**Gap 3: DLO State Uncertainty in Collision Checking**
- All existing collision avoidance assumes known, deterministic DLO state. No work propagates DLO state uncertainty into collision constraints.
- Potential: Use diffusion-model uncertainty from UniStateDLO or covariance from TrackDLO for probabilistic collision constraints.

**Gap 4: Real-Time Contact Force Integration in Collision Avoidance**
- Chen et al. (IROS 2023) uses contact forces for shaping but not collision avoidance during contact transitions. Cannot guarantee collision-free arm motion while DLO is routed through clips.

**Gap 5: Sim-to-Real Transfer for Obstacle-Aware DLO Control**
- No paper provides systematic methodology for reducing sim-to-real gap in constrained dual-arm DLO manipulation.
- Potential: DER model parameter identification (MuJoCo) + domain randomization.

---

## PART B: AIC CHALLENGE LITERATURE (Cable Connector Insertion)

---

### B.1 Online Force Modeling

**Tracy et al. -- "Efficient Online Learning of Contact Force Models for Connector Insertion" (2023)**
- Authors: Ajinkya Jain, Keegan Go, Stefan Schaal (Intrinsic); Tom Erez, Yuval Tassa (Google DeepMind)
- Note: Written by **Intrinsic AI's own researchers** -- intellectual foundation of the AIC challenge itself.
- What it does: Learns linear quasi-static contact force model y_hat = G * Omega(q, u) mapping configuration + control to predicted F/T values. LML algorithm runs in real-time on CPU, updates as new measurements arrive.
- Key details: Feature vector Omega contains TCP position(3), orientation quat(4), velocity(6), gripper width(1), cross-terms(~10) = ~24 features. Update is Recursive Least Squares (rank-1, no matrix inversion).
- Link: [model-based-plugging.github.io](https://model-based-plugging.github.io) (Colab notebooks available)

### B.2 Sim-to-Real Transfer for Insertion

**Marougkas et al. -- "Integrating Model-based Control and RL for Sim2Real Transfer of Tight Insertion" (2025)**
- Link: [arxiv.org/abs/2505.11858](https://arxiv.org/abs/2505.11858)
- What it does: Sub-1mm insertion with zero-shot sim-to-real transfer by combining potential-field model controller with residual RL. Model-based handles gross motion; residual RL (trained with sparse reward) provides fine corrections. Curriculum over observation noise and action magnitude bridges sim-to-real gap.

### B.3 Symbolic State Estimation

**Zhao et al. -- "Symbolic State Estimation with Predicates for Contact-Rich Manipulation" (2022)**
- Link: [arxiv.org/abs/2203.02468](https://arxiv.org/abs/2203.02468)
- What it does: Bayesian state estimation using predicate classifiers to detect symbolic states (SEARCHING, ALIGNED, INSERTING, INSERTED) from F/T data. Minimal training data, generalizes across connector types.

### B.4 Surgical / Force-Guided Insertion

**Kim et al. -- "Deep Learning Guided Autonomous Surgery: Sub-Millimeter Needle Insertion" (2023)**
- Venue: JHU system
- Link: [arxiv.org/abs/2306.10133](https://arxiv.org/abs/2306.10133)
- What it does: 22 um XY accuracy for retinal vein cannulation using monocular visual servoing + MPC + deep learning contact detection. Decomposition: visual approach -> contact detection -> constrained MPC insertion. All 24 trials succeeded.
- Key insight: Force-based puncture/contact event detection using small CNNs on F/T time windows.

### B.5 Spiral Search

**Park et al. -- "Compliant Peg-in-Hole Using Partial Spiral Force Trajectory (PSFT)" (2020)**
- Link: [doi.org/10.1109/LRA.2020.3000428](https://doi.org/10.1109/LRA.2020.3000428)
- What it does: Improved spiral search that reduces search-time variance by 91.7% vs standard spiral. Uses compliance (no F/T needed for searching) and tilted peg posture for reliable chamfer entry.
- Key details: Archimedean spiral r(t) = a + b*t, spacing = clearance/(2*pi), tilt 3-5 deg.

### B.6 Compliant Insertion / Manipulation Funnels

**Chen et al. -- "Robust Peg-in-Hole via Compliant Funnel-based Manipulation" (RSS 2025)**
- Link: [roboticsproceedings.org/rss21/p060.html](https://roboticsproceedings.org/rss21/p060.html)
- What it does: Manipulation funnels using contact-inclusive planning to iteratively localize hole and refine insertion -- learning-free. Works on NIST Assembly Task Board with tight tolerances. Generalizes across shapes/materials.

### B.7 Cable Connector Mating

**Kienle et al. -- "AI-based Framework for Connector Mating in Robotic Wire Harness Installation" (CASE 2025)**
- Link: [arxiv.org/abs/2503.09409](https://arxiv.org/abs/2503.09409)
- What it does: Directly addresses cable connector mating using force control + deep visuotactile learning. Multimodal transformer on visual, tactile, proprioceptive data optimizes search-and-insertion strategies.

### B.8 Extremum-Seeking Wiggle

**Burner et al. -- "ESTac: Extremum Seeking Controlled Wiggling for Insertion" (2025)**
- arXiv: 2410.02595
- Link: [arxiv.org/abs/2410.02595](https://arxiv.org/abs/2410.02595)
- What it does: Oscillates end-effector while pushing. Uses F/T gradient to find direction increasing insertion depth. 71-84% success on complex geometries. ~5 Hz sinusoidal XY oscillation, sub-mm amplitude.

### B.9 Iterative Reference Learning

**Salt-Ducaju et al. -- "Iterative Reference Learning for Insertion" (IROS 2024)**
- Link: [10.1109/IROS58592.2024.10801796](https://ieeexplore.ieee.org/document/10801796)
- What it does: Franka Panda completes peg-in-hole by iteratively updating Cartesian reference trajectory -- converges in 3 iterations. No NN, no GPU, no RL. Pure control theory. Algorithm is single matrix update.

### B.10 Safe RL with Force Limits

**Liu et al. -- "Dynamic Safety Lock (DSL) + Simple RL"**
- Link: [arxiv.org/abs/2302.10842](https://arxiv.org/abs/2302.10842)
- What it does: Even simple RL (PPO with small MLP) can learn insertion in ~500 episodes with a dynamic safety lock that hard-limits forces. With MuJoCo at 40 Hz on CPU, ~2 hours training. DSL prevents emergency stops and force penalties.

### B.11 Force-Aware Reactive Policies

**FoAR -- Force-Aware Reactive Policy (RA-L 2025)**
- Authors: Alan He et al.
- Link: [arxiv.org/abs/2411.15753](https://arxiv.org/abs/2411.15753)
- Code: [github.com/Alan-Heoooh/FoAR](https://github.com/Alan-Heoooh/FoAR)
- What it does: F/T + vision fusion, contact predictor, CPU-runnable inference for reactive insertion correction.

### B.12 Residual Assembly

**ResiP -- Residual Assembly Policy**
- Link: [residual-assembly.github.io](https://residual-assembly.github.io)
- What it does: Behavior Cloning base policy + residual RL correction, sim-to-real distillation. Open code + data.

### B.13 Variable Impedance via RL

**Variable Impedance Control via RL for Contact Tasks**
- Venue: Various (Franka Panda contact tasks)
- Link: [arxiv.org/abs/1906.08880](https://arxiv.org/abs/1906.08880)
- What it does: Learned stiffness/damping schedule per task phase. Adaptive impedance from RL.

### B.14 Safe Bayesian Optimization (SafeOpt)

**Berkenkamp et al. -- "Bayesian Optimization with Safety Constraints: Safe and Automatic Parameter Tuning in Robotics"**
- Authors: Felix Berkenkamp, Andreas Krause, Angela P. Schoellig
- Venue: IEEE ICRA (originally 2016), extended journal version
- Link: [arxiv.org/abs/1602.04450](https://arxiv.org/abs/1602.04450)
- What it does: Bayesian Optimization that finds optimal controller parameters while guaranteeing no unsafe evaluation. GP model ensures safety constraints (e.g., force limits) are never exceeded during exploration. Starts from known-safe conservative parameters, then explores better parameters safely. Needs only 20-30 evaluations. CPU-only. Proven on real Franka Panda.
- Relevance: For AIC, use after CMA-ES to refine impedance parameters with guaranteed force safety. Directly applicable to per-state impedance tuning.

### AIC Challenge Literature Summary

| Paper | Year | Key Technique | CPU-Only |
|-------|------|--------------|----------|
| Tracy et al. (Intrinsic) | 2023 | Online LML force model, RLS | Yes |
| Marougkas et al. | 2025 | Residual RL + model-based, sim2real | Yes (small MLP) |
| Zhao et al. | 2022 | Bayesian symbolic state estimation | Yes |
| Kim et al. (JHU) | 2023 | Surgical decomposition, MPC insertion | Yes |
| Park et al. (PSFT) | 2020 | Spiral search, 91.7% variance reduction | Yes |
| Chen et al. (RSS) | 2025 | Manipulation funnels, learning-free | Yes |
| Kienle et al. | CASE 2025 | Multimodal transformer connector mating | No (transformer) |
| Burner et al. (ESTac) | 2025 | Extremum-seeking wiggle, 71-84% | Yes |
| Salt-Ducaju et al. (IRL) | IROS 2024 | Iterative reference learning, 3 iters | Yes |
| Liu et al. (DSL) | -- | Dynamic safety lock + PPO | Yes |
| FoAR (He et al.) | RA-L 2025 | Force-aware reactive policy | Yes |
| ResiP | -- | BC + residual RL | Slow but yes |
| Berkenkamp et al. (SafeOpt) | ICRA 2016+ | Safe BO with GP constraints | Yes |

### Medical/Surgical Technique Transfer Table

| Surgical Technique | Original Domain | Application |
|-------------------|----------------|-------------|
| Force-guided needle insertion with MPC | Retinal vein cannulation (22um) | Force-guided connector insertion |
| Adaptive impedance with friction compensation | Dexterous hand (0.16 deg error) | Adaptive stiffness/damping per phase |
| Bayesian contact event detection | Connector-socket insertion | Symbolic FSM for phase transitions |
| Spiral search (PSFT) | Peg-in-hole assembly (91.7% variance reduction) | Fallback port search without vision |
| Online quasi-static force model | Connector insertion (Intrinsic AI) | MPC forward model for predictive safety |
| Residual RL on model-based | Tight insertion (<1mm, zero-shot sim2real) | Fine corrections during insertion |
| Manipulation funnels via compliance | NIST ATB peg-in-hole (learning-free) | Formal convergence guarantee |
| Variable impedance via RL | Franka Panda contact tasks | Learned stiffness/damping per phase |

---

## PART C: ALL CODE REPOSITORIES

---

### C.1 Thesis Repos (DLO / Dual-Arm / Collision Avoidance)

| Repo | Paper/Purpose | Language | Status |
|------|--------------|----------|--------|
| [Mingrui-Yu/DLO_planning_2](https://github.com/Mingrui-Yu/DLO_planning_2) | IJRR 2024: Whole-body dual-arm DLO planner | C++ + ROS + Unity | Active |
| [Mingrui-Yu/shape_control_DLO_2](https://github.com/Mingrui-Yu/shape_control_DLO_2) | T-RO 2023: Global model learning for DLO control | Python | Active |
| [lar-unibo/dlo_manipulation_online_params](https://github.com/lar-unibo/dlo_manipulation_online_params) | RA-L 2024: Online parameter estimation | Python | Active |
| [lar-unibo/RT-DLO](https://github.com/lar-unibo/RT-DLO) | RA-L: Real-time DLO segmentation | Python | Active |
| [RMDLO/trackdlo](https://github.com/RMDLO/trackdlo) | RA-L: DLO tracking under occlusion | Python + ROS | Active |
| [RMDLO/abb_dual_arm](https://github.com/RMDLO/abb_dual_arm) | ABB dual-arm ROS packages | ROS | Active |
| [StanfordASL/oscbf](https://github.com/StanfordASL/oscbf) | ICRA 2025: CBFpy -- operational space CBF | Python | Active |
| [suryarobotcontrol/Dual-Arm-Manipulation](https://github.com/suryarobotcontrol/Dual-Arm-Manipulation) | Frontiers 2025: iAPF dual-arm collision avoidance | Python | Active |
| [sites.google.com/view/icra2025-sdfsc](https://sites.google.com/view/icra2025-sdfsc) | ICRA 2025: SDF-SC fast collision detection | -- | Active |
| [Autrio/MuJoCo-Dual-Arm](https://github.com/Autrio/MuJoCo-Dual-Arm) | Franka bi-manual in MuJoCo (template) | Python | Available |
| [qj25/adapteddlo_muj](https://github.com/qj25/adapteddlo_muj) | DER cable model for MuJoCo (thesis foundation) | Python + C++ | Active |

### C.2 Challenge Repos (Robotics / Bimanual MuJoCo)

| Repo | What It Has |
|------|------------|
| [ir-lab/irl_control](https://github.com/ir-lab/irl_control) | Dual UR5 MuJoCo + OSC + Admittance + NIST insertion task (random pos/angle), teleoperation, PID tuning |
| [ir-lab/bimanual-imitation](https://github.com/ir-lab/bimanual-imitation) | Updated MuJoCo API (not mujoco-py), dual-arm imitation |
| [RPM-lab-UMN/dual-arm-peg-in-hole-mujoco-sim](https://github.com/RPM-lab-UMN/dual-arm-peg-in-hole-mujoco-sim) | UR5e dual-arm peg-in-hole, OSC, Gymnasium, dm_control |
| [kevinzakka/mjctrl](https://github.com/kevinzakka/mjctrl) | Single-file MuJoCo controllers: impedance, OSC, joint PD -- minimal deps |
| [wengmister/impedance_control_mujoco](https://github.com/wengmister/impedance_control_mujoco) | Franka Panda impedance in MuJoCo with null-space freedom |
| [ADVRHumanoids/RobotImpedanceModulation](https://github.com/ADVRHumanoids/RobotImpedanceModulation) | ROS 2 variable impedance, auto-computed from task force + precision |
| [google-deepmind/mujoco discussions #879](https://github.com/google-deepmind/mujoco/discussions/879) | Peg-in-hole MuJoCo XML with convex decomposition (Blender), hardware-validated |

### C.3 Challenge Repos (Medical Robotics -- Force-Guided Insertion)

| Repo | What It Has |
|------|------------|
| [airvlab/cathsim](https://github.com/airvlab/cathsim) | Endovascular catheter simulator -- DLO catheter + aorta + real-time force + RL (SAC/PPO), CPU-friendly. Structurally identical to cable routing through clips. |
| [ZhouyangX/CardioXplorer](https://github.com/ZhouyangX/CardioXplorer) | Robotic catheter 3-DoF (axial + rotation + tip) -- admittance control |
| [woo-rookie/ur3_admittance_controller](https://github.com/woo-rookie/ur3_admittance_controller) | UR3 admittance controller -- F/T-driven velocity, full ROS |

### C.4 Challenge Repos (Industrial Peg-in-Hole)

| Repo | What It Has |
|------|------------|
| [Alan-Heoooh/FoAR](https://github.com/Alan-Heoooh/FoAR) | Force-Aware Reactive Policy (RA-L 2025) -- F/T + vision, contact predictor, CPU inference |
| [residual-assembly.github.io](https://residual-assembly.github.io) (ResiP) | BC + residual RL, sim-to-real distillation, open code + data |
| [BaiShuanghao/Awesome-Robotics-Manipulation](https://github.com/BaiShuanghao/Awesome-Robotics-Manipulation) | Curated list 200+ manipulation repos with code |
| [jack-sherman01/Awesome-Learning4Safe-Contact-rich-tasks](https://github.com/jack-sherman01/Awesome-Learning4Safe-Contact-rich-tasks) | Curated list: safe learning for contact-rich tasks |

### C.5 Challenge Repos (Extremum Seeking / Optimization)

| Repo | What It Has |
|------|------------|
| [michael-sankur/extremum-seeking](https://github.com/michael-sankur/extremum-seeking) | Plug-and-play 1D/2D/ND extremum seeking + Jupyter notebooks |
| Burner et al. ESTac (2025) | Code on paper website (arXiv:2410.02595) |
| [pycma (Hansen)](https://github.com/CMA-ES/pycma) | Official CMA-ES Python library |
| [ModelDBRepository/245563](https://github.com/ModelDBRepository/245563) | CMA-ES parameter optimization |

---

## PART D: JOURNAL & CONFERENCE VENUE REFERENCE

| Journal/Conference | Impact Factor | Scope |
|-------------------|--------------|-------|
| IEEE Transactions on Robotics (T-RO) | ~9.4 | Robotics methodology |
| International Journal of Robotics Research (IJRR) | ~9.0 | Top robotics journal |
| IEEE RA-L (Robotics and Automation Letters) | ~5.2 | Letters format, fast turnaround |
| IEEE T-ASE (Automation Science and Engineering) | ~6.4 | Automation + robotics |
| IEEE/ASME T-Mechatronics | ~6.1 | Mechatronics systems |
| Advanced Intelligent Systems (Wiley) | ~6.8 | AI + robotics interdisciplinary |
| Robotics and Autonomous Systems (Elsevier) | ~4.3 | Broad robotics |
| Frontiers in Robotics and AI | ~2.9 | Open access, broad |
| Sensors (MDPI) | ~3.9 | Sensors + perception |
| IEEE ICRA / IROS | N/A (top conf) | Premier robotics conferences |
| RSS (Robotics: Science and Systems) | N/A (top conf) | Premier robotics conference |
| Nature Scientific Reports | ~4.6 | Broad science |
| Journal of Manufacturing Systems | ~12.1 | Manufacturing |
| Robotics and Computer-Integrated Manufacturing | ~10.4 | Industrial robotics |
| Advanced Engineering Informatics | ~8.0 | Engineering AI |
| IEEE Humanoids | N/A (conf) | Humanoid robotics |
| IEEE CASE | N/A (conf) | Automation conference |

---

## PART E: TUM-SPECIFIC RESEARCH (Chen, Bing, Knoll Lab)

Papers from the TUM group directly relevant to the thesis setup and advisor alignment.

### E.1 DLO Manipulation (Chen et al.)

**Contact-Aware Shaping and Maintenance of DLOs With Fixtures** -- see Step 4.5 above (IROS 2023, founding paper)

**Real-Time Contact State Estimation in Shape Control of DLOs Under Small Environmental Constraints** -- see Step 4.5 above (ICRA 2024)

**Multi-Robot Assembly of Deformable Linear Objects Using Multi-Modal Perception** -- see Step 4.5 above (ICRA 2025)

### E.2 Motion Planning (Zhang, Chen, Bing et al.)

**Direction Informed Trees (DIT*)** -- see Step 3.3 above (2025)

**JIT*: Manipulability-Aware Asymptotically Optimized Motion Planning** -- see Step 3.3 above (2025)

**Flexible Informed Trees (FIT*): Adaptive Batch-Size Sampling-Based Planner** -- see Step 3.3 above (IROS 2023)

### E.3 Safety-Critical Control (Zhang, Bing et al.)

**Adaptive Safety-Critical Control for High-Order Systems: A Real-Time Gaussian Process Approach** -- see Step 5.7 above (T-ASE 2025)

**Robust Dual-Filter Safety Control for Mobile Robots in Dynamic Multiobstacle Environments** -- see Step 5.7 above (TMech 2025)

**Meta-Learning-Based Safety-Critical Control in Multi-Obstacles Environments (Meta-CBF / Meta-BRCBF)**
- Authors: Bing, Zhang et al. (TUM)
- Venue: IEEE Transactions on Automation Science and Engineering, Vol. 22, 2025
- Link: [ieeexplore.ieee.org/document/10980124](https://ieeexplore.ieee.org/document/10980124/)
- What it does: MetaSDF + Meta-Bayesian CBF (Meta-BRCBF) uses meta-learning to adapt safety constraints to novel obstacle configurations from few observations. Validated on a real robot arm in multi-obstacle environments. See also Step 5.8 above for full details.
- Relevance: Most critical TUM group paper for thesis collision avoidance backbone.

**Safety Guaranteed Manipulation Based on RL Planner and MPC Actor**
- Authors: Bing et al. (TUM)
- Venue: 2023
- Link: [arxiv.org/abs/2304.09119](https://arxiv.org/abs/2304.09119)
- What it does: Combines RL planner with MPC actor for safety-guaranteed manipulation.

**Online Efficient Safety-Critical Control for Mobile Robots in Unknown Dynamic Multi-Obstacle Environments**
- Authors: Bing et al. (TUM)
- Venue: IEEE/RSJ IROS 2024
- Link: [arxiv.org/abs/2402.16449](https://arxiv.org/abs/2402.16449)
- What it does: Online efficient safety-critical control in unknown dynamic environments with multiple obstacles.

### E.4 Tactile & Imitation Learning (TUM)

**1 kHz Behavior Tree for Self-Adaptable Tactile Insertion**
- Venue: IEEE ICRA 2024
- Link: [10.1109/ICRA57147.2024.10610835](https://frankiewoo.github.io/publication/wu-2024-icra/wu-2024-icra.pdf)
- What it does: High-frequency (1 kHz) behavior tree for self-adaptable tactile insertion tasks.

**Task-Based Compliance Control for Bottle Screw Manipulation with Dual-Arm Robot**
- Venue: 2023
- Link: [10.1109/TIE.2023.3260342](https://mediatum.ub.tum.de/doc/1703739/document.pdf)
- What it does: Task-based compliance control for contact-rich bottle screw manipulation using dual-arm robot.

**TacDiffusion**
- Venue: IEEE ICRA 2025
- Link: [arxiv.org/abs/2409.11047](https://arxiv.org/abs/2409.11047)
- Github: [popnut123/TacDiffusion](https://github.com/popnut123/TacDiffusion
- What it does: Diffusion-based tactile policy for manipulation tasks.

**LEMMo-Plan: LLM-Enhanced Learning from Multi-Modal Demonstration**
- Venue: IEEE ICRA 2025
- Link: [lemmo-plan.github.io/LEMMo-Plan/](https://lemmo-plan.github.io/LEMMo-Plan/)
- What it does: LLM-enhanced learning from multi-modal demonstrations for robotic manipulation.

**Long-Horizon Language-Conditioned Imitation Learning for Robotic Manipulation**
- Authors: Bing et al. (TUM)
- Venue: 2025
- Link: [10.1109/TMECH.2025.3547047](https://ieeexplore.ieee.org/abstract/document/10934975)
- What it does: Long-horizon language-conditioned imitation learning for complex manipulation sequences.

### E.5 Planning & Scheduling (TUM)

**Ontology Based AI Planning and Scheduling for Robotic Assembly**
- Authors: Bing et al. (TUM)
- Venue: IEEE/RSJ IROS 2024
- Link: [10.1109/IROS58592.2024.10802295](https://ieeexplore.ieee.org/document/10802295)
- What it does: Ontology-based AI planning and scheduling for robotic assembly tasks.

---

## PART F: SURVEYS & FOUNDATIONAL WORKS

### F.1 Surveys

**Robotic Perception and Manipulation of Deformable Linear Objects: A Survey** -- see Step 1.4 above (IJRR 2026, Caporali et al.)

**Robotic Manipulation of Deformable Linear Objects: A Survey**
- Authors: Yu, Li
- Venue: ROBOT (Chinese Journal of Robotics), 2024
- Link: [10.13973/j.cnki.robot.240139](https://robot.sia.cn/en/article/doi/10.13973/j.cnki.robot.240139)
- What it does: Chinese-language survey on robotic DLO manipulation.

**Modeling, Learning, Perception, and Control for Deformable Object Manipulation**
- Authors: Yin, Varava, Kragic
- Venue: 2021
- Link: [doi.org/10.1126/scirobotics.abd8803](https://doi.org/10.1126/scirobotics.abd8803)
- What it does: Comprehensive survey covering modeling, learning, perception, and control for deformable object manipulation broadly.

**A Review of Robotic Manipulation Solutions for Deformable Linear Objects (Wire Harness Assembly)**
- Link: [doi.org/10.1016/j.robot.2026.105375](https://doi.org/10.1016/j.robot.2026.105375)
- What it does: Technical review focused on wire harness assembly solutions using robotic manipulation.

**A Survey on Robotic Manipulation of Deformable Objects**
- Venue: IEEE Transactions on Industrial Informatics, 2024
- Link: [arxiv.org/abs/2312.10419](https://arxiv.org/abs/2312.10419)
- What it does: Reviews 150+ papers on all deformable object types, with a DLO-specific section covering shape estimation, modeling, and task-level planning. High-impact survey in IEEE T-II (Q1).
- Relevance: Background reference for introduction and related work chapters covering deformable object manipulation broadly.

**Deformable and Fragile Object Manipulation: A Review and Prospects**
- Venue: Sensors (MDPI), 2025
- Link: [doi.org/10.3390/s25175430](https://www.mdpi.com/1424-8220/25/17/5430)
- What it does: Perception-to-control pipeline review with DLO-specific sections covering recent deep learning integration methods and sensor fusion strategies for deformable and fragile object manipulation.
- Relevance: Additional survey covering sensor fusion and perception aspects of DLO manipulation relevant to Stage 1 of thesis.

**A Multi-Robot Collaborative Manipulation Framework for Dynamic and Deformable Objects**
- Venue: Frontiers in Robotics and AI, Vol. 12, 2025 — DOI: 10.3389/frobt.2025.1585544
- Link: [doi.org/10.3389/frobt.2025.1585544](https://doi.org/10.3389/frobt.2025.1585544)
- What it does: Addresses collaborative manipulation of dynamic deformable objects with multiple robots, coordinating task decomposition, motion planning, and execution. Validated in Gazebo simulation with ROS.
- Relevance: Multi-robot framework for deformable object manipulation — provides baseline framework for multi-robot DLO coordination in thesis.

**LLM-Driven Symbolic Planning and Hierarchical Imitation Learning for DLO Manipulation**
- Authors: PolyU Group (Navarro-Alarcón group)
- Venue: Robotics and Computer-Integrated Manufacturing, accepted January 2026
- Link: [doi.org/10.1016/j.rcim.2025.103096](https://www.sciencedirect.com/science/article/abs/pii/S0736584525001504)
- What it does: Uses large language models to generate task-level symbolic plans for DLO manipulation, combined with low-level imitation controllers. Represents the emerging paradigm of high-level task decomposition for cable routing.
- Relevance: LLM-guided planning for DLO manipulation — potential direction for Stage 3 global planning with natural language specification of routing tasks.

**Cooperative Manipulation Control with Task-Prioritized Real-Time Optimization for Free-Floating Dual-Arm Space Robots**
- Authors: Su, Shi et al.
- Venue: Aerospace Science and Technology, 2025/2026
- Link: [doi.org/10.1016/j.ast.2025.111584](https://www.sciencedirect.com/science/article/abs/pii/S1270963825016487)
- What it does: Hierarchical Quadratic Programming (HQP) framework for dual-arm space robots handling internal wrench limits and self-collision constraints simultaneously. HQP architecture where collision avoidance is a lower-priority task below primary task-space tracking.
- Relevance: HQP design pattern directly applicable to thesis — collision avoidance as lower-priority task in the shape control hierarchy.

**Robust Optical Transceiver Manipulation in Cluttered Cable Environments**
- Venue: IEEE ICRA, 2025
- Link: [10.1109/ICRA55743.2025.11127450](https://ieeexplore.ieee.org/document/11127450)
- What it does: Addresses cable-routing problems from the grasp-point perspective in environments cluttered with other cables — relevant to fixture-dense environments of automotive wire harness assembly.
- Relevance: Demonstrates robustness requirements for manipulation in cable-cluttered environments — motivates robust collision avoidance for industrial DLO setups.

### F.2 Foundational / Earlier Works

**Robotic Manipulation Planning for Shaping DLOs with Environmental Contacts**
- Authors: Zhu et al.
- Venue: 2019
- Link: [10.1109/LRA.2019.2944304](https://ieeexplore.ieee.org/document/8851170)
- What it does: Early work on manipulation planning for DLOs using environmental contacts for shaping.

**Manipulating Deformable Objects by Interleaving Prediction, Planning, and Control**
- Authors: McConachie et al.
- Venue: 2020
- Link: [doi.org/10.1177/0278364920918299](https://doi.org/10.1177/0278364920918299)
- What it does: Interleaving prediction, planning, and control for deformable object manipulation.

---

## PART G: SOFTWARE TOOLS & PAPERS

**Extending MoveIt with Advanced Manipulation Functions for Industrial Applications**
- Authors: Pablomalvido et al.
- Venue: 2023
- Link: [doi.org/10.1016/j.rcim.2023.102559](https://www.sciencedirect.com/science/article/pii/S0736584523000352)
- Code: [github.com/pablomalvido/Advanced_manipulation_moveit](https://github.com/pablomalvido/Advanced_manipulation_moveit)
- What it does: MoveIt extensions for advanced manipulation including synchronized motion and ATC.

**ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation**
- Authors: Huang et al.
- Venue: 2024
- Link: [arxiv.org/abs/2409.01652](https://arxiv.org/abs/2409.01652)
- Code: [github.com/huangwl18/ReKep](https://github.com/huangwl18/ReKep)
- What it does: Relational keypoint constraints for robotic manipulation planning.

**SceneSmith: Agentic Generation of Simulation-Ready Indoor Scenes**
- Authors: Pfaff et al.
- Link: [scenesmith.github.io](https://scenesmith.github.io/)
- Code: [github.com/nepfaff/scenesmith](https://github.com/nepfaff/scenesmith)
- What it does: Agentic generation of simulation-ready indoor scenes for robotics.

**cuRobo: Parallelized Collision-Free Minimum-Jerk Robot Motion Generation**
- Authors: Murali et al.
- Venue: 2023
- Link: [arxiv.org/abs/2310.17274](https://arxiv.org/abs/2310.17274)
- Code: [github.com/NVlabs/curobo](https://github.com/NVlabs/curobo)
- What it does: CUDA-accelerated collision-free, minimum-jerk robot motion generation.

**PyRoki: A Modular Toolkit for Robot Kinematic Optimization**
- Authors: Kim et al.
- Venue: 2025
- Link: [pyroki-toolkit.github.io](https://pyroki-toolkit.github.io/)
- Code: [github.com/chungmin99/pyroki](https://github.com/chungmin99/pyroki)
- What it does: JAX-based modular toolkit for robot kinematic optimization and differentiable IK.

---

## PART H: TECHNICAL REPORTS & THESES

- **Dual-Arm-Manipulator-Pick-and-Drop.pdf** -- MuJoCo Dual-Arm Simulation Technical Report
- **Robotics-Thesis-Demo-for-Collaboration.pdf** -- Strategic Technical Roadmap
- **DLO Segmentation and Estimation for Dual-Arm Robot Cable Manipulation** -- Tampere University Thesis

---

## PART C (CONTINUED): ALL MISSING CODE REPOSITORIES

### C.6 DLO Repos (Additional)

| Repo | What It Has |
|------|------------|
| [Mingrui-Yu/arm_planning](https://github.com/Mingrui-Yu/arm_planning) | Sampling-based robotic arm planning |
| [lar-unibo/DLO_MultiView_Tracking](https://github.com/lar-unibo/DLO_MultiView_Tracking) | Cosserat rod multiview DLO tracking |
| [qj25/adapteddlo_muj](https://github.com/qj25/adapteddlo_muj) | Discrete Elastic Rods in MuJoCo |
| [roahmlab.github.io/DEFORM/](https://roahmlab.github.io/DEFORM/) | Differentiable DER project page |
| [tan-liam/CableRouting](https://github.com/tan-liam/CableRouting) | Multi-stage cable routing (T-RO paper) |
| [Mingrui-Yu/DLO_following](https://github.com/Mingrui-Yu/DLO_following) | In-hand DLO following — IROS 2024 |
| [parkergu.github.io/work_dlo](https://parkergu.github.io/work_dlo) | GA-Net DLO tracking project page (T-ASE 2025) |
| [sites.google.com/view/dlom](https://sites.google.com/view/dlom) | EA-PE-GAT hybrid force-position code (arXiv:2508.07319) |

### C.7 Dual-Arm & Bimanual Repos (Additional)

| Repo | What It Has |
|------|------------|
| [Badenhoop/chair_manipulation](https://github.com/Badenhoop/chair_manipulation) | Dual-arm chair manipulation |
| [fiveages-sim/arms_ros2_control](https://github.com/fiveages-sim/arms_ros2_control) | ROS2-control for single/dual arm |
| [robotcourse1/ros2-openarm-project](https://github.com/robotcourse1/ros2-openarm-project) | OpenArm dual-arm pipeline |
| [moveit/moveit2_tutorials](https://github.com/moveit/moveit2_tutorials) | Dual Arms MoveIt 2 tutorial configuration |
| [danielhoeltgen/Dual-Arm-Robot-Force-Controlled-Object-Manipulation](https://github.com/danielhoeltgen/Dual-Arm-Robot-Force-Controlled-Object-Manipulation) | UR5+UR10 force control |
| [tenfoldpaper/multipanda_ros2](https://github.com/tenfoldpaper/multipanda_ros2) | Multi-Panda ROS 2 MuJoCo setup |
| [kkaytekin/Bimanual-Manipulation](https://github.com/kkaytekin/Bimanual-Manipulation) | CoppeliaSim Lua scripts |
| [labicon/bimanual-manipulation](https://github.com/labicon/bimanual-manipulation) | Heterogeneous robot MuJoCo setups |

### C.8 Simulation, Kinematics & Planners

| Repo | What It Has |
|------|------------|
| [caelan/pybullet-planning](https://github.com/caelan/pybullet-planning) | PyBullet TAMP and IKFast |
| [stack-of-tasks/pinocchio](https://github.com/stack-of-tasks/pinocchio) | Rigid body dynamics and analytical derivatives |
| [ian-chuang/Manipulator-Mujoco](https://github.com/ian-chuang/Manipulator-Mujoco) | Base MuJoCo Gymnasium environment for OSC |
| [hsp-iit/pybullet-robot-envs](https://github.com/hsp-iit/pybullet-robot-envs) | PyBullet RL environments |
| [ARISE-Initiative/robosuite](https://github.com/ARISE-Initiative/robosuite) | MuJoCo bimanual robot learning framework |
| [NVlabs/collab-sim](https://github.com/NVlabs/collab-sim) | Isaac Sim VR teleoperation with CuRobo |
| [loco-3d/crocoddyl](https://github.com/loco-3d/crocoddyl) | Multi-contact optimal control |
| [Simple-Robotics/aligator](https://github.com/Simple-Robotics/aligator) | Constrained trajectory optimization |
| [google-deepmind/mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie) | High-quality MuJoCo robot models |
| [vikashplus/franka_sim](https://github.com/vikashplus/franka_sim) | Franka Panda hardware-tested MJCF models |
| [OMPL](https://ompl.kavrakilab.org/) (Open Motion Planning Library) | Standard ROS motion planning library |
| [volunt4s/Simple-MuJoCo-PickNPlace](https://github.com/volunt4s/Simple-MuJoCo-PickNPlace) | Single-Arm Pick & Place Tutorial |
| [kevinzakka/mink](https://github.com/kevinzakka/mink) | Task-space IK library |

### C.9 Controllers & Safety (Additional)

| Repo | What It Has |
|------|------------|
| [frankarobotics/franka_ros2](https://github.com/frankarobotics/franka_ros2) | ROS 2 integration for Franka |
| [NVlabs/curobo](https://github.com/NVlabs/curobo) | CUDA accelerated collision-free motion generation |

### C.10 Scene Generation & Perception

| Repo | What It Has |
|------|------------|
| [huangwl18/ReKep](https://github.com/huangwl18/ReKep) | Relational keypoint constraints |
| [nepfaff/scenesmith](https://github.com/nepfaff/scenesmith) | Agentic simulation scene generation |
| [chungmin99/pyroki](https://github.com/chungmin99/pyroki) | JAX kinematic optimization / differentiable IK |
| [pablomalvido/Advanced_manipulation_moveit](https://github.com/pablomalvido/Advanced_manipulation_moveit) | MoveIt extensions for ATC and sync |
