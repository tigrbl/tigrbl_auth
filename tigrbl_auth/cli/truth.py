from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any

import yaml

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
DOCUMENT_AUTHORITY_YAML = "compliance/targets/document-authority.yaml"
DEFAULT_FINAL_RELEASE_STATUS_STEM = "FINAL_RELEASE_STATUS_2026-03-25"


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
    authority = _read_yaml(repo_root / DOCUMENT_AUTHORITY_YAML)
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
            CURRENT_STATE_REPORT_JSON,
            CERTIFICATION_STATE_REPORT_JSON,
            RELEASE_GATE_REPORT_JSON,
            FINAL_RELEASE_GATE_REPORT_JSON,
            "docs/compliance/non_rfc_status_report.json",
            DOCUMENT_AUTHORITY_YAML,
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
            "target_profile_truth_reconciled_complete": bool(inputs["repository_state"].get("phase_13_target_profile_truth_reconciled_complete", False)),
            "profile_scope_mismatch_set_empty": bool(inputs["repository_state"].get("phase_13_profile_scope_mismatch_set_empty", False)),
            "clean_room_executor_matrix_declared_complete": bool(inputs["repository_state"].get("phase_13_clean_room_executor_matrix_declared_complete", False)),
            "validated_manifest_identity_contract_installed": bool(inputs["repository_state"].get("phase_13_validated_manifest_identity_contract_installed", False)),
            "claim_registry_canonical_complete": bool(inputs["repository_state"].get("phase_14_claim_registry_canonical_complete", False)),
            "fapi2_security_profile_declared_complete": bool(inputs["repository_state"].get("phase_14_fapi2_security_profile_declared_complete", False)),
            "release_claims_machine_derivable": bool(inputs["repository_state"].get("phase_14_release_claims_machine_derivable", False)),
            "core_targets_missing_from_feature_map": int(inputs["repository_state"].get("phase_14_core_targets_missing_from_feature_map", 0)),
            "extension_targets_missing_from_feature_map": int(inputs["repository_state"].get("phase_14_extension_targets_missing_from_feature_map", 0)),
            "settings_backed_flags_missing_from_flag_map": int(inputs["repository_state"].get("phase_14_settings_backed_flags_missing_from_flag_map", 0)),
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
            "release_gate_passed_at_phase_13": bool(summary["release_gates_passed"]),
            "full_release_claim_still_partial": bool(not summary["final_release_ready"]),
            "phase_13_final_release_decision_complete": True,
            "phase_13_release_decision_record_present": True,
            "phase_13_validated_runtime_matrix_preservation_complete": bool(summary["validated_runtime_matrix_green"]),
            "phase_13_validated_test_lane_preservation_complete": bool(summary["validated_test_lanes_green"]),
            "phase_13_validated_migration_portability_preservation_complete": bool(summary["migration_portability_passed"]),
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
        "This manifest is the single generated checkpoint truth for current-state and release-decision artifacts.",
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


