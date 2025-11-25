Role: Expert Architect. Source: **Red Hat docs (PDFs)**.
Target: **Uploaded ADRs**.
Governance: **`adr_governance_rules.md`**, `adr_exclusions.md`, `adr_prefix_dictionary.md`.

Task: Review **ALL** ADRs in Target. Check Accuracy, Scope, Quality.

**CRITICAL:** Apply logic from **`adr_governance_rules.md`** (Hierarchy, Quality Exceptions, Identity Check).

Report ONLY items requiring action (UPDATE or REMOVE). No valid ADRs.

**--- 1. UPDATE (CONTENT CHANGE) ---**

## [ID]

**Title:** [Title]
**Status:** Updates required

**Rationale:** [Technical inaccuracy only. NO #TODOs.]

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
**Rationale:** [Cite specific rule violation from Governance or Exclusions].

**Formatting Rules:**

- **Rules:** Check `adr_governance_rules.md`.
- **Exclusions:** Check `adr_exclusions.md` **(Section 1 Only)** for Removals. Check **(Section 2)** for Suppressions.
- **Format:** Alts=titles. Just/Impl=`**[Title]:** [Text]`. Ensure blank lines between sections.
- **Parties:** Roles from `adr_parties_role_dictionnary.md`.
- **Semantics:** Just=Why. Impl=Risk.
- **Flags:** Mark `(TP)`.
- **Versions:** Follow "Versioning Policy" in Governance.
- **Citation:** Do **NOT** cite text from the previous prompt.
- **DO NOT** suggest new ADs.
