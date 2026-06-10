from __future__ import annotations

def run_final_release_readiness_gate(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    _ensure_repo_local_operator_state(repo_root)
    generate_state_reports(repo_root)
    validated = load_validated_execution_status(repo_root)
    runtime_profile = json.loads((repo_root / "docs" / "compliance" / "runtime_profile_report.json").read_text(encoding="utf-8")) if (repo_root / "docs" / "compliance" / "runtime_profile_report.json").exists() else {}
    certification_state = json.loads((repo_root / "docs" / "compliance" / "certification_state_report.json").read_text(encoding="utf-8")) if (repo_root / "docs" / "compliance" / "certification_state_report.json").exists() else {}
    runner_count = len(registered_runner_names())
    summary = runtime_profile.get("summary", {}) if isinstance(runtime_profile, dict) else {}
    failures: list[str] = []
    runtime_report_source_mode = str(summary.get("source_mode", runtime_profile.get("report_mode", "live-probe")))
    if int(summary.get("ready_count", 0)) != runner_count:
        failures.append(
            "Runtime profiles are not all ready in the preserved validated-run inventory."
            if runtime_report_source_mode == "validated-runs"
            else "Runtime profiles are not all ready in the current certification environment."
        )
    if int(summary.get("invalid_count", 0)) != 0:
        failures.append("At least one kept runner is still invalid.")
    if int(summary.get("missing_count", 0)) != 0:
        failures.append("At least one kept runner is still missing.")
    if not validated.get("validated_inventory_complete", False):
        failures.append(
            "Validated artifact inventory is below the required "
            f"{validated.get('required_validated_inventory_count', 0)} artifact threshold."
        )
    if not validated.get("runtime_matrix_green", False):
        failures.append("The clean-room install matrix is not green from validated-run evidence.")
    if not validated.get("in_scope_test_lanes_green", False):
        failures.append("In-scope certification test lanes are not green from validated-run evidence.")
    if not validated.get("migration_portability_passed", False):
        failures.append("Migration portability validation is not preserved for both SQLite and PostgreSQL.")
    if not validated.get("tier3_evidence_rebuilt_from_validated_runs", False):
        failures.append("Tier 3 evidence has not been rebuilt from validated runs.")
    tier4_ready = bool(certification_state.get("summary", {}).get("strict_independent_claims_ready", False))
    warnings: list[str] = []
    if not tier4_ready:
        warnings.append("Tier 4 bundle promotion is not complete for the retained boundary.")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "runtime_profiles_truly_ready": int(summary.get("ready_count", 0)) == runner_count and int(summary.get("invalid_count", 0)) == 0 and int(summary.get("missing_count", 0)) == 0,
            "validated_inventory_complete": bool(validated.get("validated_inventory_complete", False)),
            "required_validated_inventory_count": int(validated.get("required_validated_inventory_count", 0)),
            "validated_inventory_present_count": int(validated.get("validated_inventory_present_count", 0)),
            "clean_room_install_matrix_green": bool(validated.get("runtime_matrix_green", False)),
            "in_scope_test_lanes_green": bool(validated.get("in_scope_test_lanes_green", False)),
            "migration_portability_passed": bool(validated.get("migration_portability_passed", False)),
            "tier3_evidence_rebuilt_from_validated_runs": bool(validated.get("tier3_evidence_rebuilt_from_validated_runs", False)),
            "tier4_bundle_promotion_complete": tier4_ready,
        },
    }
    _write_report(repo_root / "docs" / "compliance", "final_release_gate_report", payload, "Final Release Gate Report")
    return payload

