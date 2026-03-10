# Interactive Script Demo

This shows what architects will see when running `./run_customer_adrs.sh`

## Example Session

```bash
$ ./run_customer_adrs.sh
```

```
================================================================================
  Customer ADR Workflow - Interactive Setup
================================================================================

ℹ️  Checking Python version...
✅ Python 3.14.3 detected
ℹ️  Checking PyYAML dependency...
✅ PyYAML installed
ℹ️  Checking repository structure...
✅ Repository structure verified

================================================================================
  Interactive Product Selection
================================================================================

Available ADR templates:

   1) GITOPS          (6 ADRs)
   2) LOG             (6 ADRs)
   3) NETOBSERV       (7 ADRs)
   4) NVIDIA-GPU      (9 ADRs)
   5) OCP-BASE        (15 ADRs)
   6) OCP-BM          (58 ADRs)
   7) OCP-HCP         (11 ADRs)
   8) OCP-MGT         (17 ADRs)
   9) OCP-MON         (9 ADRs)
  10) OCP-NET         (44 ADRs)
  11) OCP-OSP         (12 ADRs)
  12) OCP-SEC         (19 ADRs)
  13) OCP-STOR        (7 ADRs)
  14) ODF             (14 ADRs)
  15) PIPELINES       (8 ADRs)
  16) POWERMON        (2 ADRs)
  17) RHOAI-SM        (53 ADRs)
  18) TRACING         (6 ADRs)
  19) VIRT            (7 ADRs)

================================================================================

Select products (enter numbers separated by spaces, or 'all' for all products):
Example: 1 3 5  (selects products #1, #3, and #5)

Your selection: 5 10 17

✅ Selected products:
  - OCP-BASE (15 ADRs)
  - OCP-NET (44 ADRs)
  - RHOAI-SM (53 ADRs)

  Total ADRs: 112

================================================================================
  Customer Information
================================================================================

Customer organization name: ACME Corp
Engagement date [YYYY-MM-DD] (default: today): 2026-03-15
Architect name (default: Laurent TOURREAU):
Output directory (default: ./acme-corp-ADRs):

================================================================================
  Summary
================================================================================

  Customer:        ACME Corp
  Products:        OCP-BASE OCP-NET RHOAI-SM
  Total ADRs:      112
  Engagement Date: 2026-03-15
  Architect:       Laurent TOURREAU
  Output:          ./acme-corp-ADRs

Proceed with generation? [Y/n] y

================================================================================
  Generating ADR Pack...
================================================================================

================================================================================
Generating ADR pack for ACME Corp
================================================================================

📄 Processing OCP-BASE...
📄 Processing OCP-NET...
📄 Processing RHOAI-SM...

📊 Generated metadata.yaml
📖 Generated README.md

================================================================================
✅ Generated ADR pack for ACME Corp
================================================================================

📁 Output: ./acme-corp-ADRs/
📊 Total ADRs: 112
   - OCP-BASE: 15
   - OCP-NET: 44
   - RHOAI-SM: 53
⏱️  Estimated workshop time: ~19 hours
📖 Next: Review ./acme-corp-ADRs/README.md for instructions


================================================================================
✅ ADR pack generation complete!
================================================================================

Next steps:

  1. Review the generated ADRs:
     cd ./acme-corp-ADRs
     cat README.md

  2. During workshops, fill Decision and Agreeing Parties fields

  3. Validate completion:
     ./run_customer_adrs.sh check ./acme-corp-ADRs

  4. Export to Google Docs:
     ./run_customer_adrs.sh export ./acme-corp-ADRs

```

## Non-Interactive Usage

```bash
# Direct Python script usage (for automation/CI)
python scripts/customer_adrs.py generate \
    --customer "ACME Corp" \
    --products "OCP-BASE,OCP-NET,RHOAI-SM" \
    --engagement-date "2026-03-15"

# Check completion (pass through)
./run_customer_adrs.sh check ./acme-corp-ADRs/

# Export (pass through)
./run_customer_adrs.sh export ./acme-corp-ADRs/
```

## Product Selection Examples

**Example 1: Basic OCP deployment**
```
Your selection: 5 10 12 13
  → OCP-BASE, OCP-NET, OCP-SEC, OCP-STOR
  → Total: ~85 ADRs, ~14 hours of workshops
```

**Example 2: AI/ML deployment**
```
Your selection: 5 10 17 4
  → OCP-BASE, OCP-NET, RHOAI-SM, NVIDIA-GPU
  → Total: ~121 ADRs, ~20 hours of workshops
```

**Example 3: All products**
```
Your selection: all
  → All 19 products
  → Total: ~291 ADRs, ~48 hours of workshops (not recommended!)
```

## Key Features

✅ **Prerequisite checks** - Python version, PyYAML, repository structure
✅ **Interactive multi-select** - Choose products by number
✅ **Smart defaults** - Engagement date (today), architect (git user)
✅ **Validation** - Checks output directory, confirms overwrites
✅ **Summary preview** - Shows total ADRs and estimated time
✅ **Next steps guidance** - Shows what to do after generation
