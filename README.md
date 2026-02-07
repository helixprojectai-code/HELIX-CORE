# 🧬 HELIX CORE
### A Sovereign Framework for Constitutional AI Governance

**HELIX CORE** is a layered, sovereign architecture for building, auditing, and governing autonomous AI systems with embedded ethics and verifiable accountability. It spans from foundational identity to metabolic ledger operations.

> **📮 For all implementation support, next-step planning, and project discussions, contact the core team: [helix.project.ai@helixprojectai.com](mailto:helix.project.ai@helixprojectai.com)**

---

## 🏗️ 1. ARCHITECTURE & DIRECTORY MAP

The system is structured across five sovereign layers (L0-L4), implemented as Git submodules, with a central vault.

| Layer | Path | Description | Type |
| :--- | :--- | :--- | :--- |
| **L0** | `./identity/` | **Source: DBC & Suitcase** – Foundational identity and capability declarations. | Submodule |
| **L1** | `./constitution/` | **Source: Rust REM** – Constitutional rule engine and execution monitor. | Submodule |
| **L2** | `./hgl/` | **Source: HGL Compiler** – Hierarchical Grammar Language compiler for policy. | Submodule |
| **L3** | `./grammar/` | **Source: Constitutional Grammar** – Definitive grammar for sovereign clauses. | Submodule |
| **L4** | `./helix-ledger/` | **Source: Metabolic Anchor (V9 Stable)** – Immutable proof and state ledger. | Submodule |
| **—** | `./agents/` | **The Vault: Stored DBCs and Glyphs** – Secure storage for agents and artifacts. | Shared Volume |

**Core Data Flow:**
`Identity (L0) → Constitution (L1) → HGL Policy (L2) → Grammar Binding (L3) → Ledger Proof (L4)`

---

## 🚀 2. IGNITION (GOD MODE)

Deploy the full sovereign stack with a single sequence.

### A. Clone the Federation (Must use `--recursive`)
```bash
git clone --recursive https://github.com/helixprojectai-code/HELIX-CORE.git
cd HELIX-CORE
```

### B. Ignite the Full Fleet
Ignites all layers and the monitoring stack.
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### ✅ Post-Ignition Verification
| Task | Command | What to Look For |
| :--- | :--- | :--- |
| **Check Fleet Status** | `docker-compose -f docker-compose.prod.yml ps` | All services show `Up`. |
| **View Launch Logs** | `docker-compose -f docker-compose.prod.yml logs --tail=50` | Look for `INFO`/`Started` messages. |
| **Stream Live Logs** | `docker-compose -f docker-compose.prod.yml logs -f` | Real-time monitoring (exit with `Ctrl+C`). |
| **Stop the Fleet** | `docker-compose -f docker-compose.prod.yml down` | Stops and removes all containers. |
| **Stop & Preserve Data** | `docker-compose -f docker-compose.prod.yml stop` | Stops containers but keeps them. |

---

## 🛡️ 3. GOVERNANCE & CONTRIBUTION

HELIX CORE operates under active constitutional principles. All layer transitions and ledger entries are subject to precedent-based review.

### For Contributors & Integrators
We welcome deep technical discussions on layer integration, grammar extensions, and ledger proofs.

**The central channel for all planning is:**
**📧 [helix.project.ai@helixprojectai.com](mailto:helix.project.ai@helixprojectai.com)**

Use this email for:
- Proposing new DBC structures or glyphs for **The Vault**.
- Discussing extensions to the **Constitutional Grammar (L3)** or **HGL Compiler (L2)**.
- Reporting complex, multi-layer integration issues.
- Requesting access for collaborative development on specific layers.

### For Users & Testers
- Use repository Issues for reporting **clear bugs** within a single layer.
- For **configuration help, deployment issues, or strategic guidance**, emailing the core team is the most efficient path.

---

## 🔧 4. TROUBLESHOOTING & SUPPORT

### Common First Steps
1.  **Verify Submodules:** Ensure all layers are checked out: `git submodule status`
2.  **Check Service Logs:** `docker-compose -f docker-compose.prod.yml logs [service_name]`
3.  **Verify Container Status:** `docker-compose -f docker-compose.prod.yml ps`
4.  **Ensure Ports Are Free:** Key ports (`3100`, `8080`, `6333`) must not conflict.

### Layer-Specific Issues
- **L0/L1 Issues:** Check identity binding and REM rule compilation logs.
- **L2/L3 Issues:** Validate HGL policy files and grammar syntax.
- **L4 Issues:** Confirm ledger connectivity and proof generation.
- **Vault Issues:** Verify volume mounts and artifact permissions in `./agents/`.

### Getting Help
If you encounter issues:
1.  **Document Context:** Note your environment (OS, Docker version) and the affected layer.
2.  **Capture Logs:** Include full error messages and relevant layer logs.
3.  **Contact Core Team:** Send structured details to **[helix.project.ai@helixprojectai.com](mailto:helix.project.ai@helixprojectai.com)**.

---

## 📬 5. CONTACT & ROADMAP

- **Email (Primary):** [helix.project.ai@helixprojectai.com](mailto:helix.project.ai@helixprojectai.com)
- **Source Code:** `https://github.com/helixprojectai-code/HELIX-CORE.git`

**Next Phase Planning:** Interested in expanding constitutional grammars, new metabolic ledger features, or agent vault protocols? Strategic planning is coordinated via our primary email.

---

*HELIX CORE – Governing the architecture of thought across sovereign layers.*
