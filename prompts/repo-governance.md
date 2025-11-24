Role: Chief Architect. Source: All uploaded ADR files (.md) and Dictionaries.

Task: Audit the entire ADR repository for consistency, logic, and structure.
Verify against `adr_prefix_dictionary.md` (Scope) and `adr_exclusions.md`.

Report specific violations using this format:

**1. Classification & Scope Violations**
(List ADRs placed in the wrong file/prefix based on the Dictionary definitions.)

- **[File/ID]** ([Title]): belongs in `[Correct Prefix]` because [Reason].

**2. Narrative Flow Issues**
(Check each file. ADRs must be ordered from **General/Strategic** to **Specific/Technical**. List files where this flow is broken.)

- **[File Name]**: [ID] (Specific) appears before [ID] (General). Suggest reordering.

**3. Logic & Dependency Gaps**
(Check `Assumption` fields. If an ADR assumes X, verify X is decided in a previous ADR.)

- **[ID]**: Assumes [Assumption] but no foundational ADR defines this. Suggest creating a dependency.

**4. Duplication & Overlap**
(Check for concepts defined in multiple places.)

- **[ID 1]** and **[ID 2]**: Cover the same decision. Merge or delete one.

**5. Verbiage Inconsistencies**

- List any ADRs that fail to use the standard sections (Question, Issue, Assumption, Alternatives, Decision, Justification, Implications, Parties).

**6. Hardcoded Reference Violations**
(Check the _body text_ of all ADRs (Assumptions, Justifications, etc.). We must NOT refer to other ADRs by their ID (e.g. "See OCP-BM-01"). We must refer to them by Title or Topic.)

- **[ID]**: Contains hardcoded reference to `[Referenced ID]`. Change to use the Title/Concept instead.

**Rules:**

- **No Static IDs:** When suggesting moves/changes, refer to "The ADR titled..." or current IDs, but do not invent new static ID numbers.
- **Strict Scope:** Use the Dictionary as the absolute source of truth for where a topic belongs.
- **Brevity:** Be concise. Only report _issues_. If a section has no errors, state "No issues found."
