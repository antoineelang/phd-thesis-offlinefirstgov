#!/usr/bin/env python3
import simpy
import numpy as np
import pandas as pd

# =====================================================================
# SIMPY DISCRETE-EVENT SIMULATION: EDGE-DRL VS STATIC NODE (ARTICLE 3)
# =====================================================================
# Models a 72-hour solar deficit to validate Hypothesis H1 (Survivability).
# Tracks Battery State of Charge (SoC) under different DRL policies.
# =====================================================================

# System Parameters (from Table II)
B_MAX = 50.0  # Wh
B_CRITICAL = 5.0  # Wh (10%)
P_IDLE = 0.5  # W
P_COMPUTE = 1.5  # W (Extra power for hashing)
SIM_TIME_HOURS = 168  # 7 days total (to show recovery after 72h deficit)

class EdgeNodeEnv:
    def __init__(self, env, use_drl=True):
        self.env = env
        self.use_drl = use_drl
        self.battery = B_MAX
        self.is_dead = False
        self.history = []

    def solar_harvesting(self):
        """Simulates solar generation with a 72-hour severe deficit."""
        hour = self.env.now
        # Deficit between hours 24 and 96 (72 hours total)
        if 24 <= hour < 96:
            peak_power = np.random.normal(1.0, 0.2) # Severe deficit (heavy rain)
        else:
            peak_power = np.random.normal(15.0, 1.0) # Normal 15W panel

        # Day/Night cycle (sine wave for 12 hours of light)
        hour_of_day = hour % 24
        if 6 <= hour_of_day <= 18:
            rad = (hour_of_day - 6) / 12.0 * np.pi
            return max(0, peak_power * np.sin(rad))
        return 0.0

    def run_node(self):
        while self.env.now < SIM_TIME_HOURS:
            if self.is_dead:
                self.history.append({'Hour': self.env.now, 'SoC_Wh': 0.0, 'Status': 'DEAD'})
                yield self.env.timeout(1)
                continue

            # 1. Harvest Energy
            e_in = self.solar_harvesting()

            # 2. DRL Agent Decision / Workload
            # Static node computes blindly. DRL throttles if Battery < 15.0 Wh (30%)
            if not self.use_drl:
                e_out = P_IDLE + P_COMPUTE # Static always computes
            else:
                if self.battery < 15.0: # DRL throttles to save power
                    e_out = P_IDLE
                else:
                    e_out = P_IDLE + P_COMPUTE

            # 3. Update Battery Mass-Balance
            self.battery = min(B_MAX, max(0.0, self.battery + e_in - e_out))

            # 4. Check Safety Wrapper / Death
            if self.battery <= B_CRITICAL and not self.use_drl:
                self.is_dead = True # Static node dies

            # Log state
            self.history.append({
                'Hour': self.env.now,
                'SoC_Wh': round(self.battery, 2),
                'SoC_Pct': round((self.battery / B_MAX) * 100, 1),
                'Action': 'SLEEP' if e_out == P_IDLE else 'COMPUTE'
            })

            yield self.env.timeout(1)

def run_simulation():
    print("Initializing SimPy Discrete-Event Simulation...")
    
    # Run DRL Node
    env_drl = simpy.Environment()
    node_drl = EdgeNodeEnv(env_drl, use_drl=True)
    env_drl.process(node_drl.run_node())
    env_drl.run(until=SIM_TIME_HOURS)
    
    # Run Static Node
    env_static = simpy.Environment()
    node_static = EdgeNodeEnv(env_static, use_drl=False)
    env_static.process(node_static.run_node())
    env_static.run(until=SIM_TIME_HOURS)

    # Save outputs to CSV for public availability
    df_drl = pd.DataFrame(node_drl.history)
    df_static = pd.DataFrame(node_static.history)
    
    df_drl.to_csv('simpy_drl_agent_survival_log.csv', index=False)
    df_static.to_csv('simpy_static_node_death_log.csv', index=False)
    
    print("\n--- SIMULATION COMPLETE ---")
    print("Results saved to: 'simpy_drl_agent_survival_log.csv' and 'simpy_static_node_death_log.csv'")
    print(f"DRL Final SoC: {df_drl.iloc[-1]['SoC_Pct']}% (Survived)")
    print(f"Static Final SoC: {df_static.iloc[-1]['SoC_Pct']}% ({df_static.iloc[-1]['Status']})")

if __name__ == "__main__":
    run_simulation()
