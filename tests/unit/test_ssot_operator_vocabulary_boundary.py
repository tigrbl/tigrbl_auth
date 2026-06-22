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
    "adr:1133",
    "spc:1223",
    "spc:1224",
    "spc:1225",
}

PUBLIC_VOCABULARY_PATHS = {
    ".ssot/specs/SPEC-1000-cli-contract-json.yaml",
    ".ssot/specs/SPEC-1001-cli-contract-yaml.yaml",
    "docs/compliance/cli_conformance_snapshot.json",
    "docs/compliance/cli_conformance_snapshot.md",
    "docs/reference/CLI_SURFACE.md",
    "pkgs/20-storage/tigrbl-identity-storage/README.md",
    "pkgs/20-storage/tigrbl-identity-storage/pyproject.toml",
    "pkgs/60-runtime/tigrbl-identity-cli/src/tigrbl_identity_cli/cli/metadata/_arguments.py",
    "pkgs/60-runtime/tigrbl-identity-cli/src/tigrbl_identity_cli/cli/metadata/_base.py",
    "pkgs/60-runtime/tigrbl-identity-cli/src/tigrbl_identity_cli/cli/metadata/_runtime_flags.py",
    "pkgs/60-runtime/tigrbl-identity-runtime/src/tigrbl_identity_runtime/feature_flags.py",
    "specs/cli/cli_contract.json",
    "specs/cli/cli_contract.yaml",
}

GENERATED_CLI_CONTRACT_SNAPSHOTS = {
    ".ssot/specs/SPEC-1000-cli-contract-json.yaml",
    ".ssot/specs/SPEC-1001-cli-contract-yaml.yaml",
    "specs/cli/cli_contract.json",
    "specs/cli/cli_contract.yaml",
}

REGISTRY_TEXT_FAMILIES = ("features", "claims", "tests", "evidence")
REGISTRY_TEXT_FIELDS = ("title", "description", "body")

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
    "operator plane": re.compile(r"\boperator[-\s]+plane\b", re.IGNORECASE),
    "operator surface": re.compile(
        r"\boperator[-\s]+(?:visible\s+)?(?:package\s+)?surfaces?\b",
        re.IGNORECASE,
    ),
    "operator workflow": re.compile(
        r"\bCLI/operator\s+workflows?\b|\boperator(?:[-\s]+only)?\s+workflows?\b",
        re.IGNORECASE,
    ),
    "operator lifecycle": re.compile(r"\boperator[-\s]+lifecycle\b", re.IGNORECASE),
    "operator authority": re.compile(
        r"\boperator\s+(?:authority|role\s+model|plane)\b",
        re.IGNORECASE,
    ),
    "operator CLI help": re.compile(
        r"\boperator\s+(?:CLI|verbosity|details|log\s+level)\b",
        re.IGNORECASE,
    ),
    "platform operator": re.compile(r"\bplatform\s+operators?\b", re.IGNORECASE),
}

SSOT_DOCUMENT_FORBIDDEN_PATTERNS = {
    label: pattern
    for label, pattern in FORBIDDEN_PATTERNS.items()
    if label not in {"operator surface", "operator lifecycle", "operator CLI help"}
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
    ]


def _semantic_document_text(row: dict) -> str:
    payload = yaml.safe_load((ROOT / row["path"]).read_text(encoding="utf-8")) or {}
    parts = (payload.get("title"), payload.get("summary"), payload.get("body"))
    return "\n".join(part for part in parts if isinstance(part, str))


def test_active_ssot_documents_do_not_reintroduce_operator_vocabulary() -> None:
    offenders: list[str] = []

    for row in _active_repo_local_documents():
        text = _semantic_document_text(row)
        for label, pattern in SSOT_DOCUMENT_FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                offenders.append(f"{row['id']} {label}: {row['path']}")

    assert offenders == []


def test_public_package_and_cli_text_do_not_reintroduce_operator_vocabulary() -> None:
    offenders: list[str] = []

    for relative_path in sorted(PUBLIC_VOCABULARY_PATHS):
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                offenders.append(f"{relative_path} {label}")

    assert offenders == []


def test_generated_cli_contract_snapshots_are_synced_with_retired_vocabulary() -> None:
    offenders: list[str] = []

    for relative_path in sorted(GENERATED_CLI_CONTRACT_SNAPSHOTS):
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                offenders.append(f"{relative_path} {label}")

    assert offenders == []


def test_active_registry_display_text_does_not_reintroduce_operator_vocabulary() -> None:
    offenders: list[str] = []
    registry = _registry()

    for family in REGISTRY_TEXT_FAMILIES:
        for row in registry.get(family, ()):
            if row.get("status") in {"retired", "superseded"}:
                continue
            text = "\n".join(
                str(row.get(field) or "")
                for field in REGISTRY_TEXT_FIELDS
                if isinstance(row.get(field), str)
            )
            for label, pattern in SSOT_DOCUMENT_FORBIDDEN_PATTERNS.items():
                if pattern.search(text):
                    offenders.append(f"{family}.{row.get('id')} {label}")

    assert offenders == []
