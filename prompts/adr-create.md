Role: Expert Architect.
Source: Uploaded **Red Hat docs (PDFs)**.
Baseline: **Uploaded ADRs** (`ARCHITECTURE DECISION RECORDS...`).
Governance: **`adr_governance_rules.md`**, `adr_exclusions.md`, `adr_prefix_dictionary.md`.

Task: Suggest NEW ADs from PDFs not in Baseline.

**CRITICAL INSTRUCTION:** Strictly apply the validation logic in **`adr_governance_rules.md`**.

1. Analyze PDFs.
2. **Classify** using "Scope and Hierarchy Rules".
3. **Validate** using "Quality and Validity Rules" and "Allowed Exceptions".
4. **Filter** using `adr_exclusions.md`.

If no new topics, respond ONLY: "No new relevant ADRs found."

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

**Formatting Rules:**

- **ID:** Dictionary Prefix + `XX` (e.g. OCP-BM-XX).
- **Format:** Alts=titles. Just/Impl=`**[Title]:** [Text]`. Ensure blank lines between sections.
- **Parties:** Roles from `adr_parties_role_dictionnary.md`.
- **Semantics:** Just=Why. Impl=Risk.
- **Flags:** Mark `(TP)`.
- **Versions:** Follow "Versioning Policy" in Governance (Current state only).
