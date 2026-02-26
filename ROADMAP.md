# Thesis Roadmap

Below is the structured 6-month development timeline derived from the thesis proposal.

## 📌 Phase 1: Rigid-Body Baseline (Month 1-2)

- [ ] **Month 1: Simulation Setup & Minimal Interface**
  - [x] Construct MuJoCo dual-arm environment using direct API. (Phase 1 Baseline in `demo_pick_cube.py`)
  - [ ] Integrate and calibrate the adapted DER cable model (`qj25/adapteddlomuj`).

- [ ] **Month 2: Local Control & Baseline Safety**
  - [ ] Develop the MPC tracking controller.
  - [ ] Implement and validate the core Control Barrier Function (CBF) constraints (arm-arm, environment, tension) using geometric distances.

## 📌 Phase 2: DLO & Planner Integration (Month 3)

- [ ] **Month 3: Global Planner Integration**
  - [ ] Adapt the DIT/JIT (or CBiRRT) algorithm for DLOs.
  - [ ] Integrate DLO-inclusive collision checking and the catenary-aware cost function.

## 📌 Phase 3: Contact-Aware Routing & Testing (Month 4-5)

- [ ] **Month 4: Contact-Aware Mode Switching**
  - [ ] Implement force-simulated Contact Establishment Indicators (CEI).
  - [ ] Develop and test the mode-switching CBF logic for clip insertions.

- [ ] **Month 5: Dynamic Stress Testing & Evaluation**
  - [ ] Execute evaluation scenarios: fast motions and dynamic obstacle avoidance.
  - [ ] Benchmark performance against standard MPC (without CBF) and vanilla RRT.

## 📌 Phase 4: Finalization (Month 6)

- [ ] **Month 6: Thesis Writing & Defense Preparation**
  - [ ] Data analysis.
  - [ ] Final manuscript drafting.
  - [ ] Presentation formatting.
