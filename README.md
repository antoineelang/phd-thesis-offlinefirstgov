# Article 2: Hierarchical Offline-First Blockchain Architecture

This branch contains the artifacts for the DAG-DSR (Deterministic State Reconciliation) mechanism developed in **Article 2**.

## 📂 Repository Structure
* `/simulations/dag_state_reconciliation/`: The exact `SimPy` discrete-event simulation framework. It executes the $\lambda = 5.2$ Poisson workload and resolves cross-partition conflicts in $\mathcal{O}(n \log n)$ using the Lexicographic Tuple described in the paper.
* `/testbed/dag_dsr_engine/`: Scripts generating the 52 KB asynchronous notarization payloads and empirical hardware logs comparing DAG-DSR against an Apache CouchDB baseline.
* `/manuscript_figures/`: High-resolution original figures utilized in the final IEEE manuscript.

## 🚀 Reproducibility
As per the Appendix, the stochastic partition model is explicitly fixed with `numpy.random.seed(42)`. To execute the SimPy DAG-DSR engine:
```bash
cd simulations/dag_state_reconciliation/
python3 simulate_dag_dsr_simpy.py
