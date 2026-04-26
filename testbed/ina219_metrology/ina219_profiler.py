#!/usr/bin/env python3
import time
import numpy as np
import pandas as pd
from ina219 import INA219
from ina219 import DeviceRangeError

# ==========================================
# 1. INA219 HARDWARE CONFIGURATION
# ==========================================
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.4  

def initialize_sensor():
    """Configures the INA219 sensor based on the strict DSR methodology."""
    ina = INA219(SHUNT_OHMS, max_expected_amps=MAX_EXPECTED_AMPS, address=0x40)
    ina.configure(voltage_range=ina.RANGE_16V,
                  gain=ina.GAIN_1_40MV,
                  bus_adc=ina.ADC_128SAMP,
                  shunt_adc=ina.ADC_128SAMP)
    return ina

# ==========================================
# 2. DIFFERENTIAL MEASUREMENT PROTOCOL
# ==========================================
def capture_power_cycles(ina, cycles=1000):
    """Captures N power measurements and returns the array in milliwatts."""
    readings_mw = []
    for i in range(cycles):
        try:
            readings_mw.append(ina.power())
        except DeviceRangeError as e:
            print(f"Overflow Error: {e}")
        time.sleep(0.005) 
    return np.array(readings_mw)

def save_to_csv(filename, data_array, task_name):
    """Saves the raw numpy array to a CSV file for reproducibility."""
    df = pd.DataFrame({f'{task_name}_Power_mW': data_array})
    df.to_csv(filename, index_label='Sample_ID')
    print(f"Saved raw trace to {filename}")

def main():
    print("Initializing INA219 High-Precision Profiler...")
    ina = initialize_sensor()
    
    # --- STEP 1: MEASURE IDLE BASELINE ---
    print("\n[STEP 1] Measuring Idle Baseline (P_idle) over 1,000 cycles...")
    time.sleep(2)
    idle_readings = capture_power_cycles(ina, cycles=1000)
    p_idle_mean = np.mean(idle_readings)
    p_idle_std = np.std(idle_readings)
    print(f"P_idle Mean: {p_idle_mean:.2f} mW (σ = {p_idle_std:.2f})")
    
    # Save Idle CSV
    save_to_csv('raw_trace_idle.csv', idle_readings, 'Idle')
    
    # --- STEP 2: MEASURE TASK EXECUTION ---
    print("\n[STEP 2] Ready to measure task (P_task).")
    input("Press ENTER immediately before triggering the INT8 Inference/Task...")
    
    task_readings = capture_power_cycles(ina, cycles=1000)
    p_task_mean = np.mean(task_readings)
    p_task_std = np.std(task_readings)
    print(f"P_task Mean: {p_task_mean:.2f} mW (σ = {p_task_std:.2f})")
    
    # Save Task CSV
    save_to_csv('raw_trace_int8_inference.csv', task_readings, 'INT8_Inference')
    
    # --- STEP 3: DIFFERENTIAL CALCULATION ---
    delta_p = p_task_mean - p_idle_mean
    combined_std = np.sqrt(p_idle_std**2 + p_task_std**2)
    
    print("\n==========================================")
    print("FINAL EMPIRICAL METRICS (Paper Table IV)")
    print("==========================================")
    print(f"Differential Overhead (ΔP):  {delta_p:.2f} mW")
    print(f"Statistical Variance (σ):    ± {combined_std:.2f} mW")
    print("==========================================")

if __name_
_ == "__main__":
    main()
