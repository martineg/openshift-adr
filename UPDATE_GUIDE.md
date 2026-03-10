# ADR Update Guide

This guide explains how to update ADRs when a new product version is released.

---

## When to Update ADRs

Update ADRs when:
- ✅ New product version is released (e.g., RHOAI 3.4, OCP 4.18)
- ✅ Major feature changes announced
- ✅ Documentation updates show new architectural options
- ✅ Deprecated features removed
- ✅ New capabilities added requiring architectural decisions

**Do NOT update** for:
- ❌ Minor bug fixes
- ❌ Patch releases without feature changes
- ❌ Documentation typo corrections

---

## Step-by-Step Update Process

### Step 1: Download New Documentation

Use the documentation downloader to get the latest product docs:

```bash
cd doc_downloader

# Edit download_config.yaml to update version numbers
vim download_config.yaml

# Download all documentation
./download_all_docs.sh
```

**Example `download_config.yaml` update:**

```yaml
products:
  rhoai:
    version: "3.4"  # Update from 3.3
    base_url: "https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/3.4/pdf"
    files:
      - installing_and_uninstalling_openshift_ai_self-managed/red_hat_openshift_ai_self-managed-3.4-installing_and_uninstalling_openshift_ai_self-managed-en-us.pdf
      # ... other files
```

After running the downloader, new PDFs will be in `docs/<product>/`.

---

### Step 2: Run ADR Analysis

Use the automated update script:

```bash
# Set your Claude API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Install requirements (first time only)
pip install anthropic

# Run analysis for specific product
python scripts/update_adrs.py RHOAI-SM
```

**What it does:**
1. Reads the ADR file (e.g., `adr/RHOAI-SM.md`)
2. Analyzes against governance rules
3. Uses Claude to identify:
   - ADRs needing updates
   - ADRs to remove (obsolete)
   - New ADRs to create
4. Generates a report: `RHOAI-SM-Analysis-Report.md`

---

### Step 3: Review the Report

Open the generated report and review:

**Updates Required:**
- Which ADR IDs need changes
- What specifically changed (Question, Alternatives, Implications, etc.)
- Why the update is needed

**Removals Recommended:**
- Which ADRs are obsolete
- Justification for removal

**New ADRs Suggested:**
- New architectural questions discovered
- Proposed alternatives

**Example report section:**

```markdown
## Updates Required

### RHOAI-SM-02: Update Channel Selection

**Change:** Fast channel renamed to "early-access", new "preview" channel added

**Update needed:**
- **Alternatives section:** Add "Preview" channel as third alternative
- **Justification:** Document when to use preview vs early-access vs stable

### RHOAI-SM-05: Capabilities Enablement

**Change:** New component "Model Registry" added in 3.4

**Update needed:**
- **Alternatives section:** Update "Full MLOps" to include Model Registry
- **Implications:** Document Model Registry resource requirements
```

---

### Step 4: Apply Changes Manually

Open the ADR file and apply recommended changes:

```bash
# Edit the ADR file
vim adr/RHOAI-SM.md

# Apply changes from the report
# - Update specific ADR sections
# - Remove obsolete ADRs
# - Add new ADRs with #TODO# decisions
```

**Important:**
- Follow the ADR template structure exactly
- Update CURRENT STATE only (no version numbers)
- Use standardized roles from `dictionaries/adr_parties_role_dictionnary.md`
- Check `dictionaries/adr_exclusions.md` before adding new ADRs

---

### Step 5: Renumber ADRs

If you added or removed ADRs, renumber them sequentially:

```bash
# Dry run first to preview changes
python scripts/renumber_adrs.py --dry-run RHOAI-SM

# Apply renumbering
python scripts/renumber_adrs.py RHOAI-SM
```

This ensures ADRs are numbered consecutively (e.g., 01, 02, 03, ... no gaps).

---

### Step 6: Commit Changes

```bash
# Check what changed
git diff adr/RHOAI-SM.md

# Stage changes
git add adr/RHOAI-SM.md

# Commit with clear message
git commit -m "Update RHOAI-SM ADRs for version 3.4

- Updated RHOAI-SM-02: New preview channel
- Updated RHOAI-SM-05: Added Model Registry component
- Removed RHOAI-SM-12: Feature deprecated in 3.4
- Added RHOAI-SM-XX: New architectural decision for [feature]

Based on RHOAI 3.4 documentation analysis."

# Push to repository
git push origin main
```

