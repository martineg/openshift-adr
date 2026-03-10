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

   1) [ ] GITOPS          - OpenShift GitOps                              ( 6 ADRs)
   2) [ ] LOG             - OpenShift Logging                             ( 7 ADRs)
   3) [ ] NETOBSERV       - Network Observability                         ( 6 ADRs)
   4) [ ] NVIDIA-GPU      - NVIDIA GPU Operator                           ( 9 ADRs)
   5) [ ] OCP-BASE        - OCP - General Platform                        (15 ADRs)
   6) [ ] OCP-BM          - OCP - Bare Metal Installation                 (58 ADRs)
   7) [ ] OCP-HCP         - OCP - Hosted Control Planes                   ( 6 ADRs)
   8) [ ] OCP-MGT         - OCP - Cluster Management & Day2 Ops           (12 ADRs)
   9) [ ] OCP-MON         - OCP - Monitoring (Metrics)                    ( 6 ADRs)
  10) [ ] OCP-NET         - OCP - Networking                              (44 ADRs)
  11) [ ] OCP-OSP         - OCP - OpenStack Installation                  ( 8 ADRs)
  12) [ ] OCP-SEC         - OCP - Security & Compliance                   (19 ADRs)
  13) [ ] OCP-STOR        - OCP - Storage                                 ( 7 ADRs)
  14) [ ] ODF             - OpenShift Data Foundation                     ( 9 ADRs)
  15) [ ] PIPELINES       - OpenShift Pipelines                           ( 8 ADRs)
  16) [ ] POWERMON        - OpenShift Power Monitoring (Kepler)           ( 3 ADRs)
  17) [ ] RHOAI-SM        - OpenShift AI Self-Managed                     (53 ADRs)
  18) [ ] TRACING         - Red Hat Distributed Tracing                   ( 8 ADRs)
  19) [ ] VIRT            - OpenShift Virtualization                      ( 7 ADRs)

================================================================================

Select product number (or press ENTER to continue): 5

[Screen refreshes]

Available ADR templates:

   1) [ ] GITOPS          - OpenShift GitOps                              ( 6 ADRs)
   2) [ ] LOG             - OpenShift Logging                             ( 7 ADRs)
   3) [ ] NETOBSERV       - Network Observability                         ( 6 ADRs)
   4) [ ] NVIDIA-GPU      - NVIDIA GPU Operator                           ( 9 ADRs)
   5) [X] OCP-BASE        - OCP - General Platform                        (15 ADRs)  ← Selected!
   6) [ ] OCP-BM          - OCP - Bare Metal Installation                 (58 ADRs)
   7) [ ] OCP-HCP         - OCP - Hosted Control Planes                   ( 6 ADRs)
   8) [ ] OCP-MGT         - OCP - Cluster Management & Day2 Ops           (12 ADRs)
   9) [ ] OCP-MON         - OCP - Monitoring (Metrics)                    ( 6 ADRs)
  10) [ ] OCP-NET         - OCP - Networking                              (44 ADRs)
  11) [ ] OCP-OSP         - OCP - OpenStack Installation                  ( 8 ADRs)
  12) [ ] OCP-SEC         - OCP - Security & Compliance                   (19 ADRs)
  13) [ ] OCP-STOR        - OCP - Storage                                 ( 7 ADRs)
  14) [ ] ODF             - OpenShift Data Foundation                     ( 9 ADRs)
  15) [ ] PIPELINES       - OpenShift Pipelines                           ( 8 ADRs)
  16) [ ] POWERMON        - OpenShift Power Monitoring (Kepler)           ( 3 ADRs)
  17) [ ] RHOAI-SM        - OpenShift AI Self-Managed                     (53 ADRs)
  18) [ ] TRACING         - Red Hat Distributed Tracing                   ( 8 ADRs)
  19) [ ] VIRT            - OpenShift Virtualization                      ( 7 ADRs)

================================================================================

Selected: 1 product(s)

Select product number (or press ENTER to continue): 10

[Screen refreshes]

Available ADR templates:

   1) [ ] GITOPS          (6 ADRs)
   2) [ ] LOG             (6 ADRs)
   3) [ ] NETOBSERV       (7 ADRs)
   4) [ ] NVIDIA-GPU      (9 ADRs)
   5) [X] OCP-BASE        (15 ADRs)
   6) [ ] OCP-BM          (58 ADRs)
   7) [ ] OCP-HCP         (11 ADRs)
   8) [ ] OCP-MGT         (17 ADRs)
   9) [ ] OCP-MON         (9 ADRs)
  10) [X] OCP-NET         (44 ADRs)    ← Also selected!
  11) [ ] OCP-OSP         (12 ADRs)
  12) [ ] OCP-SEC         (19 ADRs)
  13) [ ] OCP-STOR        (7 ADRs)
  14) [ ] ODF             (14 ADRs)
  15) [ ] PIPELINES       (8 ADRs)
  16) [ ] POWERMON        (2 ADRs)
  17) [ ] RHOAI-SM        (53 ADRs)
  18) [ ] TRACING         (6 ADRs)
  19) [ ] VIRT            (7 ADRs)

================================================================================

Selected: 2 product(s)

Select product number (or press ENTER to continue): 17

[Screen refreshes]

Available ADR templates:

   1) [ ] GITOPS          (6 ADRs)
   ...
   5) [X] OCP-BASE        (15 ADRs)
   ...
  10) [X] OCP-NET         (44 ADRs)
   ...
  17) [X] RHOAI-SM        (53 ADRs)    ← Third selection!
   ...

================================================================================

Selected: 3 product(s)

Select product number (or press ENTER to continue): [ENTER]

[Screen clears]

================================================================================
  Selected Products
================================================================================

✅ You have selected 3 product(s):

  - OCP-BASE        (OCP - General Platform) - 15 ADRs
  - OCP-NET         (OCP - Networking) - 44 ADRs
  - RHOAI-SM        (OpenShift AI Self-Managed) - 53 ADRs

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

## Product Selection Features

**Toggle Selection (Select/Deselect):**
```
Select product number: 5     ← Select OCP-BASE
  5) [X] OCP-BASE

Select product number: 5     ← Select again to deselect
  5) [ ] OCP-BASE            ← Deselected!
```

**Select All Products:**
```
Select product number: all
  → All 19 products instantly selected
  → Type 'all' again to deselect all
```

**Empty Input Continues:**
```
Select product number: [ENTER]
  → Proceeds to next step if at least 1 product selected
  → Shows error if no products selected
```

## Product Selection Examples

**Example 1: Basic OCP deployment**
- Select: 5, 10, 12, 13 (one at a time)
- Products: OCP-BASE, OCP-NET, OCP-SEC, OCP-STOR
- Total: ~85 ADRs, ~14 hours of workshops

**Example 2: AI/ML deployment**
- Select: 5, 10, 17, 4 (one at a time)
- Products: OCP-BASE, OCP-NET, RHOAI-SM, NVIDIA-GPU
- Total: ~121 ADRs, ~20 hours of workshops

**Example 3: All products**
- Type: all
- Products: All 19 products
- Total: ~291 ADRs, ~48 hours of workshops (not recommended!)

## Key Features

✅ **Prerequisite checks** - Python version, PyYAML, repository structure
✅ **Interactive multi-select** - Choose products by number
✅ **Smart defaults** - Engagement date (today), architect (git user)
✅ **Validation** - Checks output directory, confirms overwrites
✅ **Summary preview** - Shows total ADRs and estimated time
✅ **Next steps guidance** - Shows what to do after generation
