from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE_NAMES = ("baseline", "production", "hardening")
BUCKET_ORDER = (
    "baseline-certifiable-now",
    "production-completion-required",
    "hardening-completion-required",
    "runtime-completion-required",
    "operator-completion-required",
    "out-of-scope/deferred",
)


REQUIRED_SCOPE_FREEZE_PROHIBITED_EXPANSIONS = (
    "RFC 7800",
    "RFC 8417",
    "RFC 8291",
    "RFC 8812",
    "RFC 8932",
    "OAuth 2.1 alignment profile",
    "SAML IdP/SP",
    "LDAP/AD federation",
    "SCIM",
    "policy-platform/federation breadth outside the declared boundary",
)


def stable_label_hash(labels: list[str]) -> str:
    normalized = sorted(dict.fromkeys(str(label) for label in labels))
    encoded = json.dumps(normalized, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def first_profile(profiles: list[str] | tuple[str, ...] | None) -> str:
    for name in profiles or ():
        if name != "peer-claim":
            return name
    return "baseline"


def classify_bucket(label: str, target: dict[str, Any], bucket_cfg: dict[str, Any]) -> str:
    family = str(target.get("family", ""))
    if family == "runtime":
        return "runtime-completion-required"
    if family == "operator":
        return "operator-completion-required"
    if label in {"OpenAPI 3.1 / 3.2 compatible public contract"}:
        return "baseline-certifiable-now"
    if label in {"OpenRPC 1.4.x admin/control-plane contract"}:
        return "production-completion-required"
    primary = first_profile(target.get("profiles"))
    if primary == "baseline":
        return "baseline-certifiable-now"
    if primary == "production":
        return "production-completion-required"
    return "hardening-completion-required"


def test_classes(test_paths: list[str], file_to_class: dict[str, str]) -> list[str]:
    classes = []
    for path in test_paths:
        if path in file_to_class and file_to_class[path] not in classes:
            classes.append(file_to_class[path])
    if not classes and test_paths:
        classes.append("planned-or-unclassified")
    return classes


def build_scope(repo_root: Path) -> dict[str, Any]:
    rfc_targets = load_yaml(repo_root / "compliance/targets/rfc-targets.yaml")
    oidc_targets = load_yaml(repo_root / "compliance/targets/oidc-targets.yaml")
    openapi_targets = load_yaml(repo_root / "compliance/targets/openapi-targets.yaml")
    openrpc_targets = load_yaml(repo_root / "compliance/targets/openrpc-targets.yaml")
    runtime_targets = load_yaml(repo_root / "compliance/targets/runtime-targets.yaml")
    operator_targets = load_yaml(repo_root / "compliance/targets/operator-targets.yaml")
    extension_targets = load_yaml(repo_root / "compliance/targets/extension-targets.yaml")
    alignment_targets = load_yaml(repo_root / "compliance/targets/alignment-targets.yaml")
    out_of_scope = load_yaml(repo_root / "compliance/targets/out-of-scope-baseline.yaml")
    target_buckets = load_yaml(repo_root / "compliance/targets/target-buckets.yaml")
    target_to_module = load_yaml(repo_root / "compliance/mappings/target-to-module.yaml")
    target_to_test = load_yaml(repo_root / "compliance/mappings/target-to-test.yaml")
    target_to_evidence = load_yaml(repo_root / "compliance/mappings/target-to-evidence.yaml")
    target_to_endpoint = load_yaml(repo_root / "compliance/mappings/target-to-endpoint.yaml")
    surface_manifest = load_yaml(repo_root / "compliance/targets/public-operator-surface.yaml")
    declared = load_yaml(repo_root / "compliance/claims/declared-target-claims.yaml")
    claim_by_target = {str(item.get("target")): item for item in declared.get("claim_set", {}).get("claims", [])}
    test_classification = load_yaml(repo_root / "compliance/mappings/test_classification.yaml")
    file_to_class = {
        path: category
        for category, paths in test_classification.get("categories", {}).items()
        for path in paths
    }
    effective = {
        profile: load_yaml(repo_root / f"compliance/claims/effective-target-claims.{profile}.yaml")
        for profile in PROFILE_NAMES
    }
    openapi_contracts = {
        profile: json.loads((repo_root / f"specs/openapi/profiles/{profile}/tigrbl_auth.public.openapi.json").read_text(encoding="utf-8"))
        for profile in PROFILE_NAMES
    }
    openrpc_contracts = {
        profile: json.loads((repo_root / f"specs/openrpc/profiles/{profile}/tigrbl_auth.admin.openrpc.json").read_text(encoding="utf-8"))
        for profile in PROFILE_NAMES
    }

    core_targets: list[dict[str, Any]] = []
    for source, payload in (
        ("rfc", rfc_targets),
        ("oidc", oidc_targets),
        ("contract", openapi_targets),
        ("contract", openrpc_targets),
        ("runtime", runtime_targets),
        ("operator", operator_targets),
    ):
        for item in payload.get("targets", []):
            entry = dict(item)
            entry["family"] = source
            core_targets.append(entry)

    bucket_items = {name: [] for name in BUCKET_ORDER}
    target_entries: list[dict[str, Any]] = []
    discrepancy_summary: dict[str, int] = {}

    for target in core_targets:
        label = str(target.get("label"))
        bucket = classify_bucket(label, target, target_buckets.get("buckets", {}))
        bucket_items[bucket].append(label)
        modules = list(target_to_module.get(label, {}).get("modules", target.get("modules", [])))
        tests = list(target_to_test.get(label, []))
        evidence = list(target_to_evidence.get(label, []))
        endpoint_map = target_to_endpoint.get(label, {})
        target_endpoints = list(endpoint_map.get("target", target.get("endpoints", [])) or [])
        current_endpoints = list(endpoint_map.get("current", []))
        claim = claim_by_target.get(label)
        discrepancies: list[str] = []
        if not claim:
            discrepancies.append("manifest-without-claim")
        if not modules:
            discrepancies.append("missing-owner-module")
        if modules and any(not (repo_root / module).exists() for module in modules):
            discrepancies.append("owner-module-path-missing")
        if not tests:
            discrepancies.append("missing-test-plan")
        if not evidence:
            discrepancies.append("missing-evidence-plan")
        if target_endpoints and set(current_endpoints) != set(target_endpoints):
            discrepancies.append("surface-drift")
        bucket_manifest_key = {
            'baseline-certifiable-now': 'baseline',
            'production-completion-required': 'production',
            'hardening-completion-required': 'hardening',
        }.get(bucket)
        if bucket_manifest_key and label not in set(target_buckets.get('buckets', {}).get(bucket_manifest_key, {}).get('labels', [])) and target.get('family') != 'contract':
            discrepancies.append('bucket-manifest-drift')

        profile_reality: dict[str, Any] = {}
        for profile in PROFILE_NAMES:
            eff = effective[profile]
            deployment = eff.get("effective_deployment", {})
            active_targets = set(deployment.get("active_targets", []))
            active_claims = {str(item.get("target")) for item in eff.get("claim_set", {}).get("claims", [])}
            openapi_paths = set(openapi_contracts[profile].get("paths", {}).keys())
            openrpc_methods = {str(item.get("name")) for item in openrpc_contracts[profile].get("methods", [])}
            present_paths = [path for path in target_endpoints if path in openapi_paths]
            required_rpc_methods = set(
                surface_manifest.get("surfaces", {})
                .get("rpc_control_plane", {})
                .get("target", {})
                .get("required_methods", [])
            )
            profile_reality[profile] = {
                "active_target": label in active_targets,
                "effective_claim": label in active_claims,
                "openapi_paths_present": present_paths,
                "openrpc_present": label == "OpenRPC 1.4.x admin/control-plane contract"
                and (required_rpc_methods <= openrpc_methods if required_rpc_methods else bool(openrpc_methods)),
            }
            if label in active_targets and label not in active_claims:
                discrepancies.append(f"active-without-effective-claim:{profile}")
        for item in discrepancies:
            discrepancy_summary[item] = discrepancy_summary.get(item, 0) + 1
        target_entries.append({
            "label": label,
            "id": target.get("id"),
            "family": target.get("family"),
            "scope_bucket": bucket,
            "delivery_track": target.get("delivery_track"),
            "minimum_claim_tier": target.get("minimum_claim_tier"),
            "first_claimable_profile": first_profile(target.get("profiles")),
            "claim": claim,
            "owner_modules": modules,
            "endpoint_surface": {
                "current": current_endpoints,
                "target": target_endpoints,
                "status": endpoint_map.get("status", "tracked") if endpoint_map else "tracked",
            },
            "tests": {
                "paths": tests,
                "classes": test_classes(tests, file_to_class),
            },
            "evidence": {"refs": evidence},
            "profile_reality": profile_reality,
            "discrepancies": sorted(dict.fromkeys(discrepancies)),
        })

    deferred_targets = []
    for target in extension_targets.get("targets", []):
        deferred_targets.append({
            "label": target.get("label"),
            "kind": "extension-quarantine",
            "reason": target.get("quarantine_reason"),
            "modules": target.get("modules", []),
        })
    for target in alignment_targets.get("targets", []):
        deferred_targets.append({
            "label": target.get("label"),
            "kind": "alignment-only",
            "reason": target.get("quarantine_reason"),
            "claimable_as_rfc": bool(target.get("claimable_as_rfc", False)),
        })
    for target in out_of_scope.get("targets", []):
        deferred_targets.append({
            "label": target.get("label"),
            "kind": "out-of-scope-baseline",
            "reason": "explicitly excluded from the default certification boundary",
        })

    retained_labels = [str(entry.get("label")) for entry in target_entries]
    rfc_labels = [str(entry.get("label")) for entry in target_entries if str(entry.get("family")) == "rfc"]
    non_rfc_labels = [str(entry.get("label")) for entry in target_entries if str(entry.get("family")) != "rfc"]
    deferred_labels = [str(item.get("label")) for item in deferred_targets]
    retained_bucket_counts = {name: len(bucket_items[name]) for name in BUCKET_ORDER[:-1]}
    boundary_freeze = {
        "decision_id": "BND-012",
        "adr": "docs/adr/ADR-0029-certification-closeout-boundary-freeze.md",
        "effective_date": "2026-03-26",
        "status": "frozen-for-certification-closeout",
        "source_of_truth": "compliance/targets/certification_scope.yaml",
        "enforced_by_checks": ["claims_linter", "boundary-scope-freeze"],
        "release_gates": ["gate-05-governance", "gate-15-boundary-enforcement", "gate-90-release"],
        "retained_target_count": len(retained_labels),
        "retained_rfc_target_count": len(rfc_labels),
        "retained_non_rfc_target_count": len(non_rfc_labels),
        "retained_bucket_counts": retained_bucket_counts,
        "deferred_target_count": len(deferred_labels),
        "retained_target_identity_hash": stable_label_hash(retained_labels),
        "retained_rfc_target_identity_hash": stable_label_hash(rfc_labels),
        "retained_non_rfc_target_identity_hash": stable_label_hash(non_rfc_labels),
        "deferred_target_identity_hash": stable_label_hash(deferred_labels),
        "no_target_count_drift_during_closeout": True,
        "closeout_scope_expansion_requires_separate_program": True,
        "fully_featured_claim_boundary_fixed": True,
        "prohibited_expansions": list(REQUIRED_SCOPE_FREEZE_PROHIBITED_EXPANSIONS),
        "notes": [
            "Do not widen the retained 48-target certification boundary during closeout.",
            "Do not silently reclassify deferred, alignment-only, or out-of-scope items as part of the fully featured claim.",
            "Any broader business claim requires a separate scope-expansion program with updated manifests, mappings, tests, evidence, and peer obligations.",
        ],
    }

    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "delivery_track": declared.get("claim_set", {}).get("delivery_track", "foundation-boundary"),
        "authoritative": True,
        "repository_tier": declared.get("claim_set", {}).get("current_repository_tier", 0),
        "authoritative_sources": {
            "target_manifests": [
                "compliance/targets/rfc-targets.yaml",
                "compliance/targets/oidc-targets.yaml",
                "compliance/targets/openapi-targets.yaml",
                "compliance/targets/openrpc-targets.yaml",
                "compliance/targets/runtime-targets.yaml",
                "compliance/targets/operator-targets.yaml",
            ],
            "claims": "compliance/claims/declared-target-claims.yaml",
            "effective_claims": [f"compliance/claims/effective-target-claims.{profile}.yaml" for profile in PROFILE_NAMES],
            "effective_evidence": [f"compliance/evidence/effective-release-evidence.{profile}.yaml" for profile in PROFILE_NAMES],
            "contracts": [
                f"specs/openapi/profiles/{profile}/tigrbl_auth.public.openapi.json" for profile in PROFILE_NAMES
            ] + [
                f"specs/openrpc/profiles/{profile}/tigrbl_auth.admin.openrpc.json" for profile in PROFILE_NAMES
            ],
            "mappings": [
                "compliance/mappings/target-to-module.yaml",
                "compliance/mappings/target-to-endpoint.yaml",
                "compliance/mappings/target-to-test.yaml",
                "compliance/mappings/target-to-evidence.yaml",
                "compliance/mappings/test_classification.yaml",
                "compliance/mappings/test-classification.yaml",
            ],
        },
        "bucket_interpretation": {
            "baseline-certifiable-now": "Baseline certification candidate set. This is a scope bucket, not a Tier 3 or Tier 4 promotion.",
            "production-completion-required": "In-scope production RFC/OIDC targets that still require route, persistence, runtime, or evidence completion.",
            "hardening-completion-required": "In-scope hardening RFC/OIDC targets that still require runtime enforcement, public surface completion, or evidence completion.",
            "runtime-completion-required": "In-scope ASGI application and runner-profile targets required before the package can truthfully claim a fully featured runtime boundary.",
            "operator-completion-required": "In-scope CLI/operator/release targets required before the package can truthfully claim a fully featured package boundary.",
            "out-of-scope/deferred": "Quarantined extension, alignment-only, or explicitly deferred capabilities that are excluded from the default certification claim boundary.",
        },
        "scope_buckets": {
            name: {"count": len(bucket_items[name]), "targets": bucket_items[name]}
            for name in BUCKET_ORDER[:-1]
        },
        "boundary_freeze": boundary_freeze,
        "deferred_targets": deferred_targets,
        "targets": target_entries,
        "discrepancy_summary": discrepancy_summary,
        "truthful_status": {
            "fully_certifiable": False,
            "fully_rfc_compliant": False,
            "note": "This retained-boundary freeze improves truthfulness and traceability, but it does not by itself complete the missing runtime, evidence, or independent validation work required for final certification.",
        },
    }


