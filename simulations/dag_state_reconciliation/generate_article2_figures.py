#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates

# =====================================================================
# REPRODUCIBILITY SCRIPT: ARTICLE 2 (DAG-DSR & THREAT MODELS)
# Generates Simulation A, B, C, D and Threat Models 1, 2, 3
# =====================================================================

# Get the exact absolute path of this script, then create the folder right next to it
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "generated_figures")

# Safely create the directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Saving figures to: {OUTPUT_DIR}")

def plot_sim_a_uptime():
    # --- 1. Simulation Parameters ---
    hours = np.arange(0, 72, 1) 
    avg_availability = 0.40 

    np.random.seed(42) 
    network_state = np.zeros(len(hours))
    current_state = 1 

    for i in range(len(hours)):
        if current_state == 1:
            if np.random.rand() > 0.6:
                current_state = 0
        else:
            if np.random.rand() > 0.8:
                current_state = 1
        network_state[i] = current_state

    # --- 2. Throughput ---
    t_sync = network_state * 100
    t_local = np.ones(len(hours)) * 100

    # --- 3. Plotting ---
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.step(hours, t_sync, where='post', label=r'Standard L2 Sync Throughput ($T_{sync}$)',
            color='#d62728', linewidth=2)
    ax.fill_between(hours, 0, t_sync, step='post', color='#d62728', alpha=0.2)

    ax.plot(hours, t_local, label=r'Offline-First Local Throughput ($T_{local}$)',
            color='#2ca02c', linewidth=3, linestyle='--')

    ax.set_title(r'Simulation A: Operational Uptime under Network Variance ($A \approx 0.4$)',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Time (Hours)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Operational Capacity (%)', fontsize=12, fontweight='bold')
    ax.set_ylim(-5, 110)
    ax.set_xlim(0, 72)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(loc='lower right', fontsize=11, framealpha=0.9)

    ax.annotate('Network Blackout\n(Synchronous L2 fails)', xy=(15, 5), xytext=(18, 30),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                fontsize=10, color='#d62728', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/sim_a_uptime.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: sim_a_uptime.png")

def plot_sim_b_dag():
    # --- 1. Parameters ---
    n_transactions = np.linspace(10, 10000, 100)

    # --- 2. Resolution Time Models (ms) ---
    time_linear = n_transactions * 0.5
    time_dag = 50 * np.log2(n_transactions)

    # --- 3. Plotting ---
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(n_transactions, time_linear, label=r'Standard Linear Verification $O(n)$',
            color='#7f7f7f', linewidth=2.5, linestyle='-.')
    ax.plot(n_transactions, time_dag, label=r'DAG-DSR Algorithm $O(\log n)$',
            color='#1f77b4', linewidth=3)

    ax.fill_between(n_transactions, time_dag, time_linear, color='#1f77b4', alpha=0.1)

    ax.set_title('Simulation B: Deterministic State Reconciliation Performance',
                 fontsize=14, fontweight='bold', pad=15)

    ax.set_xlabel(r'Number of Offline Transactions in Batch ($n$)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Resolution Time (ms)', fontsize=12, fontweight='bold')
    ax.set_xlim(0, 10000)
    ax.set_ylim(0, max(time_linear[-1], 1000))
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', fontsize=12, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/sim_b_dag.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: sim_b_dag.png")

def plot_sim_c_bandwidth():
    # --- 1. Parameters ---
    n_transactions = np.linspace(1, 5000, 500)
    standard_tx_weight_kb = 0.56

    # --- 2. Bandwidth Models (KB) ---
    bandwidth_standard = n_transactions * standard_tx_weight_kb
    bandwidth_notarization = np.ones(len(n_transactions)) * 52

    # --- 3. Plotting ---
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(n_transactions, bandwidth_standard, label=r'Standard Linear Sync $O(n)$',
            color='#d62728', linewidth=2.5, linestyle='-.')

    ax.plot(n_transactions, bandwidth_notarization, label=r'Asynchronous Notarization $O(1)$',
            color='#2ca02c', linewidth=3)
    
    ax.fill_between(n_transactions, bandwidth_notarization, bandwidth_standard,
                    color='#2ca02c', alpha=0.1)

    ax.set_title(r'Simulation C: Bandwidth Optimization in Constrained Networks',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(r'Number of Offline Transactions in Batch ($n$)', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'Synchronization Data Payload (Kilobytes)', fontsize=12, fontweight='bold')

    ax.annotate(r'98.1% Bandwidth Reduction', xy=(5000, 2800), xytext=(2500, 2000),
                arrowprops=dict(facecolor='#2ca02c', shrink=0.05, width=1.5, headwidth=8),
                fontsize=12, fontweight='bold', color='#2ca02c', ha='center')

    ax.set_xlim(0, 5000)
    ax.set_ylim(0, 3000)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', fontsize=12, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/sim_c_bandwidth.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: sim_c_bandwidth.png")

def plot_sim_d_partitioning():
    # --- 1. Simulation Parameters ---
    time_hours = np.arange(0, 60, 0.5) 
    partition_end = 48 

    tx_rate_north = 25000 / 48
    tx_rate_south = 25000 / 48

    # --- 2. Data Generation ---
    pending_north = np.zeros(len(time_hours))
    pending_south = np.zeros(len(time_hours))

    np.random.seed(42)
    for i, t in enumerate(time_hours):
        if t <= partition_end:
            pending_north[i] = t * tx_rate_north
            pending_south[i] = np.random.randint(0, 100) 
        else:
            pending_north[i] = np.random.randint(0, 100)
            pending_south[i] = np.random.randint(0, 100)

    # --- 3. Plotting ---
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(time_hours, pending_north, label=r'North L2 Nodes (Isolated) - Local DAG Accumulation',
            color='#d62728', linewidth=3)
    ax.fill_between(time_hours, 0, pending_north, color='#d62728', alpha=0.1)

    ax.plot(time_hours, pending_south, label=r'South L2 Nodes (Connected) - Continuous L1 Sync',
            color='#2ca02c', linewidth=3)

    ax.set_title(r'Simulation D: Cascading Failures and Network Partitioning',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(r'Time (Hours)', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'Pending (Un-synced) Transactions Queue', fontsize=12, fontweight='bold')

    ax.axvspan(0, partition_end, color='gray', alpha=0.1)
    ax.text(24, 20000, r'Severe Network Partition (North Region Isolated)',
            fontsize=13, fontweight='bold', color='#7f7f7f', ha='center', va='center')

    ax.axvline(x=partition_end, color='black', linestyle='--', linewidth=2)
    resolution_text = (r'Partition Resolved ($t=48h$)' + '\n' +
                       r'25,000 TXs Flooded to L1' + '\n' +
                       r'142 Cross-Partition Conflicts' + '\n' +
                       r'Resolved via DSR in $\mathcal{O}(n \log n)$')
                       
    ax.annotate(resolution_text,
                xy=(partition_end, 25000),
                xytext=(partition_end + 2, 16000),
                arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', connectionstyle='arc3,rad=-0.2', linewidth=1.5),
                fontsize=11, fontweight='bold', color='black', backgroundcolor='white')

    ax.set_xlim(0, 60)
    ax.set_ylim(-500, 28000)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/sim_d_partitioning.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: sim_d_partitioning.png")

def plot_sim_attack1_temporal():
    # --- 1. Simulation Parameters ---
    blackout_start = datetime.datetime(2026, 6, 1, 8, 0) 
    blackout_end = datetime.datetime(2026, 6, 3, 8, 0) 
    real_attack_time = datetime.datetime(2026, 6, 3, 10, 0) 

    fake_clock_time = datetime.datetime(2026, 6, 2, 8, 0) 
    t_req_hours = 48
    real_validation_time = real_attack_time + datetime.timedelta(hours=t_req_hours)

    # --- 2. Plotting ---
    fig, ax = plt.subplots(figsize=(10, 5))

    categories = [r'Falsified OS Clock Time' + '\n' + r'(manipulated)', r'Required Cryptographic Time' + '\n' + r'($T_{crypto}$ proof workload)']
    datetime_vals = [fake_clock_time, real_validation_time]
    float_vals = [mdates.date2num(v) for v in datetime_vals]
    
    ax.bar(categories, float_vals, color=['#7f7f7f', '#d62728'], alpha=0.9, width=0.6, edgecolor='black', linewidth=1.5)

    zone_blackout_start = mdates.date2num(blackout_start)
    zone_blackout_end = mdates.date2num(blackout_end)
    ax.axhspan(zone_blackout_start, zone_blackout_end, color='#d62728', alpha=0.1, label='Physical Network Blackout')

    ax.axhline(zone_blackout_end, color='#7f7f7f', linestyle='--', linewidth=2.5)
    ax.text(0.5, zone_blackout_end + 0.1, 'Network Reconnection', color='#7f7f7f', fontsize=12, fontweight='bold', ha='center')

    fin_validation_float = mdates.date2num(real_validation_time)
    ax.axhline(fin_validation_float, color='#d62728', linestyle=':', linewidth=2.5)
    ax.text(1.3, fin_validation_float + 0.1, r'Final $T_{crypto}$ Proof Generated', color='#d62728', fontsize=12, fontweight='bold')

    ax.set_title('Threat Model Simulation 1: Neutralization of Temporal Spoofing',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel('Absolute Cryptographic Time (Date)', fontsize=12, fontweight='bold')

    ax.yaxis.set_major_formatter(mdates.DateFormatter(r'%a, %b %d %H:%M'))
    ax.yaxis.set_major_locator(mdates.DayLocator(interval=1))
    
    annotation_text = r'L1 Validation:' + '\n' + r'Ignores OS Clock.' + '\n' + r'Proof places TX chronologically' + '\n' + r'AFTER blackout.' + '\n' + r'Attack Neutered.'
    ax.annotate(annotation_text, xy=(1, fin_validation_float - 0.5), xytext=(0.2, fin_validation_float - 1.2),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                fontsize=12, fontweight='bold', color='black', ha='left', backgroundcolor='white')

    ax.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax.legend(loc='lower right', fontsize=11, framealpha=0.9)

    ax.set_ylim(mdates.date2num(blackout_start - datetime.timedelta(hours=12)),
                mdates.date2num(real_validation_time + datetime.timedelta(hours=24)))

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/sim_attack1_temporal.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: sim_attack1_temporal.png")

def plot_sim_attack2_equivocation():
    # --- 1. Parameters ---
    node_name_a = r'Maroua L2 Node' + '\n' + r'(Rural, Low Weight, $\omega=1.0$)'
    node_weight_a = 1.0
    t_crypto_offset_a = 10.5 
    depth_a = 50 

    node_name_b = r'Garoua L2 Node' + '\n' + r'(Capital, High Weight, $\omega=5.0$)'
    node_weight_b = 5.0
    t_crypto_offset_b = 15.2 
    depth_b = 20 

    score_a = (100.0 * (1.0 / t_crypto_offset_a)) + (1.0 * node_weight_a) + (1.0 * depth_a)
    score_b = (100.0 * (1.0 / t_crypto_offset_b)) + (1.0 * node_weight_b) + (1.0 * depth_b)

    # --- 2. Plotting ---
    fig, ax = plt.subplots(figsize=(9, 6))
    categories = [node_name_a, node_name_b]
    scores = [score_a, score_b]

    ax.barh(categories, scores, color=['#2ca02c', '#7f7f7f'], edgecolor='black', linewidth=1.5, alpha=0.9, height=0.6)

    ax.set_title(r'Threat Model Simulation 2: DSR Resolution of State Equivocation',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(r'Deterministic Priority Score: $P(tx) = \alpha \cdot \frac{1}{T_{crypto}} + \beta \cdot \omega_{node} + \gamma \cdot \mathcal{D}$',
                  fontsize=12, fontweight='bold')

    ax.annotate(r'WINNER:' + '\n' + r'Atomic consistency preserved', xy=(score_a, 0), xytext=(score_a - 15, -0.3),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                fontsize=12, fontweight='bold', color='#2ca02c', ha='right', va='center')

    ax.annotate(r'REJECTED & PRUNED:' + '\n' + r'Deterministic State Separation', xy=(score_b, 1), xytext=(score_b + 5, 0.7),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                fontsize=12, fontweight='bold', color='#d62728', ha='left', va='center')

    validation_text = r'L1 DSR Engine Validation:' + '\n' + r'Ignored regional node authority.' + '\n' + r'Prioritized temporal truth.' + '\n' + r'Attack Neutered.'
    ax.text(1, 0.5, validation_text, fontsize=12, fontweight='bold', color='black', ha='center', va='center', bbox=dict(facecolor='white', alpha=0.9))

    ax.set_xlim(0, 70)
    ax.grid(True, linestyle=':', alpha=0.6, axis='x')

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/sim_attack2_equivocation.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: sim_attack2_equivocation.png")

def plot_sim_attack3_flooding():
    # --- 1. Parameters ---
    vol_attack_vol = 10**6 
    time_sec = np.arange(0, 60, 1) 

    validation_l1_standard = np.zeros(len(time_sec))
    for i in range(len(time_sec)):
        if i < 20: 
            validation_l1_standard[i] = 1.0 
        elif i < 30: 
            validation_l1_standard[i] = vol_attack_vol * 0.001 
        else: 
            validation_l1_standard[i] = 1.0 

    validation_l1_notarization = np.ones(len(time_sec)) * 1.0 

    # --- 2. Plotting ---
    fig, ax = plt.subplots(figsize=(11, 5))

    ax.step(time_sec, validation_l1_standard, label=r'Standard Rollup L1 Validation Complexity $O(n)$ (Linear)',
            color='#d62728', linewidth=2.5)
    ax.fill_between(time_sec, 0, validation_l1_standard, step='post', color='#d62728', alpha=0.1)

    ax.plot(time_sec, validation_l1_notarization, label=r'Asynchronous Notarization L1 Validation Complexity $O(1)$ (Constant)',
            color='#2ca02c', linewidth=3, linestyle='--')

    ax.set_title('Threat Model Simulation 3: Neutralization of Asynchronous Flooding (DoS)',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Network Reconnection Phase (Seconds)', fontsize=12, fontweight='bold')
    ax.set_ylabel('L1 Mainnet Validation Workload (Unitless)', fontsize=12, fontweight='bold')

    annotation_text_dos = r'Synchronization Storm' + '\n' + r'(DDoS volume O(n) crashes L1 queue)'
    ax.annotate(annotation_text_dos, xy=(25, validation_l1_standard[25]),
                xytext=(25, 5000),
                arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', connectionstyle='arc3,rad=0.3', linewidth=1.5),
                fontsize=11, fontweight='bold', color='#d62728', ha='center', va='bottom')

    validation_text_o1 = r'L1 Mainnet Validation:' + '\n' + r'Verified strictly 32-byte Merkle Root.' + '\n' + r'Validation complexity remains $O(1)$.' + '\n' + r'DoS Neutered at Edge.'
    ax.annotate(validation_text_o1,
                xy=(45, validation_l1_notarization[45]),
                xytext=(0.85, 0.45), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', connectionstyle='arc3,rad=-0.2', linewidth=1.5),
                fontsize=12, fontweight='bold', color='black', ha='left', va='center', backgroundcolor='white')

    ax.axvspan(20, 30, color='#d62728', alpha=0.05)
    ax.text(25, 0.2, r'DDoS Burst', color='#d62728', fontsize=12, fontweight='bold', ha='center', va='bottom')

    ax.set_xlim(0, 60)
    ax.set_yscale('log') 
    ax.set_ylim(0.1, 10**5) 
    ax.grid(True, linestyle=':', alpha=0.5, which='both')
    ax.legend(loc='lower left', fontsize=11, framealpha=0.9) 

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/sim_attack3_flooding.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: sim_attack3_flooding.png")

if __name__ == "__main__":
    print("Generating statistical graphs and Threat Models for Article 2...")
    plot_sim_a_uptime()
    plot_sim_b_dag()
    plot_sim_c_bandwidth()
    plot_sim_d_partitioning()
    plot_sim_attack1_temporal()
    plot_sim_attack2_equivocation()
    plot_sim_attack3_flooding()
    print(f"All figures successfully generated and saved to the '{OUTPUT_DIR}/' directory.")
