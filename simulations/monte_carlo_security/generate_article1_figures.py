#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os

# =====================================================================
# REPRODUCIBILITY SCRIPT: ARTICLE 1 (TETRALEMMA & LIMITATIONS)
# Generates: Monte Carlo Security Sweep, Sensitivity Analysis, 
# Energy Wall limit, and Resilience Ratio
# =====================================================================

np.random.seed(42) # Deterministic seed for reviewers

# INCREASED FONT SIZES PER IEEE REVIEWER REQUEST
plt.rcParams.update({
    'font.size': 14, 
    'axes.labelsize': 18,     # Significantly increased x/y label size
    'axes.titlesize': 16,     # Title size increased
    'xtick.labelsize': 14,    # Axis tick numbers increased
    'ytick.labelsize': 14,    # Axis tick numbers increased
    'legend.fontsize': 12, 
    'lines.linewidth': 2.5,   # Thicker lines for visibility
    'figure.dpi': 300
})

OUTPUT_DIR = "generated_figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_sim_a_monte_carlo():
    """Monte Carlo Security Degradation & Mitigation Sweep"""
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

    plt.figure(figsize=(8, 6))
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

    plt.xlabel('Average Network Availability ($A$)', fontweight='bold')
    plt.ylabel('Probability of Detection ($P_{detect}$)', fontweight='bold')
    plt.title('Monte Carlo Security Sweep') 
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sim_security_sweep.png")
    print("Generated: sim_security_sweep.png")

def plot_sensitivity_analysis():
    """Sensitivity Analysis S = dP/dA"""
    A_values = np.linspace(0.0, 1.0, 100)
    N = 10
    S = N * (1 - A_values)**(N-1)
    
    plt.figure(figsize=(8, 6))
    plt.plot(A_values, S, color='crimson', linewidth=3.0)
    plt.fill_between(A_values, 0, S, where=(A_values >= 0.2) & (A_values <= 0.5), color='red', alpha=0.15, label='Unstable Equilibrium Zone')
    
    plt.xlabel('Average Network Availability ($A$)', fontweight='bold')
    plt.ylabel('Sensitivity ($S = dP/dA$)', fontweight='bold')
    plt.title('Sensitivity Analysis of Fraud Detection') 
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sim_sensitivity.png")
    print("Generated: sim_sensitivity.png")

def plot_energy_wall():
    """The Energy Wall for ZK-Rollups"""
    transactions = np.linspace(0, 12000, 100)
    
    E_current = 1.0 # mWh/tx
    E_target = 0.4  # mWh/tx
    B_daily_mWh = 5.0 * 1000 # 5 Wh converted to mWh
    
    consumption_current = transactions * E_current
    consumption_target = transactions * E_target
    
    plt.figure(figsize=(8, 6))
    plt.plot(transactions, consumption_current, color='red', linewidth=3.0, label='Current ZK implementations ($1.0$ mWh/tx)')
    plt.plot(transactions, consumption_target, color='green', linewidth=3.0, label='Optimized Target ($0.4$ mWh/tx)')
    plt.axhline(B_daily_mWh, color='black', linestyle='--', linewidth=2.5, label='Solar Battery Limit ($B_{daily} = 5$ Wh)')
    
    plt.scatter([5000], [5000], color='darkred', zorder=5, s=80)
    plt.annotate('Energy Wall Breach', xy=(5000, 5000), xytext=(2000, 7000),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=2), fontsize=12, fontweight='bold')
                 
    plt.axvline(10000, color='gray', linestyle=':', label='Target Daily Volume')
    
    plt.xlabel('Daily Transaction Volume', fontweight='bold')
    plt.ylabel('Cumulative Energy Consumption (mWh)', fontweight='bold')
    plt.title('The ZK-Rollup Energy Wall') 
    plt.legend(loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/sim_energy_wall.png")
    print("Generated: sim_energy_wall.png")

def plot_resilience_ratio():
    """Resilience Ratio (Phi) vs Technical Uptime (rho)"""
    rho_values = np.linspace(0.0, 1.0, 100)
    
    # Literacy (L) and Regulatory friction (U) constants
    L_urban, U_urban = 0.7, 0.6
    Phi_urban = (L_urban * rho_values) / U_urban
    
    L_rural, U_rural = 0.3, 0.6
    Phi_rural = (L_rural * rho_values) / U_rural
    
    plt.figure(figsize=(8, 6))
    
    # Plotting the lines
    plt.plot(rho_values, Phi_urban, color='#4682b4', linewidth=3.0, label='Urban Profile (Yaoundé): $L=0.7$')
    plt.plot(rho_values, Phi_rural, color='#d62728', linewidth=3.0, label='Rural Profile (Mokolo): $L=0.3$')
    
    # Heeks Failure Zone
    plt.axhline(0.2, color='darkred', linestyle='--', linewidth=2.5, label=r'Heeks Failure Line ($\Phi < 0.2$)')
    plt.fill_between(rho_values, 0, 0.2, color='red', alpha=0.1)
    
    # Text annotation to make the graph more informative (addressing reviewer's concern)
    plt.text(0.5, 0.1, 'HIGH PROBABILITY OF ABANDONMENT', color='darkred', 
             fontsize=12, fontweight='bold', ha='center', va='center', alpha=0.7)
    
    # Scatter points for typical operating regimes
    plt.scatter([0.85], [(0.7*0.85)/0.6], color='#4682b4', s=100, zorder=5) 
    plt.scatter([0.40], [(0.3*0.40)/0.6], color='#d62728', s=100, zorder=5) 
    
    # Annotate the specific rural failure point
    plt.annotate('Rural Node\nDrops below survival', xy=(0.40, 0.2), xytext=(0.45, 0.3),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                 fontsize=11, fontweight='bold')

    # Formatting
    plt.xlabel(r'Technical Uptime Reliability ($\rho$)', fontweight='bold')
    plt.ylabel(r'Resilience Ratio ($\Phi$)', fontweight='bold')
    plt.title('System Viability Thresholds')
    
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.02, 0.55)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left', fontsize=11)
    plt.tight_layout()
    
    plt.savefig(f"{OUTPUT_DIR}/sim_resilience.png")
    print("Generated: sim_resilience.png")

if __name__ == "__main__":
    print("Generating updated statistical graphs for Article 1...")
    plot_sim_a_monte_carlo()
    plot_sensitivity_analysis()
    plot_energy_wall()
    plot_resilience_ratio()
    print(f"All figures successfully saved to the '{OUTPUT_DIR}/' directory.")
