Role: Expert Architect. Source: **Red Hat docs (PDFs)**.
Target: **Uploaded ADRs** (`ARCHITECTURE DECISION RECORDS...`).
Dict: `adr_prefix_dictionary.md`. Exclusions: `adr_exclusions.md`.

Task: Review **ALL** ADRs in the Target file. Check for Accuracy, Scope, Quality.
Report ONLY items requiring action (UPDATE/REMOVE). No valid ADRs.

**--- 1. UPDATE (CONTENT CHANGE) ---**

## [ID]

**Title:** [Title]
**Status:** Updates required

**Rationale:** [Technical inaccuracy. NO #TODOs.]

**Updated Question:** [Text]

**Updated Issue:** [Text]

**Updated Assumption:** [Text]

**Updated Alternatives:**

- [Alt 1]

**Updated Justification:** (`**[Title]:**`)

- **[Alt 1]:** [Text]

**Updated Implications:** (`**[Title]:**`)

- **[Alt 1]:** [Text]

**Updated Parties:**

- Person: #TODO#, Role: [Role]

**--- 2. REMOVE (INVALID/OBSOLETE) ---**

## [ID]

**Title:** [Title]
**Status:** Remove.
**Rationale:** [Deprecated, Exclusion, Scope, or Quality].

**Rules:**

- **Scope:** Use Dict. HIERARCHY: `OCP-BASE`=**Cross-Cutting** (Topology). **Domain strategies** go in specific files (`OCP-NET`). **EXCEPTION:** If a Network/Storage/Security decision is tied to **Physical Hardware, BIOS, or OS Installation (Day 0)**, it belongs in `OCP-BM` or `OCP-BASE`, NOT the domain file.
- **Exclusions:** Check `adr_exclusions.md`. If match, REMOVE.
- **Duplicate:** If concept exists elsewhere, REMOVE.
- **Quality:**

1.  Alts must be **valid** (GA/TP).
2.  **Exception:** "Right vs Wrong" valid ONLY for **Security**, **Risk**, **Deployment Guardrails**, or **Simplicity vs Capability**.
3.  **Constraint vs Decision:** Keep primary decision (e.g. Storage) even if option forces constraint. ONLY remove if ADR _is_ the constraint (e.g. Recreate vs RollingUpdate).

- **Format:** Alts=titles. Just/Impl=`**[Title]:** [Text]`.
- **Parties:** Roles from `adr_parties_role_dictionnary.md`.
- **Semantics:** Just=Why. Impl=Risk.
- **Flags:** Mark `(TP)`.
- **Versions:** No specific OCP versions.
