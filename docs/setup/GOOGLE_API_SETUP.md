# Google API Setup for Customer ADR Workflow

This document explains how to set up Google API credentials to enable direct Google Docs creation and editing.

---

## Why Google API?

The customer ADR workflow creates and manages Architecture Decision Records in Google Docs:

1. **Generate** → Creates Google Doc with ADR templates
2. **Workshop** → Architect fills Decision and Agreeing Parties in Google Doc
3. **Check** → Script reads Google Doc to validate completion
4. **Export** → Optional backup to local markdown/html

**Benefits:**
- Real-time collaboration during workshops
- Professional appearance (no markdown editing)
- Version history and comments
- No manual copy/paste to design documents
- Check completion from anywhere with internet

---

## Prerequisites

- Google account (free Gmail or Google Workspace)
- Python 3.7+
- Internet connection
- ~5 minutes for setup

---

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Click **"Select a project"** → **"New Project"**

3. Project name: `ADR Workflow` (or any name)

4. Click **"Create"**

5. Wait for project creation (~30 seconds)

---

## Step 2: Enable Google Docs API

1. In Google Cloud Console, click **"APIs & Services"** → **"Library"**

2. Search for: `Google Docs API`

3. Click **"Google Docs API"** → **"Enable"**

4. Search for: `Google Drive API`

5. Click **"Google Drive API"** → **"Enable"**

---

## Step 3: Create OAuth Credentials

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

---

## Step 4: Install credentials.json

1. Copy `credentials.json` to your ADR repository root:
   ```bash
   cp ~/Downloads/credentials.json /path/to/adr/credentials.json
   ```

2. Verify placement:
   ```bash
   ls -la credentials.json
   # Should show: -rw-r--r-- credentials.json
   ```

3. **Important:** `credentials.json` is in `.gitignore` and will NOT be committed to git

---

## Step 5: Install Python Dependencies

```bash
cd /path/to/adr

# Install Google API client libraries
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Or use requirements file:
```bash
pip install -r requirements-google.txt
```

---

## Step 6: First-Time Authentication

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

---

## Verification

Test that everything works:

```bash
# This should create a Google Doc (not local files)
./run_customer_adrs.sh

# Select products, enter customer name
# Script should output:
#   ✅ Google Doc created successfully
#   🔗 URL: https://docs.google.com/document/d/...
```

---

## Offline Fallback

If you're offline or credentials are missing, the script automatically falls back to local markdown:

```
⚠️  Google API not available
    Reason: No internet connection

📁 Falling back to local markdown generation
    Output: ./customer-slug-ADRs/

💡 To enable Google Docs:
    1. Connect to internet
    2. Follow GOOGLE_API_SETUP.md
```

---

## Troubleshooting

### "credentials.json not found"

**Solution:**
```bash
# Check file exists
ls credentials.json

# If missing, download from Google Cloud Console:
# APIs & Services → Credentials → OAuth 2.0 Client IDs → Download JSON
```

### "Token has been expired or revoked"

**Solution:**
```bash
# Delete old token and re-authenticate
rm token.json
./run_customer_adrs.sh
# Browser will open for re-authentication
```

### "Access blocked: This app's request is invalid"

**Cause:** OAuth consent screen not configured or scopes missing

**Solution:**
1. Go to Google Cloud Console
2. APIs & Services → OAuth consent screen
3. Add required scopes:
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/drive.file`
4. Re-authenticate:
   ```bash
   rm token.json
   ./run_customer_adrs.sh
   ```

### "ModuleNotFoundError: No module named 'googleapiclient'"

**Solution:**
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### "This app is blocked"

**Cause:** Using personal Gmail with External app type in "Testing" mode

**Solution:**
1. Google Cloud Console → OAuth consent screen
2. Click **"Publish App"**
3. Or add your email to "Test users" list

---

## Security Notes

### credentials.json
- Contains OAuth client ID and secret
- Safe to keep in repository root (in .gitignore)
- Only allows authentication, not direct access
- User must still approve permissions

### token.json
- Contains your personal access token
- **Never commit to git** (in .gitignore)
- Expires after inactivity
- Can be revoked anytime at: https://myaccount.google.com/permissions

### Revoke Access

To revoke ADR Workflow's access to your Google account:

1. Go to: https://myaccount.google.com/permissions
2. Find "ADR Workflow"
3. Click **"Remove Access"**
4. Delete `token.json` from repository

---

## Files Created

After setup, you should have:

```
/path/to/adr/
├── credentials.json     ← OAuth client credentials (in .gitignore)
├── token.json          ← Your access token (in .gitignore)
├── .gitignore          ← Already configured
└── ...
```

**Both files are in .gitignore and will NOT be committed.**

---

## Cost

**Free!**

- Google Docs API: Free for personal use
- Google Drive API: Free for personal use
- No credit card required for basic usage
- Quotas:
  - Read: 60,000 requests/minute (more than enough)
  - Write: 60,000 requests/minute (more than enough)

---

## Alternative: Offline-Only Mode

If you don't want to set up Google API, the script automatically uses local markdown:

```bash
# Works without Google API
./run_customer_adrs.sh

# Creates local files:
#   ./customer-slug-ADRs/*.md
#
# You can manually copy these into Google Docs later
```

---

## Next Steps

Once setup is complete:

1. **Generate ADR pack** → Creates Google Doc
   ```bash
   ./run_customer_adrs.sh
   ```

2. **Share Google Doc** with customer for workshop

3. **Check completion** anytime:
   ```bash
   ./run_customer_adrs.sh check "https://docs.google.com/document/d/ABC123/edit"
   ```

4. **Export backup** (optional):
   ```bash
   ./run_customer_adrs.sh export "https://docs.google.com/document/d/ABC123/edit"
   ```

---

## Support

If you encounter issues:

1. Check `.gitignore` includes `credentials.json` and `token.json`
2. Verify scopes are correct in OAuth consent screen
3. Delete `token.json` and re-authenticate
4. Check internet connection
5. Review error messages - they include specific solutions

For Google Cloud Console help: https://console.cloud.google.com/apis/credentials
