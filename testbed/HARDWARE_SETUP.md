# 🛠️ Hardware Testbed Reproduction Guide (Article 3)

This document provides the exact specifications, wiring diagrams, and OS configurations required to independently verify the empirical power metrics ($\approx 0.62$ mW INT8 inference overhead) reported in the manuscript.

---

## 1. Raspberry Pi OS Environment & Image Hash
To ensure the baseline system power ($E_{sys}$) is reproducible, we utilize a headless (no GUI) lightweight OS. The exact image used for our testbed is tracked via its SHA-256 hash.

* **OS Version:** Raspberry Pi OS (Legacy, 64-bit) Lite - Debian Bookworm
* **Kernel:** Linux 6.6.20-v8+
* **Target Hardware:** Raspberry Pi 4 Model B (4GB RAM)
* **SHA-256 Image Hash:** `1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b` *(Note: This is a placeholder for your actual hash)*

> **Justification:** The "Lite" version strictly eliminates background desktop environment processes, ensuring that our idle power baseline ($\sim 1850$ mW) is stable and isolated from graphical processing noise.

---

## 2. I2C Hardware Wiring Diagram
The testbed utilizes an **INA219** High-Side DC Current Sensor and an **ATECC608A** Hardware Security Module (HSM). Both components share the Raspberry Pi's primary I2C bus (`I2C-1`).

### Logic & Sensor Wiring (I2C Bus)
| Raspberry Pi 4 Pin | INA219 Sensor Pin | ATECC608A (HSM) Pin | Function |
| :--- | :--- | :--- | :--- |
| **Pin 1 (3.3V)** | VCC | VCC | Logic Power Supply |
| **Pin 6 (GND)** | GND | GND | Common Ground |
| **Pin 3 (GPIO 2)** | SDA | SDA | I2C Data Line |
| **Pin 5 (GPIO 3)** | SCL | SCL | I2C Clock Line |

### INA219 Differential Power Wiring (Load Sensing)
To accurately measure the power overhead of the CPU computing the INT8 DRL inference and the cryptographic primitives, the INA219 shunt resistor ($0.1\Omega$) is placed inline with the 5V power supply.

* **VIN+**: Connected to the positive terminal of the main power source (e.g., PiJuice 5V output).
* **VIN-**: Connected to the Raspberry Pi 5V Input (Physical Pin 2 or 4).

---

## 3. Metrology Scripts & Verification
To reproduce the differential measurement methodology described in the paper:
1. Navigate to the metrology folder: `cd ina219_metrology/`
2. Install the driver: `pip install pi-ina219 numpy pandas`
3. Run the profiler: `python3 ina219_profiler.py`

The script configures the INA219 with a PGA gain of `/1` and `128-sample` hardware averaging, captures $N=1,000$ baseline cycles, and compares them against the active task cycles to output the differential overhead $\Delta P$. The raw outputs are exported as `.csv` traces in the same directory.
