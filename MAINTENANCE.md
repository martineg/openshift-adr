# MAINTENANCE - Repository Maintainer Guide

This guide is for **maintainers** of the ADR Template Repository. If you're an **architect** using the customer ADR workflow, see [USER_MANUAL.md](USER_MANUAL.md).

---

## Repository Maintenance Tasks

### 1. Adding New ADR Templates

When adding new ADR templates to the repository:

**Step 1: Edit Template File**

```bash
# Edit the appropriate product file
vim adr_templates/OCP-NET.md

# Add new ADR section following the template structure
```

**ADR Template Structure:**
```markdown
## OCP-NET-XX

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

**Step 2: Renumber ADRs**

After adding/removing ADRs, renumber them sequentially:

```bash
python3 scripts/renumber_adrs.py OCP-NET

# Preview changes first
python3 scripts/renumber_adrs.py OCP-NET --dry-run
```

**Step 3: Validate**

Check governance rules:
```bash
# Verify against dictionaries/adr_governance_rules.md
# Ensure roles match dictionaries/adr_parties_role_dictionnary.md
# Check exclusions in dictionaries/adr_exclusions.md
```

---

### 2. Updating ADR Templates for New Product Versions

When Red Hat releases new product versions:

**Step 1: Update Documentation Sources**

```bash
cd doc_downloader
vim download_config.yaml
# Update version numbers for products

./download_all_docs.sh
# Downloads latest documentation PDFs
```

**Step 2: Analyze Templates**

```bash
cd ..
export ANTHROPIC_API_KEY="your-api-key"

python3 scripts/update_adrs.py RHOAI-SM
# Uses Claude API to analyze ADRs against new documentation
```

**Step 3: Review and Apply Changes**

- Review suggested changes carefully
- Verify against official documentation
- Update ADRs manually
- Follow versioning policy: document current state only, no version numbers

---

### 3. Renumbering ADRs

**When to renumber:**
- After adding new ADRs
- After removing deprecated ADRs
- After reorganizing ADR order

**Command:**
```bash
python3 scripts/renumber_adrs.py <PREFIX>

# Examples:
python3 scripts/renumber_adrs.py OCP-NET
python3 scripts/renumber_adrs.py OCP-BASE
python3 scripts/renumber_adrs.py --dry-run RHOAI-SM  # Preview
```

**What it does:**
- Renumbers ADR IDs sequentially (01, 02, 03...)
- Updates internal references
- Maintains ADR content unchanged

---

### 4. Managing Product Prefixes

**Add new product:**

1. Update `dictionaries/adr_prefix_dictionary.md`
2. Create template file: `adr_templates/NEW-PREFIX.md`
3. Add product mapping in `scripts/customer_adrs.py`:

```python
PRODUCT_NAMES = {
    # ... existing products
    'NEW-PREFIX': 'Full Product Name',
}
```

**Remove deprecated product:**

1. Mark as deprecated in `dictionaries/adr_prefix_dictionary.md`
2. Move template file to archive
3. Document removal in CHANGELOG.md

---

### 5. Governance Rules Maintenance

**Update validation rules:**

```bash
vim dictionaries/adr_governance_rules.md
```

**Update role dictionary:**

```bash
vim dictionaries/adr_parties_role_dictionnary.md
```

**Update exclusions:**

```bash
vim dictionaries/adr_exclusions.md
```

After updating dictionaries, run tests:
```bash
python3 tests/test_customer_adrs.py
```

---

### 6. Testing Changes

**Run automated test suite:**

```bash
python3 tests/test_customer_adrs.py
```

**Manual testing workflow:**

```bash
# Generate test customer pack
./run_customer_adrs.sh

# Test with offline mode
python3 scripts/customer_adrs.py generate --local \
    --customer "Test Customer" \
    --products "OCP-BASE"

# Validate
python3 scripts/customer_adrs.py check ./customer-test-customer-ADRs/

# Clean up
rm -rf customer-test-customer-ADRs/
```

---

### 7. Building ADR Presentation

Generate presentation from Red Hat template:

```bash
python3 scripts/build_presentation.py
# Requires credentials.json and token.json (Google API)
```

---

### 8. PDF Documentation Utilities

**Split large PDF files:**

```bash
python3 scripts/split_pdf.py <path_to_pdf> <max_size_mb>

# Example:
python3 scripts/split_pdf.py documentation.pdf 20
# Creates: documentation-part1.pdf, documentation-part2.pdf, etc.
```

---

## Repository Structure (Maintainer View)

```
/adr_templates/          # ADR template files (edit these)
  ├── OCP-BASE.md
  ├── OCP-NET.md
  ├── RHOAI-SM.md
  └── ...

/dictionaries/           # Governance rules (validate against these)
  ├── adr_governance_rules.md
  ├── adr_prefix_dictionary.md
  ├── adr_parties_role_dictionnary.md
  └── adr_exclusions.md

/scripts/                # Maintenance scripts
  ├── renumber_adrs.py       # ADR renumbering
  ├── update_adrs.py         # Version update automation
  ├── build_presentation.py  # Presentation generator
  └── split_pdf.py           # PDF utilities

/doc_downloader/         # Documentation download automation
  ├── download_all_docs.sh
  └── download_config.yaml

/tests/                  # Automated tests
  └── test_customer_adrs.py
```

---

## Quality Checklist

Before committing changes:

- [ ] Renumber ADRs if IDs changed
- [ ] Run automated tests: `python3 tests/test_customer_adrs.py`
- [ ] Verify against governance rules
- [ ] Check role names match dictionary
- [ ] Ensure no version numbers in ADRs
- [ ] Update CHANGELOG.md with changes
- [ ] Test customer workflow still works

---

## Release Process

1. **Update version in CHANGELOG.md**
2. **Run full test suite**
3. **Generate test customer pack**
4. **Verify Google Docs integration**
5. **Update documentation if needed**
6. **Commit and push changes**
7. **Tag release** (if applicable)

---

## Common Maintenance Tasks

### Quick Reference

| Task | Command |
|------|---------|
| Renumber ADRs | `python3 scripts/renumber_adrs.py <PREFIX>` |
| Update templates | `python3 scripts/update_adrs.py <PREFIX>` |
| Run tests | `python3 tests/test_customer_adrs.py` |
| Download docs | `cd doc_downloader && ./download_all_docs.sh` |
| Split PDF | `python3 scripts/split_pdf.py <file> <size>` |
| Build presentation | `python3 scripts/build_presentation.py` |

---

## Support

For maintainer questions:
- Review `dictionaries/adr_governance_rules.md` for quality standards
- Check `docs/development/` for technical specifications
- See `CLAUDE.md` for AI assistant guidelines

For user questions:
- Direct them to `USER_MANUAL.md`
- Setup issues: `SETUP.md`
- Workflow questions: `docs/usage/ARCHITECT_WORKFLOW.md`