---

## Update Frequency

**Recommended schedule:**

| Product | Update Trigger | Frequency |
|---------|---------------|-----------|
| RHOAI-SM | Minor version (3.3 → 3.4) | Quarterly |
| OCP | Minor version (4.17 → 4.18) | Quarterly |
| GitOps | Major updates | As needed |
| ACM | Major updates | As needed |

**Note:** Patch releases (e.g., 3.4.0 → 3.4.1) rarely require ADR updates unless architectural features change.

---

## Governance Checklist

Before finalizing updates, verify:

- ✅ All ADRs follow template structure
- ✅ No version numbers mentioned (document current state only)
- ✅ Valid ADRs have 2+ viable alternatives (not right vs wrong)
- ✅ New ADRs checked against `dictionaries/adr_exclusions.md`
- ✅ Standardized roles used from `dictionaries/adr_parties_role_dictionnary.md`
- ✅ ADRs renumbered sequentially (no gaps)
- ✅ Changes committed with clear commit message

---

## Troubleshooting

### "Documentation not found"

```bash
# Check docs directory
ls -la docs/rhoai/

# If empty, run downloader
cd doc_downloader
./download_all_docs.sh
```

### "ANTHROPIC_API_KEY not set"

```bash
# Get API key from https://console.anthropic.com/
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Add to ~/.bashrc for persistence
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.bashrc
```

### "ADR file not found"

```bash
# List available ADR files
ls adr/*.md

# Use correct prefix (e.g., RHOAI-SM not RHOAI)
python scripts/update_adrs.py RHOAI-SM
```

### "Analysis report has false positives"

This is normal - Claude may suggest updates that aren't needed. Always review the report critically:

1. Check if the suggested change is truly architectural (not just configuration)
2. Verify the change is in the latest documentation
3. Confirm it's not in the exclusions list
4. Apply only valid updates

---

## Manual Update Workflow (Alternative)

If you prefer not to use the automation script:

1. **Read new documentation** in `docs/<product>/`
2. **Compare with ADRs** in `adr/<PREFIX>.md`
3. **Identify changes:**
   - New features requiring decisions
   - Changed alternatives
   - Deprecated options
4. **Update ADR file manually**
5. **Renumber if needed:** `python scripts/renumber_adrs.py <PREFIX>`
6. **Commit changes**

---

## Example: RHOAI 3.3 → 3.4 Update

```bash
# 1. Update download config
vim doc_downloader/download_config.yaml
# Change version: "3.3" → "3.4"

# 2. Download new docs
cd doc_downloader
./download_all_docs.sh

# 3. Run analysis
cd ..
export ANTHROPIC_API_KEY="your-key"
python scripts/update_adrs.py RHOAI-SM

# 4. Review report
cat RHOAI-SM-Analysis-Report.md

# 5. Apply changes
vim adr/RHOAI-SM.md
# (make changes based on report)

# 6. Renumber
python scripts/renumber_adrs.py RHOAI-SM

# 7. Commit
git add adr/RHOAI-SM.md
git commit -m "Update RHOAI-SM ADRs for 3.4"
git push
```

---

## Getting Help

- **Governance rules:** See `dictionaries/adr_governance_rules.md`
- **Exclusions:** See `dictionaries/adr_exclusions.md`
- **ADR template:** See `README.md` or any existing ADR file
- **Issues:** Open issue at repository URL

---

## Best Practices

1. **Update one product at a time** - Don't mix RHOAI updates with OCP updates in one commit
2. **Test the analysis** - Run `--dry-run` on renumber script first
3. **Review carefully** - AI suggestions need human validation
4. **Document changes** - Clear commit messages help future reviewers
5. **Keep docs synced** - Download new docs before running analysis
6. **Follow governance** - Adhere to quality rules strictly

---

## Version History

This guide covers the current update process as of 2026-03-10.

For historical update workflows, see git history of this file.
