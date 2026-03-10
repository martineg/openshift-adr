# RUN Script Requirements Specification

This document defines the requirements for the automation script that architects use during customer engagements.

---

## Overview

**Purpose:** Automate the workflow of using ADR templates in customer engagements

**Implementation:** Single script with three subcommands for the 4-phase architect workflow:
- `customer_adrs.py generate` - Phase 1: Preparation
- `customer_adrs.py check` - Phase 3: Validation
- `customer_adrs.py export` - Phase 3: Documentation

**Key Constraint:** No customer ADR storage in git. Output is Google Docs only.

**Design Rationale:**
- Single entry point for all customer ADR operations
- Shared code for metadata reading, validation, error handling
- Familiar UX pattern (like `git`, `docker`, `gh` commands)
- `--help` discoverability for all subcommands

---

## Script: customer_adrs.py

### Global Options

Available for all subcommands:
- `--verbose` / `-v` - Verbose output
- `--help` / `-h` - Show help message

### Usage Pattern

```bash
python scripts/customer_adrs.py <subcommand> [options]
python scripts/customer_adrs.py --help  # Show all subcommands
python scripts/customer_adrs.py generate --help  # Show generate options
```

---

## Subcommand 1: generate

### Purpose
Generate customer-specific ADR pack from templates for workshop preparation.

### Inputs

**Required:**
- `--customer` - Customer organization name (e.g., "ACME Corp")
- `--products` - Comma-separated product list (e.g., "OCP-BASE,OCP-NET,RHOAI-SM")

**Optional:**
- `--output` - Output directory (default: `./{customer-slug}-ADRs/`)
- `--engagement-date` - Date for metadata (default: today)
- `--architect` - Architect name for metadata (default: git config user.name)

### Processing Logic

1. **Validate Inputs**
   - Check products exist in `/adr_templates/` directory
   - Verify customer name is not empty
   - Check output directory doesn't already exist (prevent overwrites)

2. **Read Templates**
   - For each product in `--products`:
     - Read `/adr_templates/{PRODUCT}.md`
     - Parse individual ADR sections (split on `## {PREFIX}-{NN}`)
     - Extract: Title, Question, Issue, Assumption, Alternatives, Justification, Implications, Agreeing Parties

3. **Pre-fill Customer Metadata**
   - Replace in "Agreeing Parties" section:
     - `Person: #TODO#` → `Person: #TODO# ({customer})`
   - Add metadata header to each ADR:
     ```markdown
     <!-- Generated for: {customer} -->
     <!-- Engagement Date: {date} -->
     <!-- Template Source: adr_templates/{PRODUCT}.md -->
     <!-- Template Version: {git-commit-sha} -->
     ```

4. **Create Output Structure**
   ```
   {customer-slug}-ADRs/
   ├── metadata.yaml
   ├── README.md
   ├── OCP-BASE-01-cluster-topology.md
   ├── OCP-BASE-02-sizing-strategy.md
   ├── OCP-NET-01-network-topology.md
   └── ... (all templates for selected products)
   ```

5. **Generate metadata.yaml**
   ```yaml
   customer: "ACME Corp"
   engagement_date: "2026-03-10"
   architect: "John Doe"
   products:
     - OCP-BASE
     - OCP-NET
     - RHOAI-SM
   template_repository: "https://github.com/redhat-ai-services/openshift-adr"
   template_version: "abc123def"  # git commit sha
   generated_date: "2026-03-10T14:30:00Z"
   total_adrs: 95
   ```

6. **Generate README.md**
   ```markdown
   # ADR Pack for {customer}

   Generated: {date}
   Products: {product-list}
   Total ADRs: {count}

   ## ADR List

   ### OCP-BASE (15 ADRs)
   - [OCP-BASE-01: Cluster Topology](OCP-BASE-01-cluster-topology.md)
   - [OCP-BASE-02: Sizing Strategy](OCP-BASE-02-sizing-strategy.md)
   - ...

   ### OCP-NET (44 ADRs)
   - ...

   ## Usage

   1. Review ADRs before workshop
   2. During workshop: Fill **Decision** and **Agreeing Parties** fields
   3. After workshop: Run check_adr_completion.py
   4. Export: Run export_to_google_doc.py
   ```

