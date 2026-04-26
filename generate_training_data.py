#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd

# =====================================================================
# DATASET GENERATOR FOR EDGE-DRL ENVIRONMENT (ARTICLE 3)
# =====================================================================
# Generates representative traces for Sub-Saharan constraints:
# 1. Solar Irradiance (NASA POWER style) with a 72-hour severe deficit.
# 2. Telecom Quality of Service (ART style) with ~40% average availability.
# =====================================================================

np.random.seed(42) # For reproducibility
HOURS_IN_MONTH = 24 * 30

def generate_solar_data():
    """Generates diurnal solar irradiance (W/m2) with a 72-hour deficit."""
    time_index = np.arange(HOURS_IN_MONTH)
    irradiance = np.zeros(HOURS_IN_MONTH)
    
    for h in time_index:
        hour_of_day = h % 24
        # Sunlight roughly between 06:00 and 18:00
        if 6 <= hour_of_day <= 18:
            # Sine wave to simulate the sun rising and setting
            base_peak = np.random.normal(800, 50) # Normal day peak ~800 W/m2
            
            # Apply 72-hour severe solar deficit (Days 10 to 12)
            if 240 <= h < 312:
                base_peak = np.random.normal(150, 30) # Heavy rain/cloud cover
                
            # Calculate hourly irradiance
            rad = (hour_of_day - 6) / 12.0 * np.pi
            irradiance[h] = max(0, base_peak * np.sin(rad))
            
    df = pd.DataFrame({
        'Hour': time_index,
        'Irradiance_W_m2': np.round(irradiance, 2)
    })
    
    # Save to the specific data folder
    os.makedirs('data/nasa_power_solar', exist_ok=True)
    df.to_csv('data/nasa_power_solar/adamawa_solar_trace_30days.csv', index=False)
    print("Saved Solar Data: data/nasa_power_solar/adamawa_solar_trace_30days.csv")

def generate_telecom_data():
    """Generates telecom link quality using a Gilbert-Elliott model (~40% availability)."""
    # State 1: Good (LQE ~ 80-100%), State 0: Bad/Outage (LQE ~ 0-10%)
    # Probabilities to achieve long outages and ~40% overall uptime
    p_good_to_bad = 0.15 
    p_bad_to_good = 0.10
    
    states = np.zeros(HOURS_IN_MONTH)
    lqe = np.zeros(HOURS_IN_MONTH)
    
    # Initial state
    current_state = 0 
    
    for h in range(HOURS_IN_MONTH):
        if current_state == 1:
            if np.random.rand() < p_good_to_bad:
                current_state = 0
            lqe[h] = np.random.uniform(75, 100) # High quality connection
        else:
            if np.random.rand() < p_bad_to_good:
                current_state = 1
            lqe[h] = np.random.uniform(0, 15) # Phantom connection / congestion
            
        states[h] = current_state

    df = pd.DataFrame({
        'Hour': np.arange(HOURS_IN_MONTH),
        'Network_State_Binary': states.astype(int),
        'Link_Quality_Estimate_Pct': np.round(lqe, 2)
    })
    
    # Save to the specific data folder
    os.makedirs('data/art_telecom_qos', exist_ok=True)
    df.to_csv('data/art_telecom_qos/rural_lqe_trace_30days.csv', index=False)
    print(f"Saved Telecom Data: data/art_telecom_qos/rural_lqe_trace_30days.csv (Avg Uptime: {states.mean()*100:.1f}%)")

if __name__ == "__main__":
    print("Generating representative dataset traces...")
    generate_solar_data()
    generate_telecom_data()
    print("Done!")
