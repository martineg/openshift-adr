#!/usr/bin/env python3
"""Regenerate dictionaries/adr_prefix_dictionary.md from dictionaries/products.yaml.

Usage: python scripts/regen_prefix_dictionary.py
"""
from pathlib import Path
import sys
import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _REPO_ROOT / "dictionaries" / "products.yaml"
_OUTPUT_PATH = _REPO_ROOT / "dictionaries" / "adr_prefix_dictionary.md"

_HEADER = """\
<!-- GENERATED FILE — do not edit. Source: dictionaries/products.yaml.
     Regenerate: python scripts/regen_prefix_dictionary.py -->

# Architecture Prefix Dictionary

This file maps workshop topics and products to their official Architecture Decision (AD) prefix.

| id_ad_prefix   | Topic / Product                                                                    |
| :------------- | :--------------------------------------------------------------------------------- |
"""


def main() -> None:
    with _CONFIG_PATH.open() as f:
        data = yaml.safe_load(f)

    products = sorted(data["products"], key=lambda p: p["prefix"])

    rows = []
    for p in products:
        prefix = p["prefix"]
        description = p["description"]
        rows.append(f"| {prefix:<14} | {description:<82} |\n")

    output = _HEADER + "".join(rows)

    output_file = Path(sys.argv[1]) if len(sys.argv) > 1 else _OUTPUT_PATH
    output_file.write_text(output)
    print(f"Written: {output_file}")


if __name__ == "__main__":
    main()
