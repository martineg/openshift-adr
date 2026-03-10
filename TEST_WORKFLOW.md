# Complete Customer ADR Workflow Test

This document demonstrates the end-to-end workflow with all three subcommands.

## Test Scenario

Customer: "Demo Corp"
Products: OCP-BASE (15 ADRs)
Workflow stages: Generate → Fill → Check → Export

---

## Step 1: Generate Customer ADR Pack

```bash
python scripts/customer_adrs.py generate \
    --customer "Demo Corp" \
    --products "OCP-BASE" \
    --output "./demo-corp-ADRs/"
```

**Output:**
```
================================================================================
Generating ADR pack for Demo Corp
================================================================================

📄 Processing OCP-BASE...

📊 Generated metadata.yaml
📖 Generated README.md

================================================================================
✅ Generated ADR pack for Demo Corp
================================================================================

📁 Output: demo-corp-ADRs/
📊 Total ADRs: 15
   - OCP-BASE: 15
⏱️  Estimated workshop time: ~2 hours
📖 Next: Review demo-corp-ADRs/README.md for instructions
```

**Files Created:**
```
demo-corp-ADRs/
├── metadata.yaml
├── README.md
├── OCP-BASE-01-environment-isolation-strategy.md
├── OCP-BASE-02-cloud-model.md
├── ... (13 more ADRs)
```

---

## Step 2: Check Initial State (All Incomplete)

```bash
python scripts/customer_adrs.py check demo-corp-ADRs/
```

**Output:**
```
================================================================================
ADR Completion Report for Demo Corp
================================================================================

✅ Completed: 0 ADRs (no #TODO# markers)
⏳ Incomplete: 0 ADRs (has #TODO# or issues)
⏭️  Not Discussed: 15 ADRs (entire ADR is #TODO#)

Not Discussed (can be excluded from export using --exclude-not-discussed):
--------------------------------------------------------------------------------
  - OCP-BASE: Environment Isolation Strategy
  - OCP-BASE: Cloud model
  - OCP-BASE: Internet Connectivity Model
  ... and 12 more

Summary:
--------------------------------------------------------------------------------
⚠️  No ADRs have been discussed yet (all are #TODO#)

Next steps:
  1. Conduct design workshops
  2. Fill Decision and Agreeing Parties fields
  3. Re-run: python scripts/customer_adrs.py check demo-corp-ADRs
```

---

## Step 3: Simulate Workshop (Fill Some ADRs)

Manually edit files to simulate workshop:

**Complete ADR #1:**
```bash
# Fill Decision
sed -i 's|#TODO: Document the decision.#|Prod/Non-Prod Split Model|' \
    demo-corp-ADRs/OCP-BASE-01-environment-isolation-strategy.md

# Fill all Agreeing Parties
sed -i 's/#TODO# (Demo Corp)/John Smith (Demo Corp)/;
        s/#TODO# (Demo Corp)/Jane Doe (Demo Corp)/;
        s/#TODO# (Demo Corp)/Bob Wilson (Demo Corp)/;
        s/#TODO# (Demo Corp)/Alice Johnson (Demo Corp)/' \
    demo-corp-ADRs/OCP-BASE-01-environment-isolation-strategy.md
```

**Partially Fill ADR #2:**
```bash
# Fill Decision only (leave Agreeing Parties incomplete)
sed -i 's|#TODO: Document the decision.#|Private Cloud Model|' \
    demo-corp-ADRs/OCP-BASE-02-cloud-model.md
```

**Leave Others Untouched:** ADRs #3-15 remain as #TODO#

---

## Step 4: Check Mixed State

```bash
python scripts/customer_adrs.py check demo-corp-ADRs/
```