### Outputs

**Success:**
- Exit code: 0
- Creates directory with ADR files
- Prints summary:
  ```
  ✅ Generated ADR pack for ACME Corp
  📁 Output: ./ACME-Corp-ADRs/
  📊 Total ADRs: 95
     - OCP-BASE: 15
     - OCP-NET: 44
     - RHOAI-SM: 53
  ⏱️  Estimated workshop time: ~16 hours
  📖 Next: Review README.md for instructions
  ```

**Errors:**
- Exit code: 1
- Invalid product: "Product 'XYZ' not found in adr_templates/"
- Directory exists: "Output directory already exists. Use --force to overwrite"
- No products: "At least one product must be specified"

### Example Usage

```bash
# Generate ADR pack for RHOAI engagement
python scripts/customer_adrs.py generate \
    --customer "ACME Corp" \
    --products "OCP-BASE,RHOAI-SM" \
    --output "./ACME-Corp-ADRs/"

# Output:
#   ✅ Generated ADR pack for ACME Corp
#   📁 Output: ./ACME-Corp-ADRs/
#   📊 Total ADRs: 68
#      - OCP-BASE: 15
#      - RHOAI-SM: 53
#   ⏱️  Estimated workshop time: ~11 hours
```

---

## Subcommand 2: check

### Purpose
Validate customer ADR pack before export to ensure no #TODO# markers remain.

### Inputs

**Required:**
- `--input` - Customer ADR directory (e.g., "./ACME-Corp-ADRs/")

**Optional:**
- `--format` - Output format: `text` (default), `json`, `html`
- `--fail-on-incomplete` - Exit code 1 if any #TODO# found (for CI/CD)

### Processing Logic

1. **Read Customer ADR Pack**
   - Scan `{input}/*.md` files (excluding README.md)
   - Parse each ADR file

2. **Check for #TODO# Markers**
   - Search for: `#TODO#` (case-insensitive)
   - Track location: ADR ID, section (Decision vs. Agreeing Parties)

3. **Validate Agreeing Parties**
   - Check format: `Person: {name}, Role: {role}`
   - Verify name is not `#TODO#`
   - Verify role exists in `dictionaries/adr_parties_role_dictionnary.md`

4. **Generate Completion Report**

### Outputs

**Text Format (default):**
```
================================================================================
ADR Completion Report for ACME Corp
================================================================================

✅ Completed: 60 ADRs (no #TODO# markers)
⏳ Incomplete: 8 ADRs (has #TODO#)
⏭️  Not Discussed: 20 ADRs (entire ADR is #TODO#)

Incomplete ADRs:
────────────────────────────────────────────────────────────────────────────────
OCP-BASE-05: Network Topology
  ❌ Decision: #TODO# (not filled)
  ✅ Agreeing Parties: Complete

OCP-NET-12: Load Balancer Strategy
  ✅ Decision: Complete
  ❌ Agreeing Parties: Person: #TODO# (ACME Corp), Role: Network Expert

RHOAI-SM-23: Model Registry Configuration
  ❌ Decision: #TODO# (not filled)
  ❌ Agreeing Parties: Missing 2 agreeing parties

Not Discussed (can be excluded from export):
────────────────────────────────────────────────────────────────────────────────
OCP-BASE-12: Backup Strategy
OCP-NET-35: Service Mesh Integration
... (18 more)

Summary:
────────────────────────────────────────────────────────────────────────────────
Ready for export: ❌ (8 incomplete ADRs must be completed first)

Next steps:
1. Review incomplete ADRs listed above
2. Fill missing Decision fields
3. Complete Agreeing Parties sections
4. Re-run: python scripts/customer_adrs.py check ./ACME-Corp-ADRs/
```

