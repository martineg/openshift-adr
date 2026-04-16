# Architect Workflow: Using ADR Templates in Customer Engagements

This document describes how architects use the ADR Template Repository during customer engagements.

---

## Overview

The ADR Template Repository contains **291 pre-defined ADR templates** across 19 Red Hat products. Architects use these templates to:
1. Prepare for design workshops
2. Facilitate architectural decision-making with customers
3. Document decisions in customer design documents

**Key Distinction:**
- **ADR Templates** (this repository): Reusable patterns for common architectural decisions
- **Customer ADR Instances**: Completed ADRs specific to a customer engagement (go in design documents)

---

## The 4-Phase Workflow

### Phase 1: PRE-ENGAGEMENT PREPARATION (Before Workshop)

**What the architect does:**
1. Identifies which Red Hat products the customer will use
2. Selects relevant ADR templates from this repository
3. Creates a customer-specific ADR pack
4. Reviews templates to prepare for workshop facilitation

**Current manual process:**
```bash
# 1. Clone the ADR template repository
git clone https://github.com/redhat-ai-services/openshift-adr.git

# 2. Manually identify relevant templates
# - Browse /adr_templates/ directory
# - Read OCP-BASE.md, OCP-NET.md, RHOAI-SM.md, etc.
# - Copy relevant ADR templates to customer folder

# 3. Manually create customer folder
mkdir ACME-Corp-ADRs/
cp selected-templates/*.md ACME-Corp-ADRs/
```

**Automated process (RECOMMENDED):**
```bash
# Generate customer ADR pack in Google Docs (fast - 4-11 seconds)
python scripts/customer_adrs.py generate \
    --customer "ACME Corp" \
    --products "OCP-BASE,OCP-NET,RHOAI-SM" \
    --engagement-date "2026-03-10" \
    --architect "Jane Smith"

# Output: Google Doc URL for real-time collaboration
# Example: https://docs.google.com/document/d/ABC123/edit

# OR generate local markdown files (offline mode)
python scripts/customer_adrs.py generate \
    --customer "ACME Corp" \
    --products "OCP-BASE,OCP-NET,RHOAI-SM" \
    --local

# Output directory:
#   ./acme-corp-ADRs/
#   ├── metadata.yaml (customer name, date, products)
#   ├── OCP-BASE-01-cluster-topology.md
#   ├── OCP-BASE-02-sizing-strategy.md
#   ├── OCP-NET-01-network-topology.md
#   └── ... (all templates for selected products)
```

**What gets generated:**
- Google Doc with all ADR templates in structured tables
- Yellow highlighting on #TODO# markers
- Red cleanup instructions for non-selected alternatives
- Nested table for "Agreeing Parties" (Person/Role columns)
- Product headings and proper formatting
- Everything remains as #TODO# (filled during workshop)

**Time estimate:** 4-11 seconds (Google Docs) vs. 2 hours (manual)

---

### Phase 2: WORKSHOP FACILITATION (During Design Workshop)

**What the architect does:**
1. Present each architectural question from templates
2. Explain alternatives (pros/cons from template)
3. Capture customer's decision on Miro/paper
4. Note agreeing parties (names and roles)
5. Mark which ADRs were discussed vs. deferred

**During the workshop:**
- Templates serve as **facilitation guide**
- Architect reads "Architectural Question" to customer
- Architect explains "Alternatives" with "Justification" and "Implications"
- Customer makes decision
- Decision captured on Miro/whiteboard/paper

**After each session:**
```bash
# Update customer ADR files with decisions
# (Manual editing during/after workshop)

vim ACME-Corp-ADRs/OCP-BASE-01-cluster-topology.md
# Change: **Decision** #TODO#
# To:     **Decision** Alternative 2: Prod/Non-Prod Split

# Fill in agreeing parties
# Change: Person: #TODO#, Role: Enterprise Architect
# To:     Person: John Smith, Role: Enterprise Architect
```

**Time estimate per ADR:** 5 minutes to facilitate + 5 minutes to document = 10 minutes total

**For 53 RHOAI ADRs:** ~9 hours of workshop time (spread across multiple sessions)

---

### Phase 3: DESIGN DOCUMENTATION (After Workshop)

**What the architect does:**
1. Finalize all customer ADR instances
2. Export to Google Docs format
3. Insert into customer design document
4. Cross-reference with HLD diagrams

