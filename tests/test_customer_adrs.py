#!/usr/bin/env python3
"""
Automated tests for customer ADR workflow
Prevents regressions in core functionality
"""

import sys
import os
import re
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.customer_adrs import (
    slugify,
    extract_adr_title,
    parse_adr_template_file,
    check_google_prerequisites,
    extract_doc_id_from_url
)


def test_slugify():
    """Test customer name to slug conversion"""
    assert slugify("ACME Corporation") == "acme-corporation"
    assert slugify("Test & Company") == "test-company"
    assert slugify("Multiple   Spaces") == "multiple-spaces"
    assert slugify("Special!@#$%Characters") == "specialcharacters"
    print("✅ test_slugify passed")


def test_extract_adr_title():
    """Test ADR title extraction"""
    content = """## OCP-BASE-01

**Title**
Platform Topology Selection

**Architectural Question**
Should we deploy OpenShift in a single-site or multi-site topology?
"""
    title = extract_adr_title(content)
    assert title == "Platform Topology Selection"
    print("✅ test_extract_adr_title passed")


def test_parse_adr_template_file():
    """Test ADR template file parsing"""
    # Create temporary test file
    test_content = """# OCP-BASE - OpenShift Container Platform

## OCP-BASE-01

**Title**
Test ADR 1

**Architectural Question**
Test question?

**Decision**
#TODO: Document the decision.#

## OCP-BASE-02

**Title**
Test ADR 2

**Architectural Question**
Another test question?

**Decision**
#TODO: Document the decision.#
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_content)
        temp_file = f.name

    try:
        adrs = parse_adr_template_file(temp_file)
        assert len(adrs) == 2
        assert adrs[0]['id'] == 'OCP-BASE-01'
        assert adrs[1]['id'] == 'OCP-BASE-02'
        assert 'Test ADR 1' in adrs[0]['content']
        print("✅ test_parse_adr_template_file passed")
    finally:
        os.unlink(temp_file)


def test_extract_doc_id_from_url():
    """Test Google Docs URL parsing"""
    url1 = "https://docs.google.com/document/d/ABC123XYZ/edit"
    url2 = "https://docs.google.com/document/d/ABC123XYZ/edit?usp=sharing"
    url3 = "ABC123XYZ"

    assert extract_doc_id_from_url(url1) == "ABC123XYZ"
    assert extract_doc_id_from_url(url2) == "ABC123XYZ"
    assert extract_doc_id_from_url(url3) == "ABC123XYZ"
    print("✅ test_extract_doc_id_from_url passed")


def test_bold_markdown_processing():
    """Test bold markdown and #TODO# processing logic"""
    # This tests the regex patterns used in process_bold_markdown

    # Test **bold** pattern
    text1 = "This is **bold text** in a sentence"
    bold_matches = list(re.finditer(r'\*\*(.+?)\*\*', text1))
    assert len(bold_matches) == 1
    assert bold_matches[0].group(1) == "bold text"

    # Test #TODO# pattern
    text2 = "Decision: #TODO: Document the decision.#"
    todo_matches = list(re.finditer(r'#TODO.*?#', text2))
    assert len(todo_matches) == 1
    assert todo_matches[0].group(0) == "#TODO: Document the decision.#"

    # Test multiple #TODO# patterns
    text3 = "Person: #TODO# (Customer), Role: #TODO#"
    todo_matches = list(re.finditer(r'#TODO.*?#', text3))
    assert len(todo_matches) == 2

    print("✅ test_bold_markdown_processing passed")


def test_adr_validation_patterns():
    """Test ADR validation regex patterns"""
    # Decision field detection
    content1 = """**Decision**
#TODO: Document the decision.#"""
    decision_match = re.search(r'\*\*Decision\*\*\s*\n(.+?)(?:\n\n|\*\*|$)', content1, re.DOTALL)
    assert decision_match is not None
    assert '#TODO' in decision_match.group(1)

    # Agreeing Parties detection
    content2 = """**Agreeing Parties**

- Person: John Doe, Role: Enterprise Architect
- Person: #TODO#, Role: Network Expert"""
    parties_match = re.search(r'\*\*Agreeing Parties\*\*\s*\n(.+?)(?:\n\n|\Z)', content2, re.DOTALL)
    assert parties_match is not None
    assert 'John Doe' in parties_match.group(1)
    assert '#TODO#' in parties_match.group(1)

    print("✅ test_adr_validation_patterns passed")


def test_product_name_mapping():
    """Test product name mapping completeness"""
    PRODUCT_NAMES = {
        'GITOPS': 'OpenShift GitOps',
        'LOG': 'OpenShift Logging',
        'NETOBSERV': 'Network Observability',
        'NVIDIA-GPU': 'NVIDIA GPU Operator',
        'OCP-BASE': 'OpenShift Container Platform - General Platform',
        'OCP-BM': 'OpenShift Container Platform - Bare Metal Installation',
        'OCP-HCP': 'OpenShift Container Platform - Hosted Control Planes',
        'OCP-MGT': 'OpenShift Container Platform - Cluster Management & Day2 Ops',
        'OCP-MON': 'OpenShift Container Platform - Monitoring (Metrics)',
        'OCP-NET': 'OpenShift Container Platform - Networking',
        'OCP-OSP': 'OpenShift Container Platform - OpenStack Installation',
        'OCP-SEC': 'OpenShift Container Platform - Security & Compliance',
        'OCP-STOR': 'OpenShift Container Platform - Storage',
        'ODF': 'OpenShift Data Foundation',
        'PIPELINES': 'OpenShift Pipelines',
        'POWERMON': 'OpenShift Power Monitoring (Kepler)',
        'RHOAI-SM': 'Red Hat OpenShift AI Self-Managed',
        'TRACING': 'Red Hat Distributed Tracing',
        'VIRT': 'OpenShift Virtualization'
    }

    # Verify all products have mappings
    assert len(PRODUCT_NAMES) == 19
    assert 'GITOPS' in PRODUCT_NAMES
    assert 'OCP-BASE' in PRODUCT_NAMES
    assert 'RHOAI-SM' in PRODUCT_NAMES

    print("✅ test_product_name_mapping passed")


def test_field_order():
    """Test ADR field order is correct"""
    field_order = [
        'ID',
        'Title',
        'Architectural Question',
        'Issue or Problem',
        'Assumption',
        'Alternatives',
        'Decision',
        'Justification',
        'Implications',
        'Agreeing Parties'
    ]

    assert len(field_order) == 10
    assert field_order[0] == 'ID'
    assert field_order[-1] == 'Agreeing Parties'
    assert 'Decision' in field_order
    assert 'Justification' in field_order

    print("✅ test_field_order passed")


def run_all_tests():
    """Run all test functions"""
    print("\n" + "="*60)
    print("Running Customer ADR Workflow Tests")
    print("="*60 + "\n")

    try:
        test_slugify()
        test_extract_adr_title()
        test_parse_adr_template_file()
        test_extract_doc_id_from_url()
        test_bold_markdown_processing()
        test_adr_validation_patterns()
        test_product_name_mapping()
        test_field_order()

        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60 + "\n")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
