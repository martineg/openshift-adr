# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an **ADR Template Repository** for OpenShift Container Platform and related Red Hat products. It contains 291 pre-defined ADR templates that architects use as starting points for customer engagements.

**Templates vs. Instances:**
- **Templates** (this repository): Reusable patterns for common architectural decisions
- **Customer ADR Instances** (design documents): Completed ADRs specific to a customer engagement

**Current Statistics**: 291 ADR templates across 19 products

## Repository Structure

- **`/adr_templates/`**: ADR markdown template files organized by product prefix
  - Each file contains multiple numbered ADR templates (e.g., `OCP-BASE-01`, `OCP-BASE-02`)
  - Naming: `OCP-BASE.md`, `OCP-NET.md`, `RHOAI-SM.md`, `GITOPS.md`, etc.

- **`/dictionaries/`**: Governance and reference files
  - `adr_governance_rules.md`: Strict validation rules for ADR quality
  - `adr_prefix_dictionary.md`: Maps products/topics to official prefix codes
  - `adr_parties_role_dictionnary.md`: Standardized roles for "Agreeing Parties"
  - `adr_exclusions.md`: Forbidden topics and false positive suppressions

- **`/scripts/`**: Automation utilities
  - `renumber_adrs.py`: Renumber ADRs sequentially after additions/removals
  - `split_pdf.py`: Split large PDF documentation files
  - `update_adrs.py`: Automated ADR updates using Claude API
  - `build_presentation.py`: Generate ADR presentation from Red Hat template

- **`/doc_downloader/`**: Documentation automation
  - `download_all_docs.sh`: Download Red Hat product documentation
  - `download_config.yaml`: Configuration for documentation URLs and versions

- **`UPDATE_GUIDE.md`**: Complete workflow for updating ADRs when product versions change

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

**Strictly enforce** these rules from `dictionaries/adr_governance_rules.md`:

### Scope Hierarchy
- **OCP-BASE**: Cross-cutting platform strategy (Topology, Sizing, Multi-site, Compliance)
- **OCP-BM**: Physical hardware, BIOS, firmware, OS installation (Day 0)
- **Domain Specifics** (OCP-NET, OCP-SEC, OCP-STOR, etc.): Day 2 configurations and operator settings

### Quality Rules
- **Valid ADR**: Choice between 2+ supported, viable architectural strategies
- **Invalid**: "Correct Configuration vs. Misconfiguration" (unless allowed exceptions apply)
- **Invalid**: Documenting constraints forced by another decision

### Allowed Exceptions
Document "right vs. wrong" decisions ONLY if they serve:
1. Deployment Guardrail (prevents installation failure)
2. Security Policy (explicitly forbid insecure defaults)
3. Risk Acceptance (document acceptance of known trade-offs)
4. Simplicity vs. Capability (procedural choice where complexity buys features)
5. Platform-Specific Gaps (enable features off by default)
6. Backing Service Selection (how to back core components)

### Versioning Policy
- Document **current state only** for current target version
- **Never** mention specific version numbers (e.g., "4.12", "4.17")
- **Never** describe legacy behaviors or version history

### Exclusion Rules
Check `dictionaries/adr_exclusions.md` before creating/updating ADRs.

## Common Commands

Commands are organized into two categories:

### RUN Commands (Architects Using Templates in Engagements)

**Generate Customer ADR Pack** (🚧 Coming soon)
```bash
# Create customer-specific ADR instances from templates
python scripts/customer_adrs.py generate \
    --customer "ACME Corp" \
    --products "OCP-BASE,OCP-NET,RHOAI-SM" \
    --output "./ACME-Corp-ADRs/"
```

**Check ADR Completion Status** (🚧 Coming soon)
```bash
# Verify all #TODO# markers filled before handover
python scripts/customer_adrs.py check ./ACME-Corp-ADRs/
```

**Export to Google Docs** (🚧 Coming soon)
```bash
# Export completed customer ADRs to design document
python scripts/customer_adrs.py export \
    --input "./ACME-Corp-ADRs/" \
    --output-format "google-doc"
```

See [ARCHITECT_WORKFLOW.md](ARCHITECT_WORKFLOW.md) for complete workflow.

---

### BUILD Commands (Maintaining the Template Repository)

**Update Templates for New Product Version**

```bash
# 1. Download new documentation
cd doc_downloader
vim download_config.yaml  # Update version numbers
./download_all_docs.sh

# 2. Analyze ADRs against new documentation
cd ..
export ANTHROPIC_API_KEY="your-api-key"
python scripts/update_adrs.py RHOAI-SM

# 3. Review generated report
cat RHOAI-SM-Analysis-Report.md

# 4. Apply changes manually to ADR file
vim adr_templates/RHOAI-SM.md

# 5. Renumber if ADRs were added/removed
python scripts/renumber_adrs.py RHOAI-SM
```

See `UPDATE_GUIDE.md` for complete workflow details.

**Renumber ADR Templates**

```bash
# After adding/removing templates in repository
python scripts/renumber_adrs.py <PREFIX>

# Examples:
python scripts/renumber_adrs.py OCP-NET
python scripts/renumber_adrs.py --dry-run OCP-BASE  # Preview changes
```

**Build ADR Presentation**

```bash
# Requires credentials.json and token.json (Google API)
python scripts/build_presentation.py

# Creates presentation from Red Hat template
# - 8 slides (title + 6 content + closing)
# - Includes 291 ADR repository statistics
# - Speaker notes for 10-minute delivery
```

### Split Large PDF Documentation