**Current manual process:**
```bash
# 1. Copy each ADR manually into Google Doc
# Open each .md file
# Copy content
# Paste into design document
# Format manually (headings, bullets, etc.)
# Repeat 53 times for RHOAI...

# 2. Create table of contents manually
# List all ADRs
# Create hyperlinks
# Organize by category
```

**Automated process (TO BE IMPLEMENTED):**
```bash
# Check completion status first
python scripts/customer_adrs.py check ./ACME-Corp-ADRs/

# Output:
#   ✅ 45 ADRs completed (no #TODO# markers)
#   ⏳ 8 ADRs partially complete (has #TODO#)
#   ⏭️ 20 ADRs deferred (not discussed)
#
#   Missing agreeing parties: OCP-NET-05, OCP-SEC-02
#   Missing decisions: OCP-BASE-12

# Export completed ADRs to Google Doc
python scripts/customer_adrs.py export \
    --input "./ACME-Corp-ADRs/" \
    --customer "ACME Corp" \
    --output-format "google-doc" \
    --create-toc

# Output:
#   ✅ Created Google Doc: "ACME Corp - Architecture Decisions"
#   🔗 URL: https://docs.google.com/document/d/ABC123.../edit
#
#   Document structure:
#   - Table of Contents (45 ADRs with clickable links)
#   - Section 1: Platform Strategy (15 ADRs)
#   - Section 2: Networking (12 ADRs)
#   - Section 3: AI/ML (18 ADRs)
#
#   Ready to copy into design document Section 5.
```

**Alternative: Insert directly into design doc template**
```bash
# Insert into existing design document
python scripts/customer_adrs.py export \
    --input "./ACME-Corp-ADRs/" \
    --design-doc-id "XYZ789..." \
    --section "5. Architecture Decisions" \
    --insert

# Output:
#   ✅ Inserted 45 ADRs into design document
#   ✅ Created table of contents
#   ✅ Applied Red Hat formatting
#   🔗 URL: https://docs.google.com/document/d/XYZ789.../edit
```

**Time estimate:** 10 minutes (automated) vs. 4 hours (manual for 53 ADRs)

---

### Phase 4: HANDOVER TO CONSULTANT (End of Design Phase)

**What the architect does:**
1. Review completed design document with ADRs
2. Handover to implementation consultant
3. Consultant has full context for "why" decisions were made

**What consultant receives:**
- Design document with ADRs section
- Each ADR shows:
  - ✅ What question was answered
  - ✅ What alternatives were considered
  - ✅ Why the decision was made
  - ✅ What the implications are
  - ✅ Who agreed to it

**Consultant can:**
- Understand rationale without asking architect
- Reference ADRs during implementation
- Validate implementation matches decisions
- Answer customer questions about "why"

**Time saved:** Eliminates constant "why did we decide X?" clarification meetings

---

