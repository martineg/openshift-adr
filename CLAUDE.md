# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an Architecture Decision Records (ADR) repository for OpenShift Container Platform and related Red Hat products. ADRs document strategic architectural choices between valid alternatives, not simple configuration decisions or right-vs-wrong choices (with specific exceptions).

## Repository Structure

- **`/adr/`**: ADR markdown files organized by product prefix (e.g., `OCP-BASE.md`, `OCP-NET.md`, `GITOPS.md`)
  - Each file contains multiple numbered ADRs for that topic area (e.g., `OCP-BASE-01`, `OCP-BASE-02`)

- **`/dictionaries/`**: Governance and reference files
  - `adr_governance_rules.md`: Strict validation rules for creating/updating/reviewing ADRs
  - `adr_prefix_dictionary.md`: Maps products/topics to their official prefix codes
  - `adr_parties_role_dictionnary.md`: Standardized roles for "Agreeing Parties" sections
  - `adr_exclusions.md`: Forbidden topics and false positive suppressions

- **`/prompts/`**: NotebookLM prompts for ADR maintenance
  - `adr-create.md`: Prompt for discovering new ADRs from documentation
  - `adr-update-review.md`: Prompt for reviewing existing ADRs for accuracy
  - Other specialized prompts for auditing and visibility checks

- **`/scripts/`**: Python utilities
  - `renumber_adrs.py`: Renumbers ADR IDs sequentially within a file
  - `split_pdf.py`: Splits large PDF documentation files

## ADR Structure Template

Each ADR follows this exact structure:

```markdown
## [PREFIX]-[NN]

**Title**
[Concise title]

**Architectural Question**
[The strategic question being answered]

**Issue or Problem**
[Why this decision is needed]

**Assumption**
[N/A or stated dependency]

**Alternatives**

- [Alternative 1]
- [Alternative 2]
- [Alternative 3]

**Decision**
#TODO: Document the decision.#

**Justification**

- **[Alternative 1]:** [Why choose this option]
- **[Alternative 2]:** [Why choose this option]

**Implications**

- **[Alternative 1]:** [Consequences/risks/requirements]
- **[Alternative 2]:** [Consequences/risks/requirements]

**Agreeing Parties**

- Person: #TODO#, Role: [Role from dictionary]
```

## Critical Governance Rules

When working with ADRs, **strictly enforce** these rules from `dictionaries/adr_governance_rules.md`:

### Scope Hierarchy
- **OCP-BASE**: Cross-cutting platform strategy (Topology, Sizing, Multi-site, Compliance)
- **OCP-BM**: Physical hardware, BIOS, firmware, OS installation (Day 0)
- **Domain Specifics** (OCP-NET, OCP-SEC, OCP-STOR, etc.): Day 2 configurations and operator settings

### Quality Rules
- **Valid ADR**: Choice between two or more supported, viable architectural strategies
- **Invalid**: "Correct Configuration vs. Misconfiguration" (unless it falls under allowed exceptions)
- **Invalid**: Documenting constraints that are forced by another decision

### Allowed Exceptions
Document "right vs. wrong" decisions ONLY if they serve:
1. Deployment Guardrail (prevents installation failure)
2. Security Policy (explicitly forbid insecure defaults)
3. Risk Acceptance (document acceptance of known trade-offs)
4. Simplicity vs. Capability (procedural choice where complexity buys features)
5. Platform-Specific Gaps (enable features off by default)
6. Backing Service Selection (how to back core components)

### Versioning Policy
- Document **current state only** for the current target version
- **Never** mention specific version numbers (e.g., "4.12", "4.17")
- **Never** describe legacy behaviors or version history

### Exclusion Rules
Check `dictionaries/adr_exclusions.md` before creating/updating ADRs. Forbidden topics include:
- Network Teaming (deprecated)
- Mixed/Hybrid IPAM strategies
- Default catalog source configurations in disconnected environments

## Common Commands

### Renumber ADRs
After adding/removing ADRs, renumber them sequentially:
```bash
python scripts/renumber_adrs.py <PREFIX>

# Example:
python scripts/renumber_adrs.py OCP-NET
python scripts/renumber_adrs.py --dry-run OCP-BASE  # Preview changes
```

### Split Large PDF Documentation
```bash
python scripts/split_pdf.py <path_to_pdf> <max_size_mb>

# Example:
python scripts/split_pdf.py documentation.pdf 20
```

## Workflow for ADR Maintenance

The repository uses a **NotebookLM-based workflow** with "Focused Notebooks":

1. Create a dedicated NotebookLM notebook for each topic
2. Upload ONLY relevant files: the ADR file, dictionaries, and official Red Hat documentation (PDFs)
3. Use prompts from `/prompts/` to review or create ADRs
4. The "Focused Notebook" strategy prevents noisy, unreliable results

**Note**: While the primary workflow uses NotebookLM, Claude Code can assist with:
- Formatting and structural consistency
- Renumbering ADRs
- Validating against governance rules
- Editing specific sections

## File Naming Convention

- ADR files use uppercase prefix with `.md` extension: `OCP-NET.md`, `GITOPS.md`
- Individual ADRs within files use format: `PREFIX-NN` (e.g., `OCP-BASE-01`, `OCP-NET-15`)
- Numbers are zero-padded to 2 digits

## Standard Roles for Agreeing Parties

Use only these standardized roles (from `dictionaries/adr_parties_role_dictionnary.md`):
- Enterprise Architect
- Infra Leader
- Network Expert
- Storage Expert
- Security Expert
- Operations Expert
- OCP Platform Owner
- DevOps Engineer
- AI/ML Platform Owner
- Lead Data Scientist
- MLOps Engineer