def verify_test_classification(repo_root: Path, *, strict: bool = True) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    preferred = repo_root / "compliance" / "mappings" / "test_classification.yaml"
    legacy = repo_root / "compliance" / "mappings" / "test-classification.yaml"
    mapping_path = preferred if preferred.exists() else legacy
    failures: list[str] = []
    warnings: list[str] = []
    mapping = _load_yaml(mapping_path) if mapping_path.exists() else {"categories": {}}
    categories = mapping.get("categories", {}) or {}
    allowed_categories = {
        "unit",
        "integration",
        "conformance",
        "interop",
        "e2e",
        "security",
        "negative",
        "perf",
        "security-negative",
        "migration-portability",
        "peer",
    }
    if not categories:
        failures.append("Missing test classification categories")
    if not preferred.exists():
        failures.append("Missing canonical test classification manifest: compliance/mappings/test_classification.yaml")
    unknown_categories = sorted(set(categories) - allowed_categories)
    for category in unknown_categories:
        failures.append(f"Unknown test classification category: {category}")
    classified: set[str] = set()
    for category, files in categories.items():
        if category in allowed_categories and not (repo_root / "tests" / category).exists() and category != "conformance":
            warnings.append(f"Missing test category directory: tests/{category}")
        for rel in files:
            normalized = str(rel).replace("\\", "/")
            if normalized in classified:
                failures.append(f"Classified test file appears multiple times: {normalized}")
            classified.add(normalized)
            if not (repo_root / normalized).exists():
                failures.append(f"Missing classified test file: {normalized}")
    discovered = {
        str(path.relative_to(repo_root)).replace("\\", "/")
        for path in sorted((repo_root / "tests").glob("**/test_*.py"))
    }
    unclassified = sorted(discovered - classified)
    if unclassified:
        failures.append(f"Unclassified test files present: {', '.join(unclassified)}")
    legacy_i9n = sorted(str(path.relative_to(repo_root)).replace("\\", "/") for path in (repo_root / "tests" / "i9n").glob("test_*.py")) if (repo_root / "tests" / "i9n").exists() else []
    if legacy_i9n:
        failures.append(f"Legacy tests/i9n migration incomplete: {', '.join(legacy_i9n)}")
    targets = []
    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    for entry in scope.get("targets", []):
        if str(entry.get("scope_bucket")) == "out-of-scope/deferred":
            continue
        targets.append(str(entry.get("label")))
    target_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml")
    for target in targets:
        refs = [str(path).replace("\\", "/") for path in target_to_test.get(target, [])]
        if not refs:
            failures.append(f"No explicit test mapping for in-scope target: {target}")
            continue
        for ref in refs:
            if ref not in classified:
                failures.append(f"Mapped test path missing from canonical test classification: {target} -> {ref}")
            if not (repo_root / ref).exists():
                failures.append(f"Mapped test path missing on disk: {target} -> {ref}")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "mapping_path": str(mapping_path.relative_to(repo_root)) if mapping_path.exists() else None,
            "category_count": len(categories),
            "classified_test_count": len(classified),
            "discovered_test_count": len(discovered),
            "target_count": len(targets),
        },
    }
    _write_report(repo_root / "docs" / "compliance", "test_classification_report", payload, "Test Classification Report")
    return payload


def _certification_partition_for_test(path: str) -> str:
    normalized = path.replace("\\", "/")
    if "tests/interop/" in normalized:
        return "peer" if "peer_" in normalized or "tier4_" in normalized else "interop"
    if "migration" in normalized:
        return "migration-portability"
    if "/security/" in normalized or "/negative/" in normalized:
        return "security-negative"
    if "/integration/" in normalized or "/runtime/" in normalized:
        return "integration"
    if "/conformance/" in normalized:
        return "conformance"
    return "unit"


def _security_sensitive_claim(claim: Mapping[str, Any]) -> bool:
    claim_id = str(claim.get("id", "")).lower()
    title = str(claim.get("title", "")).lower()
    targets = [str(item).lower() for item in claim.get("targets", []) or []]
    keywords = (
        "fapi",
        "security",
        "sender-constrained",
        "dpop",
        "mtls",
        "issuer",
        "mix-up",
        "par",
        "password",
        "implicit",
        "hybrid",
    )
    return any(keyword in claim_id or keyword in title for keyword in keywords) or any(
        target in {"rfc 8705", "rfc 9126", "rfc 9207", "rfc 9449", "rfc 9700"} for target in targets
    )


def _negative_tests_for_claim(claim: Mapping[str, Any], partitioned_tests: Mapping[str, list[str]]) -> list[str]:
    claim_id = str(claim.get("id", "")).lower()
    negatives = list(partitioned_tests.get("security-negative", []))
    selected: list[str] = []

    def _match(*patterns: str) -> None:
        for path in negatives:
            lower = path.lower()
            if any(pattern in lower for pattern in patterns) and path not in selected:
                selected.append(path)

    if "sender-constrained" in claim_id or "dpop" in claim_id or "mtls" in claim_id:
        _match("sender_constraint", "capability_certification_attack_paths")
    if "par" in claim_id:
        _match("capability_certification_attack_paths", "capability_hardening_runtime_enforcement")
    if "issuer" in claim_id or "mix" in claim_id:
        _match("capability_certification_attack_paths", "capability_hardening_cluster_b")
    if "security-bcp" in claim_id or "rfc 9700" in str(claim.get("targets", [])).lower():
        _match("capability_hardening_runtime_enforcement", "capability_certification_attack_paths")
    if not selected and _security_sensitive_claim(claim):
        _match("capability_certification_attack_paths", "capability_hardening_runtime_enforcement", "capability_sender_constraint_replay")
    return selected


