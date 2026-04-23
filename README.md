# Article 3: Resource-Aware Blockchain Orchestration

This branch contains the physical testbed logs, AI orchestrator, and energy simulations for **Article 3**.

## 📂 Repository Structure (Article 3)
* `/testbed/rust_l2_sequencer/`: Scaffold of the lightweight cryptographic execution client.
* `/testbed/python_drl_orchestrator/`: The INT8-quantized Deep Q-Network policy.
* `/testbed/ina219_metrology/`: Differential measurement scripts and raw CSV traces capturing the 0.62 mW overhead.
* `/simulations/energy_wall_analysis/`: SimPy discrete-event simulations for battery mass-balance.
* `/data/`: Empirical traces for solar irradiance and telecommunication Quality of Service.

## 🚀 Reproducibility
To execute the SimPy battery survivability model:
```bash
cd simulations/energy_wall_analysis/
python3 simulate_drl_battery_simpy.py
