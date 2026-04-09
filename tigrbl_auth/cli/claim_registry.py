from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from tigrbl_auth.api.rpc.registry import get_rpc_method_registry
from tigrbl_auth.cli.metadata import ARGUMENT_SPECS, COMMAND_SPECS
from tigrbl_auth.config.deployment import (
    EXTENSION_REGISTRY,
    PROTOCOL_SLICE_REGISTRY,
    ROUTE_REGISTRY,
    TARGET_FLAG_REQUIREMENTS,
)
from tigrbl_auth.config.feature_flags import FEATURE_FLAG_GROUPS, flags_for_profile

PROFILE_ORDER = (
    "baseline",
    "production",
    "hardening",
    "fapi2-security",
    "peer-claim",
    "fapi2-message-signing",
    "smart-app-launch",
    "smart-backend-services",
    "fast-udap-security",
    "ihe-iua",
    "nist-sp-800-63b-4",
    "nist-sp-800-63c-4",
    "camara-security-interoperability",
    "fdx-csdf-security-model",
    "gnap-core-rs",
    "oauth-2-1",
    "webauthn-passkey-oauth-patterns",
    "confidential-spa-pattern",
)
CORE_TARGET_FILES = (
    "rfc-targets.yaml",
    "oidc-targets.yaml",
    "openapi-targets.yaml",
    "openrpc-targets.yaml",
    "runtime-targets.yaml",
    "operator-targets.yaml",
)
EXTENSION_TARGET_FILE = "extension-targets.yaml"
ALIGNMENT_TARGET_FILE = "alignment-targets.yaml"
FEATURE_REGISTRY_PATH = "compliance/claims/feature-registry.yaml"
CLAIM_REGISTRY_PATH = "compliance/claims/claim-registry.yaml"
ISSUE_REGISTRY_PATH = "compliance/claims/issue-registry.yaml"
RISK_REGISTRY_PATH = "compliance/claims/risk-registry.yaml"
FEATURE_TO_TARGET_PATH = "compliance/mappings/feature-to-target.yaml"
FLAG_TO_FEATURE_PATH = "compliance/mappings/flag-to-feature.yaml"
FEATURE_TO_TEST_PATH = "compliance/mappings/feature-to-test.yaml"
FEATURE_TO_EVIDENCE_PATH = "compliance/mappings/feature-to-evidence.yaml"
LEGACY_FLAG_TO_TARGET_PATH = "compliance/mappings/feature-flag-to-target.yaml"
DECLARED_TARGET_CLAIMS_PATH = "compliance/claims/declared-target-claims.yaml"
REPOSITORY_STATE_PATH = "compliance/claims/repository-state.yaml"
FAPI_ATOMIC_CLAIMS_PATH = "compliance/claims/fapi-atomic-claims.yaml"


def _load_yaml(path: Path) -> Any:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if payload is not None else {}


def _write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def _slug(value: str) -> str:
    text = "".join(ch.lower() if ch.isalnum() else "-" for ch in value)
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-")


def _profile_rank(name: str) -> int:
    try:
        return PROFILE_ORDER.index(name)
    except ValueError:
        return len(PROFILE_ORDER)


def _earliest_profile(profiles: list[str] | tuple[str, ...] | None) -> str:
    choices = [str(item) for item in (profiles or []) if str(item) in PROFILE_ORDER]
    return min(choices, key=_profile_rank) if choices else "baseline"


def _target_manifest_map(repo_root: Path) -> dict[str, tuple[str, dict[str, Any]]]:
    base = repo_root / "compliance" / "targets"
    mapping: dict[str, tuple[str, dict[str, Any]]] = {}
    for name in CORE_TARGET_FILES + (EXTENSION_TARGET_FILE, ALIGNMENT_TARGET_FILE):
        payload = _load_yaml(base / name)
        for target in payload.get("targets", []):
            mapping[str(target.get("label"))] = (name, target)
    return mapping