**Output:**
```
================================================================================
ADR Completion Report for Demo Corp
================================================================================

✅ Completed: 1 ADRs (no #TODO# markers)
⏳ Incomplete: 1 ADRs (has #TODO# or issues)
⏭️  Not Discussed: 13 ADRs (entire ADR is #TODO#)

Incomplete ADRs:
--------------------------------------------------------------------------------

OCP-BASE: Cloud model
  ❌ Agreeing Parties incomplete

Not Discussed (can be excluded from export using --exclude-not-discussed):
--------------------------------------------------------------------------------
  - OCP-BASE: Internet Connectivity Model
  - OCP-BASE: Mirrored images registry (Disconnected Environments)
  ... and 11 more

Summary:
--------------------------------------------------------------------------------
❌ Not ready: 1 incomplete ADR(s) must be completed first

Next steps:
  1. Review incomplete ADRs listed above
  2. Fill missing Decision fields
  3. Complete Agreeing Parties sections
  4. Re-run: python scripts/customer_adrs.py check demo-corp-ADRs
```

---

## Step 5: Check with JSON Output (for CI/CD)

```bash
python scripts/customer_adrs.py check demo-corp-ADRs/ --format json
```

**Output:**
```json
{
  "customer": "Demo Corp",
  "total_adrs": 15,
  "completed": 1,
  "incomplete": 1,
  "not_discussed": 13,
  "ready_for_export": false,
  "completed_adrs": [
    {
      "id": "OCP-BASE",
      "title": "Environment Isolation Strategy"
    }
  ],
  "incomplete_adrs": [
    {
      "id": "OCP-BASE",
      "title": "Cloud model",
      "filename": "OCP-BASE-02-cloud-model.md",
      "issues": ["Agreeing Parties incomplete"]
    }
  ],
  "not_discussed_adrs": [
    {"id": "OCP-BASE", "title": "Internet Connectivity Model"},
    ...
  ]
}
```

---

## Step 6: Export to Markdown (Include All)

```bash
python scripts/customer_adrs.py export \
    --input demo-corp-ADRs/ \
    --output-format markdown
```

**Output:**
```
================================================================================
✅ Export to Markdown Complete
================================================================================

📄 Output: demo-corp-ADRs-export.md
📊 Total ADRs: 15

💡 Open with: cat demo-corp-ADRs-export.md
```

**File Generated:** `demo-corp-ADRs-export.md`
- Complete ADRs: Fully documented
- Incomplete ADRs: Shows partial completion
- Not Discussed: Included with #TODO# placeholders

---

## Step 7: Export to Markdown (Exclude Not Discussed)

```bash
python scripts/customer_adrs.py export \
    --input demo-corp-ADRs/ \
    --output-format markdown \
    --exclude-not-discussed
```

**Output:**
```
================================================================================
✅ Export to Markdown Complete
================================================================================

📄 Output: demo-corp-ADRs-export.md
📊 Total ADRs: 2

💡 Open with: cat demo-corp-ADRs-export.md
```

**Result:** Only 2 ADRs exported (1 complete + 1 incomplete)

---

## Step 8: Export to HTML

```bash
python scripts/customer_adrs.py export \
    --input demo-corp-ADRs/ \
    --output-format html \
    --exclude-not-discussed
```

**Output:**
```
================================================================================
✅ Export to HTML Complete
================================================================================

📄 Output: demo-corp-ADRs-export.html
📊 Total ADRs: 2

💡 Open with: open demo-corp-ADRs-export.html
```

**HTML Features:**
- Red Hat styling (red header with #c00)
- Table of contents with anchor links
- Responsive design
- Professional appearance
- Ready for browser or Confluence

---

## Summary

### Complete Workflow

```bash
# 1. Generate ADR pack
python scripts/customer_adrs.py generate --customer "X" --products "Y,Z"

# 2. Conduct workshops (fill ADRs manually)

# 3. Check completion
python scripts/customer_adrs.py check ./X-ADRs/

# 4. Export when ready
python scripts/customer_adrs.py export --input ./X-ADRs/ --output-format markdown
```

### Key Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `generate` | Create ADR pack from templates | Directory with ADR files |
| `check` | Validate completion | Text/JSON/HTML report |
| `export` | Export to document format | Markdown/HTML file |

### Success Criteria

✅ **Generate:** Creates customer-specific ADR pack in <1 minute
✅ **Check:** Validates 100+ ADRs in <2 seconds
✅ **Export:** Generates formatted document in <3 seconds
✅ **Total Time Saved:** 5+ hours per engagement

### Next Steps

1. Fill remaining Demo Corp ADRs (13 more)
2. Re-check until all complete
3. Export final version to design document
4. Future: Implement Google Docs API integration
