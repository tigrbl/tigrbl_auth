from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Mapping

import yaml

from tigrbl_auth.document_authority import SSOT_DOCUMENT_AUTHORITY_SPEC, load_document_authority

ROOT_CURRENT_STATE = "CURRENT_STATE.md"
ROOT_CERTIFICATION_STATUS = "CERTIFICATION_STATUS.md"
TRUTH_CHAIN_JSON = "docs/compliance/truth_chain.json"
TRUTH_CHAIN_MD = "docs/compliance/truth_chain.md"
CURRENT_STATE_REPORT_JSON = "docs/compliance/current_state_report.json"
CURRENT_STATE_REPORT_MD = "docs/compliance/current_state_report.md"
CERTIFICATION_STATE_REPORT_JSON = "docs/compliance/certification_state_report.json"
CERTIFICATION_STATE_REPORT_MD = "docs/compliance/certification_state_report.md"
RELEASE_GATE_REPORT_JSON = "docs/compliance/release_gate_report.json"
RELEASE_GATE_REPORT_MD = "docs/compliance/release_gate_report.md"
FINAL_RELEASE_GATE_REPORT_JSON = "docs/compliance/final_release_gate_report.json"
FINAL_RELEASE_GATE_REPORT_MD = "docs/compliance/final_release_gate_report.md"
RELEASE_DECISION_RECORD_MD = "docs/compliance/RELEASE_DECISION_RECORD.md"
REPOSITORY_STATE_YAML = "compliance/claims/repository-state.yaml"
DEFAULT_FINAL_RELEASE_STATUS_STEM = "FINAL_RELEASE_STATUS_2026-03-25"
REPOSITORY_STATE_KEY_ALIASES = {
    "target_profile_truth_reconciled_complete": (),
    "profile_scope_mismatch_set_empty": (),
    "clean_room_executor_matrix_declared_complete": (),
    "validated_manifest_identity_contract_installed": (),
    "claim_registry_canonical_complete": (),
    "fapi2_security_profile_declared_complete": (),
    "release_claims_machine_derivable": (),
    "core_targets_missing_from_feature_map": (),
    "extension_targets_missing_from_feature_map": (),
    "settings_backed_flags_missing_from_flag_map": (),
    "release_gate_passed_for_final_decision": (),
    "final_release_decision_complete": (),
    "release_decision_record_present": (),
    "validated_runtime_matrix_preservation_complete": (),
    "validated_test_lane_preservation_complete": (),
    "validated_migration_portability_preservation_complete": (),
}
CHRONOLOGY_SCOPED_REPOSITORY_STATE_KEYS = {
    "boundary_lock_complete",
    "claim_boundary_rebaseline_complete",
    "tigrbl_runtime_foundation_complete",
    "persistence_domain_split_complete",
    "baseline_interoperable_auth_server_complete",
    "partial_feature_boundary_enforcement_complete",
    "boundary_decisions_enforcement_complete",
    "rfc_family_runtime_completion_checkpoint",
    "tier3_evidence_subset_complete",
    "external_peer_framework_complete",
    "independent_peer_program_extended_complete",
    "target_to_peer_mapping_complete",
    "peer_counterpart_catalog_complete",
    "peer_schema_and_tooling_extended",
    *{
        alias
        for aliases in REPOSITORY_STATE_KEY_ALIASES.values()
        for alias in aliases
    },
}


def _state_value(repository_state: Mapping[str, Any], key: str, default: Any = False) -> Any:
    if key in repository_state:
        return repository_state[key]
    for alias in REPOSITORY_STATE_KEY_ALIASES.get(key, ()):
        if alias in repository_state:
            return repository_state[alias]
    return default


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, json.dumps(payload, indent=2))


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    _write_text(path, yaml.safe_dump(payload, sort_keys=False))


