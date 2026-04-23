# Article 1: Limitations of Layer 2 Blockchain Solutions

This branch contains the mathematical modeling and simulation artifacts for **Article 1**.

## 📂 Repository Structure (Article 1)
* `/simulations/monte_carlo_security/`: Monte Carlo stochastic models evaluating Optimistic Rollup security degradation under Sub-Saharan grid variance.
* `/simulations/energy_wall_analysis/`: Empirical modeling of ZK-SNARK energy consumption limits on edge devices.

## 🚀 Reproducibility
To regenerate the IEEE-formatted graphs (Figures 3, 4, 6, and 9) demonstrating the "Tetralemma":
```bash
cd simulations/monte_carlo_security/
pip install matplotlib numpy
python3 generate_article1_figures.py
