from __future__ import annotations

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
            "delivery_track": "release-claim-canonicalization",
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
            "tigrbl_identity_cli.cli.metadata",
            "tigrbl_identity_runtime.deployment",
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
            "tigrbl_identity_cli.cli.metadata",
            "tigrbl_identity_runtime.deployment",
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
    for key in LEGACY_CLAIM_MODEL_STATE_KEYS:
        repository_state.pop(key, None)
    repository_state.update(
        {
            "claim_registry_canonical_complete": verification["passed"],
            "fapi2_security_profile_declared_complete": True,
            "public_route_atomic_claims_complete": verification["public_route_claim_count"] == len([path for path, meta in ROUTE_REGISTRY.items() if str(meta.get("surface_set")) == "public-rest"]),
            "cli_atomic_claims_complete": verification["cli_flag_claim_count"] == len(ARGUMENT_SPECS) and verification["cli_verb_claim_count"] >= 1,
            "core_targets_missing_from_feature_map": verification["core_targets_missing_from_feature_map"],
            "extension_targets_missing_from_feature_map": verification["extension_targets_missing_from_feature_map"],
            "settings_backed_flags_missing_from_flag_map": verification["settings_backed_flags_missing_from_flag_map"],
            "release_claims_machine_derivable": verification["passed"],
        }
    )
    repository_state_payload["schema_version"] = int(repository_state_payload.get("schema_version", 1) or 1)
    repository_state_payload["repository_state"] = repository_state
    _write_yaml(repo_root / REPOSITORY_STATE_PATH, repository_state_payload)
    return verification


__all__ = ["generate_claim_registries", "verify_claim_registries"]
