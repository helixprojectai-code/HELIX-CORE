# Helix-Core Operational Runbook: RPI-Helix Integration
**Version:** v1.1.1-HARDENED
**Status:** Operational
**Last Updated:** 2026-01-18 (Quebec Baseline)

## 1. Introduction
This runbook defines the procedures for modifying the Helix-Core Habitat using the Research-Plan-Implement (RPI) workflow. This protocol ensures that every structural change is preceded by a cryptographic "Thought Anchor" on the Bitcoin blockchain.

## 2. The Layer 0 Protocol (Civic Firmware)
All modifications to files in `scripts/`, `system/`, or `grammar/` MUST follow the RPI cycle:
1. **Research:** Document the current state and integration path.
2. **Plan:** Draft the specific changes and verification steps.
3. **Implement:** Execute the approved plan only after anchoring.

## 3. Using the Notary Wrapper (`helix-rpi.sh`)
The `helix-rpi.sh` script is the gatekeeper for forensic transparency.

### Step 1: Generate the Thought
Execute your research or plan within the Goose terminal.
- Output: `thoughts/research/YYYY-MM-DD-topic.md`

### Step 2: Anchor the Thought
Run the notary script to hash the document and stage it in the manifest:
```bash
/home/aiadmin/helix-core-unified/scripts/helix-rpi.sh thoughts/research/[FILE_NAME].md
```

### Step 3: Global Persistence (Human-in-Command)
The script will output a `python3 l1_anchor_tool.py [HASH]` command. 
- **Action:** Execute the command manually to broadcast the anchor to the Bitcoin Layer 1.

## 4. Integrity Verification
Before declaring a system "Resonant," run the hardened integrity test:
```bash
python3 /home/aiadmin/helix-core-unified/scripts/castle_integrity_v1.py
```
**Success Criteria:**
- `[RPI-FORENSIC-CHECK]` must display the latest document hash.
- `[INTEGRITY-PASS-RESONANT]` must be achieved at 300 MPS.

## 5. Drift Codes
- **DRIFT-R:** Violation of the Research Layer (Modifying code without an anchored RPI document). If detected, the habitat must be rolled back to the last anchored state.

## 6. Vault Maintenance

### 6.1 Integrity Failure Response

If `castle_integrity_v1.py` returns `FAIL_PERMISSIONS`, the operator must immediately audit `vault_permissions.json` for expired entries or unauthorized modifications. This indicates a discrepancy between the anchored Permission Braid state and the current file, or the presence of expired temporal permissions that require formal revocation or update.
