#!/usr/bin/env python3
"""
Customer ADR Workflow Script

Automate the workflow of using ADR templates in customer engagements.

Subcommands:
  generate - Generate customer-specific ADR pack from templates
  check    - Validate ADR completion before export
  export   - Export completed ADRs to Google Docs

Usage:
  python scripts/customer_adrs.py generate --customer "ACME Corp" --products "OCP-BASE,RHOAI-SM"
  python scripts/customer_adrs.py check ./ACME-Corp-ADRs/
  python scripts/customer_adrs.py export --input ./ACME-Corp-ADRs/ --format google-doc
"""

import os
import sys
import argparse
import re
import subprocess
import json
import socket
from pathlib import Path
from datetime import datetime
import yaml

# Google API imports (optional - check availability)
GOOGLE_API_AVAILABLE = False
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    pass

# Repository paths
REPO_ROOT = Path(__file__).parent.parent
ADR_TEMPLATES_DIR = REPO_ROOT / 'adr_templates'
DICTIONARIES_DIR = REPO_ROOT / 'dictionaries'

# Valid roles from dictionaries/adr_parties_role_dictionnary.md
VALID_ROLES = [
    'Enterprise Architect',
    'Infra Leader',
    'Infrastructure Leader',  # Alias
    'Network Expert',
    'Storage Expert',
    'Security Expert',
    'Operations Expert',
    'OCP Platform Owner',
    'DevOps Engineer',
    'AI/ML Platform Owner',
    'Lead Data Scientist',
    'MLOps Engineer'
]

# Google API Scopes
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file'
]


def check_internet():
    """Check if internet connection is available"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def check_google_prerequisites():
    """Check if Google API prerequisites are met"""
    issues = []

    # Check internet
    if not check_internet():
        issues.append("No internet connection")

    # Check Google API packages
    if not GOOGLE_API_AVAILABLE:
        issues.append("Google API packages not installed (pip install -r requirements-google.txt)")

    # Check credentials.json
    credentials_file = REPO_ROOT / 'credentials.json'
    if not credentials_file.exists():
        issues.append("credentials.json not found (see GOOGLE_API_SETUP.md)")

    return issues


def get_google_credentials():
    """Get Google API credentials via OAuth flow"""
    creds = None
    token_file = REPO_ROOT / 'token.json'
    credentials_file = REPO_ROOT / 'credentials.json'

    # Load existing token
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), GOOGLE_SCOPES)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), GOOGLE_SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds


def create_google_doc_from_adrs(customer, adrs_by_product, engagement_date, architect, args):
    """Create Google Doc with ADR templates"""
    try:
        creds = get_google_credentials()
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        # Create new document
        doc_title = f"ADR Pack - {customer}"
        doc = docs_service.documents().create(body={'title': doc_title}).execute()
        doc_id = doc['documentId']
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

        # Build document content
        requests = []

        # Insert title
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': f"Architecture Decision Records\n{customer}\n\nGenerated: {engagement_date}\nArchitect: {architect}\n\n"
            }
        })

        # Insert ADRs by product
        index = 1
        for product, product_adrs in adrs_by_product.items():
            # Product section header
            requests.append({
                'insertText': {
                    'location': {'index': index},
                    'text': f"\n{'='*80}\n{product} ({len(product_adrs)} ADRs)\n{'='*80}\n\n"
                }
            })

            # Insert each ADR
            for adr in product_adrs:
                adr_text = adr['content']
                # Remove metadata comments
                adr_text = re.sub(r'<!--.*?-->', '', adr_text, flags=re.DOTALL).strip()
                requests.append({
                    'insertText': {
                        'location': {'index': index},
                        'text': adr_text + "\n\n" + "-"*80 + "\n\n"
                    }
                })

        # Apply formatting (batch update)
        if requests:
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()

        return {'url': doc_url, 'id': doc_id}

    except HttpError as error:
        print(f"❌ Google API Error: {error}")
        return None


def extract_doc_id_from_url(url):
    """Extract document ID from Google Docs URL"""
    # https://docs.google.com/document/d/DOCUMENT_ID/edit
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    # Maybe it's already just the ID
    if re.match(r'^[a-zA-Z0-9-_]+$', url):
        return url
    return None


def read_google_doc(doc_url_or_id):
    """Read content from Google Doc"""
    try:
        creds = get_google_credentials()
        docs_service = build('docs', 'v1', credentials=creds)

        doc_id = extract_doc_id_from_url(doc_url_or_id)
        if not doc_id:
            return None

        doc = docs_service.documents().get(documentId=doc_id).execute()

        # Extract text content
        content = doc.get('body', {}).get('content', [])
        text = ''
        for element in content:
            if 'paragraph' in element:
                for text_run in element['paragraph'].get('elements', []):
                    if 'textRun' in text_run:
                        text += text_run['textRun'].get('content', '')

        return text

    except HttpError as error:
        print(f"❌ Google API Error: {error}")
        return None


def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def get_git_commit_sha():
    """Get current git commit SHA"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return "unknown"