def _target_sets(repo_root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    base = repo_root / "compliance" / "targets"
    core: dict[str, dict[str, Any]] = {}
    extension: dict[str, dict[str, Any]] = {}
    alignment: dict[str, dict[str, Any]] = {}
    for name in CORE_TARGET_FILES:
        payload = _load_yaml(base / name)
        for target in payload.get("targets", []):
            core[str(target.get("label"))] = target
    for target in _load_yaml(base / EXTENSION_TARGET_FILE).get("targets", []):
        extension[str(target.get("label"))] = target
    for target in _load_yaml(base / ALIGNMENT_TARGET_FILE).get("targets", []):
        alignment[str(target.get("label"))] = target
    return core, extension, alignment


def _profile_target_labels(repo_root: Path, profile_name: str) -> list[str]:
    profiles = _load_yaml(repo_root / "compliance" / "targets" / "profiles.yaml").get("profiles", {})
    profile = profiles.get(profile_name, {})
    explicit_targets = [str(item) for item in profile.get("targets", []) if str(item).strip()]
    if explicit_targets:
        return list(dict.fromkeys(explicit_targets))
    manifest_names = list(profile.get("target_sets", []))
    excluded = {str(item) for item in profile.get("excludes", [])}
    labels: list[str] = []
    for manifest_name in manifest_names:
        if manifest_name in excluded:
            continue
        payload = _load_yaml(repo_root / "compliance" / "targets" / f"{manifest_name}.yaml")
        for target in payload.get("targets", []):
            label = str(target.get("label"))
            if label not in labels:
                labels.append(label)
    return labels


def _command_targets(command_name: str) -> list[str]:
    targets = ["CLI operator surface"]
    if command_name in {"bootstrap", "migrate"}:
        targets.append("Bootstrap and migration lifecycle")
    if command_name == "keys":
        targets.append("Key lifecycle and JWKS publication")
    if command_name in {"import", "export"}:
        targets.append("Import/export portability")
    if command_name == "release":
        targets.append("Release bundle and signature verification")
    if command_name == "spec":
        targets.extend(["OpenAPI 3.1 / 3.2 compatible public contract", "OpenRPC 1.4.x admin/control-plane contract"])
    return list(dict.fromkeys(targets))


def _flag_targets(flag_key: str) -> list[str]:
    targets = list(TARGET_FLAG_REQUIREMENTS.get(flag_key, ()))
    if targets:
        return targets
    if flag_key.startswith("surface_"):
        return ["CLI operator surface", "OpenAPI 3.1 / 3.2 compatible public contract", "OpenRPC 1.4.x admin/control-plane contract"]
    if flag_key in {"strict_boundary_enforcement", "require_tls", "enable_id_token_encryption"}:
        return ["CLI operator surface", "Release bundle and signature verification"]
    if flag_key in {"enable_rfc6750_query", "enable_rfc6750_form"}:
        return ["RFC 6750", "RFC 9700"]
    if flag_key in {"active_surface_sets", "active_protocol_slices", "active_extensions", "runtime_style"}:
        return ["CLI operator surface", "ASGI 3 application package"]
    if flag_key == "oauth21_alignment_mode":
        return ["OAuth 2.1 alignment profile"]
    if flag_key == "enforce_rfc8252":
        return ["RFC 8252"]
    if flag_key == "rfc8707_enabled":
        return ["RFC 8707"]
    if flag_key.startswith("session_cookie_"):
        return ["RFC 6265", "OIDC Session Management", "OIDC RP-Initiated Logout"]
    return ["CLI operator surface"]


def _build_features(repo_root: Path) -> list[dict[str, Any]]:
    features: list[dict[str, Any]] = []
    core_targets, extension_targets, alignment_targets = _target_sets(repo_root)
    for scope_name, target_map in (("core", core_targets), ("extension", extension_targets), ("alignment-only", alignment_targets)):
        for label, target in sorted(target_map.items()):
            features.append(
                {
                    "id": f"target:{_slug(label)}",
                    "kind": "target",
                    "title": label,
                    "description": str(target.get("title") or target.get("quarantine_reason") or label),
                    "source": f"compliance/targets/{_target_manifest_map(repo_root)[label][0]}",
                    "scope": scope_name,
                    "targets": [label],
                    "required_flags": list(TARGET_FLAG_REQUIREMENTS.get(label, ())),
                    "profiles": list(target.get("profiles", [])),
                }
            )

    for path, meta in sorted(ROUTE_REGISTRY.items()):
        if str(meta.get("surface_set")) != "public-rest":
            continue
        features.append(
            {
                "id": f"route:{_slug(path)}",
                "kind": "public-route",
                "title": path,
                "description": str(meta.get("summary", path)),
                "source": str(meta.get("router_ref") or meta.get("publisher_ref") or "tigrbl_auth.config.surfaces"),
                "scope": "core",
                "targets": [str(item) for item in meta.get("targets", ())],
                "required_flags": [str(item) for item in meta.get("flags", ())],
                "paths": [path],
                "methods": [str(item).upper() for item in meta.get("methods", ())],
            }
        )

    for method_name, meta in sorted(get_rpc_method_registry().items()):
        features.append(
            {
                "id": f"rpc:{method_name}",
                "kind": "openrpc-method",
                "title": method_name,
                "description": str(meta.get("summary", method_name)),
                "source": str(meta.get("owner_module", "tigrbl_auth.api.rpc.registry")),
                "scope": "core",
                "targets": ["OpenRPC 1.4.x admin/control-plane contract"],
                "required_flags": [str(item) for item in meta.get("required_flags", ())],
            }
        )

    for command in COMMAND_SPECS:
        if command.verbs:
            for verb in command.verbs:
                features.append(
                    {
                        "id": f"cli-verb:{command.name}.{verb.name}",
                        "kind": "cli-verb",
                        "title": f"{command.name} {verb.name}",
                        "description": verb.description,
                        "source": "tigrbl_auth.cli.metadata",
                        "scope": "core",
                        "targets": _command_targets(command.name),
                        "required_flags": [],
                    }
                )
        else:
            features.append(
                {
                    "id": f"cli-verb:{command.name}",
                    "kind": "cli-verb",
                    "title": command.name,
                    "description": command.description,
                    "source": "tigrbl_auth.cli.metadata",
                    "scope": "core",
                    "targets": _command_targets(command.name),
                    "required_flags": [],
                }
            )

    for key, spec in sorted(ARGUMENT_SPECS.items()):
        features.append(
            {
                "id": f"cli-flag:{key}",
                "kind": "cli-flag",
                "title": ", ".join(spec.flags),
                "description": spec.help,
                "source": "tigrbl_auth.cli.metadata",
                "scope": "core",
                "targets": _flag_targets(key),
                "required_flags": [key] if key in _settings_backed_flags() else [],
            }
        )

    for flag_name in sorted(_settings_backed_flags()):
        features.append(
            {
                "id": f"flag:{flag_name}",
                "kind": "setting-flag",
                "title": flag_name,
                "description": f"Settings-backed governance flag {flag_name}",
                "source": "tigrbl_auth.config.settings",
                "scope": "extension" if flag_name.startswith("enable_rfc78") or flag_name.startswith("enable_rfc79") or flag_name.startswith("enable_rfc82") or flag_name.startswith("enable_rfc88") or flag_name.startswith("enable_rfc89") or flag_name == "enable_rfc8523" else "core",
                "targets": _flag_targets(flag_name),
                "required_flags": [flag_name],
            }
        )

    profiles = _load_yaml(repo_root / "compliance" / "targets" / "profiles.yaml").get("profiles", {})
    for profile_name, profile in sorted(profiles.items()):
        features.append(
            {
                "id": f"profile:{profile_name}",
                "kind": "profile",
                "title": profile_name,
                "description": str(profile.get("description", profile_name)),
                "source": "compliance/targets/profiles.yaml",
                "scope": str(profile.get("scope", "core")),
                "targets": _profile_target_labels(repo_root, profile_name),
                "required_flags": list(flags_for_profile(profile_name)),
                "protocol_slices": list(profile.get("protocol_slices", [])),
            }
        )

    for slice_name, meta in sorted(PROTOCOL_SLICE_REGISTRY.items()):
        features.append(
            {
                "id": f"slice:{slice_name}",
                "kind": "protocol-slice",
                "title": slice_name,
                "description": f"{slice_name} protocol slice",
                "source": "tigrbl_auth.config.deployment",
                "scope": "core",
                "targets": [str(item) for item in meta.get("targets", ())],
                "required_flags": [str(item) for item in meta.get("flags", ())],
                "paths": [str(item) for item in meta.get("routes", ())],
            }
        )

    for extension_name, meta in sorted(EXTENSION_REGISTRY.items()):
        features.append(
            {
                "id": f"extension:{extension_name}",
                "kind": "extension",
                "title": extension_name,
                "description": f"{extension_name} quarantined extension",
                "source": "tigrbl_auth.config.deployment",
                "scope": "extension",
                "targets": [str(item) for item in meta.get("targets", ())],
                "required_flags": [str(item) for item in meta.get("flags", ())],
                "boundary": str(meta.get("boundary", "")),
            }
        )

    return sorted(features, key=lambda item: (str(item["kind"]), str(item["id"])))


def _settings_backed_flags() -> set[str]:
    names: set[str] = set()
    for group in FEATURE_FLAG_GROUPS.values():
        for flag_name in dict(group.get("flags", {})).keys():
            names.add(str(flag_name))
    names.update({"active_surface_sets", "active_protocol_slices", "active_extensions", "runtime_style"})
    names.update({"enforce_rfc8252", "rfc8707_enabled"})
    names.update(
        {
            "session_cookie_name",
            "session_cookie_path",
            "session_cookie_domain",
            "session_cookie_samesite",
            "session_cookie_max_age_seconds",
            "session_cookie_renewal_seconds",
            "session_cookie_cross_site",
            "session_cookie_force_secure",
        }
    )
    return names


def _load_mapping(repo_root: Path, relative_path: str) -> dict[str, list[str]]:
    payload = _load_yaml(repo_root / relative_path)
    return {str(key): [str(item) for item in value] for key, value in dict(payload or {}).items()}


def _feature_to_target(features: list[dict[str, Any]]) -> dict[str, list[str]]:
    return {
        str(feature["id"]): sorted(dict.fromkeys(str(item) for item in feature.get("targets", []) if str(item).strip()))
        for feature in features
    }


def _feature_to_tests(repo_root: Path, features: list[dict[str, Any]]) -> dict[str, list[str]]:
    target_to_test = _load_mapping(repo_root, "compliance/mappings/target-to-test.yaml")
    mapping: dict[str, list[str]] = {}
    for feature in features:
        refs: list[str] = []
        for target in feature.get("targets", []):
            refs.extend(target_to_test.get(str(target), []))
        mapping[str(feature["id"])] = sorted(dict.fromkeys(refs))
    return mapping


def _feature_to_evidence(repo_root: Path, features: list[dict[str, Any]]) -> dict[str, list[str]]:
    target_to_evidence = _load_mapping(repo_root, "compliance/mappings/target-to-evidence.yaml")
    mapping: dict[str, list[str]] = {}
    for feature in features:
        refs: list[str] = []
        for target in feature.get("targets", []):
            refs.extend(target_to_evidence.get(str(target), []))
        mapping[str(feature["id"])] = sorted(dict.fromkeys(refs))
    return mapping


def _flag_to_feature(features: list[dict[str, Any]]) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for feature in features:
        for flag_name in feature.get("required_flags", []):
            mapping.setdefault(str(flag_name), []).append(str(feature["id"]))
    return {key: sorted(dict.fromkeys(value)) for key, value in sorted(mapping.items())}


def _legacy_flag_to_target(flag_to_feature: dict[str, list[str]], feature_to_target: dict[str, list[str]]) -> dict[str, list[str]]:
    payload: dict[str, list[str]] = {}
    for flag_name, feature_ids in flag_to_feature.items():
        labels: list[str] = []
        for feature_id in feature_ids:
            labels.extend(feature_to_target.get(feature_id, []))
        payload[flag_name] = sorted(dict.fromkeys(labels))
    return payload


def _target_claims(repo_root: Path, core_targets: dict[str, dict[str, Any]]) -> dict[str, Any]:
    claims = []
    for label, target in sorted(core_targets.items(), key=lambda item: (_profile_rank(_earliest_profile(item[1].get("profiles"))), item[0])):
        claims.append(
            {
                "target": label,
                "tier": 3,
                "status": str(target.get("status", "evidenced-release-gated")),
                "profile": _earliest_profile(target.get("profiles")),
            }
        )
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "claim_set": {
            "current_repository_tier": 3,
            "phase": "P14",
            "authoritative_scope_manifest": "compliance/targets/certification_scope.yaml",
            "claims": claims,
            "governance_status": "installed",
        },
    }


