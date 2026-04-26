# Article 3: Resource-Aware Blockchain Orchestration (Edge-DRL)

This branch contains the physical testbed logs, the INT8 AI orchestrator logic, and energy mass-balance simulations developed for **Article 3**.

## 📂 Repository Structure

### 1. 📊 Empirical Data (`/data/`)
Contains the raw traces utilized to train and validate the Deep Reinforcement Learning agent:
* `/nasa_power_solar/`: Contains `adamawa_solar_trace_30days.csv` (Hourly solar irradiance with a severe 72-hour deficit).
* `/art_telecom_qos/`: Contains `rural_lqe_trace_30days.csv` (Gilbert-Elliott telecommunication Link Quality Estimates).
* `generate_training_data.py`: The script used to synthesize these specific environmental constraints.

### 2. 🖥️ Simulations (`/simulations/energy_wall_analysis/`)
Contains the Python discrete-event simulations proving the physical survivability of the node:
* `simulate_drl_battery_simpy.py`: Implements the Battery Mass-Balance (Eq. 1) and the Deterministic Safety Wrapper (Alg. 1).
* `simpy_drl_agent_survival_log.csv` & `simpy_static_node_death_log.csv`: The raw output logs proving the static node dies at hour 28 while the DRL node survives.
* `generate_paper_figures.py`: Generates the IEEE-formatted graphs utilized in the manuscript.

### 3. 🛠️ Hardware Testbed (`/testbed/`)
Contains the actual software and hardware configurations deployed on the physical Raspberry Pi:
* **`/ina219_metrology/`**: The differential power measurement scripts (`ina219_profiler.py`) and the raw CSV traces proving the 0.62 mW INT8 inference overhead.
* **`/python_drl_orchestrator/`**: The INT8-quantized Deep Q-Network policy (`dqn_policy_int8.tflite`) and the execution loop (`drl_orchestrator.py`).
* **`/rust_l2_sequencer/`**: The deterministic, ultra-lightweight cryptographic client written in Rust (`main.rs` & `Cargo.toml`).
* `HARDWARE_SETUP.md`: The wiring diagram and exact OS specifications for independent reproduction.

---

## 🚀 Reproducibility
To verify the mathematical mass-balance model proving the Static node dies at hour 28 while the DRL node survives:
```bash
cd simulations/energy_wall_analysis/
python3 simulate_drl_battery_simpy.py
