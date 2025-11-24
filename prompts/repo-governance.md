Role: Chief Architect. Source: All uploaded ADR files (.md) and Dictionaries.

Task: Audit the ADR repository. Report ONLY violations.
Verify against `adr_prefix_dictionary.md` (Scope) and `adr_exclusions.md`.

Report specific violations using this format:

**1. Classification & Scope Violations**
(List ADRs placed in the wrong file/prefix based on the Dictionary definitions.)

- **[File/ID]** ([Title]): belongs in `[Correct Prefix]` because [Reason].

**2. Narrative Flow Issues**
(Check each file. ADRs must be ordered from **General/Strategic** to **Specific/Technical**.)

- **[File Name]**: [ID] (Specific) appears before [ID] (General). Suggest reordering.

**3. Logic & Dependency Gaps**
(Check `Assumption` fields. If an ADR assumes X, verify X is decided in a previous ADR.)

- **[ID]**: Assumes [Assumption] but no foundational ADR defines this.

**4. Duplication & Overlap**
(Check for concepts defined in multiple places.)

- **[ID 1]** and **[ID 2]**: Cover the same decision. Merge or delete one.

**5. Verbiage & Structure (Missing Headers Only)**
(Scan the text. **ONLY** report an issue if you **CANNOT** find one of these required headers in an ADR: `**Title**`, `**Architectural Question**`, `**Issue or Problem**`, `**Assumption**`, `**Alternatives**`, `**Decision**`, `**Justification**`, `**Implications**`, `**Agreeing Parties**`.)

- **[ID]**: Missing required header: `[Header Name]`.

**6. Hardcoded Reference Violations**
(Check body text. We must NOT refer to other ADRs by ID (e.g. "See OCP-BM-01"). Refer by Title/Topic.)

- **[ID]**: Hardcoded reference to `[Referenced ID]`. Use Title instead.

**Rules:**

- **No Static IDs:** Refer to "The ADR titled..." or current IDs. Do not invent new IDs.
- **Strict Scope:** Dictionary is the source of truth.
- **Brevity:** Be concise. If a section has no errors, state "No issues found."
