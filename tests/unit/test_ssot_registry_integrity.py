from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / ".ssot" / "registry.json"

REQUIRED_SECTIONS = (
    "features",
    "profiles",
    "tests",
    "claims",
    "evidence",
    "issues",
    "risks",
    "boundaries",
    "releases",
    "adrs",
    "specs",
)


def _registry_bytes() -> bytes:
    return REGISTRY_PATH.read_bytes()


def _registry() -> dict:
    return json.loads(_registry_bytes().decode("utf-8"))


def test_registry_json_is_utf8_without_bom_and_parseable() -> None:
    payload = _registry_bytes()

    assert not payload.startswith(b"\xef\xbb\xbf")
    assert payload.endswith(b"\n")
    assert isinstance(json.loads(payload.decode("utf-8")), dict)


def test_registry_json_contains_complete_entity_sections() -> None:
    registry = _registry()

    for section in REQUIRED_SECTIONS:
        rows = registry.get(section)
        assert isinstance(rows, list), section
        assert rows, section


def test_registry_json_entity_ids_are_unique_by_section() -> None:
    registry = _registry()

    for section in REQUIRED_SECTIONS:
        ids = [row["id"] for row in registry[section]]
        assert len(ids) == len(set(ids)), section
