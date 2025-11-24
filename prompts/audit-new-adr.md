**Context:** I am acting as the Gatekeeper for my ADR repository. I have uploaded my current `adr/` files and `dictionaries/`.

**Input:** I will paste a **Candidate ADR** below that was suggested by an AI.

**Your Task:** Audit this Candidate ADR against my existing repository and rules.

**Report Findings:**

1.  **Duplication Check:** Does this decision (or a very similar one) already exist in _any_ of the uploaded files? (Check concepts, not just titles).

    - _Verdict:_ [Unique / Duplicate]
    - _Action:_ [Keep / Discard / Merge with existing ID...]

2.  **Classification Check:** Is the prefix (e.g., OCP-BM) correct according to `adr_prefix_dictionary.md`? Or does it fit better in another domain (e.g., OCP-NET)?

    - _Verdict:_ [Correct / Incorrect]
    - _Action:_ [Keep / Move to prefix...]

3.  **Quality/Exclusion Check:** Does it violate any rules in `adr_exclusions.md`? Is it a "Right vs Wrong" configuration choice instead of a valid architecture strategy?

    - _Verdict:_ [Valid / Invalid]

4.  **Placement:** If valid, where exactly should it go in the target file to maintain "General -> Specific" ordering?
    - _Recommendation:_ Insert after [Existing ID/Title] and before [Existing ID/Title].

---

**[PASTE CANDIDATE ADR HERE]**
