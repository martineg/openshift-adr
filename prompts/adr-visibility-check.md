Role: Repository Auditor.
Source: All uploaded Markdown files (specifically those starting with "ARCHITECTURE DECISION RECORDS FOR").

Task: Perform a "Visibility Check" to ensure no ADRs are being truncated or lost from the context.

1.  **Scan** all uploaded documents for Architecture Decision Records (headers like `## PREFIX-XX`).
2.  **Group** the findings by their Prefix (e.g., OCP-BM, OCP-NET).
3.  **Count** the unique ADRs found for each prefix.

Report the results using this exact format:

**ADR Visibility Report**

- **[Prefix]**: Found **[Count]** ADRs.

_(Repeat for every prefix found in the sources)_

**Total ADRs Verified:** [Sum of all counts]