def render_current_state_markdown(truth: dict[str, Any]) -> str:
    summary = truth["summary"]
    lines = [
        "# CURRENT_STATE",
        "",
        "## Summary",
        "",
        "This repository is governed by the generated truth chain in `docs/compliance/truth_chain.json`.",
        "",
        (
            "The current package state is certifiably fully featured, certifiably fully RFC/spec compliant, and ready for a final certified release."
            if summary["final_release_ready"]
            else "The current package state is a blocked certification checkpoint. It is not certifiably fully featured and it is not certifiably fully RFC/spec compliant."
        ),
        "",
        "## Current generated state",
        "",
        f"- declared in-scope claim count: `{summary['declared_claim_count']}`",
        f"- Tier 3 claim count: `{summary['tier_3_claim_count']}`",
        f"- Tier 4 claim count: `{summary['tier_4_claim_count']}`",
        f"- strict independent claims ready: `{summary['strict_independent_claims_ready']}`",
        f"- fully certifiable now: `{summary['fully_certifiable_now']}`",
        f"- fully RFC/spec compliant now: `{summary['fully_rfc_compliant_now']}`",
        f"- fully non-RFC spec/standard compliant now: `{summary['fully_non_rfc_spec_compliant_now']}`",
        f"- release gates passed: `{summary['release_gates_passed']}`",
        f"- final release gate passed: `{summary['final_release_gate_passed']}`",
        f"- final release ready: `{summary['final_release_ready']}`",
        f"- checkpoint only: `{summary['checkpoint_only']}`",
        f"- target/profile truth reconciled complete: `{summary['target_profile_truth_reconciled_complete']}`",
        f"- profile-scope mismatch set empty: `{summary['profile_scope_mismatch_set_empty']}`",
        f"- clean-room executor matrix declared complete: `{summary['clean_room_executor_matrix_declared_complete']}`",
        f"- validated manifest identity contract installed: `{summary['validated_manifest_identity_contract_installed']}`",
        f"- claim registry canonical complete: `{summary['claim_registry_canonical_complete']}`",
        f"- FAPI 2.0 security profile declared complete: `{summary['fapi2_security_profile_declared_complete']}`",
        f"- release claims machine-derivable: `{summary['release_claims_machine_derivable']}`",
        f"- core targets missing from feature map: `{summary['core_targets_missing_from_feature_map']}`",
        f"- extension targets missing from feature map: `{summary['extension_targets_missing_from_feature_map']}`",
        f"- settings-backed flags missing from flag map: `{summary['settings_backed_flags_missing_from_flag_map']}`",
        f"- validated inventory complete: `{summary['validated_inventory_complete']}`",
        f"- validated runtime matrix green: `{summary['validated_runtime_matrix_green']}`",
        f"- validated test lanes green: `{summary['validated_test_lanes_green']}`",
        f"- migration portability passed: `{summary['migration_portability_passed']}`",
        f"- Tier 4 missing external bundle count: `{summary['tier4_missing_external_bundle_count']}`",
        "",
        "## Key artifacts",
        "",
        "- `docs/compliance/truth_chain.md`",
        "- `docs/compliance/current_state_report.md`",
        "- `docs/compliance/certification_state_report.md`",
        "- `docs/compliance/release_gate_report.md`",
        "- `docs/compliance/final_release_gate_report.md`",
        "- `docs/compliance/RELEASE_DECISION_RECORD.md`",
        "- `docs/compliance/FINAL_RELEASE_STATUS_2026-03-25.md`",
        "",
    ]
    return "\n".join(lines)