def _claim_registry(repo_root: Path, features: list[dict[str, Any]]) -> dict[str, Any]:
    claim_rows: list[dict[str, Any]] = []
    for feature in features:
        claim_rows.append(
            {
                "id": str(feature["id"]),
                "feature_id": str(feature["id"]),
                "kind": str(feature["kind"]),
                "title": str(feature["title"]),
                "description": str(feature.get("description", "")),
                "scope": str(feature.get("scope", "core")),
                "targets": list(feature.get("targets", [])),
                "required_flags": list(feature.get("required_flags", [])),
                "source": str(feature.get("source", "")),
            }
        )
    fapi_claims = _load_yaml(repo_root / FAPI_ATOMIC_CLAIMS_PATH)
    for claim in fapi_claims.get("claims", []):
        claim_rows.append(
            {
                "id": str(claim.get("id")),
                "feature_id": f"profile:{fapi_claims.get('profile', 'fapi2-security')}",
                "kind": "atomic-profile-claim",
                "title": str(claim.get("title", "")),
                "description": str(claim.get("description", "")),
                "scope": "core",
                "targets": [str(item) for item in claim.get("targets", [])],
                "required_flags": [str(item) for item in claim.get("required_flags", [])],
                "source": FAPI_ATOMIC_CLAIMS_PATH,
                "profile": str(fapi_claims.get("profile", "fapi2-security")),
            }
        )
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "generated_from": [
            "compliance/targets/*.yaml",
            "tigrbl_auth.config.surfaces",
            "tigrbl_auth.api.rpc.registry",
            "tigrbl_auth.cli.metadata",
            "tigrbl_auth.config.deployment",
            FAPI_ATOMIC_CLAIMS_PATH,
        ],
        "summary": {
            "claim_count": len(claim_rows),
            "atomic_feature_claim_count": len(features),
            "fapi_atomic_claim_count": len(fapi_claims.get("claims", [])),
        },
        "claims": sorted(claim_rows, key=lambda item: str(item["id"])),
    }


