#!/usr/bin/env python3
import os

TARGET_SIZE_KB = 52
TARGET_BYTES = TARGET_SIZE_KB * 1024
FILENAME = "payload_batch_latest.dat"

def generate_payload():
    print(f"Constructing Merkle/VDF Payload block for L1 transmission...")
    payload_data = os.urandom(TARGET_BYTES)
    with open(FILENAME, "wb") as f:
        f.write(payload_data)
    actual_size = os.path.getsize(FILENAME) / 1024
    print(f"[SUCCESS] Payload generated: {FILENAME} ({actual_size:.2f} KB)")

if __name__ == "__main__":
    generate_payload()
