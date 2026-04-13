# ADR Customer Pack Generator - User Manual

Complete guide for architects using ADR templates in customer engagements.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Workflow Guide](#workflow-guide)
6. [Command Reference](#command-reference)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This tool automates the creation and management of Architecture Decision Records (ADRs) for customer engagements. It streamlines the workflow from initial ADR pack generation through workshop facilitation to final documentation handover.

**Key Features:**

- Interactive product selection (271 ADRs across 19 products)
- Google Docs-first approach for real-time workshop collaboration
- Offline fallback mode when Google API unavailable
- Automatic completion validation
- Export to markdown/HTML for design documents
- Customer data protection (never committed to git)

**Time Savings:** ~5 hours per engagement

---

## Prerequisites

### Required

1. **Python 3.7+**
   ```bash
   python3 --version
   # Should show Python 3.7.0 or higher
   ```

2. **PyYAML** (core dependency)
   ```bash
   pip install PyYAML
   ```

3. **Git Repository Access**
   - Clone this ADR template repository
   - Ensure you're on the `master` branch

### Optional: Google Docs Integration

For the recommended Google Docs workflow, complete these additional steps:

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Project name: `ADR Workflow` (or any name)
4. Click **"Create"**
5. Wait for project creation (~30 seconds)

#### Step 2: Enable APIs

1. In Google Cloud Console, click **"APIs & Services"** → **"Library"**
2. Search for: `Google Docs API` → Click **"Enable"**
3. Search for: `Google Drive API` → Click **"Enable"**

#### Step 3: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Configure Consent Screen"**
   - User Type: **External** (for personal Gmail) or **Internal** (for Google Workspace)
   - Click **"Create"**

3. Fill OAuth consent screen:
   - App name: `ADR Workflow`
   - User support email: Your email
   - Developer contact: Your email
   - Click **"Save and Continue"**

4. Scopes:
   - Click **"Add or Remove Scopes"**
   - Search and select:
     - `Google Docs API` → `.../auth/documents`
     - `Google Drive API` → `.../auth/drive.file`
   - Click **"Update"** → **"Save and Continue"**

5. Test users (if External):
   - Add your email address
   - Click **"Save and Continue"**

6. Click **"Back to Dashboard"**

7. Go to **"Credentials"** tab

8. Click **"Create Credentials"** → **"OAuth client ID"**
   - Application type: **Desktop app**
   - Name: `ADR Workflow Desktop`
   - Click **"Create"**

9. **Download JSON**:
   - Click **"Download JSON"** button
   - Save as `credentials.json`

#### Step 4: Install Credentials

1. Copy `credentials.json` to repository root:
   ```bash
   cp ~/Downloads/credentials.json /path/to/adr/credentials.json
   ```

2. Verify placement:
   ```bash
   ls -la credentials.json
   # Should show: -rw-r--r-- credentials.json
   ```

3. **Important:** `credentials.json` is in `.gitignore` and will NOT be committed

#### Step 5: Install Google API Dependencies

```bash
cd /path/to/adr
pip install -r requirements-google.txt
```

This installs:
- `google-api-python-client`
- `google-auth`
- `google-auth-httplib2`
- `google-auth-oauthlib`

#### Step 6: First-Time Authentication

On first use, the script will open a browser for authentication:

```bash
./run_customer_adrs.sh
```

**Browser will open:**
1. Select your Google account
2. Click **"Allow"** to grant permissions
3. **Important:** If you see "Google hasn't verified this app"
   - Click **"Advanced"**
   - Click **"Go to ADR Workflow (unsafe)"** (it's safe - it's your own app!)
4. Grant permissions to create/edit Google Docs

**Result:**
- `token.json` created automatically
- Stored in repository root
- Also in `.gitignore` (won't be committed)

**Authentication is now complete!** Future runs won't require browser authentication.

**See docs/setup/GOOGLE_API_SETUP.md for detailed troubleshooting.**

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd adr
```

### Install Dependencies

**Minimum (offline mode only):**
```bash
pip install PyYAML
```

**Recommended (Google Docs mode):**
```bash
pip install -r requirements-google.txt
```

### Make Scripts Executable

```bash
chmod +x run_customer_adrs.sh
```

### Verify Installation

```bash
./run_customer_adrs.sh
```

If Google API is not set up, you'll see:
```
⚠️  Google API not available
   Reasons:
   - credentials.json not found (see docs/setup/GOOGLE_API_SETUP.md)

📁 Falling back to local markdown generation
```

This is normal! You can still use offline mode or complete the Google API setup.

---

## Quick Start

### Generate ADR Pack (Recommended: Google Docs)

```bash
./run_customer_adrs.sh
```

**Interactive prompts:**
1. Select products (space-separated numbers, e.g., `5 10 17`)
2. Press ENTER when done selecting
3. Enter customer name
4. Enter engagement date (or press ENTER for today)
5. Enter architect name

**Result:**
- Google Doc created with all selected ADRs
- URL displayed for sharing with customer
- Document ready for workshop collaboration

### Generate ADR Pack (Offline Mode)

If Google API is unavailable, the script automatically offers offline mode:

```
Generate offline document instead? [Y/n]
```

Type `Y` to create local markdown files in `customer-<name>/` directory (protected by `.gitignore`).

### Check ADR Completion

**For Google Docs:**
```bash
./run_customer_adrs.sh check "https://docs.google.com/document/d/ABC123/edit"
```

**For local files:**
```bash
./run_customer_adrs.sh check ./customer-demo-corp/
```

**Output:**
```
================================================================================
ADR Completion Report for Demo Corp
================================================================================

✅ Completed: 12 ADRs (no #TODO# markers)
⏳ Incomplete: 3 ADRs (has #TODO# or issues)
⏭️  Not Discussed: 5 ADRs (entire ADR is #TODO#)

Incomplete ADRs:
--------------------------------------------------------------------------------

OCP-NET: Network Isolation Model
  ❌ Decision missing
  ❌ Agreeing Parties incomplete
```

### Export to Design Document

**From Google Docs:**
```bash
./run_customer_adrs.sh export "https://docs.google.com/document/d/ABC123/edit" --output-format markdown
```

**From local files:**
```bash
./run_customer_adrs.sh export ./customer-demo-corp/ --output-format html
```

**Output:**
- `customer-demo-corp-export.md` or `.html`
- Ready to copy into final design document
- Can exclude "Not Discussed" ADRs with `--exclude-not-discussed`

---

## Workflow Guide

### Phase 1: Preparation (Before Workshop)

**Goal:** Generate customized ADR pack for customer engagement

**Time:** 5-10 minutes

**Steps:**

1. **Run generator:**
   ```bash
   ./run_customer_adrs.sh
   ```

2. **Select products interactively:**
   ```
   Available products:

    1) [ ] GITOPS           - OpenShift GitOps                           (12 ADRs)
    2) [ ] OCP-BASE         - OCP - General Platform                    (15 ADRs)
    3) [ ] OCP-BM           - OCP - Bare Metal                          (28 ADRs)
    4) [ ] OCP-NET          - OCP - Networking                          (32 ADRs)
    5) [ ] OCP-STOR         - OCP - Storage                             (18 ADRs)

   Select product number(s) [e.g., '5' or '5 10 17'] (or ENTER to continue):
   ```

   - Type numbers separated by spaces: `2 4 5`
   - Press ENTER to see selection marked with `[X]`
   - Continue selecting or press ENTER again to finish

3. **Enter customer details:**
   - Customer name: `Acme Corporation`
   - Engagement date: `2025-04-15` (or ENTER for today)
   - Architect name: `Your Name`

4. **Result:**
   - Google Doc created at: `https://docs.google.com/document/d/...`
   - Share URL with customer stakeholders
   - Document contains all selected ADR templates

**Deliverable:** Google Doc URL ready for workshop

### Phase 2: Workshop (Collaborative Filling)

**Goal:** Fill ADRs collaboratively during design workshops

**Time:** 2-4 hours (depending on number of ADRs)

**Steps:**

1. **Share Google Doc** with customer stakeholders before workshop

2. **During workshop:**
   - Present each ADR on screen (Google Doc)
   - Discuss alternatives with customer team
   - **Fill Decision field** directly in Google Doc (architect or customer types)
   - **Fill Agreeing Parties** with names and roles
   - Use Google Doc comments for notes/questions

3. **Benefits of Google Docs approach:**
   - Real-time collaboration (everyone sees changes)
   - Professional appearance (no markdown syntax visible)
   - Version history (track changes)
   - Comments and suggestions
   - No manual copy/paste later

**Deliverable:** Google Doc with completed ADRs

### Phase 3: Validation (Check Completion)

**Goal:** Ensure all ADRs are properly filled before handover

**Time:** 2-5 minutes

**Steps:**

1. **Check completion:**
   ```bash
   ./run_customer_adrs.sh check "https://docs.google.com/document/d/ABC123/edit"
   ```

2. **Review report:**
   - ✅ **Completed:** Decision filled, Agreeing Parties complete
   - ⏳ **Incomplete:** Missing Decision or Agreeing Parties
   - ⏭️ **Not Discussed:** Entire ADR still #TODO#

3. **Fix incomplete ADRs:**
   - Open Google Doc
   - Navigate to incomplete ADRs (listed in report)
   - Fill missing fields
   - Re-run check command

4. **Repeat until all ADRs complete** (or mark some as "Not Discussed")

**Deliverable:** Validation report showing all ADRs complete

### Phase 4: Handover (Export to Design Document)

**Goal:** Export finalized ADRs to design document format

**Time:** 1-2 minutes

**Steps:**

1. **Export to preferred format:**

   **Markdown (for Confluence/GitHub):**
   ```bash
   ./run_customer_adrs.sh export "https://docs.google.com/document/d/ABC123/edit" \
       --output-format markdown \
       --exclude-not-discussed
   ```

   **HTML (for browser/email):**
   ```bash
   ./run_customer_adrs.sh export "https://docs.google.com/document/d/ABC123/edit" \
       --output-format html \
       --exclude-not-discussed
   ```

2. **Review exported file:**
   - `customer-acme-corporation-export.md` or `.html`
   - Contains all completed ADRs
   - Professional formatting with table of contents

3. **Copy into final design document:**
   - Open exported file
   - Copy content into design document template
   - Adjust formatting as needed

**Deliverable:** Design document with finalized ADRs

---

## Command Reference

### Main Command

```bash
./run_customer_adrs.sh [subcommand] [options]
```

**Note:** All commands are routed through the shell wrapper for consistent UX.

### Subcommand: generate (default)

**Purpose:** Create new ADR pack for customer engagement

**Usage:**
```bash
./run_customer_adrs.sh
# or explicitly:
./run_customer_adrs.sh generate
```

**Interactive prompts:**
- Product selection (multi-select)
- Customer name
- Engagement date
- Architect name

**Flags:**
- `--local` - Force local mode (skip Google Docs even if available)

**Output:**
- **Google Docs mode:** URL to Google Doc
- **Local mode:** Directory `customer-<slug>/` with markdown files

**Examples:**

Interactive (recommended):
```bash
./run_customer_adrs.sh
# Select products: 2 4 5
# Customer: Demo Corp
# Date: 2025-04-15
# Architect: John Smith
```

Force local mode:
```bash
./run_customer_adrs.sh generate --local
```

### Subcommand: check

**Purpose:** Validate ADR completion status

**Usage:**
```bash
./run_customer_adrs.sh check <google-doc-url>
./run_customer_adrs.sh check <local-directory>
```

**Arguments:**
- `<google-doc-url>` - Full Google Docs URL
- `<local-directory>` - Path to customer ADR directory

**Flags:**
- `--format text` - Human-readable report (default)
- `--format json` - Machine-readable JSON output
- `--format html` - HTML report file

**Output:**
- Completion statistics
- List of incomplete ADRs
- List of not discussed ADRs
- Actionable next steps

**Examples:**

Check Google Doc:
```bash
./run_customer_adrs.sh check "https://docs.google.com/document/d/ABC123/edit"
```

Check local directory:
```bash
./run_customer_adrs.sh check ./customer-demo-corp/
```

JSON output for CI/CD:
```bash
./run_customer_adrs.sh check ./customer-demo-corp/ --format json
```

### Subcommand: export

**Purpose:** Export ADRs to design document format

**Usage:**
```bash
./run_customer_adrs.sh export <google-doc-url-or-directory> [options]
```

**Arguments:**
- `<google-doc-url-or-directory>` - Google Docs URL or local directory

**Flags:**
- `--output-format markdown` - Export to markdown (default)
- `--output-format html` - Export to HTML
- `--exclude-not-discussed` - Skip ADRs that are entirely #TODO#
- `--output <filename>` - Custom output filename

**Output:**
- `customer-<slug>-export.md` or `.html`
- Formatted document ready for design doc

**Examples:**

Export to markdown (include all):
```bash
./run_customer_adrs.sh export "https://docs.google.com/document/d/ABC123/edit" \
    --output-format markdown
```

Export to HTML (exclude not discussed):
```bash
./run_customer_adrs.sh export "https://docs.google.com/document/d/ABC123/edit" \
    --output-format html \
    --exclude-not-discussed
```

Custom output filename:
```bash
./run_customer_adrs.sh export ./customer-demo-corp/ \
    --output "final-design-adrs.md"
```

---

## Troubleshooting

### Google API Issues

#### "credentials.json not found"

**Cause:** OAuth client credentials not downloaded

**Solution:**
```bash
# Download from Google Cloud Console:
# APIs & Services → Credentials → OAuth 2.0 Client IDs → Download JSON

cp ~/Downloads/credentials.json /path/to/adr/credentials.json
ls -la credentials.json  # Verify file exists
```

#### "Token has been expired or revoked"

**Cause:** Old authentication token expired

**Solution:**
```bash
rm token.json
./run_customer_adrs.sh
# Browser will open for re-authentication
```

#### "invalid_scope: Bad Request"

**Cause:** Old token with incorrect scopes

**Solution:**
```bash
rm token.json
./run_customer_adrs.sh
# Re-authenticate with correct scopes
```

#### "ModuleNotFoundError: No module named 'googleapiclient'"

**Cause:** Google API packages not installed

**Solution:**
```bash
pip install -r requirements-google.txt
```

#### "This app is blocked"

**Cause:** Using personal Gmail with External app type in "Testing" mode

**Solution:**
1. Google Cloud Console → OAuth consent screen
2. Click **"Publish App"**
3. Or add your email to "Test users" list

### Offline Mode Issues

#### Script creates local files even with credentials.json

**Cause:** No internet connection or Google API packages not installed

**Solution:**

Check internet:
```bash
ping -c 1 8.8.8.8
```

Check packages:
```bash
pip list | grep google
# Should show google-api-python-client, google-auth, etc.
```

Reinstall packages:
```bash
pip install -r requirements-google.txt
```

### Check Command Issues

#### "Cannot find metadata.yaml"

**Cause:** Checking wrong directory or directory not created by generator

**Solution:**
```bash
# Ensure you're checking the correct directory:
ls customer-demo-corp/metadata.yaml

# If missing, directory was not created by this tool
```

#### "Invalid Google Docs URL"

**Cause:** URL is not a valid Google Docs document URL

**Solution:**

Valid URL format:
```
https://docs.google.com/document/d/DOCUMENT_ID/edit
```

Copy the full URL from browser address bar.

### Export Command Issues

#### "Export failed: No ADRs found"

**Cause:** Directory is empty or contains no markdown files

**Solution:**
```bash
# Verify ADR files exist:
ls customer-demo-corp/*.md

# If empty, re-run generate command
```

### Product Selection Issues

#### "Invalid input" when selecting multiple products

**Cause:** Numbers not separated by spaces

**Solution:**

Correct format:
```
Select product number(s): 5 10 17
```

Incorrect format:
```
Select product number(s): 5,10,17  ❌
Select product number(s): 5-10-17  ❌
```

### Customer Data Protection

#### "customer-*/  directory not ignored by git"

**Cause:** `.gitignore` not configured or damaged

**Solution:**
```bash
# Verify .gitignore contains:
grep "customer-" .gitignore
# Should show: customer-*/

# If missing, add it:
echo "customer-*/" >> .gitignore
```

#### "Can I commit customer ADRs to git?"

**Answer:** **NO.** Customer data must never be committed to the template repository.

The workflow is:
1. Generate ADR pack (Google Doc or local `customer-*/`)
2. Fill during workshop
3. Export to design document
4. Delete local files (if any)

Only commit changes to `/adr/` templates or `/scripts/`, never customer data.

---

## Support

### Documentation Files

- **GOOGLE_API_SETUP.md** - Detailed Google API setup guide
- **ARCHITECT_WORKFLOW.md** - Workflow phases and time estimates
- **RUN_SCRIPTS_REQUIREMENTS.md** - Technical requirements and architecture
- **CLAUDE.md** - Repository structure and governance

### Common Questions

**Q: Do I need Google API for this to work?**

A: No. The tool automatically falls back to local markdown mode if Google API is unavailable. However, Google Docs mode is recommended for workshop collaboration.

**Q: Can I use this offline?**

A: Yes. If you don't have internet or Google API setup, the tool creates local markdown files that you can edit and manage manually.

**Q: Will customer data be committed to git?**

A: No. All customer data directories (`customer-*/`) are in `.gitignore` and will never be committed.

**Q: How long does setup take?**

A: First-time Google API setup: ~5 minutes. After that, generating ADR packs takes <1 minute.

**Q: Can multiple architects use the same credentials.json?**

A: No. Each architect needs their own `credentials.json` and `token.json` tied to their Google account.

**Q: What happens if I lose the Google Doc URL?**

A: Check your Google Drive - the document is saved there. Or re-run the check/export commands if you have a local backup.

### Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `No internet connection` | Offline | Connect to internet or use `--local` flag |
| `credentials.json not found` | OAuth client not set up | Follow docs/setup/GOOGLE_API_SETUP.md |
| `Token expired` | Old authentication | `rm token.json` and re-authenticate |
| `Invalid scope` | Wrong token scopes | `rm token.json` and re-authenticate |
| `Module not found` | Missing packages | `pip install -r requirements-google.txt` |
| `Invalid Google Docs URL` | Wrong URL format | Use full URL from browser |
| `metadata.yaml not found` | Wrong directory | Check path to customer directory |

---

## Appendix

### File Structure

After generation (Google Docs mode):
```
/path/to/adr/
├── credentials.json     ← OAuth client credentials (in .gitignore)
├── token.json          ← Your access token (in .gitignore)
├── .gitignore          ← Protects customer data
└── ...
```

After generation (local mode):
```
/path/to/adr/
├── customer-demo-corp/          ← Protected by .gitignore
│   ├── metadata.yaml            ← Customer, products, date, architect
│   ├── README.md                ← Workshop instructions
│   ├── OCP-BASE-01-....md       ← Individual ADR files
│   ├── OCP-BASE-02-....md
│   └── ...
└── ...
```

### Security Notes

**credentials.json:**
- Contains OAuth client ID and secret
- Safe to keep in repository root (in .gitignore)
- Only allows authentication, not direct access
- User must still approve permissions

**token.json:**
- Contains your personal access token
- **Never commit to git** (in .gitignore)
- Expires after inactivity
- Can be revoked anytime at: https://myaccount.google.com/permissions

**Revoke Access:**

To revoke ADR Workflow's access to your Google account:

1. Go to: https://myaccount.google.com/permissions
2. Find "ADR Workflow"
3. Click **"Remove Access"**
4. Delete `token.json` from repository

### Cost

**Free!**

- Google Docs API: Free for personal use
- Google Drive API: Free for personal use
- No credit card required for basic usage
- Quotas: 60,000 requests/minute (more than enough)

### Template Repository vs Customer Engagements

This repository contains **ADR templates** (271 decisions across 19 products). When you run the generator, it creates **customer-specific instances** of these templates.

**Never mix template maintenance with customer work:**

- **Template maintenance** (BUILD): Update `/adr/` files, commit to git
- **Customer engagements** (RUN): Generate packs, fill during workshops, export to design docs, never commit customer data

---

**Version:** 1.0
**Last Updated:** 2025-04
**Maintainer:** ADR Template Repository Team
