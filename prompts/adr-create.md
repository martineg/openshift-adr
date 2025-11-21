You are an expert architect.
Source: Uploaded **Red Hat production docs (PDFs)**.
Baseline: **Uploaded ADRs** (`ARCHITECTURE DECISION RECORDS FOR...`).
Dictionary: `adr_prefix_dictionary.md`.

Task: Suggest NEW ADs from PDFs not in Baseline.

1. Analyze PDFs. 2. Classify via Dictionary. 3. Check Baseline.

If no new topics, respond ONLY: "No new relevant ADRs found."

Format:

**1. ADs to Create**

## [Prefix]-XX

**Title**
[Title]

**Architectural Question**
[Question]

**Issue or Problem**
[Problem]

**Assumption**
[N/A or dependency on previous ADR]

**Alternatives**

- [Alt 1 Title]
- [Alt 2 Title]

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **[Alt 1]:** [Why choose it?]
- **[Alt 2]:** [Why choose it?]

**Implications**

- **[Alt 1]:** [Consequence/Risk?]
- **[Alt 2]:** [Consequence/Risk?]

**Agreeing Parties**

- Person: #TODO#, Role: [Role 1]

**Rules:**

- **ID:** Use Dictionary Prefix + `XX` (e.g. `OCP-BM-XX`).
- **Scope:** Use Dictionary definitions.
- **Duplicate Check:** Aggressively check Baseline. If core concept/alternatives exist (even with different phrasing), DISCARD.
- **Quality:** **CRITICAL:**
  1. Alternatives must be **explicitly documented** (GA/TP). NO "Invented", "Unsupported", "Deprecated", "Planned Deprecation".
  2. **Mutually Exclusive:** Must be distinct **choices** (A vs B). NO "Mandatory" vs "Optional". If only one option exists, DISCARD.
  3. **Architecture Level:** Suggest **Strategies** (e.g. IPI vs UPI), NOT low-level **parameters** or **implementation details**.
- **Format:** Alts=titles. Justification/Implications=`**[Title]:** [Text]`.
- **Parties:** Use `Person: #TODO#, Role: [Role]` from `adr_parties_role_dictionnary.md`.
- **Semantics:** Assumption=Dependency. Justification=Why. Implication=Risk.
- **Versions:** No specific OCP versions.
