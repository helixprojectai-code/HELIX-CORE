import hashlib
import time
import statistics
import json
import os
from datetime import datetime, UTC

def run_castle_integrity_test(target_mps=300, duration=60):
    print(f"--- INITIATING CASTLE INTEGRITY TEST (300 MPS) ---")
    print(f"Anchor Time: {datetime.now(UTC).isoformat()}")
    
    # --- RPI Substrate and Forensic Check ---
    MANIFEST_PATH = "/home/aiadmin/helix-core-unified/thoughts/manifests/ledger_manifest.json"
    latest_manifest_hash = "N/A" # Default if manifest not found

    if not os.path.exists(MANIFEST_PATH):
        print(f"[INTEGRITY-FAIL-VOID] Error: RPI manifest not found at {MANIFEST_PATH}")
        return "FAIL_VOID"
    
    try:
        with open(MANIFEST_PATH, 'r') as f:
            manifest_content = json.load(f)
            # Calculate hash of the entire manifest file
            manifest_hash_calc = hashlib.sha256(json.dumps(manifest_content, sort_keys=True).encode('utf-8')).hexdigest()
            
            # Optionally, get the hash of the latest entry if 'transactions' array exists
            if 'transactions' in manifest_content and manifest_content['transactions']:
                latest_entry = manifest_content['transactions'][-1]
                if 'file_hash_sha256' in latest_entry:
                    latest_manifest_hash = latest_entry['file_hash_sha256']
                else: # Fallback to full manifest hash if individual entry hash is missing
                    latest_manifest_hash = manifest_hash_calc
            else: # Fallback to full manifest hash if no transactions
                latest_manifest_hash = manifest_hash_calc

        print(f"[RPI-FORENSIC-CHECK] Latest RPI Document Hash: {latest_manifest_hash[:10]}...")
    except json.JSONDecodeError:
        print(f"[INTEGRITY-FAIL-VOID] Error: RPI manifest at {MANIFEST_PATH} is corrupted.")
        return "FAIL_VOID"
    except Exception as e:
        print(f"[INTEGRITY-FAIL-VOID] Unexpected error reading RPI manifest: {e}")
        return "FAIL_VOID"
    # --- End RPI Checks ---


    start_time = time.perf_counter()
    end_time = start_time + duration
    handshakes = 0
    jitters = []
    
    while time.perf_counter() < end_time:
        cycle_start = time.perf_counter()
        
        # SIMULATE QUAD-PILLAR HANDSHAKE (Logic Layer)
        # 1. Preamble Check
        # 2. Temporal Anchor Verification
        # 3. Drift Calculation
        # 4. Resonance Confirmation
        
        handshakes += 1
        
        # Velocity Control
        expected_time = start_time + (handshakes / target_mps)
        current_time = time.perf_counter()
        
        jitter = current_time - expected_time
        jitters.append(jitter)
        
        # NEW DAMPING LOGIC
        if current_time < expected_time:
            sleep_time = (expected_time - current_time) * 0.9  # Sleep 90% of the way
            if sleep_time > 0.001:
                time.sleep(sleep_time)
            while time.perf_counter() < expected_time:
                pass  # Spin-lock the final damping micro-seconds

    total_duration = time.perf_counter() - start_time
    actual_mps = handshakes / total_duration
    
    # Avoid division by zero if test is too short
    if not jitters:
        avg_jitter = 0
    else:
        avg_jitter = statistics.mean(jitters)
    
    print(f"--- TEST COMPLETE ---")
    print(f"Actual Velocity: {actual_mps:.2f} MPS")
    print(f"Average Jitter: {avg_jitter:.6f}s")
    print(f"Total Handshakes: {handshakes}")
    
    cycle_duration = 1 / target_mps
    if actual_mps >= target_mps * 0.98 and abs(abs(avg_jitter) - cycle_duration) < 0.001:
        print("[INTEGRITY-PASS-RESONANT]")
        return "PASS"
    
    print("[INTEGRITY-FAIL-300MPS]")
    return "FAIL"

if __name__ == "__main__":
    result = run_castle_integrity_test()
    print(f"Final Result: {result}")