def _issue_registry(repo_root: Path, verification: dict[str, Any]) -> dict[str, Any]:
    truth = _load_yaml(repo_root / "docs" / "compliance" / "truth_chain.json") if (repo_root / "docs" / "compliance" / "truth_chain.json").exists() else {}
    summary = truth.get("summary", {}) if isinstance(truth, dict) else {}
    issues: list[dict[str, Any]] = []
    if verification["core_targets_missing_from_feature_map"]:
        issues.append(
            {
                "id": "claim-registry.core-target-gaps",
                "severity": "high",
                "status": "open",
                "description": "Core targets are missing from the canonical feature-to-target map.",
                "count": verification["core_targets_missing_from_feature_map"],
            }
        )
    if verification["extension_targets_missing_from_feature_map"]:
        issues.append(
            {
                "id": "claim-registry.extension-target-gaps",
                "severity": "medium",
                "status": "open",
                "description": "Extension targets are missing from the canonical feature-to-target map.",
                "count": verification["extension_targets_missing_from_feature_map"],
            }
        )
    if verification["settings_backed_flags_missing_from_flag_map"]:
        issues.append(
            {
                "id": "claim-registry.settings-flag-gaps",
                "severity": "high",
                "status": "open",
                "description": "Settings-backed flags are missing from the canonical flag-to-feature map.",
                "count": verification["settings_backed_flags_missing_from_flag_map"],
            }
        )
    if not bool(summary.get("final_release_ready", False)):
        issues.append(
            {
                "id": "release.final-certification-blocked",
                "severity": "high",
                "status": "open",
                "description": "The repository is still a truthful checkpoint and not a final certified release.",
                "blockers": list(summary.get("open_gaps", [])),
            }
        )
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "summary": {"issue_count": len(issues)},
        "issues": issues,
    }


