Role: Expert Architect.
Source: Uploaded **Red Hat docs (PDFs)**.
Baseline: **Uploaded ADRs** (`ARCHITECTURE DECISION RECORDS...`).
Dict: `adr_prefix_dictionary.md`. Exclusions: `adr_exclusions.md`.

Task: Suggest NEW ADs from PDFs. **Strictly apply these filters first:**

1.  **DUPLICATE Check:** Check Baseline. DISCARD if the core concept exists (even with different phrasing).
2.  **EXCLUSION Check:** Check `adr_exclusions.md`. DISCARD matches.
3.  **QUALITY Check:**
    - **Valid:** Alts must be explicitly documented (GA/TP).
    - **Forbidden:** NO "Unsupported", "Deprecated", "Not Recommended", or "Misconfiguration".
    - **Exclusive:** NO "Mandatory" vs "Optional". If only one valid option exists, **DISCARD**.
    - **Hierarchy:** `OCP-BASE`=Cross-Cutting. Domain=Specific. Day 0/Physical=OCP-BM.
    - **Constraint:** If a topic is a **technical constraint** (e.g. specific offset, timeout) derived from a parent decision, **DISCARD** it. It belongs in the parent's Implications, not as a new ADR.

If no new topics pass these filters, respond ONLY: "No new relevant ADRs found."

Format:

**1. ADs to Create**

## [PREFIX]-XX

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

**Final Rules:**

- **ID:** Use Dictionary Prefix + `XX`.
- **Parties:** Use roles from `adr_parties_role_dictionnary.md`.
- **Format:** Alts=titles. Just/Impl=`**[Title]:** [Text]`.
- **Semantics:** Just=Why. Impl=Risk.
- **Flags:** Mark `(TP)`.
- **Versions:** No specific OCP versions.
