from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / ".ssot" / "registry.json"

GUARDRAIL_DOCUMENT_IDS = {
    "adr:1078",
    "adr:1132",
    "spc:1223",
    "spc:1224",
}

GENERATED_CONTRACT_SNAPSHOTS = {
    ".ssot/specs/SPEC-1000-cli-contract-json.yaml",
    ".ssot/specs/SPEC-1001-cli-contract-yaml.yaml",
}

FORBIDDEN_PATTERNS = {
    "public operator surface": re.compile(r"\bpublic\s+operator\s+surfaces?\b", re.IGNORECASE),
    "operator-style": re.compile(r"\boperator-style\b", re.IGNORECASE),
    "operator action": re.compile(
        r"\boperator(?:[-\s]+specific)?\s+actions?\b|\boperator\s+action\s+family\b",
        re.IGNORECASE,
    ),
    "operator state": re.compile(
        r"\boperator[-\s]+(?:owned\s+)?state(?:\s+model)?\b",
        re.IGNORECASE,
    ),
    "operator workflow": re.compile(
        r"\bCLI/operator\s+workflows?\b|\boperator(?:[-\s]+only)?\s+workflows?\b",
        re.IGNORECASE,
    ),
    "operator authority": re.compile(
        r"\boperator\s+(?:authority|role\s+model|plane)\b",
        re.IGNORECASE,
    ),
    "platform operator": re.compile(r"\bplatform\s+operators?\b", re.IGNORECASE),
}


def _registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _active_repo_local_documents() -> list[dict]:
    registry = _registry()
    rows = registry["adrs"] + registry["specs"]
    return [
        row
        for row in rows
        if row.get("origin") == "repo-local"
        and row.get("status") != "superseded"
        and row["id"] not in GUARDRAIL_DOCUMENT_IDS
        and row["path"] not in GENERATED_CONTRACT_SNAPSHOTS
    ]


def _semantic_document_text(row: dict) -> str:
    payload = yaml.safe_load((ROOT / row["path"]).read_text(encoding="utf-8")) or {}
    parts = (payload.get("title"), payload.get("summary"), payload.get("body"))
    return "\n".join(part for part in parts if isinstance(part, str))


def test_active_ssot_documents_do_not_reintroduce_operator_vocabulary() -> None:
    offenders: list[str] = []

    for row in _active_repo_local_documents():
        text = _semantic_document_text(row)
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                offenders.append(f"{row['id']} {label}: {row['path']}")

    assert offenders == []