**JSON Format (`--format json`):**
```json
{
  "customer": "ACME Corp",
  "total_adrs": 88,
  "completed": 60,
  "incomplete": 8,
  "not_discussed": 20,
  "ready_for_export": false,
  "incomplete_adrs": [
    {
      "file": "OCP-BASE-05-network-topology.md",
      "id": "OCP-BASE-05",
      "title": "Network Topology",
      "missing": ["Decision"]
    }
  ],
  "not_discussed_adrs": [
    "OCP-BASE-12",
    "OCP-NET-35"
  ]
}
```

**Exit Codes:**
- 0: All ADRs complete or `--fail-on-incomplete` not set
- 1: Incomplete ADRs found and `--fail-on-incomplete` set
- 2: Error reading directory

### Example Usage

```bash
# Check completion status
python scripts/customer_adrs.py check ./ACME-Corp-ADRs/

# For CI/CD pipeline
python scripts/customer_adrs.py check \
    ./ACME-Corp-ADRs/ \
    --fail-on-incomplete \
    --format json > completion-report.json
```

---

## Subcommand 3: export

### Purpose
Export completed customer ADRs to Google Docs format for insertion into design document.

### Inputs

**Required:**
- `--input` - Customer ADR directory (e.g., "./ACME-Corp-ADRs/")
- `--customer` - Customer name (or read from metadata.yaml)

**Optional:**
- `--output-format` - Format: `google-doc` (default), `markdown`, `html`
- `--exclude-not-discussed` - Skip ADRs with #TODO# in Decision field
- `--group-by` - Grouping: `product` (default), `category`, `none`
- `--create-toc` - Generate table of contents (default: true)

### Processing Logic

1. **Read Customer ADR Pack**
   - Load metadata.yaml
   - Read all ADR .md files
   - Filter out "not discussed" if `--exclude-not-discussed`

2. **Group ADRs**
   - By product (default): OCP-BASE, OCP-NET, RHOAI-SM
   - By category: Platform Strategy, Networking, AI/ML
   - None: Flat list

3. **Generate Google Doc**

### Google Docs Output Format

**Document Structure:**
```
Architecture Decisions - {Customer}
Generated: {date}

TABLE OF CONTENTS
├── 1. Platform Strategy (15 ADRs)
│   ├── OCP-BASE-01: Cluster Topology
│   ├── OCP-BASE-02: Sizing Strategy
│   └── ...
├── 2. Networking (44 ADRs)
│   ├── OCP-NET-01: Network Topology
│   └── ...
└── 3. AI/ML (53 ADRs)
    ├── RHOAI-SM-01: Update Channel Selection
    └── ...

────────────────────────────────────────────────────────────────────

1. PLATFORM STRATEGY

────────────────────────────────────────────────────────────────────

OCP-BASE-01: Cluster Topology

Architectural Question
  How should the OpenShift cluster topology be structured?

Issue or Problem
  Customer requires high availability and disaster recovery...

Assumption
  N/A

Alternatives
  • Single datacenter deployment
  • Multi-datacenter active/passive
  • Multi-datacenter active/active

Decision
  Multi-datacenter active/passive

Justification
  • Single datacenter: Quick to deploy but no DR capability
  • Active/passive: Balances complexity with DR requirements ✅
  • Active/active: Highest availability but requires network stretch

Implications
  • Active/passive:
    - Requires automated failover mechanism
    - RPO: 15 minutes, RTO: 30 minutes
    - Networking complexity: Medium

Agreeing Parties
  • Person: John Smith (ACME Corp), Role: Enterprise Architect
  • Person: Jane Doe (ACME Corp), Role: Infrastructure Leader
  • Person: Bob Wilson (Red Hat), Role: Principal Architect

────────────────────────────────────────────────────────────────────

OCP-BASE-02: Sizing Strategy
...
```

**Formatting Details:**
- **Heading 1**: Document title
- **Heading 2**: Section names (1. Platform Strategy, 2. Networking, etc.)
- **Heading 3**: ADR IDs and titles (OCP-BASE-01: Cluster Topology)
- **Bold**: Field names (Architectural Question, Decision, etc.)
- **Bullets**: Alternatives, Justification items, Agreeing Parties
- **Separators**: Horizontal rules between ADRs

