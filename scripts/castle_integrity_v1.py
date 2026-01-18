import hashlib
import time
import statistics
import json
import os
from datetime import datetime, UTC, timezone

def calculate_file_hash(filepath):
    """Calculates the SHA256 hash of a file."""
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def check_permission_coherence(manifest_path, permission_file_path):
    """
    Checks for permission coherence between the ledger manifest and
    the current vault_permissions.json.
    """
    print("""
--- Running Permission Coherence Check ---
""")
    if not os.path.exists(manifest_path):
        print(f"  Error: Manifest file not found at {manifest_path}")
        return False
    if not os.path.exists(permission_file_path):
        print(f"  Error: Permission file not found at {permission_file_path}")
        return False

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    latest_braid_state = None
    for transaction in reversed(manifest.get('transactions', [])):
        if transaction.get('type') == 'PERMISSION_BRAID_STATE' and \
           transaction.get('filepath') == permission_file_path:
            latest_braid_state = transaction
            break

    if not latest_braid_state:
        print("  Warning: No 'PERMISSION_BRAID_STATE' entry found in manifest.")
        print("  Permission Coherence: UNKNOWN (No baseline for comparison)")
        return False

    expected_hash = latest_braid_state.get('file_hash_sha256')
    current_hash = calculate_file_hash(permission_file_path)

    print(f"  Latest Braid State in Manifest (Hash): {expected_hash[:10]}...")
    print(f"  Current vault_permissions.json Hash: {current_hash[:10]}...")

    if expected_hash == current_hash:
        print("  Permission Coherence: PASSED. Current vault_permissions.json matches latest anchored state.")
        return True
    else:
        print("  Permission Coherence: FAILED. Current vault_permissions.json DOES NOT match latest anchored state.")
        print("  Discrepancy detected: Permissions file may have been modified without anchoring.")
        return False

def check_temporal_blinding(permission_file_path):
    """
    Checks for expired 'valid_until' timestamps in the current
    vault_permissions.json.
    """
    print("""
--- Running Temporal Blinding Check ---
""")
    if not os.path.exists(permission_file_path):
        print(f"  Error: Permission file not found at {permission_file_path}")
        return False

    with open(permission_file_path, 'r') as f:
        permissions_data = json.load(f)

    now_utc = datetime.now(timezone.utc)
    expired_permissions = []

    for permission in permissions_data.get('permissions', []):
        valid_until_str = permission.get('valid_until')
        if valid_until_str:
            try:
                if valid_until_str.endswith('Z'):
                    valid_until_str = valid_until_str.replace('Z', '+00:00')
                valid_until_dt = datetime.fromisoformat(valid_until_str)
                if valid_until_dt < now_utc:
                    expired_permissions.append(permission)
            except ValueError:
                print(f"  Warning: Invalid 'valid_until' format for hash {permission.get('document_hash')}: {valid_until_str}")

    if expired_permissions:
        print("  Temporal Blinding Check: DETECTED EXPIRED PERMISSIONS.")
        for p in expired_permissions:
            print(f"    - Document Hash: {p.get('document_hash')[:10]}..., Owner: {p.get('owner_id')}, Expired On: {p.get('valid_until')}")
        print("  Action required: These permissions should be formally revoked or updated.")
        return False
    else:
        print("  Temporal Blinding Check: PASSED. No expired permissions found.")
        return True

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

    # --- Permission Coherence and Temporal Blinding Checks ---
    PERMISSION_FILE_PATH = "/home/aiadmin/helix-core-unified/thoughts/vault_permissions.json"
    permission_coherence_passed = check_permission_coherence(MANIFEST_PATH, PERMISSION_FILE_PATH)
    temporal_blinding_passed = check_temporal_blinding(PERMISSION_FILE_PATH)

    if not (permission_coherence_passed and temporal_blinding_passed):
        print("[INTEGRITY-FAIL-PERMISSIONS] Permission Coherence or Temporal Blinding Failed.")
        return "FAIL_PERMISSIONS"
    # --- End Permission Checks ---

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
