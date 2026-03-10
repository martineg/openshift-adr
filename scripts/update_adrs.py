#!/usr/bin/env python3
"""
Update ADRs using Claude Code API

This script automates ADR review and updates when a new product version is released.

Prerequisites:
1. Download new product documentation using doc_downloader
2. Set ANTHROPIC_API_KEY environment variable
3. Install: pip install anthropic

Usage:
    export ANTHROPIC_API_KEY="your-api-key"
    python scripts/update_adrs.py <PREFIX>

Example:
    python scripts/update_adrs.py RHOAI-SM

The script will:
1. Read the ADR file (adr/<PREFIX>.md)
2. Read documentation from docs/<product>/*.pdf
3. Use Claude to analyze for updates needed
4. Generate a report with recommended changes
5. Optionally apply changes (with confirmation)
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("❌ Error: anthropic package not installed")
    print("Install with: pip install anthropic")
    sys.exit(1)

# Repository paths
REPO_ROOT = Path(__file__).parent.parent
ADR_DIR = REPO_ROOT / 'adr'
DOCS_DIR = REPO_ROOT / 'docs'
DICTIONARIES_DIR = REPO_ROOT / 'dictionaries'

def read_file(filepath):
    """Read file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def get_documentation_context(prefix):
    """Get product documentation context based on prefix"""
    # Map prefixes to documentation directories
    doc_mapping = {
        'RHOAI-SM': 'rhoai',
        'OCP-BASE': 'ocp',
        'OCP-BM': 'ocp',
        'OCP-NET': 'ocp',
        'OCP-SEC': 'ocp',
        'OCP-STOR': 'ocp',
        'GITOPS': 'gitops',
        # Add more mappings as needed
    }

    product_key = prefix.split('-')[0]
    if prefix in doc_mapping:
        doc_subdir = doc_mapping[prefix]
    elif product_key in doc_mapping:
        doc_subdir = doc_mapping[product_key]
    else:
        doc_subdir = prefix.lower()

    doc_path = DOCS_DIR / doc_subdir

    if not doc_path.exists():
        print(f"⚠️  Warning: Documentation not found at {doc_path}")
        print(f"   Run: cd doc_downloader && ./download_all_docs.sh")
        return ""

    # List available PDFs
    pdf_files = list(doc_path.glob('*.pdf'))
    if pdf_files:
        print(f"📚 Found {len(pdf_files)} documentation files:")
        for pdf in pdf_files:
            print(f"   - {pdf.name}")
        return f"Documentation available in: {doc_path}"
    else:
        return ""

def build_prompt(prefix, adr_content, governance_rules, exclusions):
    """Build Claude prompt for ADR review"""

    prompt = f"""You are reviewing Architecture Decision Records (ADRs) for updates based on new product documentation.

# Task
Review the ADRs in {prefix}.md and identify:
1. ADRs that need updates (changed features, new alternatives, deprecated options)
2. ADRs that should be removed (obsolete, no longer applicable)
3. New ADRs needed (new features requiring architectural decisions)

# ADR File Content
{adr_content}

# Governance Rules
{governance_rules}

# Exclusion Rules
{exclusions}

# Instructions
1. Compare each ADR against the latest product documentation
2. Identify specific changes needed (be precise with ADR IDs)
3. For updates: specify exactly what changed and why
4. For removals: explain why the ADR is obsolete
5. For new ADRs: suggest the architectural question and alternatives

# Output Format
Provide a structured report:

## Updates Required
[List ADR IDs with specific changes needed]

## Removals Recommended
[List ADR IDs with removal justification]

## New ADRs Suggested
[List new architectural questions discovered]

## Summary
[Brief statistics and overall assessment]

# Important
- Document CURRENT STATE ONLY (no version numbers)
- Valid ADRs have 2+ viable alternatives (not right vs wrong)
- Check exclusions list before suggesting new ADRs
- Be specific with changes (include ADR section: Question, Alternatives, Decision, etc.)
"""

    return prompt

def analyze_adrs(prefix, api_key):
    """Analyze ADRs using Claude"""

    # Read ADR file
    adr_file = ADR_DIR / f"{prefix}.md"
    if not adr_file.exists():
        print(f"❌ Error: ADR file not found: {adr_file}")
        print(f"   Available: {', '.join([f.stem for f in ADR_DIR.glob('*.md')])}")
        sys.exit(1)

    adr_content = read_file(adr_file)
    if not adr_content:
        sys.exit(1)

    # Read governance files
    governance_file = DICTIONARIES_DIR / 'adr_governance_rules.md'
    exclusions_file = DICTIONARIES_DIR / 'adr_exclusions.md'

    governance_rules = read_file(governance_file) or "No governance rules available"
    exclusions = read_file(exclusions_file) or "No exclusions available"

    # Get documentation context
    doc_context = get_documentation_context(prefix)

    print("="*80)
    print(f"Analyzing ADRs: {prefix}")
    print("="*80)
    print(f"\n📄 ADR file: {adr_file}")
    print(f"📚 Documentation: {doc_context if doc_context else 'Not found - download required'}")
    print(f"\n🤖 Using Claude Sonnet 4.5 for analysis...\n")

    # Initialize Claude client
    client = Anthropic(api_key=api_key)

    # Build prompt
    prompt = build_prompt(prefix, adr_content, governance_rules, exclusions)

    # Call Claude
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        analysis = message.content[0].text

        # Save report
        report_file = REPO_ROOT / f"{prefix}-Analysis-Report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# {prefix} ADR Analysis Report\n\n")
            f.write(f"**Generated:** {__import__('datetime').datetime.now().isoformat()}\n\n")
            f.write(f"**Analyzed:** {adr_file}\n\n")
            f.write("---\n\n")
            f.write(analysis)

        print("="*80)
        print("✅ Analysis complete")
        print("="*80)
        print(f"\n📊 Report saved: {report_file}")
        print(f"\n📝 Review the report and apply changes manually to {adr_file}")
        print("\n💡 Tip: Use scripts/renumber_adrs.py after adding/removing ADRs")

        return analysis

    except Exception as e:
        print(f"❌ Error calling Claude API: {e}")
        sys.exit(1)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Update ADRs using Claude Code API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze RHOAI-SM ADRs
  python scripts/update_adrs.py RHOAI-SM

  # Analyze OCP-NET ADRs
  python scripts/update_adrs.py OCP-NET

Prerequisites:
  1. Download documentation: cd doc_downloader && ./download_all_docs.sh
  2. Set API key: export ANTHROPIC_API_KEY="your-key"
  3. Install package: pip install anthropic
        """
    )

    parser.add_argument('prefix', help='ADR prefix (e.g., RHOAI-SM, OCP-NET)')

    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        print("\nGet your API key from: https://console.anthropic.com/")
        sys.exit(1)

    # Analyze ADRs
    analyze_adrs(args.prefix, api_key)

if __name__ == '__main__':
    main()
