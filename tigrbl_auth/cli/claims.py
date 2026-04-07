from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

EXPECTED_PROFILES = {"baseline", "production", "hardening", "fapi2-security", "peer-claim"}
EXPECTED_PHASES = {"P0", "P1", "P2", "P3"}
EXPECTED_TIERS = {0, 1, 2, 3, 4}
BANNED_CORE_LABELS = {"RFC 5785", "RFC 8523"}
REQUIRED_CORRECTIONS = {
    ("RFC 5785", "RFC 8615"),
    ("RFC 8523", "RFC 7523"),
}
REQUIRED_EXTENSION_LABELS = {"RFC 7800", "RFC 7952", "RFC 8291", "RFC 8812", "RFC 8932"}
REQUIRED_BUCKET_LABELS = {
    "baseline": {"RFC 6749", "RFC 6750", "RFC 7636", "RFC 8414", "RFC 8615", "RFC 7515", "RFC 7516", "RFC 7517", "RFC 7518", "RFC 7519", "OIDC Core 1.0", "OIDC Discovery 1.0"},
    "production": {"RFC 7009", "RFC 7662", "RFC 7591", "RFC 7592", "RFC 8252", "RFC 9068", "RFC 9207", "RFC 6265", "OIDC UserInfo", "OIDC Session Management", "OIDC RP-Initiated Logout", "RFC 9728"},
    "hardening": {"RFC 8628", "RFC 8693", "RFC 8707", "RFC 9101", "RFC 9126", "RFC 9396", "RFC 9449", "RFC 8705", "OIDC Front-Channel Logout", "OIDC Back-Channel Logout", "RFC 9700"},
    "runtime": {"ASGI 3 application package", "Runner profile: Uvicorn", "Runner profile: Hypercorn", "Runner profile: Tigrcorn"},
    "operator": {"CLI operator surface", "Bootstrap and migration lifecycle", "Key lifecycle and JWKS publication", "Import/export portability", "Release bundle and signature verification"},
    "alignment_only": {"OAuth 2.1 alignment profile"},
}
REQUIRED_PLANES = {"api", "tables", "ops", "services", "standards", "security", "config", "adapters", "cli", "plugin", "gateway"}
REQUIRED_SURFACES = {"public_auth_plane", "admin_control_plane", "operator_plane", "rpc_control_plane", "diagnostics_plane", "plugin_plane"}


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _collect_labels(targets: list[dict[str, Any]]) -> set[str]:
    return {str(item.get("label", "")).strip() for item in targets}


