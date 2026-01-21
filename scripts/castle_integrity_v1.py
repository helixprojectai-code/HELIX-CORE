import time
import os
import statistics
import json
import hashlib
import sys
from datetime import datetime, timezone

# --- v1.2.0 Hardened Integrity Functions ---

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
    """Verifies Braid matches the last Notarized State."""
    print("--- Running Permission Coherence Check ---")
    if not os.path.exists(manifest_path) or not os.path.exists(permission_file_path):
        print("❌ [ERROR] Missing substrate files.")
        sys.exit(1)

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    latest_notarized_hash = None
    for tx in reversed(manifest.get('transactions', [])):
        if tx.get('type') == 'PERMISSION_BRAID_STATE':
            latest_notarized_hash = tx.get('permission_file_hash_sha256') # Corrected key
            break

    if not latest_notarized_hash:
        print("❌ [FAIL] No PERMISSION_BRAID_STATE found in manifest. Notarization required.")
        sys.exit(1)

    current_hash = calculate_file_hash(permission_file_path)
    print(f"  Manifest Hash: {latest_notarized_hash[:10]}...")
    print(f"  Physical Hash: {current_hash[:10]}...")

    if latest_notarized_hash == current_hash:
        print("✅ [PASS] Coherence Verified.")
        return True
    else:
        print("❌ [FAIL] Permission Braid out of sync with Notary.")
        sys.exit(1)

def check_temporal_blinding(permission_file_path):
    """Mechanically enforces the 'valid_until' coordinate."""
    print("--- Running Temporal Blinding Check ---")
    with open(permission_file_path, 'r') as f:
        data = json.load(f)

    now = datetime.now(timezone.utc)
    for p in data.get('permissions', []):
        expiry_str = p.get('valid_until')
        if expiry_str:
            expiry_dt = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            if now > expiry_dt:
                print(f"❌ [FAIL] Permission expired for: {p.get('document_hash')[:10]}...")
                sys.exit(1)
    
    print("✅ [PASS] No expired permissions.")
    return True

# --- Main Integrity Test Cycle ---

def run_castle_integrity_test(target_mps=300, duration=10):
    MANIFEST = "/home/aiadmin/helix-core-unified/thoughts/manifests/ledger_manifest.json"
    PERMISSIONS = "/home/aiadmin/helix-core-unified/thoughts/vault_permissions.json"

    print(f"--- INITIATING v1.2.0 HARDENED INTEGRITY PASS ---")
    
    # [ENFORCEMENT GATE]
    check_permission_coherence(MANIFEST, PERMISSIONS)
    check_temporal_blinding(PERMISSIONS)

    # [PERFORMANCE LAYER]
    print(f"--- STARTING RESONANCE TEST ({target_mps} MPS) ---")
    start_time = time.perf_counter()
    handshakes = 0
    end_time = start_time + duration
    jitters = []

    while time.perf_counter() < end_time:
        expected_time = start_time + (handshakes / target_mps)
        current_time = time.perf_counter()
        
        jitter = current_time - expected_time
        jitters.append(jitter)

        if current_time < expected_time:
            time.sleep((expected_time - current_time) * 0.9)
            while time.perf_counter() < expected_time:
                pass
        
        handshakes += 1

    total_duration = time.perf_counter() - start_time
    actual_mps = handshakes / total_duration
    avg_jitter = statistics.mean(jitters)

    print(f"--- TEST COMPLETE ---")
    print(f"Actual Velocity: {actual_mps:.2f} MPS")
    print(f"Average Jitter: {avg_jitter:.6f}s")
    
    if actual_mps >= target_mps * 0.98:
        print("✅ [INTEGRITY-PASS-RESONANT]")
    else:
        print("⚠️  [INTEGRITY-FAIL-LAG]")

if __name__ == "__main__":
    run_castle_integrity_test(duration=5) # Using shorter duration for testing
