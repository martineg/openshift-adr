# Architecture Decision Records (ADR) Repository

**291 ADR templates for OpenShift and Red Hat product consulting engagements**

This repository provides:
- **ADR Templates**: 291 pre-defined architectural decision records across 19 products
- **Customer ADR Workflow**: Automated tools for generating customer-specific ADR packs
- **Governance Rules**: Quality standards and validation for consistent ADRs

**Documentation:**
- **For Users (Architects):** [SETUP.md](SETUP.md) → [USER_MANUAL.md](USER_MANUAL.md)
- **For Maintainers:** [MAINTENANCE.md](MAINTENANCE.md)
- **Complete Index:** [docs/README.md](docs/README.md)

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
/adr_templates/         # 291 ADR templates (19 products)
  ├── OCP-BASE.md       # Cross-cutting platform (15 ADRs)
  ├── OCP-NET.md        # Networking (44 ADRs)
  ├── OCP-BM.md         # Bare metal installation (58 ADRs)
  ├── RHOAI-SM.md       # OpenShift AI (53 ADRs)
  └── ...               # 15 more product files

/dictionaries/          # Governance and validation
  ├── adr_governance_rules.md        # Quality rules
  ├── adr_prefix_dictionary.md       # Product codes
  ├── adr_parties_role_dictionnary.md # Standard roles
  └── adr_exclusions.md              # Forbidden topics

/scripts/               # Automation tools
  ├── customer_adrs.py  # Customer ADR workflow
  ├── renumber_adrs.py  # ADR renumbering
  ├── split_pdf.py      # PDF utilities
  └── update_adrs.py    # Template updates

/docs/                  # Documentation
  ├── setup/           # Installation guides
  ├── usage/           # User workflows
  └── development/     # Technical specs

/tests/                 # Automated tests
  └── test_customer_adrs.py # Non-regression tests

BUILD.md               # Setup instructions
RUN.md                 # Usage guide
USER_MANUAL.md         # Complete user manual
CLAUDE.md              # AI assistant instructions
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

## Quick Start

### 1. Setup (5 minutes)

```bash
# Clone repository
git clone <repository-url>
cd adr

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-google.txt  # Optional: for Google Docs

# Run tests
python3 tests/test_customer_adrs.py
```

**See [SETUP.md](SETUP.md) for detailed installation instructions**

### 2. Generate Customer ADR Pack

```bash
# Interactive mode
./run_customer_adrs.sh

# Non-interactive
python3 scripts/customer_adrs.py generate \
    --customer "ACME Corp" \
    --products "OCP-BASE,OCP-NET,RHOAI-SM"
```

**Output:** Google Doc URL (online) or local directory (offline)

### 3. Conduct Workshop

- Share Google Doc with customer stakeholders
- Project on screen during workshop
- Fill **Decision** and **Agreeing Parties** collaboratively
- Real-time updates visible to all

### 4. Validate and Export

```bash
# Check completion
./run_customer_adrs.sh check "<google-doc-url>"

# Export to design document (markdown backup)
./run_customer_adrs.sh export "<google-doc-url>"
```

**See [USER_MANUAL.md](USER_MANUAL.md) for complete usage guide**

---

## Features

### Customer ADR Workflow
- ✅ **Google Docs Integration** - Real-time collaboration during workshops
- ✅ **Ultra-Fast Generation** - 128 ADRs in 15 seconds (HTML conversion approach)
- ✅ **Native Document Outline Navigation** - Instant access to all ADRs via sidebar
- ✅ **Progress Tracking** - Checkbox in each ADR heading for visual progress
- ✅ **Offline Mode** - Works without internet or Google account
- ✅ **Automated Validation** - Check completion before export
- ✅ **Multiple Export Formats** - Markdown, HTML with Red Hat styling
- ✅ **Customer Data Protection** - Never commits customer ADRs to git

### Template Management
- ✅ **291 ADR Templates** - Covering 19 Red Hat products
- ✅ **Automated Renumbering** - Keep ADR IDs sequential
- ✅ **Version Updates** - Tools for updating templates with new product versions
- ✅ **Quality Governance** - Validation rules and standards

### Documentation Highlights
- **Document Outline Navigation** - Hierarchical sidebar for instant ADR access
- **Progress Tracking Checkboxes** - Track completion directly in ADR headings (☐ → ☑)
- **Navigation Banner** - Clear instructions for desktop and mobile users
- **Yellow #TODO# Highlighting** - Visual indicators for incomplete fields
- **Nested Agreeing Parties Table** - Clean Person/Role columns
- **Red Cleanup Instructions** - Guidance for removing non-selected alternatives
- **Bold Markdown Processing** - Professional formatting in Google Docs
- **10pt Table Font** - Consistent, readable formatting
- **2-Column Tables** - Field labels with gray background

---

## Maintenance Scripts

### For Repository Maintainers

**Renumber ADRs after changes:**
```bash
python3 scripts/renumber_adrs.py OCP-NET
```

**Update templates for new product versions:**
```bash
# See docs/development/ for complete workflow
python3 scripts/update_adrs.py RHOAI-SM
```

**Run automated tests:**
```bash
python3 tests/test_customer_adrs.py
```

---

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

## Product Coverage

**291 ADRs across 19 products:**

| Product | ADRs | Product | ADRs |
|---------|------|---------|------|
| OCP-BM | 58 | RHOAI-SM | 53 |
| OCP-NET | 44 | OCP-SEC | 19 |
| OCP-BASE | 15 | OCP-MGT | 12 |
| ODF | 9 | NVIDIA-GPU | 9 |
| TRACING | 8 | PIPELINES | 8 |
| OCP-OSP | 8 | VIRT | 7 |
| OCP-STOR | 7 | LOG | 7 |
| OCP-MON | 6 | OCP-HCP | 6 |
| NETOBSERV | 6 | GITOPS | 6 |
| POWERMON | 3 | | |

## Why ADRs Matter

**The Problem**: Architects facilitate workshops and capture decisions on Miro/paper, but these captures aren't formalized into design documents. Workshop outputs vanish. Consultants implement without context.

**The Solution**: ADRs bridge three gaps:
1. **Workshop → Design**: Formalize Miro captures into permanent documentation
2. **Architect → Consultant**: Provide full context for implementation
3. **Design → Operations**: Create permanent record for future audits

**The Opportunity**: Just 5 minutes per ADR transforms ephemeral workshop captures into complete design deliverables with smooth handover and reduced disputes.

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
