"""Single source of truth for product metadata.

Reads dictionaries/products.yaml once per process.
Callers: customer_adrs.py, stats.py, build_presentation.py.
"""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
import yaml

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _REPO_ROOT / "dictionaries" / "products.yaml"


@lru_cache(maxsize=1)
def _load() -> list[dict]:
    with _CONFIG_PATH.open() as f:
        data = yaml.safe_load(f)
    return data["products"]


def all_products(include_planned: bool = False) -> list[dict]:
    products = _load()
    if include_planned:
        return products
    return [p for p in products if p["status"] == "active"]


def by_prefix(prefix: str) -> dict | None:
    for p in _load():
        if p["prefix"] == prefix:
            return p
    return None


def short_name(prefix: str) -> str:
    p = by_prefix(prefix)
    return p["short_name"] if p else prefix


def long_name(prefix: str) -> str:
    p = by_prefix(prefix)
    return p["long_name"] if p else prefix


def by_category() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for p in all_products():
        out.setdefault(p["category"], []).append(p)
    return out