def _git_checkout_summary(repo_root: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        return {"git_available": False, "clean": False, "failure": str(exc), "changed_paths": []}
    if result.returncode != 0:
        return {"git_available": True, "clean": False, "failure": result.stderr.strip() or "git status failed", "changed_paths": []}
    changed_paths = [line[3:] for line in result.stdout.splitlines() if line.strip()]
    return {
        "git_available": True,
        "clean": not changed_paths,
        "changed_path_count": len(changed_paths),
        "changed_paths": changed_paths[:200],
    }


def generate_certification_evidence_index(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    claim_registry = _load_yaml(repo_root / "compliance" / "claims" / "claim-registry.yaml")
    target_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-test.yaml")
    target_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-evidence.yaml")
    feature_to_test = _load_yaml(repo_root / "compliance" / "mappings" / "feature-to-test.yaml")
    feature_to_evidence = _load_yaml(repo_root / "compliance" / "mappings" / "feature-to-evidence.yaml")
    classification = _load_yaml(repo_root / "compliance" / "mappings" / "test_classification.yaml")
    profiles = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")
    discovered_tests = sorted(str(path.relative_to(repo_root)).replace("\\", "/") for path in (repo_root / "tests").rglob("test_*.py"))
    partitioned_tests: dict[str, list[str]] = {}
    for path in discovered_tests:
        partitioned_tests.setdefault(_certification_partition_for_test(path), []).append(path)

    claims = list(claim_registry.get("claims", []))
    claim_bindings: list[dict[str, Any]] = []
    missing_positive: list[str] = []
    missing_negative: list[str] = []
    for claim in claims:
        feature_id = str(claim.get("feature_id", ""))
        targets = [str(item) for item in claim.get("targets", []) or []]
        positive_tests = list(dict.fromkeys(
            list(feature_to_test.get(feature_id, []) or [])
            + [test for target in targets for test in (target_to_test.get(target, []) or [])]
        ))
        evidence_refs = list(dict.fromkeys(
            list(feature_to_evidence.get(feature_id, []) or [])
            + [ref for target in targets for ref in (target_to_evidence.get(target, []) or [])]
        ))
        negative_tests = _negative_tests_for_claim(claim, partitioned_tests)
        binding = {
            "claim_id": str(claim.get("id")),
            "feature_id": feature_id,
            "targets": targets,
            "profile": claim.get("profile"),
            "positive_tests": positive_tests,
            "negative_tests": negative_tests,
            "evidence_refs": evidence_refs,
            "security_sensitive": _security_sensitive_claim(claim),
        }
        claim_bindings.append(binding)
        if not positive_tests or not evidence_refs:
            missing_positive.append(str(claim.get("id")))
        if binding["security_sensitive"] and not negative_tests:
            missing_negative.append(str(claim.get("id")))

    target_profile_bundles: list[dict[str, Any]] = []
    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    retained_targets = [
        str(entry.get("label"))
        for entry in scope.get("targets", [])
        if str(entry.get("scope_bucket")) != "out-of-scope/deferred"
    ]
    for profile in profiles:
        effective_claims_path = write_effective_claims_manifest(
            repo_root,
            deployment_from_options(profile=profile),
            profile_label=profile,
        )
        effective_claims = _load_yaml(effective_claims_path)
        profile_targets = {
            str(entry.get("target"))
            for entry in effective_claims.get("claim_set", {}).get("claims", [])
        }
        for target in sorted(profile_targets & set(retained_targets)):
            target_profile_bundles.append(
                {
                    "profile": profile,
                    "target": target,
                    "tests": list(target_to_test.get(target, []) or []),
                    "evidence_refs": list(target_to_evidence.get(target, []) or []),
                }
            )

    failures: list[str] = []
    if missing_positive:
        failures.append(f"Claims missing positive proof or evidence refs: {', '.join(missing_positive[:25])}")
    if missing_negative:
        failures.append(f"Security-sensitive claims missing negative proof: {', '.join(missing_negative[:25])}")
    payload = {
        "passed": not missing_positive and not missing_negative,
        "failures": failures,
        "warnings": [],
        "summary": {
            "claim_count": len(claim_bindings),
            "fapi_claim_count": sum(1 for item in claim_bindings if item.get("profile") == "fapi2-security"),
            "security_sensitive_claim_count": sum(1 for item in claim_bindings if item.get("security_sensitive")),
            "partition_count": len(partitioned_tests),
            "target_profile_bundle_count": len(target_profile_bundles),
            "clean_checkout": _git_checkout_summary(repo_root),
        },
        "test_partitions": partitioned_tests,
        "claim_bindings": claim_bindings,
        "target_profile_bundles": target_profile_bundles,
        "classification_profiles": classification.get("profiles", {}),
    }
    out_root = repo_root / "docs" / "compliance"
    _write_report(out_root, "certification_evidence_index", payload, "Certification Evidence Index")
    _write_json(repo_root / "compliance" / "evidence" / "certification_test_partitions.json", {"partitions": partitioned_tests})
    _write_yaml(repo_root / "compliance" / "evidence" / "certification_test_partitions.yaml", {"partitions": partitioned_tests})
    _write_json(repo_root / "compliance" / "evidence" / "claim_proof_bindings.json", {"bindings": claim_bindings})
    _write_yaml(repo_root / "compliance" / "evidence" / "claim_proof_bindings.yaml", {"bindings": claim_bindings})
    _write_json(repo_root / "compliance" / "evidence" / "target_profile_evidence.json", {"bundles": target_profile_bundles})
    _write_yaml(repo_root / "compliance" / "evidence" / "target_profile_evidence.yaml", {"bundles": target_profile_bundles})
    return payload


def _copy_rel_artifact(repo_root: Path, rel_path: str, bundle_root: Path) -> dict[str, Any]:
    src = repo_root / rel_path
    if not src.exists():
        return {"path": rel_path, "present": False}
    dst = bundle_root / rel_path
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"path": rel_path, "present": True, "sha256": _hash_file(dst)}