```bash
python scripts/split_pdf.py <path_to_pdf> <max_size_mb>

# Example:
python scripts/split_pdf.py documentation.pdf 20
```

## Automated Update Workflow

The `update_adrs.py` script uses Claude API to analyze ADRs against product documentation:

**What it does:**
1. Reads ADR template file (e.g., `adr_templates/RHOAI-SM.md`)
2. Reads governance rules and exclusions
3. Uses Claude to identify updates needed, removals recommended, new ADR templates suggested
4. Generates analysis report (e.g., `RHOAI-SM-Analysis-Report.md`)

**Prerequisites:**
- Product documentation in `docs/<product>/` (use doc_downloader)
- `ANTHROPIC_API_KEY` environment variable set
- `pip install anthropic`

**Human validation required:** Always review AI-generated recommendations before applying changes.

## Presentation Generation

The `build_presentation.py` script generates a complete ADR presentation:

**Architecture:**
- Copies Red Hat Consulting template (ID: `1B5s3eIrvbW7ZXDX0BH5qKb8b09pYudWyYPJUjw1ruQI`)
- Deletes unnecessary slides, keeps title + content template + closing
- Duplicates content template to create 6 content slides
- Populates slides with structured content (bullet levels 0/1/2)
- Applies formatting: bold headers, bullet nesting (disc/circle style)
- Adds speaker notes for 10-minute presentation

**Content structure format:**
```python
[
    {'text': 'Header text', 'level': 0, 'bold': True},   # No bullet
    {'text': 'Main point', 'level': 1, 'bold': False},   # Disc bullet (●)
    {'text': 'Sub-point', 'level': 2, 'bold': False},    # Circle bullet (○)
]
```

**Bullet formatting approach:**
1. Delete all existing bullets
2. Apply bold formatting where needed
3. Re-create bullets with `createParagraphBullets` API
4. Apply indentation (18pt for level 1, 54pt for level 2)

This "toggle" approach ensures consistent bullet alignment across all slides.

## File Naming Conventions

- ADR files: Uppercase prefix with `.md`: `OCP-NET.md`, `GITOPS.md`
- Individual ADRs: Format `PREFIX-NN`: `OCP-BASE-01`, `OCP-NET-15`
- Numbers: Zero-padded to 2 digits (01, 02, ..., 58)

## Standard Roles for Agreeing Parties

Use **only** these roles from `dictionaries/adr_parties_role_dictionnary.md`:
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

## Architecture Notes

### ADR Update Workflow
1. **Documentation Download**: `doc_downloader/` fetches PDFs from Red Hat docs site
2. **Analysis**: `update_adrs.py` uses Claude API to compare ADRs against current docs
3. **Report Generation**: Creates markdown report with specific changes needed
4. **Manual Application**: Human reviews and applies recommended changes
5. **Renumbering**: `renumber_adrs.py` ensures sequential numbering

### Presentation Generation Workflow
1. **Template Copy**: Uses Google Drive API to copy Red Hat template
2. **Slide Deletion**: Removes 129 template slides, keeps 3 (title, content, closing)
3. **Slide Duplication**: Creates 6 content slides from template
4. **Content Population**: Three-phase approach (delete text → insert text → format)
5. **Bullet Formatting**: Three-phase approach (delete bullets → format text → create bullets)
6. **Speaker Notes**: Adds complete sentences for natural delivery

### Time Estimates
- **Formalizing one ADR**: 5 minutes (workshop capture → design doc)
- **ADR analysis run**: 2-5 minutes (depends on file size and API)
- **Presentation build**: 30-60 seconds (full automation)
- **Updating ADRs for new version**: 15-30 minutes per product (download → analyze → review → apply)

## Common Pitfalls

### ADR Quality
- **Don't** create ADRs for configuration vs. misconfiguration (unless exceptions apply)
- **Don't** mention version numbers in ADR content
- **Do** check exclusions list before creating new ADRs
- **Do** ensure 2+ viable alternatives exist

### Presentation Formatting
- Google Slides API doesn't support `TEXT_AUTOFIT` - content must fit without shrinking
- `nestingLevel` field doesn't exist - use manual indentation instead
- Must delete bullets before re-creating for proper alignment
- Bold formatting must be applied after text insertion but before bullet creation

### Update Workflow
- Always download latest documentation before running analysis
- AI suggestions need human validation - false positives can occur
- Renumber after adding/removing ADRs to maintain sequential IDs
- Use `--dry-run` flag to preview renumbering changes

## Git Workflow Notes

- **Never commit**: `credentials.json`, `token.json`, `docs/` PDFs
- **Avoid committing**: `*SUMMARY*.md`, `*STATUS*.md`, `GITHUB_READY.md` (internal tracking files)
- **Always commit**: ADR changes, script updates, governance rule updates
- Commit messages should reference specific ADR IDs when applicable

## Integration Points

### Google Slides API
- Requires OAuth2 credentials (`credentials.json`)
- Token stored in `token.json` (auto-refreshed)
- Scopes: `presentations`, `drive`
- Template ID hardcoded in `build_presentation.py`

### Claude API
- Requires `ANTHROPIC_API_KEY` environment variable
- Model: `claude-sonnet-4-20250514`
- Max tokens: 8000 for analysis responses
- Used only in `update_adrs.py`

### Documentation Sources
- Red Hat documentation PDFs from `docs.redhat.com`
- URLs and versions configured in `doc_downloader/download_config.yaml`
- Downloaded to `docs/<product>/` (excluded from git)
