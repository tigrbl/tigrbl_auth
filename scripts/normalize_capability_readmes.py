"""Normalize layer-40 README ownership sections from the capability registry."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_ROOT = ROOT / "pkgs" / "40-capabilities"


def _items(values: list[str], empty: str) -> str:
    return "\n".join(f"- `{value}`" for value in values) if values else f"- {empty}"


def normalize() -> None:
    registry = json.loads((CAPABILITY_ROOT / "capability-families.json").read_text(encoding="utf-8"))
    for record in registry["capabilities"]:
        readme = CAPABILITY_ROOT / record["package"] / "README.md"
        text = readme.read_text(encoding="utf-8").rstrip()
        dependencies = record["dependencies"]
        injected = dependencies["providers"] + dependencies["durability"] + dependencies["capabilities"]
        operations = [
            operation
            for implementation in record["implementations"]
            for operation in implementation["operations"]
        ]
        sections = {
            "## Injected dependencies": _items(injected, "No package-mandated runtime dependency; callables are constructor-injected."),
            "## Operations and readiness": _items(operations, "See the capability report for the effective operation registry and readiness."),
            "## Protocol consumers": _items(record["protocol_packages"], "Protocol-neutral; layer-50 packages may bind these operations."),
            "## Non-goals": "- No HTTP or protocol wire schemas.\n- No direct layer-01 table access.\n- No hidden mutable persistence or provider selection.",
        }
        for heading, body in sections.items():
            if heading not in text:
                text += f"\n\n{heading}\n\n{body}"
        readme.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    normalize()