def write_boundary_docs(repo_root: Path, scope: dict[str, Any]) -> None:
    freeze = scope.get("boundary_freeze", {})
    warning_banner = [
        "> [!WARNING] Non-authoritative active document. For current release and certification truth, use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` and the generated current-state reports.",
        "",
    ]
    boundary_lines = warning_banner + [
        "# Certification Boundary",
        "",
        "This document declares the authoritative certification boundary for the current `tigrbl_auth` checkpoint.",
        "",
        "## Authority",
        "",
        "- Canonical scope manifest: `compliance/targets/certification_scope.yaml`",
        "- Repository tier: `{}`".format(scope.get("repository_tier")),
        "- Fully certifiable now: `{}`".format(scope.get("truthful_status", {}).get("fully_certifiable", False)),
        "- Fully RFC compliant now: `{}`".format(scope.get("truthful_status", {}).get("fully_rfc_compliant", False)),
        "",
        "## Boundary freeze",
        "",
        "- Decision: `{}`".format(freeze.get("decision_id", "unrecorded")),
        "- ADR: `{}`".format(freeze.get("adr", "unrecorded")),
        "- Effective date: `{}`".format(freeze.get("effective_date", "unrecorded")),
        "- Status: `{}`".format(freeze.get("status", "unrecorded")),
        "- Retained targets: `{}`".format(freeze.get("retained_target_count", 0)),
        "- Retained RFC targets: `{}`".format(freeze.get("retained_rfc_target_count", 0)),
        "- Retained non-RFC targets: `{}`".format(freeze.get("retained_non_rfc_target_count", 0)),
        "- Deferred / excluded targets tracked: `{}`".format(freeze.get("deferred_target_count", 0)),
        "- No target-count drift during closeout: `{}`".format(freeze.get("no_target_count_drift_during_closeout", False)),
        "- Separate scope-expansion program required for wider claims: `{}`".format(freeze.get("closeout_scope_expansion_requires_separate_program", False)),
        "",
        "## Scope buckets",
        "",
    ]
    for name, payload in scope.get("scope_buckets", {}).items():
        boundary_lines.append(f"### {name}")
        boundary_lines.append("")
        boundary_lines.append(f"- Count: `{payload.get('count', 0)}`")
        boundary_lines.append(f"- Meaning: {scope.get('bucket_interpretation', {}).get(name, '')}")
        boundary_lines.append("")
    boundary_lines.extend([
        "## Why this file exists",
        "",
        "The repository uses this artifact to keep targets, claims, active routes, contracts, tests, and evidence planning aligned in one authoritative scope document so discrepancies are explicit and reviewable.",
        "",
        "## Current truthful status",
        "",
        "- The baseline candidate set is materially stronger than the production and hardening candidate sets.",
        "- Production and hardening targets remain in scope, and most are now implementation-backed, but several remain evidence-incomplete, profile-bounded, or not yet independently validated.",
        "- Extension and alignment-only work remains deferred or quarantined from the default certification claim boundary.",
        "",
        "## Most common discrepancies",
        "",
    ])
    discrepancies = sorted(scope.get("discrepancy_summary", {}).items(), key=lambda item: (-item[1], item[0]))[:12]
    if discrepancies:
        for name, count in discrepancies:
            boundary_lines.append(f"- `{name}`: `{count}` targets")
    else:
        boundary_lines.append("- none")
    boundary_lines.extend([
        "",
        "## Required boundary outputs present in this checkpoint",
        "",
        "- `compliance/targets/certification_scope.yaml`",
        "- `docs/compliance/BOUNDARY_FREEZE_DECISION_2026-03-26.md`",
        "- `docs/compliance/CERTIFICATION_BOUNDARY.md`",
        "- `docs/compliance/TARGET_REALITY_MATRIX.md`",
        "",
        "## Still not completed in this checkpoint",
        "",
        "- full Tier 3 evidence promotion across production and hardening targets",
        "- broader interop breadth for sender-constrained and assertion-based profiles",
        "- Tier 4 independent peer validation",
        "",
    ])
    write_text(repo_root / "docs/compliance/CERTIFICATION_BOUNDARY.md", "\n".join(boundary_lines) + "\n")

    matrix_lines = warning_banner + [
        "# Target Reality Matrix",
        "",
        "This matrix reconciles declared scope, current claims, owner modules, public surface state, test planning, and evidence planning.",
        "",
    ]
    for bucket_name in ("baseline-certifiable-now", "production-completion-required", "hardening-completion-required", "runtime-completion-required", "operator-completion-required"):
        matrix_lines.append(f"## {bucket_name}")
        matrix_lines.append("")
        matrix_lines.append("| Target | Claim | Owner | Surface | Tests | Evidence | Gaps |")
        matrix_lines.append("|---|---|---|---|---|---|---|")
        for target in [item for item in scope.get("targets", []) if item.get("scope_bucket") == bucket_name]:
            claim = target.get("claim") or {}
            claim_text = f"tier {claim.get('tier', 'n/a')} / {claim.get('status', 'unclaimed')}"
            owner_text = "<br>".join(target.get("owner_modules", [])[:2]) or "planned"
            surface = target.get("endpoint_surface", {})
            current = ", ".join(surface.get("current", [])) or "∅"
            desired = ", ".join(surface.get("target", [])) or "∅"
            surface_text = f"current: {current}<br>target: {desired}"
            tests = target.get("tests", {})
            test_text = ", ".join(tests.get("classes", [])) or "planned"
            evidence = ", ".join(target.get("evidence", {}).get("refs", [])) or "planned"
            gaps = ", ".join(target.get("discrepancies", [])) or "none"
            matrix_lines.append(f"| {target.get('label')} | {claim_text} | {owner_text} | {surface_text} | {test_text} | {evidence} | {gaps} |")
        matrix_lines.append("")
    matrix_lines.append("## out-of-scope/deferred")
    matrix_lines.append("")
    matrix_lines.append("| Target | Kind | Reason |")
    matrix_lines.append("|---|---|---|")
    for item in scope.get("deferred_targets", []):
        matrix_lines.append(f"| {item.get('label')} | {item.get('kind')} | {item.get('reason')} |")
    matrix_lines.append("")
    write_text(repo_root / "docs/compliance/TARGET_REALITY_MATRIX.md", "\n".join(matrix_lines) + "\n")

    decision_lines = [
        "# Boundary Freeze Decision — 2026-03-26",
        "",
        "## Decision",
        "",
        "Freeze the retained certification boundary for closeout at the exact target set recorded in `compliance/targets/certification_scope.yaml`. Do not silently widen the meaning of `fully featured`, `fully RFC compliant`, or `fully non-RFC spec/standard compliant` during certification closeout.",
        "",
        "## Freeze record",
        "",
        f"- decision_id: `{freeze.get('decision_id', 'unrecorded')}`",
        f"- source_of_truth: `{freeze.get('source_of_truth', 'unrecorded')}`",
        f"- effective_date: `{freeze.get('effective_date', 'unrecorded')}`",
        f"- retained_target_count: `{freeze.get('retained_target_count', 0)}`",
        f"- retained_rfc_target_count: `{freeze.get('retained_rfc_target_count', 0)}`",
        f"- retained_non_rfc_target_count: `{freeze.get('retained_non_rfc_target_count', 0)}`",
        f"- deferred_target_count: `{freeze.get('deferred_target_count', 0)}`",
        f"- retained_target_identity_hash: `{freeze.get('retained_target_identity_hash', '')}`",
        "",
        "## Required closeout rules",
        "",
        f"- no_target_count_drift_during_closeout: `{freeze.get('no_target_count_drift_during_closeout', False)}`",
        f"- closeout_scope_expansion_requires_separate_program: `{freeze.get('closeout_scope_expansion_requires_separate_program', False)}`",
        f"- fully_featured_claim_boundary_fixed: `{freeze.get('fully_featured_claim_boundary_fixed', False)}`",
        "",
        "## Explicitly prohibited silent expansions",
        "",
    ]
    for item in freeze.get("prohibited_expansions", []):
        decision_lines.append(f"- {item}")
    decision_lines.extend([
        "",
        "## Current truthful status",
        "",
        "This freeze improves claim hygiene and certification traceability. It does **not** make the package certifiably fully featured or certifiably fully RFC/spec compliant by itself. Final certification remains blocked by missing validated runtime/test/migration evidence and missing preserved Tier 4 independent peer bundles.",
        "",
    ])
    write_text(repo_root / "docs/compliance/BOUNDARY_FREEZE_DECISION_2026-03-26.md", "\n".join(decision_lines) + "\n")


def main() -> int:
    scope = build_scope(ROOT)
    write_yaml(ROOT / "compliance/targets/certification_scope.yaml", scope)
    write_boundary_docs(ROOT, scope)
    print(json.dumps({
        "scope_manifest": "compliance/targets/certification_scope.yaml",
        "boundary_doc": "docs/compliance/CERTIFICATION_BOUNDARY.md",
        "matrix_doc": "docs/compliance/TARGET_REALITY_MATRIX.md",
        "target_count": len(scope.get("targets", [])),
        "deferred_count": len(scope.get("deferred_targets", [])),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
