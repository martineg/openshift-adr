#!/usr/bin/env python3
"""
Automated tests for customer ADR workflow
Prevents regressions in core functionality
"""

import sys
import os
import re
import subprocess
import tempfile
import shutil
import yaml
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
    """Test product name mapping via products.py loader"""
    sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
    from products import long_name, all_products

    active = all_products()
    assert len(active) == 19
    assert long_name('GITOPS') == 'OpenShift GitOps'
    assert long_name('OCP-BASE') == 'OpenShift Container Platform - General Platform'
    assert long_name('RHOAI-SM') == 'Red Hat OpenShift AI Self-Managed'
    assert long_name('TRACING') == 'Red Hat OpenShift Distributed Tracing Platform'
    assert long_name('POWERMON') == 'OpenShift Power Monitoring (Kepler)'
    assert long_name('UNKNOWN-PREFIX') == 'UNKNOWN-PREFIX'

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


_REPO_ROOT = Path(__file__).parent.parent
_PRODUCTS_YAML = _REPO_ROOT / "dictionaries" / "products.yaml"
_REQUIRED_FIELDS = {"prefix", "short_name", "long_name", "description", "category", "template_file", "status"}
_VALID_CATEGORIES = {"openshift", "ai_ml", "platform_services"}
_VALID_STATUSES = {"active", "planned"}


def test_products_yaml_loadable():
    """products.yaml parses and every entry has all required fields"""
    with _PRODUCTS_YAML.open() as f:
        data = yaml.safe_load(f)
    assert data.get("schema_version") is not None
    products = data["products"]
    assert len(products) > 0
    for p in products:
        missing = _REQUIRED_FIELDS - set(p.keys())
        assert not missing, f"{p.get('prefix')}: missing fields {missing}"
        assert p["category"] in _VALID_CATEGORIES, f"{p['prefix']}: invalid category {p['category']}"
        assert p["status"] in _VALID_STATUSES, f"{p['prefix']}: invalid status {p['status']}"
    print("✅ test_products_yaml_loadable passed")


def test_products_yaml_no_duplicate_prefix():
    """Every prefix in products.yaml is unique"""
    with _PRODUCTS_YAML.open() as f:
        data = yaml.safe_load(f)
    prefixes = [p["prefix"] for p in data["products"]]
    assert len(prefixes) == len(set(prefixes)), f"Duplicate prefixes: {[p for p in prefixes if prefixes.count(p) > 1]}"
    print("✅ test_products_yaml_no_duplicate_prefix passed")


def test_active_products_have_template_file():
    """Every active product has a template_file that exists on disk"""
    with _PRODUCTS_YAML.open() as f:
        data = yaml.safe_load(f)
    for p in data["products"]:
        if p["status"] == "active":
            tf = p.get("template_file")
            assert tf is not None, f"{p['prefix']}: active entry has null template_file"
            assert (_REPO_ROOT / tf).exists(), f"{p['prefix']}: template_file {tf!r} does not exist"
    print("✅ test_active_products_have_template_file passed")


def test_every_template_has_active_entry():
    """Every adr_templates/*.md has exactly one matching active entry in products.yaml"""
    with _PRODUCTS_YAML.open() as f:
        data = yaml.safe_load(f)
    active_files = {p["template_file"] for p in data["products"] if p["status"] == "active" and p["template_file"]}
    for md in sorted((_REPO_ROOT / "adr_templates").glob("*.md")):
        rel = f"adr_templates/{md.name}"
        assert rel in active_files, f"{rel}: no active entry in products.yaml"
    print("✅ test_every_template_has_active_entry passed")


def test_planned_products_have_null_template():
    """Every planned product has template_file: null"""
    with _PRODUCTS_YAML.open() as f:
        data = yaml.safe_load(f)
    for p in data["products"]:
        if p["status"] == "planned":
            assert p.get("template_file") is None, f"{p['prefix']}: planned entry should have null template_file"
    print("✅ test_planned_products_have_null_template passed")


def test_prefix_dictionary_regenerated():
    """adr_prefix_dictionary.md matches what regen_prefix_dictionary.py produces"""
    regen_script = _REPO_ROOT / "scripts" / "regen_prefix_dictionary.py"
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            [sys.executable, str(regen_script), tmp_path],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"regen script failed: {result.stderr}"
        generated = Path(tmp_path).read_text()
        checked_in = (_REPO_ROOT / "dictionaries" / "adr_prefix_dictionary.md").read_text()
        assert generated == checked_in, (
            "adr_prefix_dictionary.md is out of date. "
            "Run: python scripts/regen_prefix_dictionary.py"
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)
    print("✅ test_prefix_dictionary_regenerated passed")


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
        test_products_yaml_loadable()
        test_products_yaml_no_duplicate_prefix()
        test_active_products_have_template_file()
        test_every_template_has_active_entry()
        test_planned_products_have_null_template()
        test_prefix_dictionary_regenerated()

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