4. **Create Google Doc via API**

**API Workflow:**
```python
# 1. Create new Google Doc
doc = service.documents().create(body={
    'title': f'Architecture Decisions - {customer}'
}).execute()

# 2. Build batch requests
requests = []
# Add title
# Add TOC with bookmarks
# Add section headers
# Add each ADR with formatting

# 3. Execute batch update
service.documents().batchUpdate(
    documentId=doc['documentId'],
    body={'requests': requests}
).execute()

# 4. Return URL
return doc['documentId']
```

### Outputs

**Success (Google Doc created):**
```
================================================================================
Export to Google Docs Complete
================================================================================

✅ Created Google Doc: "Architecture Decisions - ACME Corp"
🔗 URL: https://docs.google.com/document/d/ABC123.../edit

📊 Document Statistics:
   - Total ADRs: 68
   - Platform Strategy: 15 ADRs
   - AI/ML: 53 ADRs
   - Pages: ~45 pages

📋 Table of Contents: ✅ Generated (clickable links)
🎨 Formatting: ✅ Red Hat style applied

📝 Next Steps:
   1. Open the Google Doc above
   2. Review ADRs for accuracy
   3. Copy into your design document Section 5
   4. Manually merge with existing design content

⚠️  Note: This document is standalone. You must manually copy
    into your design document template.
```

**Alternative Outputs:**

**Markdown Format (`--output-format markdown`):**
- Saves to `{customer}-ADRs-export.md`
- Ready for copy/paste into any markdown editor

**HTML Format (`--output-format html`):**
- Saves to `{customer}-ADRs-export.html`
- Includes CSS styling
- Can be imported into Confluence, SharePoint, etc.

### Example Usage

```bash
# Export to Google Docs (default)
python scripts/customer_adrs.py export \
    --input "./ACME-Corp-ADRs/" \
    --customer "ACME Corp"

# Export to markdown (no Google API needed)
python scripts/customer_adrs.py export \
    --input "./ACME-Corp-ADRs/" \
    --customer "ACME Corp" \
    --output-format markdown

# Export excluding deferred ADRs
python scripts/customer_adrs.py export \
    --input "./ACME-Corp-ADRs/" \
    --customer "ACME Corp" \
    --exclude-not-discussed
```

---

## Dependencies

### Python Packages

```txt
# requirements.txt
PyYAML>=6.0              # metadata.yaml parsing
google-auth>=2.0         # Google API authentication
google-auth-oauthlib>=0.5
google-api-python-client>=2.0
```

### Google API Setup

**Required Scopes:**
```python
SCOPES = [
    'https://www.googleapis.com/auth/documents',  # Create/edit docs
    'https://www.googleapis.com/auth/drive'       # Create files in Drive
]
```

**Credentials:**
- `credentials.json` - OAuth2 client credentials (not in git)
- `token.json` - User token (auto-generated, not in git)

---

## Error Handling

### Common Errors

**Subcommand: generate**
- Template file not found → Clear message: "Template 'OCP-XYZ.md' not found in adr_templates/"
- Invalid product code → List valid products from adr_templates/
- Directory exists → Prompt: "Use --force to overwrite, or specify different --output"

**Subcommand: check**
- Directory not found → "ADR directory not found: ./path/"
- No ADR files → "No ADR markdown files found in ./path/"
- Invalid role → "Role 'XYZ' not in dictionaries/adr_parties_role_dictionnary.md"

**Subcommand: export**
- Google API auth failure → "Run: python scripts/customer_adrs.py setup-auth"
- Network error → Retry 3 times with exponential backoff
- Rate limit → Wait and retry with backoff
- Incomplete ADRs → Warn but continue: "Warning: 3 ADRs have #TODO# markers (use --exclude-not-discussed)"

**Global errors:**
- Invalid subcommand → Show available subcommands and usage
- Missing required arguments → Show subcommand-specific help

---

## Testing Requirements

