# Article 2: Hierarchical Offline-First Blockchain Architecture

This branch contains the artifacts for the DAG-DSR (Deterministic State Reconciliation) mechanism developed in **Article 2**.

## 📂 Repository Structure
* `/simulations/dag_state_reconciliation/`: The exact `SimPy` discrete-event simulation framework. It executes the $\lambda = 5.2$ Poisson workload and resolves cross-partition conflicts in $\mathcal{O}(n \log n)$ using the Lexicographic Tuple described in the paper.
* `/testbed/dag_dsr_engine/`: Scripts generating the 52 KB asynchronous notarization payloads and empirical hardware logs comparing DAG-DSR against an Apache CouchDB baseline.
* `/manuscript_figures/`: High-resolution original figures utilized in the final IEEE manuscript.

---

## 🛠️ Hardware Testbed Prototype and Empirical Validation

To move beyond stochastic `SimPy` outcomes and bridge the gap to physical deployment, we constructed a realistic hardware testbed. This validates the execution feasibility of the DAG-DSR algorithm and Cryptographic Notarization under strict rural energy and computational constraints.

### Testbed Architecture & Bill of Materials

To guarantee exact physical reproducibility, the hardware architecture is strictly divided into three operational zones.

| Component | Function in Architecture |
| :--- | :--- |
| **Raspberry Pi 4 Model B (4GB)** | L2 Sequencer (CPU Compute, Python Daemon, VDF) |
| **High-Endurance 64GB MicroSD** | Immutable Physical Storage for Local DAG |
| **USB HSM / Smart Card Reader** | Cryptographic Enclave for Secure ECDSA Signing |
| **Network Bridge (Linux Router)** | Network Constraint Emulator (tc/netem for 2G/Edge) |
| **x86_64 Mini-Server (16GB RAM)** | L1 Mainnet (DSR Engine, TrueNAS, ZFS Pool) |

#### 1) Layer 2: Constrained Rural Edge (L2 Sequencer)
* **Compute Node:** A Raspberry Pi 4 Model B operating on a constrained 5V/3A power budget, representative of a solar-backed deployment.
* **Cryptographic Enclave (HSM):** A secure USB authenticator configured for ECDSA `secp256k1` signing to physically isolate private keys from the primary CPU.
* **Local State Storage:** A high-endurance 64GB MicroSD card acting as the physical repository for the local DAG.
* **Logical Execution:** A Python 3.9 daemon computing the Wesolowski VDF (RSA-2048 modulus) and executing SHA-256 Merkle tree generation natively on the ARM CPU to capture true hardware latency.

#### 2) Network Constraint Emulator (The Liveness Trap)
* **Infrastructure:** A transparent Linux-based network bridge utilizing the native Traffic Control (`tc`) utility with the `netem` module.
* **Constraint Injection:** Bandwidth is limited to ~250 kbps with artificial latency inflation (400 ± 50 ms). A Markov chain script actively injects a 60% packet drop rate or toggles the interface down to simulate the $A=0.4$ blackout profile.

#### 3) Layer 1: Centralized Government Datacenter (National Mainnet)
* **Compute and Storage:** An enterprise-grade x86_64 server utilizing a TrueNAS Core architecture. The ZFS (Zettabyte File System) pools natively provide the cryptographic data integrity and snapshotting required for the global immutable state.
* **Logical Execution:** A persistent listener daemon utilizing `NetworkX` to ingest the 52 KB asynchronous payloads, perform the $\mathcal{O}(1)$ VDF verification, and execute the $\mathcal{O}(n \log n)$ Deterministic State Reconciliation (DSR).

### Summary of Execution Flow
During the testbed evaluation, the emulator severs connectivity to force the L2 Sequencer into offline mode. The L2 daemon ingests synthetic JSON transactions, signs them via the HSM, computes the VDF locking delay, and constructs the Merkle root on the SD card. Upon network restoration, the L2 daemon transmits the 52 KB payload over the constrained connection. The L1 server ingests the batch, sorts the conflicts deterministically, and logs the physical execution times to generate the performance metrics.

---

## 🚀 Reproducibility
As per the Appendix, the stochastic partition model is explicitly fixed with `numpy.random.seed(42)`. To execute the SimPy DAG-DSR engine:
```bash
cd simulations/dag_state_reconciliation/
python3 simulate_dag_dsr_simpy.py
