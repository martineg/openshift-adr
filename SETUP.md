# SETUP - Quick Installation Guide

**For Architects:** This guide covers initial setup of the Customer ADR Workflow.
**For Maintainers:** See [MAINTENANCE.md](MAINTENANCE.md) for repository maintenance tasks.

---

## Prerequisites

### Required

- **Python 3.8+**
  ```bash
  python3 --version  # Should be 3.8.0 or higher
  ```

- **Git**
  ```bash
  git --version
  ```

### Optional (for Google Docs mode)

- **Internet connection**
- **Google Cloud Project** with Docs API enabled
- **Google API credentials** (OAuth 2.0)

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd adr
```

### 2. Install Python Dependencies

**Base requirements:**
```bash
pip install -r requirements.txt
```

Installs: `PyYAML` (required for all operations)

**Google Docs integration (optional):**
```bash
pip install -r requirements-google.txt
```

Installs: Google API client libraries

### 3. Verify Installation

```bash
# Test dependencies
python3 -c "import yaml; print('✅ PyYAML installed')"

# Test script
python3 scripts/customer_adrs.py --help

# Run automated tests
python3 tests/test_customer_adrs.py
```

**Expected output:**
```
✅ All tests passed!
```

---

## Google Docs Setup (Optional)

**Skip this if you only need offline mode.**

### Why Google Docs?

- ✅ Real-time collaboration during workshops
- ✅ Professional formatting (no markdown editing on screen)
- ✅ No manual copy/paste to design documents
- ✅ Remote access via URL

### Setup Steps (5 minutes)

**Detailed guide:** [docs/setup/GOOGLE_API_SETUP.md](docs/setup/GOOGLE_API_SETUP.md)

**Quick summary:**

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project

2. **Enable APIs**
   - Enable Google Docs API
   - Enable Google Drive API

3. **Create OAuth Credentials**
   - Configure OAuth consent screen
   - Create OAuth 2.0 Client ID
   - Download `credentials.json`

4. **Place credentials**
   ```bash
   # Copy credentials.json to repository root
   cp ~/Downloads/credentials.json .
   ```

5. **First run authentication**
   ```bash
   ./run_customer_adrs.sh
   # Browser will open for OAuth authentication
   # Approve access → token.json will be created
   ```

---

## Verification

### Test Complete Setup

```bash
# Run test suite
python3 tests/test_customer_adrs.py

# Generate test ADR pack (offline mode)
python3 scripts/customer_adrs.py generate --local \
    --customer "Test" \
    --products "GITOPS"

# Verify output
ls customer-test-ADRs/

# Clean up
rm -rf customer-test-ADRs/
```

---

## Troubleshooting

### Python Version Issues
```bash
# Check version
python3 --version

# Update pip
pip install --upgrade pip
```

### Missing Dependencies
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
pip install --force-reinstall -r requirements-google.txt
```

### Google API Errors
```bash
# Verify credentials file exists
ls credentials.json

# Check internet connection
ping google.com

# See detailed troubleshooting:
# docs/setup/GOOGLE_API_SETUP.md
```

### Permission Errors
```bash
# Make scripts executable
chmod +x run_customer_adrs.sh
chmod +x scripts/*.py
chmod +x tests/*.py
```

---

## Data Protection

**Customer data is NEVER committed to git:**

`.gitignore` protects:
- `credentials.json` - Google API credentials
- `token.json` - OAuth tokens
- `customer-*/` - Customer ADR directories
- `docs/*.pdf` - Downloaded documentation

✅ Safe to work with sensitive customer data locally

---

## Next Steps

After successful setup:

1. **Read the user manual:** [USER_MANUAL.md](USER_MANUAL.md)
2. **Review the workflow:** [docs/usage/ARCHITECT_WORKFLOW.md](docs/usage/ARCHITECT_WORKFLOW.md)
3. **Generate your first ADR pack:** `./run_customer_adrs.sh`

---

## Support

- **Complete Guide:** [USER_MANUAL.md](USER_MANUAL.md)
- **Google Setup:** [docs/setup/GOOGLE_API_SETUP.md](docs/setup/GOOGLE_API_SETUP.md)
- **Workflow:** [docs/usage/ARCHITECT_WORKFLOW.md](docs/usage/ARCHITECT_WORKFLOW.md)
- **Maintenance:** [MAINTENANCE.md](MAINTENANCE.md) (for maintainers)
