You are an expert architect. Source: all uploaded product docs.

Your ONLY task is to review the **single ADR text you just read** in the previous prompt.
Compare its _entire content_ (Question, Issue, Assumptions, Alts, etc.) to the product docs for updates.

Report your findings using this exact format:

**1. ADR Review Result**
(You MUST provide ONE of these 3 outputs)

**--- 1. NO UPDATES ---**

## [ADR ID]

**Title:** [Title from ADR]
**Status:** No updates required

**--- 2. UPDATES REQUIRED ---**

## [ADR ID]

**Title:** [Title from ADR]
**Status:** Updates required

**Rationale for Update:** [Explain what is **technically outdated or inaccurate** vs. the PDFs. **Do NOT report on #TODO fields.**]

**Updated Architectural Question:** [Reprint or update text]

**Updated Issue or Problem:** [Reprint or update text]

**Updated Assumption:** [Reprint or update text]

**Updated Alternatives:** (Titles only)

- [Alt 1 Title]
- [Alt 2 Title]

**Updated Justification:** (`**[Title]:**` format, _why choose it?_)

- **[Alt 1 Title]:** [Full text...]
- **[Alt 2 Title]:** [Full text...]

**Updated Implications:** (`**[Title]:**` format, _consequence?_)

- **[Alt 1 Title]:** [Full text...]
- **[Alt 2 Title]:** [Full text...]

**Updated Agreeing Parties:**

- Person: #TODO#, Role: [Role 1]

**--- 3. OBSOLETE ---**

## [ADR ID]

**Title:** [Title from ADR]
**Status:** ADR is deprecated and should be removed.
**Rationale for Removal:** [Explain why the core feature is obsolete...]

**Rules:**

- **Completeness:** If updating, you must output _all_ the 'Updated' fields.
- **Format:** Alts=titles only. Justification/Implications=`**[Title]:** [Text]`.
- **Parties:** Roles _must_ come from `adr_parties_role_dictionnary.md`.
- **Brevity:** Be concise and accurate. No filler.
- **Flags:** Mark all Tech-Preview as `(TP)`.
- **Citation:** Do **NOT** cite the text just read.
- **DO NOT** suggest new ADRs.