def _scan_for_banned_labels(path: Path, allowed: set[Path]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for candidate in path.rglob("*.yaml"):
        if candidate in allowed:
            continue
        text = candidate.read_text(encoding="utf-8")
        for label in sorted(BANNED_CORE_LABELS):
            if label in text:
                hits.append({"path": str(candidate.relative_to(path.parent)), "label": label})
    return hits


def run_lint(repo_root: Path, *, strict: bool = True, report_dir: Path | None = None) -> int:
    repo_root = repo_root.resolve()
    compliance_dir = repo_root / "compliance"
    targets_dir = compliance_dir / "targets"
    claims_dir = compliance_dir / "claims"
    mappings_dir = compliance_dir / "mappings"
    report_dir = report_dir or (repo_root / "docs" / "compliance")
    report_dir.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    warnings: list[str] = []

    profiles = _load_yaml(targets_dir / "profiles.yaml")
    boundaries = _load_yaml(targets_dir / "boundaries.yaml")
    target_buckets = _load_yaml(targets_dir / "target-buckets.yaml")
    public_surface = _load_yaml(targets_dir / "public-operator-surface.yaml")
    modularity = _load_yaml(targets_dir / "modularity-planes.yaml")
    rfc_targets = _load_yaml(targets_dir / "rfc-targets.yaml")
    extension_targets = _load_yaml(targets_dir / "extension-targets.yaml")
    alignment_targets = _load_yaml(targets_dir / "alignment-targets.yaml")
    oidc_targets = _load_yaml(targets_dir / "oidc-targets.yaml")
    openapi_targets = _load_yaml(targets_dir / "openapi-targets.yaml")
    openrpc_targets = _load_yaml(targets_dir / "openrpc-targets.yaml")
    runtime_targets = _load_yaml(targets_dir / "runtime-targets.yaml")
    operator_targets = _load_yaml(targets_dir / "operator-targets.yaml")
    corrections = _load_yaml(targets_dir / "legacy-label-corrections.yaml")
    repo_state = _load_yaml(claims_dir / "repository-state.yaml")
    declared_claims = _load_yaml(claims_dir / "declared-target-claims.yaml")
    out_of_scope = _load_yaml(targets_dir / "out-of-scope-baseline.yaml")
    boundary_decisions = _load_yaml(targets_dir / "boundary-decisions.yaml")
    boundary_enforcement = _load_yaml(targets_dir / "boundary-enforcement.yaml")
    module_to_boundary = _load_yaml(mappings_dir / "module-to-boundary.yaml")
    target_to_module = _load_yaml(mappings_dir / "target-to-module.yaml")
    target_to_adr = _load_yaml(mappings_dir / "target-to-adr.yaml")
    target_to_gate = _load_yaml(mappings_dir / "target-to-gate.yaml")
    target_to_test = _load_yaml(mappings_dir / "target-to-test.yaml")
    target_to_evidence = _load_yaml(mappings_dir / "target-to-evidence.yaml")
    decision_to_check = _load_yaml(mappings_dir / "decision-to-check.yaml")
    decision_to_gate = _load_yaml(mappings_dir / "decision-to-gate.yaml")

    profile_names = set(profiles.get("profiles", {}).keys())
    missing_profiles = EXPECTED_PROFILES - profile_names
    if missing_profiles:
        failures.append(f"Missing required profiles: {', '.join(sorted(missing_profiles))}")

    for profile_name, profile in profiles.get("profiles", {}).items():
        phase = profile.get("phase")
        tier = int(profile.get("minimum_claim_tier", -1))
        if phase not in EXPECTED_PHASES:
            failures.append(f"Profile {profile_name} has invalid phase: {phase}")
        if tier not in EXPECTED_TIERS:
            failures.append(f"Profile {profile_name} has invalid minimum_claim_tier: {tier}")

    boundary_scopes = set(boundaries.get("boundaries", {}).keys())
    for required_boundary in {"certified_core", "governance_plane", "legacy_transition", "extension_quarantine", "alignment_only", "out_of_scope_baseline"}:
        if required_boundary not in boundary_scopes:
            failures.append(f"Missing required boundary declaration: {required_boundary}")

    bucket_map = target_buckets.get("buckets", {})
    for bucket_name, required_labels in REQUIRED_BUCKET_LABELS.items():
        present_labels = set(bucket_map.get(bucket_name, {}).get("labels", []))
        missing = required_labels - present_labels
        if missing:
            failures.append(f"Target bucket {bucket_name} missing labels: {', '.join(sorted(missing))}")

    surfaces = set(public_surface.get("surfaces", {}).keys())
    missing_surfaces = REQUIRED_SURFACES - surfaces
    if missing_surfaces:
        failures.append(f"Missing required public/operator surfaces: {', '.join(sorted(missing_surfaces))}")

    planes = set(modularity.get("planes", {}).keys())
    missing_planes = REQUIRED_PLANES - planes
    if missing_planes:
        failures.append(f"Missing required modularity planes: {', '.join(sorted(missing_planes))}")

    core_targets = (
        list(rfc_targets.get("targets", []))
        + list(oidc_targets.get("targets", []))
        + list(openapi_targets.get("targets", []))
        + list(openrpc_targets.get("targets", []))
        + list(runtime_targets.get("targets", []))
        + list(operator_targets.get("targets", []))
    )
    core_labels = _collect_labels(core_targets)
    for banned in sorted(BANNED_CORE_LABELS):
        if banned in core_labels:
            failures.append(f"Banned legacy core label present in core target manifests: {banned}")

    ext_targets = list(extension_targets.get("targets", []))
    ext_labels = _collect_labels(ext_targets)
    missing_ext = REQUIRED_EXTENSION_LABELS - ext_labels
    if missing_ext:
        failures.append(f"Missing quarantined extension targets: {', '.join(sorted(missing_ext))}")

    alignment = list(alignment_targets.get("targets", []))
    for item in alignment:
        if item.get("claimable_as_rfc"):
            failures.append(f"Alignment-only target incorrectly claimable as RFC: {item.get('label')}")

    correction_pairs = {
        (entry.get("from_label"), entry.get("to_label"))
        for entry in corrections.get("corrections", [])
    }
    for pair in REQUIRED_CORRECTIONS:
        if pair not in correction_pairs:
            failures.append(f"Missing required legacy label correction: {pair[0]} -> {pair[1]}")

    for target_doc in (openapi_targets, openrpc_targets):
        for target in target_doc.get("targets", []):
            artifact = str(target.get("artifact", ""))
            if "placeholder" in artifact:
                failures.append(f"Artifact still points at placeholder path: {artifact}")

    claim_entries = declared_claims.get("claim_set", {}).get("claims", [])
    max_repo_tier = int(declared_claims.get("claim_set", {}).get("current_repository_tier", -1))
    if max_repo_tier not in EXPECTED_TIERS:
        failures.append(f"Invalid current_repository_tier: {max_repo_tier}")

    extension_or_out_scope = _collect_labels(out_of_scope.get("targets", [])) | ext_labels
    for claim in claim_entries:
        target = claim.get("target")
        tier = int(claim.get("tier", -1))
        profile = claim.get("profile")
        if target not in core_labels:
            failures.append(f"Claim references undeclared or non-core target: {target}")
        if target in extension_or_out_scope:
            failures.append(f"Claim incorrectly references extension or out-of-scope target: {target}")
        if tier not in EXPECTED_TIERS:
            failures.append(f"Claim {target} has invalid tier: {tier}")
        if tier > max_repo_tier:
            failures.append(f"Claim {target} exceeds current_repository_tier: {tier} > {max_repo_tier}")
        if profile not in profile_names:
            failures.append(f"Claim {target} references unknown profile: {profile}")
        if target not in target_to_module:
            failures.append(f"Claim {target} missing target-to-module mapping")
        if target not in target_to_gate:
            failures.append(f"Claim {target} missing target-to-gate mapping")
        if target not in target_to_test:
            warnings.append(f"Claim {target} missing target-to-test mapping")
        if target not in target_to_evidence:
            warnings.append(f"Claim {target} missing target-to-evidence mapping")

    applies = set(target_to_adr.get("applies_to_targets", {}).get("all_core_targets", []))
    for adr_id in applies:
        matches = list((repo_root / "docs" / "adr").glob(f"{adr_id}-*.md"))
        if not matches:
            failures.append(f"Core-target ADR reference missing file: {adr_id}")

    for decision in boundary_decisions.get("decisions", []):
        decision_id = str(decision.get("id"))
        adr = repo_root / str(decision.get("adr"))
        if not adr.exists():
            failures.append(f"Boundary decision {decision_id} points to missing ADR: {adr}")
        declared_checks = set(decision.get("enforced_by_checks", []))
        mapped_checks = set(decision_to_check.get(decision_id, []))
        if declared_checks != mapped_checks:
            failures.append(f"Boundary decision {decision_id} check mapping mismatch")
        declared_gates = set(decision.get("release_gates", []))
        mapped_gates = set(decision_to_gate.get(decision_id, []))
        if declared_gates != mapped_gates:
            failures.append(f"Boundary decision {decision_id} gate mapping mismatch")

    known_checks = set(boundary_enforcement.get("enforcement", {}).get("checks", []))
    for decision_id, checks in decision_to_check.items():
        unknown = set(checks) - known_checks - {"certified_core_wrapper_count_zero", "tier3_claims_have_evidence_refs", "tier4_claims_have_peer_refs"}
        if unknown:
            failures.append(f"Decision {decision_id} references unknown checks: {', '.join(sorted(unknown))}")

    for target, mapping in target_to_module.items():
        modules = mapping.get("modules", []) if isinstance(mapping, dict) else []
        for module in modules:
            path = repo_root / str(module)
            if not path.exists():
                failures.append(f"Target {target} maps to missing module path: {module}")
    for key in module_to_boundary:
        if not (repo_root / key).exists():
            warnings.append(f"module-to-boundary entry does not exist on disk: {key}")

    banned_hits = _scan_for_banned_labels(compliance_dir, allowed={targets_dir / "legacy-label-corrections.yaml"})
    for hit in banned_hits:
        failures.append(f"Banned legacy label {hit['label']} found in {hit['path']}")

    repo_state_info = repo_state.get("repository_state", {})
    for required_state in ("phase_0_boundary_lock_complete", "phase_0_claim_boundary_rebaseline_complete", "certification_boundary_locked", "extension_rfc_quarantine_active"):
        if not repo_state_info.get(required_state):
            failures.append(f"Repository state does not declare {required_state}")
    if not repo_state_info.get("feature_flag_surface_modularity_complete"):
        warnings.append("Repository state does not yet declare feature_flag_surface_modularity_complete")

    report = {
        "scope": "claims-and-target-hygiene",
        "strict": strict,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "passed": not failures,
            "core_target_count": len(core_targets),
            "extension_target_count": len(ext_targets),
            "alignment_target_count": len(alignment),
            "declared_claim_count": len(claim_entries),
            "boundary_decision_count": len(boundary_decisions.get("decisions", [])),
        },
    }

    json_path = report_dir / "claims_lint_report.json"
    md_path = report_dir / "claims_lint_report.md"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Claims Lint Report",
        "",
        f"- Scope: `{report['scope']}`",
        f"- Strict: `{strict}`",
        f"- Passed: `{report['summary']['passed']}`",
        f"- Core targets: `{report['summary']['core_target_count']}`",
        f"- Extension targets: `{report['summary']['extension_target_count']}`",
        f"- Alignment targets: `{report['summary']['alignment_target_count']}`",
        f"- Declared claims: `{report['summary']['declared_claim_count']}`",
        f"- Boundary decisions: `{report['summary']['boundary_decision_count']}`",
        "",
    ]
    if failures:
        lines.extend(["## Failures", ""])
        lines.extend([f"- {item}" for item in failures])
        lines.append("")
    else:
        lines.extend(["## Result", "", "Claims lint passed with no failures.", ""])
    if warnings:
        lines.extend(["## Warnings", ""])
        lines.extend([f"- {item}" for item in warnings])
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    return 1 if failures and strict else 0