## Workflow Summary Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: PREPARATION (Before Workshop)                         │
├─────────────────────────────────────────────────────────────────┤
│ 1. Architect identifies products (OCP, RHOAI, etc.)            │
│ 2. Run: generate_customer_adrs.py --products "..."             │
│ 3. Output: Customer ADR pack with 53 templates                 │
│ 4. Templates have #TODO# placeholders                          │
│ Time: 15 minutes                                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: WORKSHOP (Facilitation)                               │
├─────────────────────────────────────────────────────────────────┤
│ 1. Present each ADR template as architectural question         │
│ 2. Explain alternatives from template                          │
│ 3. Customer makes decision (captured on Miro)                  │
│ 4. Architect fills Decision + Agreeing Parties fields          │
│ 5. Repeat for each ADR (5 min facilitation + 5 min document)   │
│ Time: ~9 hours for 53 ADRs (multiple workshop sessions)        │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: DOCUMENTATION (Export to Design Doc)                  │
├─────────────────────────────────────────────────────────────────┤
│ 1. Run: check_adr_completion.py (verify all #TODO# filled)     │
│ 2. Run: export_to_google_doc.py --output-format google-doc     │
│ 3. Output: Google Doc with 53 formatted ADRs + TOC             │
│ 4. Copy into customer design document Section 5                │
│ Time: 10 minutes (vs. 4 hours manual)                          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: HANDOVER (To Implementation Consultant)               │
├─────────────────────────────────────────────────────────────────┤
│ 1. Consultant receives design doc with ADR section             │
│ 2. Full context: questions, alternatives, decisions, rationale │
│ 3. Implementation proceeds with zero "why?" clarifications     │
│ 4. Customer can audit decisions 6 months later                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Metrics

| Metric | Without Automation | With Automation | Savings |
|--------|-------------------|-----------------|---------|
| **Preparation** | 2 hours (manual copy) | 15 minutes | 1h 45m |
| **Workshop** | 10 min/ADR × 53 = 9 hours | 10 min/ADR × 53 = 9 hours | 0 (same) |
| **Documentation** | 4 hours (manual export) | 10 minutes | 3h 50m |
| **Total per engagement** | ~15 hours | ~10 hours | **5 hours saved** |

**Per architect per year:**
- 10 engagements/year × 5 hours saved = **50 hours/year saved**
- 50 hours/year = **1.25 weeks** of additional billable time

---

## ADR Template Selection Guide

Not all templates are relevant to every engagement. Here's how architects select:

### By Product Category

**OpenShift Container Platform (OCP-*):**
- **OCP-BASE** (15 ADRs): Always required - covers topology, sizing, compliance
- **OCP-BM** (58 ADRs): Only if bare metal installation (not for cloud/VSphere)
- **OCP-NET** (44 ADRs): Required for custom networking (skip if defaults acceptable)
- **OCP-SEC** (19 ADRs): Required if security requirements beyond defaults
- **OCP-STOR** (7 ADRs): Required if persistent storage needed

**AI/ML Platforms:**
- **RHOAI-SM** (53 ADRs): Complete set for OpenShift AI deployments
- **NVIDIA-GPU** (9 ADRs): Only if GPU workloads planned

**Platform Services:**
- **GITOPS** (6 ADRs): If using GitOps methodology
- **PIPELINES** (8 ADRs): If CI/CD pipelines needed
- **VIRT** (7 ADRs): If virtualization workloads

### Typical Engagement Profiles

**Profile 1: Basic OCP**
- Products: OCP-BASE, OCP-NET, OCP-SEC
- ADRs: ~40 total
- Workshop time: ~7 hours

**Profile 2: OCP + AI/ML**
- Products: OCP-BASE, OCP-NET, RHOAI-SM, NVIDIA-GPU
- ADRs: ~90 total
- Workshop time: ~15 hours (split across multiple sessions)

**Profile 3: Full Stack**
- Products: All OCP-*, RHOAI-SM, GITOPS, PIPELINES
- ADRs: ~150 total
- Workshop time: ~25 hours (1 week of workshops)

---

## Success Criteria

An engagement is successful when:

1. ✅ All relevant ADR templates selected during preparation
2. ✅ All ADRs discussed during workshops (or consciously deferred)
3. ✅ Zero #TODO# markers in final ADR instances
4. ✅ All agreeing parties documented with real names
5. ✅ ADRs exported to design document Section 5
6. ✅ Consultant handover includes complete ADR context
7. ✅ Customer can audit decisions 6+ months later

---

## Common Pitfalls

**Pitfall 1: Selecting too many ADRs**
- **Problem:** Trying to cover all 291 templates overwhelms customer
- **Solution:** Start with OCP-BASE (15 ADRs) then add domain-specific as needed

**Pitfall 2: Not filling #TODO# during workshop**
- **Problem:** Architect forgets details, must schedule follow-up
- **Solution:** Fill Decision + Agreeing Parties immediately after each ADR discussion

**Pitfall 3: Manual copy-paste to design doc**
- **Problem:** 4 hours of error-prone formatting work
- **Solution:** Use export_to_google_doc.py automation

**Pitfall 4: Treating templates as instances**
- **Problem:** Modifying template repository instead of creating customer instances
- **Solution:** Always use generate_customer_adrs.py to create separate customer pack

**Pitfall 5: Missing ADR for a decision that comes up in workshop**
- **Problem:** Customer raises an architectural decision not covered by existing templates
- **Solution:** Note it during the workshop; after the engagement use the `add-adr` skill in Claude Code to contribute it back to the template library with proper governance validation

---

## Next Steps

**For this document:**
1. Review workflow accuracy with architects
2. Identify additional pain points
3. Prioritize automation development

**For automation:**
1. Build generate_customer_adrs.py (Phase 1 automation)
2. Build check_adr_completion.py (Phase 3 validation)
3. Build export_to_google_doc.py (Phase 3 automation)