def get_git_user_name():
    """Get git user name"""
    try:
        result = subprocess.run(
            ['git', 'config', 'user.name'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return "Unknown"


def parse_adr_template_file(file_path):
    """Parse ADR template file into individual ADRs"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split on ADR headers (## PREFIX-NN)
    adr_pattern = r'^## ([A-Z]+-[A-Z]+-\d+|[A-Z]+-\d+)$'

    adrs = []
    current_adr = None
    current_content = []

    for line in content.split('\n'):
        match = re.match(adr_pattern, line)
        if match:
            # Save previous ADR if exists
            if current_adr:
                adrs.append({
                    'id': current_adr,
                    'content': '\n'.join(current_content).strip()
                })

            # Start new ADR
            current_adr = match.group(1)
            current_content = [line]
        else:
            if current_adr:
                current_content.append(line)

    # Save last ADR
    if current_adr:
        adrs.append({
            'id': current_adr,
            'content': '\n'.join(current_content).strip()
        })

    return adrs


def extract_adr_title(adr_content):
    """Extract title from ADR content"""
    match = re.search(r'\*\*Title\*\*\s*\n(.+)', adr_content)
    if match:
        return match.group(1).strip()
    return "Untitled"


def prefill_customer_metadata(adr_content, customer_name, template_source, template_version, engagement_date):
    """Pre-fill customer metadata in ADR content"""
    # Add metadata header
    metadata_header = f"""<!-- Generated for: {customer_name} -->
<!-- Engagement Date: {engagement_date} -->
<!-- Template Source: {template_source} -->
<!-- Template Version: {template_version} -->

"""

    # Replace #TODO# in Agreeing Parties with #TODO# (Customer Name)
    adr_content = re.sub(
        r'Person: #TODO#',
        f'Person: #TODO# ({customer_name})',
        adr_content
    )

    return metadata_header + adr_content


def generate_customer_adrs(args):
    """Generate customer-specific ADR pack from templates"""

    customer = args.customer
    products = [p.strip() for p in args.products.split(',')]
    engagement_date = args.engagement_date if args.engagement_date else datetime.now().strftime('%Y-%m-%d')
    architect = args.architect if args.architect else get_git_user_name()

    # Check Google API prerequisites
    google_issues = check_google_prerequisites() if GOOGLE_API_AVAILABLE else ["Google API packages not installed"]

    # Decide: Google Docs or Local
    use_google_docs = len(google_issues) == 0 and not getattr(args, 'local', False)

    if use_google_docs:
        print("📊 Mode: Google Docs (online, collaborative)")
        print()
        return generate_google_doc_mode(customer, products, engagement_date, architect, args)
    else:
        # Fallback to local - ask user
        print()
        print("="*80)
        print("⚠️  Google Docs Not Available")
        print("="*80)
        print()
        for issue in google_issues:
            print(f"  • {issue}")
        print()
        print("📖 To enable Google Docs mode, see: GOOGLE_API_SETUP.md")
        print()
        print("─"*80)
        print()

        # Ask user if they want offline mode
        if not getattr(args, 'local', False):  # If not forced via --local flag
            response = input("Generate offline document instead? [Y/n] ").strip().lower()
            if response and response not in ['y', 'yes']:
                print()
                print("❌ Operation cancelled")
                print()
                print("💡 To generate Google Doc:")
                print("   1. Connect to internet")
                print("   2. Follow GOOGLE_API_SETUP.md")
                print("   3. Run: ./run_customer_adrs.sh")
                print()
                sys.exit(0)

        print()
        print("📁 Generating offline document (local markdown files)")
        print()

        # Customer data goes in customer-{slug}/ directory (in .gitignore)
        output_dir = Path(args.output) if args.output else Path(f"./customer-{slugify(customer)}")
        return generate_local_mode(customer, products, engagement_date, architect, output_dir, args)


def generate_google_doc_mode(customer, products, engagement_date, architect, args):
    """Generate ADRs in Google Docs mode"""

    print("="*80)
    print(f"Generating Google Doc for {customer}")
    print("="*80)

    # Validate products
    missing_products = []
    for product in products:
        template_file = ADR_TEMPLATES_DIR / f"{product}.md"
        if not template_file.exists():
            missing_products.append(product)

    if missing_products:
        available = [f.stem for f in ADR_TEMPLATES_DIR.glob('*.md')]
        print(f"❌ Error: Template(s) not found: {', '.join(missing_products)}")
        print(f"\nAvailable templates:")
        for tmpl in sorted(available):
            print(f"   - {tmpl}")
        sys.exit(1)

    # Get git metadata
    template_version = get_git_commit_sha()

    # Process each product
    all_adrs = []
    adrs_by_product = {}
    product_stats = {}

    for product in products:
        template_file = ADR_TEMPLATES_DIR / f"{product}.md"
        template_source = f"adr_templates/{product}.md"

        print(f"\n📄 Processing {product}...")

        # Parse template file
        adrs = parse_adr_template_file(template_file)
        product_stats[product] = len(adrs)

        # Pre-fill customer metadata
        product_adrs = []
        for adr in adrs:
            adr_id = adr['id']
            adr_content = adr['content']
            title = extract_adr_title(adr_content)

            # Pre-fill customer metadata
            adr_content = prefill_customer_metadata(
                adr_content,
                customer,
                template_source,
                template_version,
                engagement_date
            )

            product_adrs.append({
                'id': adr_id,
                'title': title,
                'content': adr_content,
                'product': product
            })

            all_adrs.append({'id': adr_id, 'title': title, 'product': product})

            if args.verbose:
                print(f"   ✓ {adr_id}: {title}")

        adrs_by_product[product] = product_adrs

    total_adrs = len(all_adrs)

    print()
    print("🔄 Creating Google Doc...")

    # Create Google Doc
    doc_result = create_google_doc_from_adrs(customer, adrs_by_product, engagement_date, architect, args)

    if not doc_result:
        print()
        print("❌ Failed to create Google Doc")
        print("   Falling back to local markdown...")
        output_dir = Path(f"./{slugify(customer)}-ADRs")
        return generate_local_mode(customer, products, engagement_date, architect, output_dir, args)

    # Calculate estimated workshop time
    estimated_hours = (total_adrs * 10) / 60

    # Success!
    print()
    print("="*80)
    print("✅ Google Doc created successfully!")
    print("="*80)
    print()
    print(f"🔗 Document URL:")
    print(f"   {doc_result['url']}")
    print()
    print(f"📊 Total ADRs: {total_adrs}")
    for product, count in product_stats.items():
        print(f"   - {product}: {count}")
    print(f"⏱️  Estimated workshop time: ~{estimated_hours:.0f} hours")
    print()
    print("📋 Next Steps:")
    print()
    print("  1. Share Google Doc with customer:")
    print(f"     {doc_result['url']}")
    print()
    print("  2. During workshop:")
    print("     - Project Google Doc on screen")
    print("     - Fill Decision and Agreeing Parties in real-time")
    print("     - Customer can see progress and collaborate")
    print()
    print("  3. Check completion anytime:")
    print(f"     ./run_customer_adrs.sh check \"{doc_result['url']}\"")
    print()
    print("  4. Optional backup:")
    print(f"     ./run_customer_adrs.sh export \"{doc_result['url']}\"")
    print()


def generate_local_mode(customer, products, engagement_date, architect, output_dir, args):
    """Generate ADRs in local markdown mode (fallback)"""

    # Validate inputs
    if not customer:
        print("❌ Error: Customer name is required")
        sys.exit(1)

    if not products:
        print("❌ Error: At least one product must be specified")
        sys.exit(1)

    # Check output directory doesn't exist
    if output_dir.exists() and not args.force:
        print(f"❌ Error: Output directory already exists: {output_dir}")
        print(f"   Use --force to overwrite, or specify different --output")
        sys.exit(1)

    # Validate products exist
    missing_products = []
    for product in products:
        template_file = ADR_TEMPLATES_DIR / f"{product}.md"
        if not template_file.exists():
            missing_products.append(product)

    if missing_products:
        available = [f.stem for f in ADR_TEMPLATES_DIR.glob('*.md')]
        print(f"❌ Error: Template(s) not found: {', '.join(missing_products)}")
        print(f"\nAvailable templates:")
        for tmpl in sorted(available):
            print(f"   - {tmpl}")
        sys.exit(1)

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get git metadata
    template_version = get_git_commit_sha()
    generated_date = datetime.now().isoformat()

    # Process each product
    all_adrs = []
    product_stats = {}

    print("="*80)
    print(f"Generating ADR pack for {customer}")
    print("="*80)

    for product in products:
        template_file = ADR_TEMPLATES_DIR / f"{product}.md"
        template_source = f"adr_templates/{product}.md"

        print(f"\n📄 Processing {product}...")

        # Parse template file
        adrs = parse_adr_template_file(template_file)
        product_stats[product] = len(adrs)

        # Generate individual ADR files
        for adr in adrs:
            adr_id = adr['id']
            adr_content = adr['content']
            title = extract_adr_title(adr_content)

            # Pre-fill customer metadata
            adr_content = prefill_customer_metadata(
                adr_content,
                customer,
                template_source,
                template_version,
                engagement_date
            )

            # Generate filename
            title_slug = slugify(title)
            filename = f"{adr_id}-{title_slug}.md"
            output_file = output_dir / filename

            # Write ADR file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(adr_content)

            all_adrs.append({
                'id': adr_id,
                'title': title,
                'filename': filename,
                'product': product
            })

            if args.verbose:
                print(f"   ✓ {adr_id}: {title}")

    total_adrs = len(all_adrs)

    # Generate metadata.yaml
    metadata = {
        'customer': customer,
        'engagement_date': engagement_date,
        'architect': architect,
        'products': products,
        'template_repository': 'https://github.com/redhat-ai-services/openshift-adr',
        'template_version': template_version,
        'generated_date': generated_date,
        'total_adrs': total_adrs
    }

    metadata_file = output_dir / 'metadata.yaml'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)

    print(f"\n📊 Generated metadata.yaml")

    # Generate README.md
    readme_content = f"""# ADR Pack for {customer}

**Generated:** {engagement_date}
**Products:** {', '.join(products)}
**Total ADRs:** {total_adrs}

---

## ADR List

"""

    # Group by product
    for product in products:
        product_adrs = [a for a in all_adrs if a['product'] == product]
        readme_content += f"\n### {product} ({len(product_adrs)} ADRs)\n\n"

        for adr in product_adrs:
            readme_content += f"- [{adr['id']}: {adr['title']}]({adr['filename']})\n"

    readme_content += f"""

---

## Usage

1. **Review ADRs before workshop**
   - Read through the architectural questions
   - Prepare to facilitate discussions

2. **During workshop: Fill Decision and Agreeing Parties fields**
   - For each ADR discussed, update:
     - `**Decision**` field with chosen alternative
     - `**Agreeing Parties**` with real names and roles

3. **After workshop: Validate completion**
   ```bash
   python scripts/customer_adrs.py check {output_dir.name}/
   ```

4. **Export to Google Docs**
   ```bash
   python scripts/customer_adrs.py export --input {output_dir.name}/
   ```

---

**Generated from:** [OpenShift ADR Template Repository]({metadata['template_repository']})
**Template Version:** {template_version[:8]}
"""

    readme_file = output_dir / 'README.md'
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"📖 Generated README.md")

    # Calculate estimated workshop time (10 min per ADR)
    estimated_hours = (total_adrs * 10) / 60

    # Final summary
    print("\n" + "="*80)
    print("✅ Generated offline ADR pack for " + customer)
    print("="*80)
    print(f"\n📁 Output: {output_dir}/")
    print(f"📊 Total ADRs: {total_adrs}")
    for product, count in product_stats.items():
        print(f"   - {product}: {count}")
    print(f"⏱️  Estimated workshop time: ~{estimated_hours:.0f} hours")
    print()
    print("🔒 Customer data protection:")
    print(f"   • Directory {output_dir}/ is in .gitignore")
    print("   • Customer ADRs will NOT be committed to git")
    print("   • Safe to work with customer data locally")
    print()
    print(f"📖 Next: Review {output_dir}/README.md for instructions")
    print()
    print("💡 For Google Docs mode (recommended for workshops):")
    print("   • Connect to internet")
    print("   • Follow GOOGLE_API_SETUP.md")
    print("   • Re-run: ./run_customer_adrs.sh")
    print()


def check_adr_completion(args):
    """Check ADR completion status"""
    input_dir = Path(args.input)

    if not input_dir.exists():
        print(f"❌ Error: ADR directory not found: {input_dir}")
        sys.exit(2)

    # Read metadata
    metadata_file = input_dir / 'metadata.yaml'
    if not metadata_file.exists():
        print(f"❌ Error: metadata.yaml not found in {input_dir}")
        sys.exit(2)

    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)

    customer = metadata.get('customer', 'Unknown')

    # Find all ADR files
    adr_files = list(input_dir.glob('*.md'))
    adr_files = [f for f in adr_files if f.name != 'README.md']

    if not adr_files:
        print(f"❌ Error: No ADR markdown files found in {input_dir}")
        sys.exit(2)

    # Analysis results
    completed_adrs = []
    incomplete_adrs = []
    not_discussed_adrs = []

    for adr_file in sorted(adr_files):
        with open(adr_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract ADR ID from filename or content
        adr_id = adr_file.stem.split('-')[0] + '-' + adr_file.stem.split('-')[1]
        title = extract_adr_title(content)

        # Check Decision field
        decision_match = re.search(r'\*\*Decision\*\*\s*\n(.+?)(?:\n\n|\*\*)', content, re.DOTALL)
        decision_text = decision_match.group(1).strip() if decision_match else ""

        # Consider it TODO if contains #TODO# or if it's the default placeholder
        has_decision_todo = '#TODO' in decision_text or decision_text == "" or decision_text.startswith('#TODO')

        # Check Agreeing Parties
        parties_match = re.search(r'\*\*Agreeing Parties\*\*\s*\n(.+?)(?:\n\n|\Z)', content, re.DOTALL)
        parties_text = parties_match.group(1).strip() if parties_match else ""

        has_parties_todo = '#TODO#' in parties_text

        # Parse agreeing parties
        parties_lines = [line.strip() for line in parties_text.split('\n') if line.strip().startswith('- Person:')]
        invalid_roles = []

        for party_line in parties_lines:
            # Extract role
            role_match = re.search(r'Role:\s*([^,\n]+)', party_line)
            if role_match:
                role = role_match.group(1).strip()
                if role not in VALID_ROLES:
                    invalid_roles.append(role)

        # Classify ADR
        if has_decision_todo and has_parties_todo:
            # Entire ADR is TODO
            not_discussed_adrs.append({
                'id': adr_id,
                'title': title,
                'filename': adr_file.name
            })
        elif has_decision_todo or has_parties_todo or invalid_roles:
            # Partially complete
            issues = []
            if has_decision_todo:
                issues.append('Decision field incomplete')
            if has_parties_todo:
                issues.append('Agreeing Parties incomplete')
            if invalid_roles:
                issues.append(f'Invalid role(s): {", ".join(invalid_roles)}')

            incomplete_adrs.append({
                'id': adr_id,
                'title': title,
                'filename': adr_file.name,
                'issues': issues
            })
        else:
            # Complete
            completed_adrs.append({
                'id': adr_id,
                'title': title,
                'filename': adr_file.name
            })

    # Generate report based on format
    total_adrs = len(adr_files)

    if args.format == 'json':
        report = {
            'customer': customer,
            'total_adrs': total_adrs,
            'completed': len(completed_adrs),
            'incomplete': len(incomplete_adrs),
            'not_discussed': len(not_discussed_adrs),
            'ready_for_export': len(incomplete_adrs) == 0,
            'completed_adrs': [{'id': a['id'], 'title': a['title']} for a in completed_adrs],
            'incomplete_adrs': incomplete_adrs,
            'not_discussed_adrs': [{'id': a['id'], 'title': a['title']} for a in not_discussed_adrs]
        }
        print(json.dumps(report, indent=2))

    elif args.format == 'html':
        print("<html><body>")
        print(f"<h1>ADR Completion Report for {customer}</h1>")
        print(f"<p><strong>✅ Completed:</strong> {len(completed_adrs)} ADRs</p>")
        print(f"<p><strong>⏳ Incomplete:</strong> {len(incomplete_adrs)} ADRs</p>")
        print(f"<p><strong>⏭️ Not Discussed:</strong> {len(not_discussed_adrs)} ADRs</p>")

        if incomplete_adrs:
            print("<h2>Incomplete ADRs</h2><ul>")
            for adr in incomplete_adrs:
                print(f"<li><strong>{adr['id']}: {adr['title']}</strong><br>")
                print(f"Issues: {', '.join(adr['issues'])}</li>")
            print("</ul>")

        print("</body></html>")

    else:  # text format (default)
        print("="*80)
        print(f"ADR Completion Report for {customer}")
        print("="*80)
        print()
        print(f"✅ Completed: {len(completed_adrs)} ADRs (no #TODO# markers)")
        print(f"⏳ Incomplete: {len(incomplete_adrs)} ADRs (has #TODO# or issues)")
        print(f"⏭️  Not Discussed: {len(not_discussed_adrs)} ADRs (entire ADR is #TODO#)")
        print()

        if incomplete_adrs:
            print("Incomplete ADRs:")
            print("-"*80)
            for adr in incomplete_adrs:
                print(f"\n{adr['id']}: {adr['title']}")
                for issue in adr['issues']:
                    print(f"  ❌ {issue}")
            print()

        if not_discussed_adrs:
            print(f"Not Discussed (can be excluded from export using --exclude-not-discussed):")
            print("-"*80)
            for adr in not_discussed_adrs[:10]:  # Show first 10
                print(f"  - {adr['id']}: {adr['title']}")
            if len(not_discussed_adrs) > 10:
                print(f"  ... and {len(not_discussed_adrs) - 10} more")
            print()

        print("Summary:")
        print("-"*80)
        if len(incomplete_adrs) == 0 and len(not_discussed_adrs) < total_adrs:
            print("✅ Ready for export: All discussed ADRs are complete")
            print()
            print("Next steps:")
            print(f"  python scripts/customer_adrs.py export --input {input_dir}")
        elif len(incomplete_adrs) == 0:
            print("⚠️  No ADRs have been discussed yet (all are #TODO#)")
            print()
            print("Next steps:")
            print("  1. Conduct design workshops")
            print("  2. Fill Decision and Agreeing Parties fields")
            print(f"  3. Re-run: python scripts/customer_adrs.py check {input_dir}")
        else:
            print(f"❌ Not ready: {len(incomplete_adrs)} incomplete ADR(s) must be completed first")
            print()
            print("Next steps:")
            print("  1. Review incomplete ADRs listed above")
            print("  2. Fill missing Decision fields")
            print("  3. Complete Agreeing Parties sections")
            print(f"  4. Re-run: python scripts/customer_adrs.py check {input_dir}")
        print()

    # Exit code
    if args.fail_on_incomplete and len(incomplete_adrs) > 0:
        sys.exit(1)
    else:
        sys.exit(0)


def export_adrs(args):
    """Export ADRs to various formats"""
    input_dir = Path(args.input)

    if not input_dir.exists():
        print(f"❌ Error: ADR directory not found: {input_dir}")
        sys.exit(2)

    # Read metadata
    metadata_file = input_dir / 'metadata.yaml'
    if not metadata_file.exists():
        print(f"❌ Error: metadata.yaml not found in {input_dir}")
        sys.exit(2)

    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)

    customer = args.customer if args.customer else metadata.get('customer', 'Unknown')
    products = metadata.get('products', [])

    # Find all ADR files
    adr_files = list(input_dir.glob('*.md'))
    adr_files = [f for f in adr_files if f.name != 'README.md']

    if not adr_files:
        print(f"❌ Error: No ADR markdown files found in {input_dir}")
        sys.exit(2)

    # Parse ADRs
    adrs = []
    for adr_file in sorted(adr_files):
        with open(adr_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract ADR ID
        adr_id = adr_file.stem.split('-')[0] + '-' + adr_file.stem.split('-')[1]
        title = extract_adr_title(content)

        # Check if discussed
        decision_match = re.search(r'\*\*Decision\*\*\s*\n(.+?)(?:\n\n|\*\*)', content, re.DOTALL)
        decision_text = decision_match.group(1).strip() if decision_match else ""
        is_discussed = '#TODO' not in decision_text and decision_text != "" and not decision_text.startswith('#TODO')

        # Extract product from ADR ID
        product = adr_id.rsplit('-', 1)[0]

        # Skip not-discussed if requested
        if args.exclude_not_discussed and not is_discussed:
            continue

        adrs.append({
            'id': adr_id,
            'title': title,
            'product': product,
            'content': content,
            'is_discussed': is_discussed
        })

    if not adrs:
        print("❌ Error: No ADRs to export (all are marked as not discussed)")
        sys.exit(1)

    # Group ADRs
    if args.group_by == 'product':
        grouped_adrs = {}
        for product in products:
            product_adrs = [a for a in adrs if a['product'] == product]
            if product_adrs:
                grouped_adrs[product] = product_adrs
    else:
        # No grouping - flat list
        grouped_adrs = {'All ADRs': adrs}

    # Export based on format
    if args.format == 'markdown':
        output_file = Path(f"{slugify(customer)}-ADRs-export.md")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Architecture Decisions - {customer}\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"**Total ADRs:** {len(adrs)}\n\n")

            # Table of contents
            if args.create_toc:
                f.write("## Table of Contents\n\n")
                for group_name, group_adrs in grouped_adrs.items():
                    f.write(f"### {group_name} ({len(group_adrs)} ADRs)\n\n")
                    for adr in group_adrs:
                        f.write(f"- [{adr['id']}: {adr['title']}](#{slugify(adr['id'])})\n")
                    f.write("\n")

            f.write("---\n\n")

            # ADR content
            for group_name, group_adrs in grouped_adrs.items():
                f.write(f"# {group_name}\n\n")
                f.write("---\n\n")

                for adr in group_adrs:
                    # Remove metadata comments
                    content = re.sub(r'<!--.*?-->', '', adr['content'], flags=re.DOTALL).strip()
                    f.write(content)
                    f.write("\n\n---\n\n")

        print("="*80)
        print("✅ Export to Markdown Complete")
        print("="*80)
        print(f"\n📄 Output: {output_file}")
        print(f"📊 Total ADRs: {len(adrs)}")
        if args.group_by == 'product':
            for group_name, group_adrs in grouped_adrs.items():
                print(f"   - {group_name}: {len(group_adrs)}")
        print(f"\n💡 Open with: cat {output_file}")
        print()

    elif args.format == 'html':
        output_file = Path(f"{slugify(customer)}-ADRs-export.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n")
            f.write(f"<title>Architecture Decisions - {customer}</title>\n")
            f.write("<style>\n")
            f.write("body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; }\n")
            f.write("h1 { color: #c00; border-bottom: 3px solid #c00; }\n")
            f.write("h2 { color: #333; margin-top: 40px; }\n")
            f.write("h3 { color: #666; }\n")
            f.write(".adr { border: 1px solid #ddd; padding: 20px; margin: 20px 0; background: #f9f9f9; }\n")
            f.write(".adr-header { background: #c00; color: white; padding: 10px; margin: -20px -20px 20px -20px; }\n")
            f.write("hr { border: none; border-top: 2px solid #ddd; margin: 40px 0; }\n")
            f.write("</style>\n</head>\n<body>\n")

            f.write(f"<h1>Architecture Decisions - {customer}</h1>\n")
            f.write(f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>\n")
            f.write(f"<p><strong>Total ADRs:</strong> {len(adrs)}</p>\n")

            # Table of contents
            if args.create_toc:
                f.write("<h2>Table of Contents</h2>\n")
                for group_name, group_adrs in grouped_adrs.items():
                    f.write(f"<h3>{group_name} ({len(group_adrs)} ADRs)</h3>\n<ul>\n")
                    for adr in group_adrs:
                        f.write(f"<li><a href='#{slugify(adr['id'])}'>{adr['id']}: {adr['title']}</a></li>\n")
                    f.write("</ul>\n")

            f.write("<hr>\n")

            # ADR content
            for group_name, group_adrs in grouped_adrs.items():
                f.write(f"<h1>{group_name}</h1>\n")
                f.write("<hr>\n")

                for adr in group_adrs:
                    f.write(f"<div class='adr' id='{slugify(adr['id'])}'>\n")
                    f.write(f"<div class='adr-header'><h2>{adr['id']}: {adr['title']}</h2></div>\n")

                    # Convert markdown to HTML
                    content = re.sub(r'<!--.*?-->', '', adr['content'], flags=re.DOTALL).strip()
                    content = re.sub(r'## .+', '', content)  # Remove ## header
                    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
                    content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
                    content = content.replace('\n\n', '</p><p>')
                    content = f"<p>{content}</p>"
                    content = content.replace('<p><li>', '<ul><li>').replace('</li></p>', '</li></ul>')

                    f.write(content)
                    f.write("</div>\n\n")

            f.write("</body>\n</html>")

        print("="*80)
        print("✅ Export to HTML Complete")
        print("="*80)
        print(f"\n📄 Output: {output_file}")
        print(f"📊 Total ADRs: {len(adrs)}")
        if args.group_by == 'product':
            for group_name, group_adrs in grouped_adrs.items():
                print(f"   - {group_name}: {len(group_adrs)}")
        print(f"\n💡 Open with: open {output_file}")
        print()

    elif args.format == 'google-doc':
        print("="*80)
        print("⚠️  Google Docs Export")
        print("="*80)
        print()
        print("Google Docs export requires API credentials setup.")
        print()
        print("For now, use markdown or HTML export:")
        print(f"  python scripts/customer_adrs.py export --input {input_dir} --format markdown")
        print()
        print("Then manually copy content into Google Docs.")
        print()
        print("Future enhancement: Direct Google Docs API integration")
        print("  See: RUN_SCRIPTS_REQUIREMENTS.md for specifications")
        print()
        sys.exit(0)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Customer ADR Workflow - Automate ADR template usage in engagements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate ADR pack
  python scripts/customer_adrs.py generate \\
      --customer "ACME Corp" \\
      --products "OCP-BASE,OCP-NET,RHOAI-SM"

  # Check completion
  python scripts/customer_adrs.py check ./ACME-Corp-ADRs/

  # Export to Google Docs
  python scripts/customer_adrs.py export \\
      --input ./ACME-Corp-ADRs/ \\
      --format google-doc

For detailed requirements, see: RUN_SCRIPTS_REQUIREMENTS.md
        """
    )

    # Global options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate subcommand
    generate_parser = subparsers.add_parser('generate',
                                           help='Generate customer ADR pack from templates')
    generate_parser.add_argument('--customer', required=True,
                                help='Customer organization name (e.g., "ACME Corp")')
    generate_parser.add_argument('--products', required=True,
                                help='Comma-separated product list (e.g., "OCP-BASE,OCP-NET")')
    generate_parser.add_argument('--output',
                                help='Output directory (default: ./{customer-slug}-ADRs/)')
    generate_parser.add_argument('--engagement-date',
                                help='Engagement date (default: today, format: YYYY-MM-DD)')
    generate_parser.add_argument('--architect',
                                help='Architect name (default: git config user.name)')
    generate_parser.add_argument('--force', action='store_true',
                                help='Overwrite existing output directory')
    generate_parser.add_argument('--local', action='store_true',
                                help='Force local mode (skip Google Docs even if available)')

    # Check subcommand
    check_parser = subparsers.add_parser('check',
                                        help='Validate ADR completion')
    check_parser.add_argument('input',
                             help='Customer ADR directory')
    check_parser.add_argument('--format', choices=['text', 'json', 'html'],
                             default='text',
                             help='Output format (default: text)')
    check_parser.add_argument('--fail-on-incomplete', action='store_true',
                             help='Exit code 1 if any #TODO# found')

    # Export subcommand
    export_parser = subparsers.add_parser('export',
                                         help='Export ADRs to Google Docs')
    export_parser.add_argument('--input', required=True,
                              help='Customer ADR directory')
    export_parser.add_argument('--customer',
                              help='Customer name (or read from metadata.yaml)')
    export_parser.add_argument('--output-format', dest='format',
                              choices=['google-doc', 'markdown', 'html'],
                              default='google-doc',
                              help='Export format (default: google-doc)')
    export_parser.add_argument('--exclude-not-discussed', action='store_true',
                              help='Skip ADRs with #TODO# in Decision field')
    export_parser.add_argument('--group-by', choices=['product', 'category', 'none'],
                              default='product',
                              help='Grouping strategy (default: product)')
    export_parser.add_argument('--create-toc', action='store_true', default=True,
                              help='Generate table of contents (default: true)')

    args = parser.parse_args()

    # Check if subcommand provided
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to appropriate handler
    if args.command == 'generate':
        generate_customer_adrs(args)
    elif args.command == 'check':
        check_adr_completion(args)
    elif args.command == 'export':
        export_adrs(args)


if __name__ == '__main__':
    main()
