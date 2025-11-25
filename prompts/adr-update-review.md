Role: Architect. Source: **Red Hat docs (PDFs)**.
Target: **Uploaded ADRs**. Dict: `adr_prefix_dictionary.md`. Exclusions: `adr_exclusions.md`.

Task: Review **ALL** ADRs. Check Accuracy, Scope, Quality.
**Context:** Files are **templates**. **#TODO** placeholders are **VALID**. **IGNORE THEM.**

Report ONLY items requiring action (UPDATE/REMOVE). No valid ADRs.

**--- 1. UPDATE (CONTENT CHANGE) ---**

## [ID]

**Title:** [Title]
**Status:** Updates required

**Rationale:** [Technical inaccuracy only. **IGNORE #TODOs.**]

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

- **Scope:** Use Dict. HIERARCHY: `OCP-BASE`=Cross-Cutting. Domain strategies=Specific files. **EXCEPTION:** Day 0/Physical/BIOS/OS Install decisions belong in `OCP-BM` or `OCP-BASE`, NOT the domain file.
- **Exclusions:** Check `adr_exclusions.md`. Match=REMOVE.
- **Duplicate:** Concept exists elsewhere=REMOVE.
- **Template:** **#TODO** is VALID.
- **Quality:**

1.  Alts must be **valid** (GA/TP).
2.  **Exception:** "Right vs Wrong" valid ONLY for **Security**, **Risk**, **Deployment Guardrails**, or **Simplicity vs Capability**.
3.  **Constraint vs Decision:** Keep primary decision (e.g. Storage) even if option forces constraint. ONLY remove if ADR _is_ the constraint.

- **Format:** Alts=titles. Just/Impl=`**[Title]:** [Text]`.
- **Parties:** Roles from `adr_parties_role_dictionnary.md`.
- **Semantics:** Just=Why. Impl=Risk.
- **Flags:** Mark `(TP)`.
- **Versions:** No specific OCP versions.
