# Google API Setup for Customer ADR Workflow

This guide walks you through setting up Google API credentials to enable direct Google Docs creation for customer ADR packs.

**Time required:** ~5 minutes

---

## Why Google API?

The customer ADR workflow creates and manages Architecture Decision Records in Google Docs:

1. **Generate** → Creates Google Doc with ADR templates (15 seconds)
2. **Workshop** → Architect fills Decision and Agreeing Parties in Google Doc
3. **Check** → Script reads Google Doc to validate completion
4. **Export** → Optional backup to local markdown/HTML

**Benefits:**
- Real-time collaboration during workshops
- Professional appearance (no markdown editing)
- Version history and comments
- Progress tracking with checkboxes
- Document Outline navigation for 100+ ADRs

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

6. Make sure your new project is selected in the top bar

---

## Step 2: Enable Google Docs API

1. In Google Cloud Console, click **"APIs & Services"** → **"Library"**

2. Search for: `Google Docs API`

3. Click **"Google Docs API"** → **"Enable"**

**Note:** You do NOT need to enable Google Drive API separately. The Google Docs API automatically provides access to the Drive scopes needed for creating and managing Google Docs files.

---

## Step 3: Configure OAuth Consent Screen

1. Click **"APIs & Services"** in left menu → **"OAuth consent screen"**

2. Click the blue **"Get started"** button

3. **App Information screen:**
   - App name: `ADR Workflow`
   - User support email: Select your email from dropdown
   - Click **"Next"**

4. **Audience screen:**
   - Select **"External"** (for personal Gmail)
   - Or select **"Internal"** (for Google Workspace - only if your organization allows it)
   - Click **"Next"**

5. **Contact Information screen:**
   - Email addresses: Enter your email
   - Click **"Next"**

6. **Finish screen:**
   - Check the box: ☑ "I agree to the Google API Services: User Data Policy"
   - Click **"Continue"**
   - Click blue **"Create"** button

7. You'll see a green message: "OAuth configuration created!"

---

## Step 4: Add Required Scopes

1. In the left sidebar, click **"Data Access"**

2. Click **"Add or remove scopes"** button

3. In the popup window, check these two scopes:
   - ☑ `Google Docs API` → `.../auth/documents`
     - Description: "See, edit, create, and delete all your Google Docs documents"
   - ☑ `Google Docs API` → `.../auth/drive.file`
     - Description: "See, edit, create, and delete only the specific Google Drive files you use with this app"

4. Click blue **"Update"** button at bottom of popup

5. Back on the Data Access page, click blue **"Save"** button

**Note:** Both scopes show "Google Docs API" even though one mentions Drive. This is correct - Google Docs API includes the Drive scopes needed to create and manage document files.

---

## Step 5: Add Test Users

**Only for External apps** - Skip this if you selected "Internal" user type.

1. In the left sidebar, click **"Audience"**

2. Scroll down to **"Test users"** section

3. Click **"+ Add users"** button

4. Enter your email address

5. Click **"Save"**

Your email should now appear in the "Test users" list with "1 user (1 test, 0 other)".

---

## Step 6: Create OAuth Client Credentials

1. In the left sidebar, click **"Clients"**

2. Click **"+ Create client"** button at the top

3. **Create OAuth client ID screen:**
   - Click **"Application type"** dropdown
   - Select **"Desktop app"**
   - Name: `ADR Workflow Desktop`
   - Click **"Create"**

4. A popup appears with your credentials:
   - Click **"Download JSON"** button
   - The file downloads with a long auto-generated name like:
     `client_secret_123456789-abcdefg.apps.googleusercontent.com.json`
   - Click **"OK"** to close the popup

---

## Step 7: Install credentials.json

1. **Rename and copy** the downloaded file to your ADR repository:

   ```bash
   cd ~/workspace/adr
   cp ~/Downloads/client_secret_*.json ./credentials.json
   ```

2. **Verify placement:**
   ```bash
   ls -la credentials.json
   # Should show: -rw-r--r-- ... credentials.json
   ```

3. **Important:** `credentials.json` is in `.gitignore` and will NOT be committed to git

---

## Step 8: Install Python Dependencies

```bash
cd ~/workspace/adr

# Install Google API client libraries
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Or use requirements file:
```bash
pip install -r requirements-google.txt
```

---

## Step 9: First-Time Authentication

On first use, the script will open a browser for authentication:

```bash
./run_customer_adrs.sh
```

**Browser will open automatically:**

1. Select your Google account

2. You'll see a warning: **"Google hasn't verified this app"**
   - This is normal! It's YOUR app, not a third-party app
   - Click **"Advanced"**
   - Click **"Go to ADR Workflow (unsafe)"** (it's safe - it's your own project!)

3. Review permissions:
   - "See, edit, create, and delete all your Google Docs documents"
   - "See, edit, create, and delete only specific Google Drive files used with this app"
   - Click **"Allow"**

**Result:**
- Browser shows "The authentication flow has completed"
- `token.json` created automatically in repository root
- Also in `.gitignore` (won't be committed)

**Authentication is now complete!** Future runs won't require browser authentication.

---

## Verification

Test that everything works:

```bash
./run_customer_adrs.sh

# Select a product (e.g., "8" for OCP-BASE)
# Enter customer name (e.g., "Test Customer")
# Press Enter through other prompts

# Script should output:
#   ✅ Google Doc created successfully!
#   🔗 Document URL: https://docs.google.com/document/d/...
```

If you see the Google Doc URL, setup is complete! 🎉

---

## Offline Fallback

If you're offline or credentials are missing, the script automatically falls back to local markdown:

```
⚠️  Google Docs Not Available

  • No internet connection

📖 To enable Google Docs mode, see: docs/setup/GOOGLE_API_SETUP.md

────────────────────────────────────────────────────────────────────────────────

Generate offline document instead? [Y/n]
```

This is normal! You can use offline mode or complete the Google API setup.

---

## Troubleshooting

### "No internet connection" (but you're online)

**Cause:** Corporate firewall blocking connectivity check

**Solution:** Already fixed in latest version. Update your repository:
```bash
git pull
```

### "credentials.json not found"

**Solution:**
```bash
# Check file exists
ls credentials.json

# If missing, re-download from Google Cloud Console:
# APIs & Services → Clients → Click your client → Download JSON
# Then rename and copy to repository root
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

**Cause:** Scopes not configured correctly

**Solution:**
1. Go to Google Cloud Console
2. APIs & Services → Data Access
3. Verify both scopes are added:
   - `.../auth/documents`
   - `.../auth/drive.file`
4. Click "Save"
5. Re-authenticate:
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

**Cause:** Using External app type without adding yourself as test user

**Solution:**
1. Google Cloud Console → APIs & Services → Audience
2. Scroll to "Test users"
3. Click "+ Add users"
4. Enter your email
5. Click "Save"

---

## Security Notes

### credentials.json
- Contains OAuth client ID and secret
- Safe to keep in repository root (in .gitignore)
- Only allows authentication flow, not direct access
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
/home/ltourrea/workspace/adr/
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
- Google Drive API: Free (scopes provided by Docs API)
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
2. Verify scopes are correct: Data Access → both scopes checked
3. Delete `token.json` and re-authenticate
4. Check internet connection
5. Review error messages - they include specific solutions

For Google Cloud Console help: https://console.cloud.google.com/apis/credentials