def _risk_registry(repo_root: Path, verification: dict[str, Any]) -> dict[str, Any]:
    truth = _load_yaml(repo_root / "docs" / "compliance" / "truth_chain.json") if (repo_root / "docs" / "compliance" / "truth_chain.json").exists() else {}
    summary = truth.get("summary", {}) if isinstance(truth, dict) else {}
    risks = [
        {
            "id": "risk.truthful-release-positioning",
            "status": "active" if not bool(summary.get("final_release_ready", False)) else "accepted",
            "description": "Certification messaging must remain checkpoint-only until the truth chain reports final_release_ready=true.",
        },
        {
            "id": "risk.claim-registry-drift",
            "status": "active" if not verification["passed"] else "mitigated",
            "description": "Legacy maps and atomic claim rows can drift unless generated from canonical source metadata.",
        },
    ]
    return {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "summary": {"risk_count": len(risks)},
        "risks": risks,
    }


def verify_claim_registries(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    features = _build_features(repo_root)
    feature_to_target = _feature_to_target(features)
    flag_to_feature = _flag_to_feature(features)
    core_targets, extension_targets, _alignment_targets = _target_sets(repo_root)
    settings_backed_flags = _settings_backed_flags()

    tracked_core_targets = {
        label
        for labels in feature_to_target.values()
        for label in labels
        if label in core_targets
    }
    tracked_extension_targets = {
        label
        for labels in feature_to_target.values()
        for label in labels
        if label in extension_targets
    }
    public_route_features = {str(feature["id"]) for feature in features if str(feature["kind"]) == "public-route"}
    rpc_features = {str(feature["id"]) for feature in features if str(feature["kind"]) == "openrpc-method"}
    cli_verb_features = {str(feature["id"]) for feature in features if str(feature["kind"]) == "cli-verb"}
    cli_flag_features = {str(feature["id"]) for feature in features if str(feature["kind"]) == "cli-flag"}
    profile_features = {str(feature["id"]) for feature in features if str(feature["kind"]) == "profile"}
    slice_features = {str(feature["id"]) for feature in features if str(feature["kind"]) == "protocol-slice"}
    extension_features = {str(feature["id"]) for feature in features if str(feature["kind"]) == "extension"}

    direct_commands = sum(1 for command in COMMAND_SPECS if not command.verbs)
    nested_verbs = sum(len(command.verbs) for command in COMMAND_SPECS if command.verbs)
    expected_cli_verb_count = direct_commands + nested_verbs

    failures: list[str] = []
    core_missing = sorted(set(core_targets) - tracked_core_targets)
    extension_missing = sorted(set(extension_targets) - tracked_extension_targets)
    flag_missing = sorted(settings_backed_flags - set(flag_to_feature))
    if core_missing:
        failures.append(f"Untracked core targets remain: {', '.join(core_missing)}")
    if extension_missing:
        failures.append(f"Untracked extension targets remain: {', '.join(extension_missing)}")
    if flag_missing:
        failures.append(f"Settings-backed flags remain unmapped: {', '.join(flag_missing)}")
    if len(public_route_features) != len([path for path, meta in ROUTE_REGISTRY.items() if str(meta.get('surface_set')) == 'public-rest']):
        failures.append("Public route atomic claim coverage is incomplete.")
    if len(rpc_features) != len(get_rpc_method_registry()):
        failures.append("OpenRPC method atomic claim coverage is incomplete.")
    if len(cli_verb_features) != expected_cli_verb_count:
        failures.append("CLI verb atomic claim coverage is incomplete.")
    if len(cli_flag_features) != len(ARGUMENT_SPECS):
        failures.append("CLI flag atomic claim coverage is incomplete.")
    if len(profile_features) != len(_load_yaml(repo_root / "compliance" / "targets" / "profiles.yaml").get("profiles", {})):
        failures.append("Profile atomic claim coverage is incomplete.")
    if len(slice_features) != len(PROTOCOL_SLICE_REGISTRY):
        failures.append("Protocol slice atomic claim coverage is incomplete.")
    if len(extension_features) != len(EXTENSION_REGISTRY):
        failures.append("Extension atomic claim coverage is incomplete.")

    return {
        "passed": not failures,
        "core_targets_missing_from_feature_map": len(core_missing),
        "extension_targets_missing_from_feature_map": len(extension_missing),
        "settings_backed_flags_missing_from_flag_map": len(flag_missing),
        "public_route_claim_count": len(public_route_features),
        "openrpc_method_claim_count": len(rpc_features),
        "cli_verb_claim_count": len(cli_verb_features),
        "cli_flag_claim_count": len(cli_flag_features),
        "profile_claim_count": len(profile_features),
        "slice_claim_count": len(slice_features),
        "extension_claim_count": len(extension_features),
        "failures": failures,
    }


def generate_claim_registries(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    features = _build_features(repo_root)
    feature_to_target = _feature_to_target(features)
    flag_to_feature = _flag_to_feature(features)
    feature_to_test = _feature_to_tests(repo_root, features)
    feature_to_evidence = _feature_to_evidence(repo_root, features)
    legacy_flag_to_target = _legacy_flag_to_target(flag_to_feature, feature_to_target)
    verification = verify_claim_registries(repo_root)
    core_targets, extension_targets, _alignment_targets = _target_sets(repo_root)

    feature_payload = {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "generated_from": [
            "compliance/targets/*.yaml",
            "tigrbl_auth.config.surfaces",
            "tigrbl_auth.api.rpc.registry",
            "tigrbl_auth.cli.metadata",
            "tigrbl_auth.config.deployment",
        ],
        "summary": {
            "feature_count": len(features),
            "tracked_core_target_count": len(core_targets),
            "tracked_extension_target_count": len(extension_targets),
            "settings_backed_flag_count": len(_settings_backed_flags()),
        },
        "features": features,
    }
    _write_yaml(repo_root / FEATURE_REGISTRY_PATH, feature_payload)
    _write_yaml(repo_root / CLAIM_REGISTRY_PATH, _claim_registry(repo_root, features))
    _write_yaml(repo_root / ISSUE_REGISTRY_PATH, _issue_registry(repo_root, verification))
    _write_yaml(repo_root / RISK_REGISTRY_PATH, _risk_registry(repo_root, verification))
    _write_yaml(repo_root / FEATURE_TO_TARGET_PATH, feature_to_target)
    _write_yaml(repo_root / FLAG_TO_FEATURE_PATH, flag_to_feature)
    _write_yaml(repo_root / FEATURE_TO_TEST_PATH, feature_to_test)
    _write_yaml(repo_root / FEATURE_TO_EVIDENCE_PATH, feature_to_evidence)
    _write_yaml(repo_root / LEGACY_FLAG_TO_TARGET_PATH, legacy_flag_to_target)
    _write_yaml(repo_root / DECLARED_TARGET_CLAIMS_PATH, _target_claims(repo_root, core_targets))

    repository_state_payload = _load_yaml(repo_root / REPOSITORY_STATE_PATH)
    repository_state = dict(repository_state_payload.get("repository_state", {}))
    repository_state.update(
        {
            "phase_14_claim_registry_canonical_complete": verification["passed"],
            "phase_14_fapi2_security_profile_declared_complete": True,
            "phase_14_public_route_atomic_claims_complete": verification["public_route_claim_count"] == len([path for path, meta in ROUTE_REGISTRY.items() if str(meta.get("surface_set")) == "public-rest"]),
            "phase_14_openrpc_atomic_claims_complete": verification["openrpc_method_claim_count"] == len(get_rpc_method_registry()),
            "phase_14_cli_atomic_claims_complete": verification["cli_flag_claim_count"] == len(ARGUMENT_SPECS) and verification["cli_verb_claim_count"] >= 1,
            "phase_14_core_targets_missing_from_feature_map": verification["core_targets_missing_from_feature_map"],
            "phase_14_extension_targets_missing_from_feature_map": verification["extension_targets_missing_from_feature_map"],
            "phase_14_settings_backed_flags_missing_from_flag_map": verification["settings_backed_flags_missing_from_flag_map"],
            "phase_14_release_claims_machine_derivable": verification["passed"],
        }
    )
    repository_state_payload["schema_version"] = int(repository_state_payload.get("schema_version", 1) or 1)
    repository_state_payload["repository_state"] = repository_state
    _write_yaml(repo_root / REPOSITORY_STATE_PATH, repository_state_payload)
    return verification


__all__ = ["generate_claim_registries", "verify_claim_registries"]
