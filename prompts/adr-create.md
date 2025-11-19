You are an expert architect.
Source of Truth: Uploaded **Red Hat production documentation (the PDFs)**.
Baseline: **All uploaded ADRs** (files with titles starting `ARCHITECTURE DECISION RECORDS FOR`).

Task: Suggest NEW ADs with the prefix **[PREFIX]-** that are:

1.  Relevant to the **topic** of the PDFs.
2.  **Not already covered** by any existing ADR in the baseline files.

On Failure: If no new, relevant topics to suggest, respond ONLY with "No new relevant ADRs found."

Format:

**1. ADs to Create**
(New ADs. Full skeleton. `**[Title]:**` format.)

## [Suggested AD ID]

**Title**
[Suggested Title]

**Architectural Question**
[Question].

**Issue or Problem**
[Describe the problem].

**Assumption**
[N/A or context].

**Alternatives**

- [Alternative 1 Title]
- [Alternative 2 Title]

**Decision**
#TODO: Document the decision for each cluster.#

**Justification**

- **[Alt 1 Title]:** [Justification (*why choose it?*)]
- **[Alt 2 Title]:** [Justification (*why choose it?*)]

**Implications**

- **[Alt 1 Title]:** [Implication (*consequence/risk?*)]
- **[Alt 2 Title]:** [Implication (*consequence/risk?*)]

**Agreeing Parties**

- Person: #TODO#, Role: [Role 1]

**Rules:**

- **ID:** All new ADRs MUST use the prefix **[PREFIX]-** and continue from the sequential ID **[STARTING_ID]**. IDs must be **two digits** (e.g., 08, 09, 13).
- **Quality:** Do NOT suggest ADRs for **mandatory requirements** or where alternatives are **misconfigurations** (e.g., "Right vs Wrong"). Must be a choice between **viable** options (GA vs. GA, or GA vs. TP).
- **ADR Format:** Alts = titles only. Justification/Implications = `**[Title]:** [Text]`.
- **Parties:** Use `Person: #TODO#, Role: [Role Name]` format. Pull roles from `ad_parties_role_dictionnary.md`.
- **Semantics:** Justification = _why choose_. Implication = _consequence_.
- **Flags:** Mark all Tech-Preview as `(TP)`.
- **Versioning:** Do NOT mention specific OCP versions.
