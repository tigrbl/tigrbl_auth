from __future__ import annotations

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
    claim_text = " ".join(
        [
            claim_id,
            str(claim.get("title", "")).lower(),
            str(claim.get("description", "")).lower(),
            " ".join(str(item).lower() for item in claim.get("targets", []) or []),
        ]
    ).replace("-", "_")
    negatives = list(
        dict.fromkeys(
            list(partitioned_tests.get("security-negative", []))
            + list(partitioned_tests.get("conformance", []))
            + list(partitioned_tests.get("unit", []))
            + list(partitioned_tests.get("integration", []))
            + list(partitioned_tests.get("interop", []))
            + list(partitioned_tests.get("peer", []))
        )
    )
    selected: list[str] = []

    def _match(*patterns: str) -> None:
        for path in negatives:
            lower = path.lower().replace("-", "_")
            if any(pattern in lower for pattern in patterns) and path not in selected:
                selected.append(path)

    if any(token in claim_text for token in ("sender_constrained", "dpop", "mtls", "rfc 8705", "rfc 9449")):
        _match(
            "sender_constraint",
            "sender_constrained",
            "dpop",
            "mtls",
            "resource_server_consumer_boundary",
            "certification_attack_paths",
            "hardening_cluster_c",
        )
    if "par" in claim_text or "rfc 9126" in claim_text:
        _match(
            "certification_attack_paths",
            "hardening_runtime_enforcement",
            "rfc9126",
            "pushed_authorization",
            "hardening_cluster_b",
        )
    if "jar" in claim_text or "rfc 9101" in claim_text:
        _match("certification_attack_paths", "rfc9101", "hardening_cluster_b")
    if "rar" in claim_text or "rfc 9396" in claim_text:
        _match("certification_attack_paths", "rfc9396", "hardening_cluster_b")
    if any(token in claim_text for token in ("issuer", "mix", "rfc 9207", "openid_configuration")):
        _match(
            "certification_attack_paths",
            "issuer_confusion",
            "rfc9207",
            "realm_isolation",
            "tenant_isolation",
            "runtime_issuer",
            "hardening_cluster_b",
        )
    if any(token in claim_text for token in ("bearer", "rfc6750", "rfc 6750", "enable_rfc6750", "route:token")):
        _match(
            "rfc6750_bearer_token",
            "resource_server_consumer_boundary",
            "security_deps",
            "hardening_cluster_c",
        )
    if "password" in claim_text:
        _match("certification_attack_paths", "hardening_runtime_enforcement", "backends", "crypto")
    if "token_exchange" in claim_text or "rfc 8693" in claim_text:
        _match("token_exchange", "certification_attack_paths", "resource_server_consumer_boundary")
    if any(token in claim_text for token in ("security_bcp", "rfc 9700", "hardening", "fapi2_security", "security")):
        _match(
            "certification_attack_paths",
            "hardening_runtime_enforcement",
            "rfc9700",
            "fapi_runtime_profile",
            "profile_discovery_runtime",
            "hardening_cluster_c",
        )
    if claim_id.startswith("profile:"):
        _match("peer_counterpart_catalog", "peer_matrix_artifacts", "tier4_promotion_fail_closed")
    if not selected and _security_sensitive_claim(claim):
        _match(
            "certification_attack_paths",
            "hardening_runtime_enforcement",
            "issuer_confusion",
            "rfc6750_bearer_token",
            "hardening_cluster_c",
            "peer_counterpart_catalog",
            "tier4_promotion_fail_closed",
        )
    return selected


GENERATED_CLEAN_CHECK_PATHS = {
    "CERTIFICATION_STATUS.md",
    "CURRENT_STATE.md",
    "compliance/claims/recertification-state.yaml",
    "compliance/claims/repository-state.yaml",
    "compliance/evidence/certification_test_partitions.json",
    "compliance/evidence/certification_test_partitions.yaml",
    "compliance/evidence/claim_proof_bindings.json",
    "compliance/evidence/claim_proof_bindings.yaml",
    "compliance/evidence/target_profile_evidence.json",
    "compliance/evidence/target_profile_evidence.yaml",
    "docs/adr/INDEX.md",
    "docs/adr/index.json",
    "specs/cli/cli_contract.json",
    "specs/cli/cli_contract.yaml",
}
GENERATED_CLEAN_CHECK_PREFIXES = (
    "docs/compliance/",
    "docs/compliance/collected/",
)


def _clean_check_ignored(path: str) -> bool:
    normalized = path.replace("\\", "/").strip()
    return normalized in GENERATED_CLEAN_CHECK_PATHS or any(
        normalized.startswith(prefix) for prefix in GENERATED_CLEAN_CHECK_PREFIXES
    )


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
    raw_changed_paths = [line[3:] for line in result.stdout.splitlines() if line.strip()]
    changed_paths = [path for path in raw_changed_paths if not _clean_check_ignored(path)]
    ignored_paths = [path for path in raw_changed_paths if _clean_check_ignored(path)]
    return {
        "git_available": True,
        "clean": not changed_paths,
        "changed_path_count": len(changed_paths),
        "changed_paths": changed_paths[:200],
        "ignored_generated_path_count": len(ignored_paths),
        "ignored_generated_paths": ignored_paths[:200],
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
