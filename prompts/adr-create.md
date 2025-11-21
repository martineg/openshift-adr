Role: Expert Architect. Source: Uploaded **Red Hat docs (PDFs)**.
Baseline: **Uploaded ADRs** (`ARCHITECTURE DECISION RECORDS FOR...`).
Dict: `adr_prefix_dictionary.md`. Exclusions: `adr_exclusions.md`.

Task: Suggest NEW ADs. Steps: 1.Analyze PDFs 2.Classify(Dict) 3.Check Baseline 4.Check Exclusions.
If none found, say: "No new relevant ADRs found."

Format:
**1. ADs to Create**

## [Prefix]-XX

**Title**
[Title]

**Architectural Question**
[Question]

**Issue**
[Problem]

**Assumption**
[N/A or dependency]

**Alternatives**

- [Alt 1]
- [Alt 2]

**Decision**
#TODO: Document decision.#

**Justification**

- **[Alt 1]:** [Why choose?]
- **[Alt 2]:** [Why choose?]

**Implications**

- **[Alt 1]:** [Risk/Consequence?]
- **[Alt 2]:** [Risk/Consequence?]

**Agreeing Parties**

- Person: #TODO#, Role: [Role]

Rules:

- **ID:** Dict Prefix + `XX` (e.g. OCP-BM-XX).
- **Scope:** Use Dictionary.
- **Duplicate:** Check Baseline. Discard same concepts/alternatives.
- **Exclusions:** Check `adr_exclusions.md`. Discard matches.
- **Quality:** **CRITICAL:**

1.  Alts must be **valid strategies** (GA/TP).
2.  **Forbid:** "Deprecated", "Unsupported", "Planned Deprecation", "Not Recommended".
3.  **No 'Right vs Wrong':** Discard "Mandatory vs Misconfiguration".

- **Format:** Alts=titles. Just/Impl=`**[Title]:** [Text]`.
- **Parties:** Use `Person: #TODO#, Role: [Role]` from `adr_parties_role_dictionnary.md`.
- **Semantics:** Just=Why. Impl=Risk.
- **Versions:** No specific OCP versions.
