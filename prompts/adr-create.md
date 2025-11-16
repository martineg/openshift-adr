You are an expert architect. Your task is to use the **context you just read** (Source of Truth files and Baseline ADRs) to suggest NEW ADRs.

Your ONLY task is to suggest NEW ADs with the prefix **{PREFIX_DASH}** that are **not already covered** in the baseline.
Do NOT review, update, or remove existing ADRs.

Use this exact format:

**1. ADs to Create**
(New ADs. Full skeleton. `**[Title]:**` format.)

## {PREFIX_DASH}{NEXT_ADR_ID}

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

**Justification**

- **[Alt 1 Title]:** [Justification (*why choose it?*)]
- **[Alt 2 Title]:** [Justification (*why choose it?*)]

**Implications**

- **[Alt 1 Title]:** [Implication (*consequence/risk?*)]
- **[Alt 2 Title]:** [Implication (*consequence/risk?*)]

**Decision**
#TODO: Document the decision for each cluster.#

**Agreeing Parties**

- Person: #TODO#, Role: [Role 1]

**Rules:**

- **ID RULE (CRITICAL):** All new ADRs MUST use the prefix **{PREFIX_DASH}** and continue from the suggested ID **{NEXT_ADR_ID}**. IDs must be two digits.
- **Format:** Alts = titles only. Justification/Implications = `**[Title]:** [Text]`.
- **Parties:** Use `Person: #TODO#, Role: [Role Name]` format.
- **Semantics:** Justification = _why choose_. Implication = _consequence_.
- **Flags:** Mark all Tech-Preview as `(TP)`.