def _hash_file(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.suffix.lower() in {".json", ".md", ".yaml", ".yml"}:
        payload = _normalized_text(path.read_text(encoding="utf-8")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalized_text(text: str) -> str:
    return text.replace("\r\n", "\n").rstrip("\n")


def _render_report_markdown(title: str, payload: dict[str, Any]) -> str:
    lines = [f"# {title}", "", f"- Passed: `{payload.get('passed', False)}`", ""]
    if payload.get("summary"):
        lines.extend(["## Summary", ""])
        for key, value in payload["summary"].items():
            lines.append(f"- {key}: `{value}`")
        lines.append("")
    if payload.get("failures"):
        lines.extend(["## Failures", ""])
        lines.extend(f"- {item}" for item in payload["failures"])
        lines.append("")
    if payload.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {item}" for item in payload["warnings"])
        lines.append("")
    if payload.get("details"):
        lines.extend(["## Details", ""])
        details = payload["details"]
        if isinstance(details, dict):
            for key, value in details.items():
                lines.append(f"- {key}: `{value}`")
        else:
            lines.extend(f"- {item}" for item in details)
        lines.append("")
    return "\n".join(lines)


def _final_release_status_stem(repo_root: Path) -> str:
    docs_dir = repo_root / "docs" / "compliance"
    candidates = sorted(path.stem for path in docs_dir.glob("FINAL_RELEASE_STATUS_*.json"))
    if candidates:
        return candidates[-1]
    candidates = sorted(path.stem for path in docs_dir.glob("FINAL_RELEASE_STATUS_*.md"))
    if candidates:
        return candidates[-1]
    return DEFAULT_FINAL_RELEASE_STATUS_STEM


def _final_release_status_paths(repo_root: Path) -> tuple[Path, Path]:
    stem = _final_release_status_stem(repo_root)
    docs_dir = repo_root / "docs" / "compliance"
    return docs_dir / f"{stem}.json", docs_dir / f"{stem}.md"


def _truth_inputs(repo_root: Path) -> dict[str, Any]:
    current = _read_json(repo_root / CURRENT_STATE_REPORT_JSON)
    certification = _read_json(repo_root / CERTIFICATION_STATE_REPORT_JSON)
    release_gate = _read_json(repo_root / RELEASE_GATE_REPORT_JSON)
    final_release_gate = _read_json(repo_root / FINAL_RELEASE_GATE_REPORT_JSON)
    non_rfc = _read_json(repo_root / "docs" / "compliance" / "non_rfc_status_report.json")
    repository_state = _read_yaml(repo_root / REPOSITORY_STATE_YAML).get("repository_state", {})
    authority = load_document_authority(repo_root)
    return {
        "current": current,
        "certification": certification,
        "release_gate": release_gate,
        "final_release_gate": final_release_gate,
        "non_rfc": non_rfc,
        "repository_state": repository_state,
        "authority": authority,
    }


def _final_release_status_payload(truth: dict[str, Any]) -> dict[str, Any]:
    summary = truth["summary"]
    blockers = list(summary.get("open_gaps", []))
    blockers.extend(summary.get("final_release_failures", []))
    ordered_blockers = list(dict.fromkeys(str(item) for item in blockers if str(item).strip()))
    return {
        "schema_version": 1,
        "passed": bool(summary["final_release_ready"]),
        "summary": {
            "final_release_ready": bool(summary["final_release_ready"]),
            "fully_certifiable_now": bool(summary["fully_certifiable_now"]),
            "fully_rfc_compliant_now": bool(summary["fully_rfc_compliant_now"]),
            "fully_non_rfc_spec_compliant_now": bool(summary["fully_non_rfc_spec_compliant_now"]),
            "strict_independent_claims_ready": bool(summary["strict_independent_claims_ready"]),
            "release_gates_passed": bool(summary["release_gates_passed"]),
            "final_release_gate_passed": bool(summary["final_release_gate_passed"]),
        },
        "details": ordered_blockers,
    }


def build_truth_chain_payload(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    inputs = _truth_inputs(repo_root)
    current_summary = inputs["current"].get("summary", {}) if isinstance(inputs["current"], dict) else {}
    cert_summary = inputs["certification"].get("summary", {}) if isinstance(inputs["certification"], dict) else {}
    release_gate_summary = inputs["release_gate"].get("summary", {}) if isinstance(inputs["release_gate"], dict) else {}
    final_gate_summary = inputs["final_release_gate"].get("summary", {}) if isinstance(inputs["final_release_gate"], dict) else {}
    non_rfc_summary = inputs["non_rfc"].get("summary", {}) if isinstance(inputs["non_rfc"], dict) else {}
    fully_non_rfc_spec_compliant_now = bool(non_rfc_summary.get("certifiably_fully_non_rfc_spec_compliant_now", False))
    fully_certifiable_now = bool(cert_summary.get("fully_certifiable_now", False))
    fully_rfc_compliant_now = bool(cert_summary.get("fully_rfc_compliant_now", False))
    strict_independent_claims_ready = bool(cert_summary.get("strict_independent_claims_ready", False))
    release_gates_passed = bool(inputs["release_gate"].get("passed", False))
    final_release_gate_passed = bool(inputs["final_release_gate"].get("passed", False))
    final_release_ready = (
        fully_certifiable_now
        and fully_rfc_compliant_now
        and fully_non_rfc_spec_compliant_now
        and strict_independent_claims_ready
        and final_release_gate_passed
    )
    deauthorized = [
        str(item)
        for item in inputs["authority"].get("explicitly_deauthorized_current_adjacent_docs", []) or []
    ]
    return {
        "schema_version": 1,
        "generated_at": date.today().isoformat(),
        "source_of_truth": [
            ".ssot/registry.json",
            SSOT_DOCUMENT_AUTHORITY_SPEC,
            CURRENT_STATE_REPORT_JSON,
            CERTIFICATION_STATE_REPORT_JSON,
            RELEASE_GATE_REPORT_JSON,
            FINAL_RELEASE_GATE_REPORT_JSON,
            "docs/compliance/non_rfc_status_report.json",
        ],
        "summary": {
            "declared_claim_count": int(current_summary.get("declared_claim_count", 0)),
            "tier_3_claim_count": int(current_summary.get("tier_3_claim_count", 0)),
            "tier_4_claim_count": int(current_summary.get("tier_4_claim_count", 0)),
            "validated_inventory_complete": bool(current_summary.get("validated_inventory_complete", False)),
            "validated_runtime_matrix_green": bool(current_summary.get("validated_clean_room_matrix_green", False)),
            "validated_test_lanes_green": bool(current_summary.get("validated_in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(current_summary.get("migration_portability_passed", False)),
            "tier3_evidence_rebuilt_from_validated_runs": bool(current_summary.get("tier3_evidence_rebuilt_from_validated_runs", False)),
            "fully_featured_package_boundary_now": bool(current_summary.get("fully_featured_package_boundary_now", False)),
            "strict_independent_claims_ready": strict_independent_claims_ready,
            "fully_certifiable_now": fully_certifiable_now,
            "fully_rfc_compliant_now": fully_rfc_compliant_now,
            "fully_non_rfc_spec_compliant_now": fully_non_rfc_spec_compliant_now,
            "release_gates_passed": release_gates_passed,
            "release_gate_count": int(release_gate_summary.get("gate_count", 0)),
            "release_gate_failed_count": int(release_gate_summary.get("failed_gate_count", 0)),
            "final_release_gate_passed": final_release_gate_passed,
            "final_release_ready": final_release_ready,
            "checkpoint_only": not final_release_ready,
            "target_profile_truth_reconciled_complete": bool(_state_value(inputs["repository_state"], "target_profile_truth_reconciled_complete", False)),
            "profile_scope_mismatch_set_empty": bool(_state_value(inputs["repository_state"], "profile_scope_mismatch_set_empty", False)),
            "clean_room_executor_matrix_declared_complete": bool(_state_value(inputs["repository_state"], "clean_room_executor_matrix_declared_complete", False)),
            "validated_manifest_identity_contract_installed": bool(_state_value(inputs["repository_state"], "validated_manifest_identity_contract_installed", False)),
            "claim_registry_canonical_complete": bool(_state_value(inputs["repository_state"], "claim_registry_canonical_complete", False)),
            "fapi2_security_profile_declared_complete": bool(_state_value(inputs["repository_state"], "fapi2_security_profile_declared_complete", False)),
            "release_claims_machine_derivable": bool(_state_value(inputs["repository_state"], "release_claims_machine_derivable", False)),
            "core_targets_missing_from_feature_map": int(_state_value(inputs["repository_state"], "core_targets_missing_from_feature_map", 0)),
            "extension_targets_missing_from_feature_map": int(_state_value(inputs["repository_state"], "extension_targets_missing_from_feature_map", 0)),
            "settings_backed_flags_missing_from_flag_map": int(_state_value(inputs["repository_state"], "settings_backed_flags_missing_from_flag_map", 0)),
            "tier4_external_bundle_count": int(cert_summary.get("tier4_external_bundle_count", current_summary.get("tier4_external_bundle_count", 0))),
            "tier4_valid_external_bundle_count": int(cert_summary.get("tier4_valid_external_bundle_count", current_summary.get("tier4_valid_external_bundle_count", 0))),
            "tier4_invalid_external_bundle_count": int(cert_summary.get("tier4_invalid_external_bundle_count", current_summary.get("tier4_invalid_external_bundle_count", 0))),
            "tier4_missing_external_bundle_count": int(cert_summary.get("tier4_missing_external_bundle_count", current_summary.get("tier4_missing_external_bundle_count", 0))),
            "open_gaps": list(cert_summary.get("open_gaps", []) or []),
            "final_release_failures": list(inputs["final_release_gate"].get("failures", []) or []),
            "final_release_warnings": list(inputs["final_release_gate"].get("warnings", []) or []),
            "explicitly_deauthorized_current_adjacent_doc_count": len(deauthorized),
        },
        "artifacts": {
            CURRENT_STATE_REPORT_JSON: _hash_file(repo_root / CURRENT_STATE_REPORT_JSON),
            CERTIFICATION_STATE_REPORT_JSON: _hash_file(repo_root / CERTIFICATION_STATE_REPORT_JSON),
            RELEASE_GATE_REPORT_JSON: _hash_file(repo_root / RELEASE_GATE_REPORT_JSON),
            FINAL_RELEASE_GATE_REPORT_JSON: _hash_file(repo_root / FINAL_RELEASE_GATE_REPORT_JSON),
            "docs/compliance/non_rfc_status_report.json": _hash_file(repo_root / "docs" / "compliance" / "non_rfc_status_report.json"),
        },
        "explicitly_deauthorized_current_adjacent_docs": deauthorized,
    }


def build_repository_state_payload(repo_root: Path, truth: dict[str, Any]) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    payload = _read_yaml(repo_root / REPOSITORY_STATE_YAML) or {"schema_version": 1, "repository_state": {}}
    state = dict(payload.get("repository_state", {}) or {})
    summary = truth["summary"]
    for key in CHRONOLOGY_SCOPED_REPOSITORY_STATE_KEYS:
        state.pop(key, None)
    state.update(
        {
            "fully_certifiable": bool(summary["fully_certifiable_now"]),
            "fully_rfc_compliant": bool(summary["fully_rfc_compliant_now"]),
            "checkpoint_only": bool(summary["checkpoint_only"]),
            "strict_independent_claims_ready": bool(summary["strict_independent_claims_ready"]),
            "tier4_external_bundle_count": int(summary["tier4_external_bundle_count"]),
            "tier4_valid_external_bundle_count": int(summary["tier4_valid_external_bundle_count"]),
            "tier4_invalid_external_bundle_count": int(summary["tier4_invalid_external_bundle_count"]),
            "tier4_missing_external_bundle_count": int(summary["tier4_missing_external_bundle_count"]),
            "tier4_retained_boundary_complete": bool(summary["strict_independent_claims_ready"]),
            "release_gate_passed_for_final_decision": bool(summary["release_gates_passed"]),
            "full_release_claim_still_partial": bool(not summary["final_release_ready"]),
            "final_release_decision_complete": True,
            "release_decision_record_present": True,
            "validated_runtime_matrix_preservation_complete": bool(summary["validated_runtime_matrix_green"]),
            "validated_test_lane_preservation_complete": bool(summary["validated_test_lanes_green"]),
            "validated_migration_portability_preservation_complete": bool(summary["migration_portability_passed"]),
            "last_release_decision_record": RELEASE_DECISION_RECORD_MD,
            "last_truth_chain_manifest": TRUTH_CHAIN_JSON,
            "last_truth_chain_generated_at": truth["generated_at"],
        }
    )
    payload["schema_version"] = int(payload.get("schema_version", 1) or 1)
    payload["repository_state"] = state
    return payload


def render_truth_chain_markdown(truth: dict[str, Any]) -> str:
    summary = truth["summary"]
    lines = [
        "# Truth Chain",
        "",
        "This manifest is a generated checkpoint projection derived from the SSOT authority policy.",
        "",
        f"- generated_at: `{truth['generated_at']}`",
        f"- final_release_ready: `{summary['final_release_ready']}`",
        f"- checkpoint_only: `{summary['checkpoint_only']}`",
        f"- release_gates_passed: `{summary['release_gates_passed']}`",
        f"- final_release_gate_passed: `{summary['final_release_gate_passed']}`",
        "",
        "## Source of truth",
        "",
    ]
    lines.extend(f"- `{item}`" for item in truth["source_of_truth"])
    lines.extend(["", "## Summary", ""])
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Explicitly deauthorized current-adjacent docs", ""])
    if truth["explicitly_deauthorized_current_adjacent_docs"]:
        lines.extend(f"- `{item}`" for item in truth["explicitly_deauthorized_current_adjacent_docs"])
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)
