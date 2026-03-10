# Architecture Decision Records (ADR) Repository

This repository contains Architecture Decision Records for Red Hat consulting engagements, documenting strategic architectural choices for OpenShift Container Platform and related products.

## What Are ADRs?

Architecture Decision Records (ADRs) document strategic choices between valid architecture alternatives during design phases in consulting engagements. ADRs capture:

- **What**: The architectural question being answered
- **Why**: The issue or problem driving the decision
- **How**: Valid alternatives (2+ viable options)
- **Justification**: Why choose each alternative
- **Implications**: Consequences, trade-offs, and risks
- **Who**: Agreeing parties (customer stakeholders + Red Hat)

**ADRs are NOT configuration checklists.** They document real architectural decisions where multiple valid alternatives exist.

## Repository Structure

```
/adr/                   # ADR markdown files by product
  ├── OCP-BASE.md       # Cross-cutting platform decisions
  ├── OCP-BM.md         # Bare metal and Day 0
  ├── OCP-NET.md        # Networking decisions
  ├── OCP-SEC.md        # Security decisions
  ├── OCP-STOR.md       # Storage decisions
  ├── RHOAI-SM.md       # OpenShift AI Self-Managed
  ├── GITOPS.md         # GitOps decisions
  └── ...

/dictionaries/          # Governance and reference files
  ├── adr_governance_rules.md        # Validation rules
  ├── adr_prefix_dictionary.md       # Product prefix codes
  ├── adr_parties_role_dictionnary.md # Standardized roles
  └── adr_exclusions.md              # Forbidden topics

/scripts/               # Utility scripts
  ├── renumber_adrs.py  # Renumber ADRs sequentially
  └── split_pdf.py      # Split large PDF docs

/presentation_scripts/  # Google Slides presentation tools
```

## ADR Structure

Each ADR follows this template:

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

## Using This Repository

### For Architects

During design workshops:

1. **Preparation**: Extract decision points from Red Hat documentation
2. **Workshop**: Present architectural questions, capture decisions (Miro/paper)
3. **Design**: Formalize captures into ADRs in design document
4. **Handover**: Provide consultants with complete context

**Time commitment**: 15-30 minutes per ADR to formalize workshop outputs

### For Consultants

When implementing:

1. Review ADRs in the design document
2. Understand the "why" behind each architectural choice
3. Reference ADRs when questions arise during implementation
4. Validate implementation matches agreed decisions

### Renumbering ADRs

After adding/removing ADRs, renumber them sequentially:

```bash
python scripts/renumber_adrs.py <PREFIX>

# Example:
python scripts/renumber_adrs.py OCP-NET
python scripts/renumber_adrs.py --dry-run OCP-BASE  # Preview changes
```

### Splitting Large PDF Documentation

```bash
python scripts/split_pdf.py <path_to_pdf> <max_size_mb>

# Example:
python scripts/split_pdf.py documentation.pdf 20
```

## Governance Rules

ADRs must follow strict quality rules (see `dictionaries/adr_governance_rules.md`):

### Scope Hierarchy
- **OCP-BASE**: Cross-cutting platform strategy (Topology, Sizing, Multi-site, Compliance)
- **OCP-BM**: Physical hardware, BIOS, firmware, OS installation (Day 0)
- **Domain Specifics** (OCP-NET, OCP-SEC, OCP-STOR, etc.): Day 2 configurations

### Valid vs Invalid ADRs
- ✅ **Valid**: Choice between 2+ supported, viable architectural strategies
- ❌ **Invalid**: "Correct Configuration vs. Misconfiguration" (unless specific exceptions apply)
- ❌ **Invalid**: Documenting constraints forced by another decision

### Allowed Exceptions
Document "right vs. wrong" decisions ONLY if they serve:
1. Deployment Guardrail (prevents installation failure)
2. Security Policy (explicitly forbid insecure defaults)
3. Risk Acceptance (document acceptance of known trade-offs)
4. Simplicity vs. Capability (procedural choice)
5. Platform-Specific Gaps (enable features off by default)
6. Backing Service Selection (how to back core components)

### Versioning Policy
- Document **current state only** for current target version
- **Never** mention specific version numbers (e.g., "4.12", "4.17")
- **Never** describe legacy behaviors or version history

### Exclusion Rules
Check `dictionaries/adr_exclusions.md` before creating/updating ADRs.

## File Naming Convention

- ADR files: Uppercase prefix with `.md` extension (e.g., `OCP-NET.md`)
- Individual ADRs: Format `PREFIX-NN` (e.g., `OCP-BASE-01`, `OCP-NET-15`)
- Numbers: Zero-padded to 2 digits

## Standard Roles

Use only standardized roles from `dictionaries/adr_parties_role_dictionnary.md`:
- Enterprise Architect
- Infrastructure Leader
- Network Expert
- Storage Expert
- Security Expert
- Operations Expert
- OCP Platform Owner
- DevOps Engineer
- AI/ML Platform Owner
- Lead Data Scientist
- MLOps Engineer

## Current Statistics

**291 documented architectural decisions** across:
- OpenShift Container Platform (OCP-BASE, OCP-BM, OCP-NET, OCP-SEC, OCP-STOR, etc.)
- Red Hat OpenShift AI Self-Managed (RHOAI-SM: 53 ADRs)
- GitOps
- Advanced Cluster Management
- And more...

## Why ADRs Matter

**The Problem**: Architects facilitate workshops and capture decisions on Miro/paper, but these captures aren't formalized into design documents. Workshop outputs vanish. Consultants implement without context.

**The Solution**: ADRs bridge three gaps:
1. **Workshop → Design**: Formalize Miro captures into permanent documentation
2. **Architect → Consultant**: Provide full context for implementation
3. **Design → Operations**: Create permanent record for future audits

**The Opportunity**: Just 15-30 minutes per ADR transforms ephemeral workshop captures into complete design deliverables with smooth handover and reduced disputes.

## Contributing

When creating or updating ADRs:

1. Follow the ADR template structure exactly
2. Check `dictionaries/adr_governance_rules.md` for quality rules
3. Verify prefix codes in `dictionaries/adr_prefix_dictionary.md`
4. Use standardized roles from `dictionaries/adr_parties_role_dictionnary.md`
5. Check exclusions in `dictionaries/adr_exclusions.md`
6. Renumber ADRs after changes using `scripts/renumber_adrs.py`

## License

This repository contains consulting deliverables for Red Hat customer engagements.
