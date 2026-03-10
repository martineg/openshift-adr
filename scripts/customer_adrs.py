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
from pathlib import Path
from datetime import datetime
import yaml

# Repository paths
REPO_ROOT = Path(__file__).parent.parent
ADR_TEMPLATES_DIR = REPO_ROOT / 'adr_templates'


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
    output_dir = Path(args.output) if args.output else Path(f"./{slugify(customer)}-ADRs")
    engagement_date = args.engagement_date if args.engagement_date else datetime.now().strftime('%Y-%m-%d')
    architect = args.architect if args.architect else get_git_user_name()

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
    print("✅ Generated ADR pack for " + customer)
    print("="*80)
    print(f"\n📁 Output: {output_dir}/")
    print(f"📊 Total ADRs: {total_adrs}")
    for product, count in product_stats.items():
        print(f"   - {product}: {count}")
    print(f"⏱️  Estimated workshop time: ~{estimated_hours:.0f} hours")
    print(f"📖 Next: Review {output_dir}/README.md for instructions\n")


def check_adr_completion(args):
    """Check ADR completion status"""
    print("⚠️  Subcommand 'check' not yet implemented")
    print("📝 See RUN_SCRIPTS_REQUIREMENTS.md for specifications")
    sys.exit(0)


def export_adrs(args):
    """Export ADRs to Google Docs"""
    print("⚠️  Subcommand 'export' not yet implemented")
    print("📝 See RUN_SCRIPTS_REQUIREMENTS.md for specifications")
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
