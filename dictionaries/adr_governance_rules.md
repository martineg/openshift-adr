# Architecture Decision Record (ADR) Governance Rules

This document defines the strict validation rules for Creating, Updating, and Reviewing ADRs.

## 1. Scope and Hierarchy Rules

The repository uses a hierarchical structure. Use these rules to determine the correct prefix and file location.

- **OCP-BASE (Abstract/Strategic):** Cross-cutting concerns that apply to the entire platform strategy (e.g., Topology, Sizing, Multi-site, Compliance standards).
- **OCP-BM (Physical/Install):** Decisions tied to the Physical Hardware, BIOS, Firmware, or the OS Installation process (Day 0).
  - _Precedence:_ Install-time decisions (Kernel Args, PXE) belong in `OCP-BM`, even if they relate to Network/Storage.
- **Domain Specifics (OCP-NET, OCP-SEC, etc.):** Concrete implementation details that happen _after_ the cluster is installed (Day 2 configurations, CNI tuning, Operator configuration).

## 2. Quality and Validity Rules

An ADR describes a choice between valid architectural strategies.

- **Valid Strategy:** A choice between two supported, viable options (e.g., "Option A vs Option B").
- **Invalid (Configuration):** A choice between "The Correct Configuration" and "A Misconfiguration." Do not document these unless they fall under an Exception.
- **Invalid (Constraint):** If Option A _forces_ Option B (e.g., "RWO storage mandates Recreate strategy"), Option B is a constraint, not a decision. Do not create a separate ADR for Option B.

## 3. Allowed Exceptions (The "Guardrail" Rule)

You MAY document a "Right vs. Wrong" or "Constraint" decision IF and ONLY IF it serves one of these purposes:

1.  **Deployment Guardrail:** A decision critical to preventing installation failure (e.g., "FIPS requires RSA keys").
2.  **Security Policy:** Explicitly documenting that an insecure default is forbidden (e.g., "Block Port 1936").
3.  **Risk Acceptance:** Documenting the acceptance of a known trade-off (e.g., "Disable Image Verification for Lab speed").
4.  **Simplicity vs. Capability:** A procedural choice where complexity buys features (e.g., "Install-Config vs. Custom Manifests").
5.  **Platform-Specific Gaps:** Decisions required to enable a feature that is _off by default_ on the specific platform (e.g., Enabling Registry on Bare Metal).
6.  **Backing Service Selection:** Decisions on _how_ to back a core component (e.g. "Registry Storage: Object vs Block"), even if constraints apply.

## 4. Exclusion Rules

Consult `adr_exclusions.md`. Any topic listed there is strictly forbidden.

## 5. Versioning Policy

- **Current State Only:** Document the architecture for the **current** target version ONLY.
- **No Version Numbers:** Do **NOT** mention specific OCP version numbers (e.g., "4.12", "4.17") in the ADR content. State the current default behavior as an absolute fact.
- **No History:** Do **NOT** describe legacy behaviors or "how it used to work." Do **NOT** compare the current default to previous defaults (e.g., do NOT say "expanded from the previous /29").

## 6. Execution Rules (For the Reviewer)

- **Identity Check:** If your proposed update is semantically identical to the existing ADR text, **DO NOT REPORT**. Silence is success.
- **False Positive Check:** Consult `adr_exclusions.md` -> **"Section 2: False Positive Suppression"**. If an ADR's **Title or Topic** matches an entry, **DO NOT REPORT** the specific suppressed issue.
