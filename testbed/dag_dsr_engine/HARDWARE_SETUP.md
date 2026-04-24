# 🛠️ Hardware Testbed & Emulation Guide (Article 2)

This document provides the exact physical specifications and network emulation commands to verify the DAG-DSR architecture.

## 1. Emulating the "Liveness Trap"
To reproduce the **Gilbert-Elliott 2G/Edge profile ($A=0.4$)** used in the manuscript, we utilized Linux Traffic Control (`tc`) between the L2 Edge and L1 Mainnet:
```bash
sudo tc qdisc add dev eth0 root netem delay 400ms 50ms loss 60% rate 250kbit
