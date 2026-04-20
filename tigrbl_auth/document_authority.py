from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import yaml

SSOT_DOCUMENT_AUTHORITY_SPEC = ".ssot/specs/SPEC-1052-ssot-document-authority.yaml"
DOCUMENT_AUTHORITY_PROJECTION_YAML = "compliance/targets/document-authority.yaml"

DEFAULT_CANONICAL_SSOT_ROOTS = (
    ".ssot/registry.json",
    ".ssot/adr",
    ".ssot/specs",
)

DEFAULT_AUTHORITATIVE_DOCS = {
    "README.md",
    "CURRENT_STATE.md",
    "CERTIFICATION_STATUS.md",
    "docs/compliance/README.md",
    "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md",
    "docs/compliance/truth_chain.md",
    "docs/compliance/current_state_report.md",
    "docs/compliance/install_substrate_report.md",
    "docs/compliance/certification_state_report.md",
    "docs/compliance/runtime_profile_report.md",
    "docs/compliance/release_gate_report.md",
    "docs/compliance/final_release_gate_report.md",
    "docs/compliance/validated_execution_report.md",
    "docs/compliance/release_signing_report.md",
    "docs/compliance/FINAL_RELEASE_STATUS_2026-03-25.md",
    "docs/compliance/RELEASE_DECISION_RECORD.md",
    "docs/reference/README.md",
    "docs/reference/CLI_SURFACE.md",
    "docs/reference/PUBLIC_ROUTE_SURFACE.md",
    "docs/reference/RPC_OPERATOR_SURFACE.md",
    "docs/reference/DISCOVERY_PROFILE_SNAPSHOTS.md",
}

DEFAULT_EXPLICITLY_DEAUTHORIZED_CURRENT_ADJACENT_DOCS = [
    "docs/compliance/BOUNDARY_FREEZE_DECISION_2026-03-26.md",
    "docs/compliance/CLEAN_ROOM_EXECUTOR_AND_EVIDENCE_CHECKPOINT_2026-03-27.md",
    "docs/compliance/STEP12_FINAL_CERTIFICATION_AGGREGATION_CHECKPOINT_2026-03-27.md",
    "docs/compliance/PEER_MATRIX_REPORT.md",
    "docs/compliance/TIER4_PROMOTION_MATRIX.md",
    "docs/compliance/CERTIFIABLE_COMPLETION_PLAN_2026-03-26.md",
    "docs/compliance/CERTIFIABLE_DELIVERY_PLAN_2026-03-27.md",
    "docs/compliance/TARGET_REALITY_MATRIX.md",
]

DEFAULT_GENERATED_CURRENT_STATE_DOCS = (
    "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.json",
    "docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md",
    "docs/compliance/truth_chain.json",
    "docs/compliance/truth_chain.md",
    "docs/compliance/current_state_report.json",
    "docs/compliance/current_state_report.md",
    "docs/compliance/install_substrate_report.json",
    "docs/compliance/install_substrate_report.md",
    "docs/compliance/certification_state_report.json",
    "docs/compliance/certification_state_report.md",
    "docs/compliance/runtime_profile_report.json",
    "docs/compliance/runtime_profile_report.md",
    "docs/compliance/release_gate_report.json",
    "docs/compliance/release_gate_report.md",
    "docs/compliance/final_release_gate_report.json",
    "docs/compliance/final_release_gate_report.md",
    "docs/compliance/validated_execution_report.json",
    "docs/compliance/validated_execution_report.md",
    "docs/compliance/release_signing_report.json",
    "docs/compliance/release_signing_report.md",
    "docs/compliance/FINAL_RELEASE_STATUS_2026-03-25.json",
    "docs/compliance/FINAL_RELEASE_STATUS_2026-03-25.md",
)

DEFAULT_SUPPORTING_CURRENT_NON_DOC_ARTIFACTS = [
    "specs/cli/cli_contract.json",
    "specs/cli/cli_contract.yaml",
]


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def load_document_authority(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    path = repo_root / SSOT_DOCUMENT_AUTHORITY_SPEC
    payload = _load_yaml(path)
    authority = payload.get("document_authority", {}) if isinstance(payload, dict) else {}
    return {
        "path": str(path.relative_to(repo_root)) if path.exists() else SSOT_DOCUMENT_AUTHORITY_SPEC,
        "projection_path": str(authority.get("projection_manifest", DOCUMENT_AUTHORITY_PROJECTION_YAML)),
        "canonical_ssot_roots": tuple(
            str(item) for item in authority.get("canonical_ssot_roots", []) or DEFAULT_CANONICAL_SSOT_ROOTS
        ),
        "authoritative_current_docs": set(
            str(item) for item in authority.get("authoritative_current_docs", []) or DEFAULT_AUTHORITATIVE_DOCS
        ),
        "archived_historical_roots": tuple(
            str(item).rstrip("/")
            for item in authority.get("archived_historical_roots", []) or ("docs/archive/historical",)
        ),
        "explicitly_deauthorized_current_adjacent_docs": [
            str(item)
            for item in authority.get("explicitly_deauthorized_current_adjacent_docs", [])
            or DEFAULT_EXPLICITLY_DEAUTHORIZED_CURRENT_ADJACENT_DOCS
        ],
        "current_release_bundle_docs": [
            str(item)
            for item in authority.get("current_release_bundle_docs", [])
            or list(DEFAULT_GENERATED_CURRENT_STATE_DOCS)
        ],
        "supporting_current_non_doc_artifacts": [
            str(item)
            for item in authority.get("supporting_current_non_doc_artifacts", [])
            or DEFAULT_SUPPORTING_CURRENT_NON_DOC_ARTIFACTS
        ],
    }


def render_document_authority_projection(authority: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at": date.today().isoformat(),
        "projection_of": authority["path"],
        "canonical_ssot_roots": list(authority["canonical_ssot_roots"]),
        "authoritative_current_docs": sorted(authority["authoritative_current_docs"]),
        "archived_historical_roots": list(authority["archived_historical_roots"]),
        "explicitly_deauthorized_current_adjacent_docs": list(
            authority["explicitly_deauthorized_current_adjacent_docs"]
        ),
        "current_release_bundle_docs": list(authority["current_release_bundle_docs"]),
        "supporting_current_non_doc_artifacts": list(authority["supporting_current_non_doc_artifacts"]),
        "notes": {
            "bundle_policy": "Only generated current-state and release-decision docs in this manifest are copied into certification release bundles.",
            "archive_policy": "Historical planning, checkpoint, and static matrix docs outside the authoritative set are non-authoritative and must not be used for current release claims.",
        },
    }
