from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from tigrbl_identity_operator.document_authority import (
    DEFAULT_GENERATED_CURRENT_STATE_DOCS,
    load_document_authority,
    render_document_authority_projection,
)

DERIVED_CURRENT_DOCS = {
    "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.json",
    "docs/compliance/current_state_report.json",
    "docs/compliance/certification_state_report.json",
    "docs/compliance/runtime_profile_report.json",
    "docs/compliance/release_gate_report.json",
    "docs/compliance/final_release_gate_report.json",
    "docs/compliance/validated_execution_report.json",
    "docs/compliance/release_signing_report.json",
    "docs/compliance/FINAL_RELEASE_STATUS_2026-03-25.json",
    "docs/compliance/final_target_decision_matrix.json",
    "docs/compliance/peer_matrix_report.json",
}


def _write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _docs_for_certification_bundle(repo_root: Path) -> list[str]:
    authority = load_document_authority(repo_root)
    docs = authority.get("current_release_bundle_docs", list(DEFAULT_GENERATED_CURRENT_STATE_DOCS))
    return [rel for rel in docs if (repo_root / rel).exists()]


def write_authoritative_current_docs_manifest(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    authority = load_document_authority(repo_root)
    _write_yaml(repo_root / authority["projection_path"], render_document_authority_projection(authority))
    payload = {
        "schema_version": 1,
        "authority_spec": authority.get("path"),
        "projection_manifest": authority.get("projection_path"),
        "canonical_ssot_roots": list(authority.get("canonical_ssot_roots", ())),
        "authoritative_current_docs": sorted(authority.get("authoritative_current_docs", set())),
        "derived_current_docs": sorted(DERIVED_CURRENT_DOCS),
        "archive_roots": list(authority.get("archived_historical_roots", ())),
        "certification_bundle_generated_current_docs": _docs_for_certification_bundle(repo_root),
        "supporting_current_non_doc_artifacts": list(authority.get("supporting_current_non_doc_artifacts", [])),
        "historical_docs_policy": "Historical and archived docs are non-authoritative and excluded from the certification bundle documentation scope.",
    }
    report_dir = repo_root / "docs" / "compliance"
    _write_json(report_dir / "AUTHORITATIVE_CURRENT_DOCS.json", payload)
    lines = [
        "# Authoritative current docs",
        "",
        "This file is a compatibility projection of the current certification and release-facing docs derived from the SSOT authority spec.",
        "",
        f"- authority_spec: `{payload['authority_spec']}`",
        f"- projection_manifest: `{payload['projection_manifest']}`",
        "- authority_note: `.ssot/` is authoritative; this file is not.",
        "",
        "## Canonical SSOT roots",
        "",
    ]
    lines.extend([f"- `{item}`" for item in payload["canonical_ssot_roots"]])
    lines.extend(["", "## Current release-facing docs", ""])
    lines.extend([f"- `{item}`" for item in payload["authoritative_current_docs"]])
    lines.extend(["", "## Derived current docs", ""])
    lines.extend([f"- `{item}`" for item in payload["derived_current_docs"]])
    lines.extend(["", "## Certification bundle documentation scope", ""])
    lines.extend([f"- `{item}`" for item in payload["certification_bundle_generated_current_docs"]])
    lines.extend(["", "## Supporting current non-doc artifacts", ""])
    lines.extend([f"- `{item}`" for item in payload["supporting_current_non_doc_artifacts"]])
    lines.extend(["", "## Archive policy", ""])
    lines.extend([f"- archive_root: `{item}`" for item in payload["archive_roots"]])
    lines.append(f"- policy: {payload['historical_docs_policy']}")
    lines.append("- projection_policy: `.ssot/` remains authoritative; this manifest is informational compatibility output.")
    lines.append("")
    (report_dir / "AUTHORITATIVE_CURRENT_DOCS.md").write_text("\n".join(lines), encoding="utf-8")
    return payload


__all__ = [
    "DERIVED_CURRENT_DOCS",
    "_docs_for_certification_bundle",
    "write_authoritative_current_docs_manifest",
]
