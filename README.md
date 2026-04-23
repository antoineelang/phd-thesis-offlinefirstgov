# Article 2: Hierarchical Offline-First Blockchain Architecture

This branch contains the artifacts for the DAG-DSR (Deterministic State Reconciliation) mechanism developed in **Article 2**.

## 📂 Repository Structure (Article 2)
* `/simulations/dag_state_reconciliation/`: Python discrete-event simulations validating the mathematical complexity of conflict resolution.
* `/testbed/dag_dsr_engine/`: Scripts generating the 52 KB asynchronous notarization payloads and empirical hardware logs comparing DAG-DSR against an Apache CouchDB baseline.

## 🚀 Reproducibility
To regenerate the scalability and network partitioning figures:
```bash
cd simulations/dag_state_reconciliation/
python3 generate_article2_figures.py
See testbed/HARDWARE_SETUP.md for physical testbed configuration and Traffic Control (tc) emulation parameters.
