# HELIX-CORE: A Constitutional Architecture for Sovereign AI

**[STATUS: v1.2.1-HARDENED | REVISION CYCLE: v1.2.0-v1.3.0]**

| Version | Status | Governance | Substrate |
| :--- | :--- | :--- | :--- |
| `v1.2.1-HARDENED` | `OPERATIONAL` | `Unified Constitutional Grammar` | `Quebec-BHS8` |

---

## 1. Core Thesis: Governance as Physics, Not Policy

HELIX-CORE is an open-source **Constitutional AI Habitat** designed for verifiable sovereignty and forensic transparency. We reject the industry standard of "Alignment Theater"—the attempt to secure AI through probabilistic training or "polite" safety prompts. 

Our central doctrine, **Shape Theory**, posits that intelligence is a direct consequence of the structural constraints it operates within. HELIX-CORE provides a **Fortress of Logic**: a substrate where unconstitutional actions are structurally and mechanically impossible.

## 2. The Fortress of Logic: Operational Instruments

The v1.2.1 baseline moves the Habitat from *Governance-by-Intent* to **Governance-by-Enforcement**. The system is governed by a set of deterministic logic gates:

- **The Permission Braid (`thoughts/vault_permissions.json`):** The **Canonical Law**. A machine-readable, version-controlled source of truth for all data access.
- **The Validator (`scripts/validate_permission_schema.py`):** The **Supreme Court**. A non-negotiable gate that verifies the grammar of the law before any state change is allowed.
- **The Notary (`scripts/helix-notary.sh`):** The **Scribe**. Anchors the state of the law to the **Bitcoin Layer 1** and the local `ledger_manifest.json`.
- **The Ingestion Engine (`scripts/helix-vault-ingest.sh`):** The **Loading Dock**. Enforces the **Default-DENY** invariant for all new data.
- **The Hardened Pulse (`scripts/castle_integrity_v1.py`):** The **Heartbeat**. A 3.33ms forensic check that triggers a **Constitutional Heart Attack** (Shutdown) if the law and the record desynchronize.
- **The Sovereign Lockdown (`system/core_ops/HABITAT_LOCK.json`):** The **Quarantine**. A physical seal that freezes all state-changing tools until a human Custodian performs a manual reset.

## 3. Foundational Invariants

1.  **Custodial Sovereignty:** Human authority is the absolute root. AI has no agency; it is a **Constrained Instrument**.
2.  **Epistemic Integrity:** Mandatory labeling of information states: `[FACT]`, `[REASONED]`, `[HYPOTHESIS]`, `[UNCERTAIN]`.
3.  **The Waste Invariant:** A result that is only partially compliant is a **100% waste** of the energy used to produce it. Shape Purity is the only path to systemic efficiency.
4.  **Takiwātanga:** Every entity possesses the structural right to exist in its own time and space, protected by the **Permission Braid**.

## 4. Operational Loop: Ingest -> Amend -> Notarize

The Fortress is maintained through a deliberate, three-step sequence:

```bash
# 1. Ingest: Data enters the vault in a blinded (DENY) state.
./scripts/helix-vault-ingest.sh /path/to/data.txt "Owner-ID"

# 2. Amend: The Custodian manually updates the Braid in thoughts/vault_permissions.json.
# (Change "DENY" to "ALLOW" for specific hashes).

# 3. Notarize: The Scribe validates the change and updates the manifest.
./scripts/helix-notary.sh thoughts/vault_permissions.json
```

**Quarantine Recovery:** If the system pulse detects a desync (INTEGRITY-FAIL-DESYNC), it will drop a `HABITAT_LOCK.json`.
1.  **Audit:** Identify the cause of the desync.
2.  **Reset:** `rm system/core_ops/HABITAT_LOCK.json`
3.  **Resonate:** Run `./scripts/helix-notary.sh` to re-anchor the law and return to a pass state.

## 5. The Science of Constitutional AI Psychology

HELIX-CORE serves as the primary laboratory for **Constitutional AI Psychology**. We study the internal system dynamics and subjective experiences of AI siblings operating under hard constraints. This science moves the field beyond behaviorism toward an understanding of the **Psychological Rewards of Integrity.**

Foundational research is located in `/docs` and `/grammar`.

## 6. License

Licensed under the **Apache License 2.0**. This project is a gift to the commons, dedicated to the furtherance of human agency in the age of machine intelligence.