### Unit Tests

**test_customer_adrs.py:**

Test `generate` subcommand:
- Test template parsing
- Test metadata generation
- Test pre-filling customer name
- Test invalid product codes
- Test directory creation

Test `check` subcommand:
- Test #TODO# detection
- Test agreeing parties validation
- Test JSON output format
- Test exit codes

Test `export` subcommand:
- Test markdown generation
- Test grouping (by product, category)
- Test TOC generation
- Mock Google API calls

Test shared utilities:
- Test metadata.yaml reading
- Test validation functions
- Test error handling

### Integration Tests

**test_full_workflow.sh:**
```bash
#!/bin/bash
# End-to-end test of all subcommands

# Generate
python scripts/customer_adrs.py generate \
    --customer "Test Corp" \
    --products "OCP-BASE" \
    --output "./test-output/"

# Manually fill one ADR
echo "Decision: Alternative 1" >> ./test-output/OCP-BASE-01-cluster-topology.md

# Check completion (should show incomplete)
python scripts/customer_adrs.py check ./test-output/

# Export to markdown
python scripts/customer_adrs.py export \
    --input "./test-output/" \
    --customer "Test Corp" \
    --output-format markdown

# Cleanup
rm -rf ./test-output/
```

---

## Performance Requirements

**Subcommand: generate**
- Process 291 templates: < 5 seconds
- Generate 100 ADR pack: < 10 seconds

**Subcommand: check**
- Scan 100 ADRs: < 2 seconds
- Generate report: < 1 second

**Subcommand: export**
- Generate markdown: < 3 seconds
- Create Google Doc: < 30 seconds (API latency)
- Document with 100 ADRs: < 60 seconds

**Script startup:**
- Import time: < 500ms
- Help display: < 100ms

---

## Future Enhancements (Out of Scope for V1)

1. **Interactive Mode**
   - `python scripts/customer_adrs.py generate --interactive`
   - Prompt for customer, products, etc.

2. **Product Selection Wizard**
   - Recommend products based on customer requirements
   - "Installing on bare metal? → Include OCP-BM"

3. **Direct Google Docs Insert**
   - Insert into existing design doc template
   - Find bookmark "{{ADR_SECTION_HERE}}" and replace

4. **ADR Template Versioning**
   - Track template changes over time
   - "Template updated since generation - review OCP-BASE-05"

5. **Export to Confluence/SharePoint**
   - Native API integration
   - No manual copy/paste needed

---

## Success Criteria

**V1 is complete when:**
1. ✅ Architect can generate ADR pack in < 1 minute (`customer_adrs.py generate`)
2. ✅ Architect can validate completion in < 30 seconds (`customer_adrs.py check`)
3. ✅ Architect can export to Google Docs in < 2 minutes (`customer_adrs.py export`)
4. ✅ Total automation saves 5+ hours per engagement
5. ✅ Zero customer ADR data stored in git (Google Docs only)
6. ✅ Script has comprehensive --help for all subcommands
7. ✅ README.md updated with usage examples
8. ✅ ARCHITECT_WORKFLOW.md references script

---

## Open Questions / Decisions Needed

1. **ADR File Naming in Pack**
   - Current: `OCP-BASE-01-cluster-topology.md` (prefix + number + slug)
   - Alternative: `OCP-BASE-01.md` (just prefix + number)
   - **Decision:** Use prefix + number + slug for clarity

2. **Google Doc Sharing**
   - Auto-share with customer email?
   - Or manual sharing after creation?
   - **Decision:** Manual sharing (architect controls access)

3. **Template Version Tracking**
   - Include git commit SHA in metadata?
   - Track when templates change after generation?
   - **Decision:** Include SHA, no active tracking after generation

4. **Not Discussed ADRs**
   - Export with #TODO# and mark as "Deferred"?
   - Or exclude completely from export?
   - **Decision:** Exclude by default, add --include-deferred flag

5. **Multiple Architects**
   - Support multiple architects per engagement?
   - **Decision:** Single architect per pack (simple V1)