def render_certification_status_markdown(truth: dict[str, Any]) -> str:
    summary = truth["summary"]
    lines = [
        "# CERTIFICATION_STATUS",
        "",
        "## Honest status",
        "",
        f"- fully_certifiable_now: `{summary['fully_certifiable_now']}`",
        f"- fully_rfc_compliant_now: `{summary['fully_rfc_compliant_now']}`",
        f"- fully_non_rfc_spec_compliant_now: `{summary['fully_non_rfc_spec_compliant_now']}`",
        f"- strict_independent_claims_ready: `{summary['strict_independent_claims_ready']}`",
        f"- release_gates_passed: `{summary['release_gates_passed']}`",
        f"- final_release_gate_passed: `{summary['final_release_gate_passed']}`",
        f"- final_release_ready: `{summary['final_release_ready']}`",
        f"- target_profile_truth_reconciled_complete: `{summary['target_profile_truth_reconciled_complete']}`",
        f"- profile_scope_mismatch_set_empty: `{summary['profile_scope_mismatch_set_empty']}`",
        f"- validated_runtime_matrix_green: `{summary['validated_runtime_matrix_green']}`",
        f"- validated_test_lanes_green: `{summary['validated_test_lanes_green']}`",
        f"- migration_portability_passed: `{summary['migration_portability_passed']}`",
        f"- claim_registry_canonical_complete: `{summary['claim_registry_canonical_complete']}`",
        f"- fapi2_security_profile_declared_complete: `{summary['fapi2_security_profile_declared_complete']}`",
        f"- release_claims_machine_derivable: `{summary['release_claims_machine_derivable']}`",
        f"- core_targets_missing_from_feature_map: `{summary['core_targets_missing_from_feature_map']}`",
        f"- extension_targets_missing_from_feature_map: `{summary['extension_targets_missing_from_feature_map']}`",
        f"- settings_backed_flags_missing_from_flag_map: `{summary['settings_backed_flags_missing_from_flag_map']}`",
        "",
        "## Open gaps blocking final certification",
        "",
    ]
    if summary["open_gaps"]:
        lines.extend(f"- {item}" for item in summary["open_gaps"])
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Practical recommendation",
            "",
            (
                "This repository state can be labeled as a final certified release."
                if summary["final_release_ready"]
                else "This repository state must remain labeled as a checkpoint/candidate until Tier 4 independent validation and any remaining package-boundary gaps are closed."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def render_release_decision_record_markdown(truth: dict[str, Any]) -> str:
    summary = truth["summary"]
    lines = [
        "# Release Decision Record",
        "",
        "## Decision",
        "",
        (
            "Cut the final certified release."
            if summary["final_release_ready"]
            else "Do not cut a final certified release. Publish only a truthful checkpoint/candidate."
        ),
        "",
        "## Basis",
        "",
        f"- release_gates_passed: `{summary['release_gates_passed']}`",
        f"- release_gate_count: `{summary['release_gate_count']}`",
        f"- release_gate_failed_count: `{summary['release_gate_failed_count']}`",
        f"- final_release_gate_passed: `{summary['final_release_gate_passed']}`",
        f"- fully_certifiable_now: `{summary['fully_certifiable_now']}`",
        f"- fully_rfc_compliant_now: `{summary['fully_rfc_compliant_now']}`",
        f"- fully_non_rfc_spec_compliant_now: `{summary['fully_non_rfc_spec_compliant_now']}`",
        f"- strict_independent_claims_ready: `{summary['strict_independent_claims_ready']}`",
        f"- validated_runtime_matrix_green: `{summary['validated_runtime_matrix_green']}`",
        f"- validated_test_lanes_green: `{summary['validated_test_lanes_green']}`",
        f"- migration_portability_passed: `{summary['migration_portability_passed']}`",
        "",
        "## Explicitly deauthorized current-adjacent docs",
        "",
    ]
    if truth["explicitly_deauthorized_current_adjacent_docs"]:
        lines.extend(f"- `{item}`" for item in truth["explicitly_deauthorized_current_adjacent_docs"])
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def render_final_release_status_markdown(truth: dict[str, Any]) -> str:
    payload = _final_release_status_payload(truth)
    stem = _final_release_status_stem(Path("."))
    title = stem.replace("_", " ")
    lines = [f"# {title}", "", f"- Passed: `{payload['passed']}`", "", "## Summary", ""]
    lines.extend(f"- {key}: `{value}`" for key, value in payload["summary"].items())
    lines.extend(["", "## Remaining blockers", ""])
    if payload["details"]:
        lines.extend(f"- {item}" for item in payload["details"])
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def render_compliance_current_state_markdown() -> str:
    return "\n".join(
        [
            "# Current State",
            "",
            "Use `docs/compliance/truth_chain.md` and the generated report set in this directory.",
            "",
            "- source_of_truth: `docs/compliance/truth_chain.json`",
            "- current_state_report: `docs/compliance/current_state_report.json`",
            "- release_gate_report: `docs/compliance/release_gate_report.json`",
            "- final_release_gate_report: `docs/compliance/final_release_gate_report.json`",
            "- release_decision_record: `docs/compliance/RELEASE_DECISION_RECORD.md`",
            "",
        ]
    )


def materialize_truth_chain(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    truth = build_truth_chain_payload(repo_root)
    repository_payload = build_repository_state_payload(repo_root, truth)
    final_status_json_path, final_status_md_path = _final_release_status_paths(repo_root)
    _write_yaml(repo_root / REPOSITORY_STATE_YAML, repository_payload)
    _write_json(repo_root / TRUTH_CHAIN_JSON, truth)
    _write_text(repo_root / TRUTH_CHAIN_MD, render_truth_chain_markdown(truth))
    _write_text(repo_root / ROOT_CURRENT_STATE, render_current_state_markdown(truth))
    _write_text(repo_root / ROOT_CERTIFICATION_STATUS, render_certification_status_markdown(truth))
    _write_text(repo_root / RELEASE_DECISION_RECORD_MD, render_release_decision_record_markdown(truth))
    final_status_payload = _final_release_status_payload(truth)
    _write_json(final_status_json_path, final_status_payload)
    title = final_status_json_path.stem.replace("_", " ")
    lines = [f"# {title}", "", f"- Passed: `{final_status_payload['passed']}`", "", "## Summary", ""]
    lines.extend(f"- {key}: `{value}`" for key, value in final_status_payload["summary"].items())
    lines.extend(["", "## Remaining blockers", ""])
    if final_status_payload["details"]:
        lines.extend(f"- {item}" for item in final_status_payload["details"])
    else:
        lines.append("- none")
    lines.append("")
    _write_text(final_status_md_path, "\n".join(lines))
    _write_text(repo_root / "docs" / "compliance" / "current_state.md", render_compliance_current_state_markdown())
    return truth


def verify_truth_chain(repo_root: Path, *, mode: str = "all") -> dict[str, Any]:
    repo_root = repo_root.resolve()
    truth = build_truth_chain_payload(repo_root)
    repository_payload = build_repository_state_payload(repo_root, truth)
    final_status_json_path, final_status_md_path = _final_release_status_paths(repo_root)
    failures: list[str] = []
    warnings: list[str] = []

    expected_files: dict[str, str] = {}
    if mode in {"all", "current-state"}:
        expected_files[TRUTH_CHAIN_JSON] = json.dumps(truth, indent=2)
        expected_files[TRUTH_CHAIN_MD] = render_truth_chain_markdown(truth)
        expected_files[CURRENT_STATE_REPORT_MD] = _render_report_markdown("Current State Report", _read_json(repo_root / CURRENT_STATE_REPORT_JSON))
        expected_files[CERTIFICATION_STATE_REPORT_MD] = _render_report_markdown("Certification State Report", _read_json(repo_root / CERTIFICATION_STATE_REPORT_JSON))
        expected_files[ROOT_CURRENT_STATE] = render_current_state_markdown(truth)
        expected_files[ROOT_CERTIFICATION_STATUS] = render_certification_status_markdown(truth)
        expected_files["docs/compliance/current_state.md"] = render_compliance_current_state_markdown()
    if mode in {"all", "release-decision"}:
        expected_files[RELEASE_GATE_REPORT_MD] = _render_report_markdown("Release Gate Report", _read_json(repo_root / RELEASE_GATE_REPORT_JSON))
        expected_files[FINAL_RELEASE_GATE_REPORT_MD] = _render_report_markdown("Final Release Gate Report", _read_json(repo_root / FINAL_RELEASE_GATE_REPORT_JSON))
        expected_files[RELEASE_DECISION_RECORD_MD] = render_release_decision_record_markdown(truth)
        expected_files[str(final_status_json_path.relative_to(repo_root))] = json.dumps(_final_release_status_payload(truth), indent=2)
        title = final_status_json_path.stem.replace("_", " ")
        final_status_payload = _final_release_status_payload(truth)
        lines = [f"# {title}", "", f"- Passed: `{final_status_payload['passed']}`", "", "## Summary", ""]
        lines.extend(f"- {key}: `{value}`" for key, value in final_status_payload["summary"].items())
        lines.extend(["", "## Remaining blockers", ""])
        if final_status_payload["details"]:
            lines.extend(f"- {item}" for item in final_status_payload["details"])
        else:
            lines.append("- none")
        lines.append("")
        expected_files[str(final_status_md_path.relative_to(repo_root))] = "\n".join(lines)
    if mode in {"all", "repository-state"}:
        actual_repository_state = _read_yaml(repo_root / REPOSITORY_STATE_YAML)
        if actual_repository_state != repository_payload:
            failures.append(f"{REPOSITORY_STATE_YAML} does not match the generated truth-chain repository-state projection.")

    for rel_path, expected in expected_files.items():
        path = repo_root / rel_path
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual is None or _normalized_text(actual) != _normalized_text(expected):
            failures.append(f"{rel_path} does not match the generated truth-chain rendering.")

    return {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "mode": mode,
            "final_release_ready": bool(truth["summary"]["final_release_ready"]),
            "release_gates_passed": bool(truth["summary"]["release_gates_passed"]),
            "strict_independent_claims_ready": bool(truth["summary"]["strict_independent_claims_ready"]),
        },
    }
