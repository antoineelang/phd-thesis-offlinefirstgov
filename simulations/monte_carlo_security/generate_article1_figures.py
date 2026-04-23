#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os

# =====================================================================
# REPRODUCIBILITY SCRIPT: ARTICLE 1 (TETRALEMMA & LIMITATIONS)
# Generates: Monte Carlo Security Sweep, Sensitivity Analysis, 
# Energy Wall limit, and Resilience Ratio (Phi)
# =====================================================================

np.random.seed(42) # Deterministic seed for reviewers

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 14,
    'legend.fontsize': 10, 'lines.linewidth': 2, 'figure.dpi': 300
})

OUTPUT_DIR = "generated_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_sim_a_monte_carlo():
    """Fig 3: Monte Carlo Security Degradation & Mitigation Sweep"""
    A_values = np.linspace(0.1, 1.0, 50)
    N = 10
    rho_geo = 0.8
    sigma = 0.10
    M = 1000 # Monte Carlo Iterations
    
    k_values = [1.0, 1.5, 2.0, 3.0, 5.0]
    results = {k: [] for k in k_values}
    variances = []

    for A in A_values:
        p_h = np.random.normal(A, sigma, (M, N))
        p_h = np.clip(p_h, 0, 1) 
        
        product_term = np.prod(1 - p_h, axis=1)
        
        for k in k_values:
            P_mitig = 1 - (product_term ** (k * rho_geo))
            results[k].append(np.mean(P_mitig))
            if k == 1.0: 
                variances.append(np.std(P_mitig))

    plt.figure(figsize=(8, 5))
    A_vals = np.array(A_values)
    
    base_mean = np.array(results[1.0])
    base_std = np.array(variances)
    plt.plot(A_vals, base_mean, 'k--', label='Baseline (k=1)')
    plt.fill_between(A_vals, np.clip(base_mean-base_std, 0, 1), np.clip(base_mean+base_std, 0, 1), color='gray', alpha=0.2, label=r'$\pm 1\sigma$ Variance')
    
    colors = ['orange', 'green', 'blue', 'purple']
    for idx, k in enumerate(k_values[1:]):
        plt.plot(A_vals, results[k], color=colors[idx], label=f'Delayed Slashing (k={k})')
        
    plt.axhline(0.99, color='red', linestyle=':', label='Security Threshold (0.99)')
    plt.axvline(0.4, color='darkred', linestyle='-.', alpha=0.5, label=r'Typical Rural $A \approx 0.4$')

    plt.xlabel('Average Network Availability ($A$)')
    plt.ylabel('Probability of Detection ($P_{detect}$)')
    plt.title('Simulation A: Monte Carlo Security Sweep')
    plt.legend(loc='lower right', fontsize=9)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sim_security_sweep.png")
    print("Generated: sim_security_sweep.png")

def plot_sensitivity_analysis():
    """Fig 4: Sensitivity Analysis S = dP/dA"""
    A_values = np.linspace(0.0, 1.0, 100)
    N = 10
    S = N * (1 - A_values)**(N-1)
    
    plt.figure(figsize=(7, 5))
    plt.plot(A_values, S, color='crimson', linewidth=2.5)
    plt.fill_between(A_values, 0, S, where=(A_values >= 0.2) & (A_values <= 0.5), color='red', alpha=0.15, label='Unstable Equilibrium Zone')
    
    plt.xlabel('Average Network Availability ($A$)')
    plt.ylabel('Sensitivity ($S = dP/dA$)')
    plt.title('Sensitivity Analysis of Fraud Detection')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sim_sensitivity.png")
    print("Generated: sim_sensitivity.png")

def plot_energy_wall():
    """Fig 6: The Energy Wall for ZK-Rollups"""
    transactions = np.linspace(0, 12000, 100)
    
    E_current = 1.0 # mWh/tx
    E_target = 0.4  # mWh/tx
    B_daily_mWh = 5.0 * 1000 # 5 Wh converted to mWh
    
    consumption_current = transactions * E_current
    consumption_target = transactions * E_target
    
    plt.figure(figsize=(8, 5))
    plt.plot(transactions, consumption_current, color='red', label='Current ZK implementations ($1.0$ mWh/tx)')
    plt.plot(transactions, consumption_target, color='green', label='Optimized Target ($0.4$ mWh/tx)')
    plt.axhline(B_daily_mWh, color='black', linestyle='--', linewidth=2, label='Solar Battery Limit ($B_{daily} = 5$ Wh)')
    
    plt.scatter([5000], [5000], color='darkred', zorder=5)
    plt.annotate('Energy Wall Breach', xy=(5000, 5000), xytext=(2000, 6000),
                 arrowprops=dict(facecolor='black', shrink=0.05))
                 
    plt.axvline(10000, color='gray', linestyle=':', label='Target Daily Volume')
    
    plt.xlabel('Daily Transaction Volume')
    plt.ylabel('Cumulative Energy Consumption (mWh)')
    plt.title('Simulation B: The ZK-Rollup Energy Wall')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sim_energy_wall.png")
    print("Generated: sim_energy_wall.png")

def plot_resilience_ratio():
    """Fig 9: Resilience Ratio (Phi) vs Technical Uptime (rho)"""
    rho_values = np.linspace(0.1, 1.0, 100)
    
    L_urban, U_urban = 0.7, 0.6
    Phi_urban = (L_urban * rho_values) / U_urban
    
    L_rural, U_rural = 0.3, 0.6
    Phi_rural = (L_rural * rho_values) / U_rural
    
    plt.figure(figsize=(8, 5))
    plt.plot(rho_values, Phi_urban, color='blue', label='Urban Profile (Yaoundé): $L=0.7$')
    plt.plot(rho_values, Phi_rural, color='orange', label='Rural Profile (Mokolo): $L=0.3$')
    
    plt.axhline(0.2, color='red', linestyle='--', label=r'Heeks Failure Line ($\Phi < 0.2$)')
    plt.fill_between(rho_values, 0, 0.2, color='red', alpha=0.1, label='Critical Failure Zone')
    
    plt.scatter([0.85], [(0.7*0.85)/0.6], color='darkblue') 
    plt.scatter([0.35], [(0.3*0.35)/0.6], color='darkorange') 
    
    plt.xlabel(r'Technical Uptime ($\rho$)')
    plt.ylabel(r'Resilience Ratio ($\Phi$)')
    plt.title('Simulation C: Socio-Technical Resilience')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sim_resilience.png")
    print("Generated: sim_resilience.png")

if __name__ == "__main__":
    print("Generating statistical graphs for Article 1...")
    plot_sim_a_monte_carlo()
    plot_sensitivity_analysis()
    plot_energy_wall()
    plot_resilience_ratio()
    print(f"All figures successfully saved to the '{OUTPUT_DIR}/' directory.")
