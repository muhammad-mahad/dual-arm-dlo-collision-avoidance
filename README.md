# Dual-Arm DLO Collision Avoidance

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Official repository:** [https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git](https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git)

This repository serves as the simulation environment and prototype controller testbed for the master's thesis: **"Safe Dual-Arm Cable Routing with Deformable Linear Objects: Hierarchical Planning and Contact-Aware Control Barrier Functions"**.

Currently, the codebase provides the foundational **Phase 1** rigid-body baseline, which demonstrates a highly accurate dual-arm pick-and-handover task operating within the MuJoCo simulator, integrated seamlessly with the `mink` inverse kinematics library.

---

## 📸 Media Preview

![Demo Setup](docs/figures/demo_screenshot.png)

*(Above: A static breakdown of the dual-arm workspace interface.)*

![Demo Animation](media/demo_preview.gif)

*(Above: The dual-arms smoothly acting in isolated freeze-frame logic, picking and carrying the cube payload.)*

---

## 📂 Complete Workspace Structure

This repository is organized to separate theoretical documentation from executable simulation scripts cleanly:

- **`README.md`**: This main documentation file.
- **`ROADMAP.md`**: Tracking timeline showing exact milestones for Phase 1-4 thesis completion.
- **`LICENSE`**: MIT open-source license.
- **`docs/`**: Thesis planning and theoretical documents.
  - `thesis_proposal.md`: The complete, official problem statement, methodology, and abstract.
  - `figures/demo_screenshot.png`: Visualization of the setup.
- **`media/`**: Demo media.
  - `demo_preview.gif`: A visual recording of the demo pick routine.
- **`requirements.txt`**: Minimal requirements file detailing necessary tools like `mujoco`, `mink`, and `numpy`.
- **`setup_env.sh` / `setup_env.bat`**: Automatic one-click shell scripts for creating virtual environments across any platform seamlessly.
- **`simulation/`**: The core runtime code pipeline.
  - `demo_pick_cube.py`: Python script running the MuJoCo viewer and issuing real-time IK target updates to control both robotic arms.
  - `franka_emika_panda/`: Folder containing exactly simulated rigid-body physics for the dual robotic arms, including `.xml` structure definitions, robot meshes, actuator settings, and limits.

---

## 🛠️ Installation & Setup

You have two choices for setting up the workspace: **Automatic** or **Manual**. Note that **Python 3.10+** is strictly required for `mink` to handle the Inverse Kinematics efficiently.

### Option 1: Automatic Installation (Recommended)

These scripts handle checking your Python version, building a `venv`, installing packages, and verifying successful installation.

**Linux / macOS**

```bash
# Make the bash script executable
chmod +x setup_env.sh
# Run it
./setup_env.sh
# Activate the created virtual environment
source venv/bin/activate
```

**Windows** (Run from Command Prompt)

```cmd
:: Run the batch script
setup_env.bat
:: Activate the virtual environment
venv\Scripts\activate.bat
```

### Option 2: Manual Installation

If you prefer to configure your environment yourself:

1. Clone the repository and navigate into the root directory:

   ```bash
   git clone https://github.com/muhammad-mahad/dual-arm-dlo-collision-avoidance.git
   cd dual-arm-dlo-collision-avoidance
   ```

2. Build the exact virtual environment locally:

   ```bash
   python -m venv venv
   ```

3. Activate the environment:
   - Linux/macOS: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Update pip and install the core dependencies exclusively:

   ```bash
   pip install -U pip
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Demonstration

Once your environment is set up and strictly activated, navigate to the `simulation` folder and execute the python script:

```bash
cd simulation
python demo_pick_cube.py
```

### What to Expect

The script spins up a MuJoCo 3.x Passive Viewer dynamically, executing the following programmed steps seamlessly:

1. **Contact-aware handover**: Precise arm movement triggered by spatial distance proximity sensing, measured via predefined marker sites on the grippers.
2. **Smooth motion interpolation**: The arms maintain zero-jump, continuous kinematics with dynamically injected damping coefficients on a fraction-of-a-millimeter-scale.
3. **Freeze-based gripper isolation**: While one arm executes payload delivery and positioning, the secondary arm's constraints are rigorously locked, fully simulating asymmetric active/frozen control within the complex 14-DoF model structure without violating physics bounds.

Use `Ctrl+C` or close the MuJoCo window to terminate the simulation at the end of the demonstration sequence.
