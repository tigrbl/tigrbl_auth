from __future__ import annotations

def build_evidence_bundle(
    repo_root: Path,
    deployment: Any,
    *,
    tier: str = "3",
    profile_label: str = "active",
    bundle_dir: Path | None = None,
) -> Path:
    repo_root = repo_root.resolve()
    profile_name = profile_label if profile_label != "active" else deployment.profile
    out_dir = bundle_dir or (repo_root / "dist" / "evidence-bundles" / profile_name / f"tier{tier}")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    evidence_index = generate_certification_evidence_index(repo_root)
    claims_path = write_effective_claims_manifest(repo_root, deployment, profile_label=profile_label)
    evidence_path = write_effective_evidence_manifest(repo_root, deployment, profile_label=profile_label)
    openapi_path = write_openapi_contract(repo_root, deployment, profile_label=profile_label)
    try:
        openrpc_path = write_openrpc_contract(repo_root, deployment, profile_label=profile_label)
    except Exception:
        openrpc_path = _openrpc_path(repo_root, profile_label)
    adr_index = build_adr_index(repo_root)
    copied = [
        _copy_rel_artifact(repo_root, str(claims_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, str(evidence_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, str(openapi_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, str(openrpc_path.relative_to(repo_root)), out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/certification_test_partitions.json", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/certification_test_partitions.yaml", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/claim_proof_bindings.json", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/claim_proof_bindings.yaml", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/target_profile_evidence.json", out_dir),
        _copy_rel_artifact(repo_root, "compliance/evidence/target_profile_evidence.yaml", out_dir),
    ]
    for item in evidence_index.get("target_profile_bundles", []):
        if str(item.get("profile")) != profile_name:
            continue
        target_slug = re.sub(r"[^a-z0-9]+", "-", str(item.get("target", "")).lower()).strip("-")
        target_dir = out_dir / "targets" / target_slug
        target_dir.mkdir(parents=True, exist_ok=True)
        target_manifest = {
            "profile": profile_name,
            "target": item.get("target"),
            "tests": item.get("tests", []),
            "evidence_refs": item.get("evidence_refs", []),
        }
        _write_json(target_dir / "bundle-manifest.json", target_manifest)
        _write_yaml(target_dir / "bundle-manifest.yaml", target_manifest)
    peer_profiles = sorted(str(path.relative_to(repo_root)) for path in (repo_root / "compliance" / "evidence" / "peer_profiles").glob("*.yaml"))
    for rel in peer_profiles:
        copied.append(_copy_rel_artifact(repo_root, rel, out_dir))
    manifest = {
        "schema_version": 1,
        "package": "tigrbl_auth",
        "version": _current_version(repo_root),
        "tier": int(tier),
        "profile": profile_name,
        "deployment": deployment.to_manifest(),
        "copied_artifacts": copied,
        "adr_index": adr_index,
        "clean_checkout": evidence_index.get("summary", {}).get("clean_checkout", {}),
        "claim_binding_summary": {
            "claim_count": evidence_index.get("summary", {}).get("claim_count", 0),
            "fapi_claim_count": evidence_index.get("summary", {}).get("fapi_claim_count", 0),
            "security_sensitive_claim_count": evidence_index.get("summary", {}).get("security_sensitive_claim_count", 0),
        },
        "documentation_policy": {
            "bundle_docs_policy": "generated-current-state-only",
            "historical_archive_root": "docs/archive/historical",
        },
    }
    _write_json(out_dir / "bundle-manifest.json", manifest)
    _write_yaml(out_dir / "bundle-manifest.yaml", manifest)
    return out_dir



def summarize_evidence_status(repo_root: Path, profile_label: str = "active") -> dict[str, Any]:
    repo_root = repo_root.resolve()
    deployment = _profile_deployment(profile_label)
    effective = build_effective_evidence_manifest(repo_root, deployment, profile_label=profile_label)
    missing_refs = effective.get("bundle_manifest", {}).get("missing_refs", [])
    peer_profile_dir = repo_root / "compliance" / "evidence" / "peer_profiles"
    executed_dir = repo_root / "compliance" / "evidence" / "tier4" / "executions"
    payload = {
        "passed": not missing_refs,
        "failures": [f"Missing evidence refs for target: {target}" for target in missing_refs],
        "warnings": [],
        "summary": {
            "profile": deployment.profile,
            "target_bundle_count": len(effective.get("bundle_manifest", {}).get("bundles", [])),
            "missing_ref_count": len(missing_refs),
            "peer_profile_count": len(list(peer_profile_dir.glob("*.yaml"))) if peer_profile_dir.exists() else 0,
            "peer_execution_count": len(list(executed_dir.glob("*.yaml"))) if executed_dir.exists() else 0,
        },
    }
    _write_report(repo_root / "docs" / "compliance", "evidence_status_report", payload, "Evidence Status Report")
    return payload




def execute_peer_profiles(
    repo_root: Path,
    deployment: Any,
    *,
    profiles: Iterable[str] | None = None,
    execution_mode: str = "self-check",
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    profile_dir = repo_root / "compliance" / "evidence" / "peer_profiles"
    counterpart_dir = repo_root / "compliance" / "evidence" / "peer_counterparts"
    execution_dir = repo_root / "compliance" / "evidence" / "tier4" / "executions"
    execution_dir.mkdir(parents=True, exist_ok=True)
    selected = set(profiles or [])
    external_root_env = os.environ.get("TIGRBL_AUTH_PEER_ARTIFACTS_ROOT")
    external_root = Path(external_root_env).resolve() if external_root_env else None
    failures: list[str] = []
    warnings: list[str] = []
    executed: list[str] = []

    scope = _load_yaml(repo_root / "compliance" / "targets" / "certification_scope.yaml")
    retained_targets = {
        str(entry.get("label"))
        for entry in scope.get("targets", [])
        if str(entry.get("scope_bucket")) != "out-of-scope/deferred"
    }
    target_to_peer = _load_yaml(repo_root / "compliance" / "mappings" / "target-to-peer-profile.yaml") or {}
    counterparts = {path.stem: _load_yaml(path) for path in sorted(counterpart_dir.glob("*.yaml"))}
    peer_profiles = {path.stem: _load_yaml(path) for path in sorted(profile_dir.glob("*.yaml"))}
    known_profiles = set(peer_profiles)
    known_counterparts = set(counterparts)

    required_counterpart_fields = {
        "schema_version",
        "id",
        "title",
        "counterpart_class",
        "execution_style",
        "independence_requirement",
        "attestation_class_required",
        "required_identity_fields",
        "required_container_fields",
        "required_artifacts",
    }
    for stem, counterpart in counterparts.items():
        missing = sorted(field for field in required_counterpart_fields if field not in counterpart)
        if missing:
            failures.append(f"Counterpart manifest missing required fields: {stem} -> {', '.join(missing)}")
        if str(counterpart.get("id", stem)) != stem:
            failures.append(f"Counterpart manifest id does not match filename: {stem}")
        if str(counterpart.get("attestation_class_required", "")).strip() != "independent-external":
            failures.append(f"Counterpart manifest must require independent-external attestation: {stem}")
        if not list(counterpart.get("required_identity_fields") or []):
            failures.append(f"Counterpart manifest missing required_identity_fields: {stem}")
        if not list(counterpart.get("required_container_fields") or []):
            failures.append(f"Counterpart manifest missing required_container_fields: {stem}")
        if not list(counterpart.get("required_artifacts") or []):
            failures.append(f"Counterpart manifest missing required_artifacts: {stem}")

    required_profile_fields = {
        "schema_version",
        "id",
        "title",
        "counterpart_id",
        "required_targets",
        "required_artifacts",
        "scenario_ids",
        "contract_profiles",
        "preferred_runtime_profile",
        "peer_verification_class",
    }
    allowed_contract_profiles = {"baseline", "production", "hardening", "fapi2-security", "peer-claim"}
    allowed_runtime_profiles = {"baseline", "production", "hardening", "fapi2-security"}
    profile_targets: dict[str, set[str]] = {}
    for stem, payload in peer_profiles.items():
        name = str(payload.get("id", stem))
        missing = sorted(field for field in required_profile_fields if field not in payload)
        if missing:
            failures.append(f"Peer profile missing required fields: {stem} -> {', '.join(missing)}")
        if name != stem:
            failures.append(f"Peer profile id does not match filename: {stem}")
        counterpart_id = str(payload.get("counterpart_id", "")).strip()
        if not counterpart_id:
            failures.append(f"Peer profile missing counterpart_id: {name}")
        elif counterpart_id not in known_counterparts:
            failures.append(f"Peer profile references unknown counterpart: {name} -> {counterpart_id}")
        if str(payload.get("peer_verification_class", "")).strip() != "external-independent":
            failures.append(f"Peer profile must declare peer_verification_class=external-independent: {name}")
        contract_profiles = [str(item) for item in payload.get("contract_profiles", [])]
        if not contract_profiles:
            failures.append(f"Peer profile missing contract_profiles: {name}")
        unknown_contract_profiles = sorted(set(contract_profiles) - allowed_contract_profiles)
        if unknown_contract_profiles:
            failures.append(f"Peer profile uses unknown contract_profiles: {name} -> {', '.join(unknown_contract_profiles)}")
        preferred_runtime_profile = str(payload.get("preferred_runtime_profile", deployment.profile))
        if preferred_runtime_profile not in allowed_runtime_profiles:
            failures.append(f"Peer profile uses unknown preferred_runtime_profile: {name} -> {preferred_runtime_profile}")
        scenario_ids = [str(item) for item in payload.get("scenario_ids", [])]
        if not scenario_ids:
            failures.append(f"Peer profile missing scenario_ids: {name}")
        elif len(set(scenario_ids)) != len(scenario_ids):
            failures.append(f"Peer profile has duplicate scenario_ids: {name}")
        required_targets = {str(item) for item in payload.get("required_targets", [])}
        profile_targets[name] = required_targets
        if not required_targets:
            failures.append(f"Peer profile missing required_targets: {name}")
        unknown_targets = sorted(required_targets - retained_targets)
        if unknown_targets:
            failures.append(f"Peer profile references unknown retained targets: {name} -> {', '.join(unknown_targets)}")
        scenario_target_map = payload.get("scenario_target_map") or {}
        unknown_scenarios = sorted(set(scenario_target_map) - set(scenario_ids))
        if unknown_scenarios:
            failures.append(f"Peer profile scenario_target_map references unknown scenarios: {name} -> {', '.join(unknown_scenarios)}")
        for scenario_id, targets in scenario_target_map.items():
            bad_targets = sorted({str(item) for item in (targets or [])} - required_targets)
            if bad_targets:
                failures.append(f"Peer profile scenario_target_map uses targets outside required_targets: {name}:{scenario_id} -> {', '.join(bad_targets)}")
        for rel in payload.get("required_artifacts", []) or []:
            if not (repo_root / str(rel)).exists():
                failures.append(f"Peer profile required_artifact missing on disk: {name} -> {rel}")

    missing_target_mappings = sorted(target for target in retained_targets if target not in target_to_peer)
    for target in missing_target_mappings:
        failures.append(f"Retained target lacks target-to-peer mapping: {target}")
    for target, mapped_profiles in (target_to_peer or {}).items():
        refs = [str(item) for item in (mapped_profiles or [])]
        if target in retained_targets and not refs:
            failures.append(f"Retained target has empty target-to-peer mapping: {target}")
        for profile_name in refs:
            if profile_name not in known_profiles:
                failures.append(f"Retained target maps to unknown peer profile: {target} -> {profile_name}")
            elif target in retained_targets and target not in profile_targets.get(profile_name, set()):
                failures.append(f"Retained target mapped to profile without corresponding required_target: {target} -> {profile_name}")
    for profile_name, required_targets in profile_targets.items():
        for target in required_targets:
            refs = {str(item) for item in target_to_peer.get(target, [])}
            if profile_name not in refs:
                failures.append(f"Peer profile required_target missing reverse mapping: {profile_name} -> {target}")

    for path in sorted(profile_dir.glob("*.yaml")):
        payload = _load_yaml(path)
        name = str(payload.get("id", path.stem))
        if selected and name not in selected:
            continue
        counterpart_id = str(payload.get("counterpart_id", "")).strip()
        counterpart = counterparts.get(counterpart_id, {})
        scenario_ids = [str(item) for item in payload.get("scenario_ids", [])]
        ext_dir = external_root / name if external_root else None
        external_available = bool(ext_dir and ext_dir.exists() and ext_dir.is_dir())
        if execution_mode == "external":
            status = "external-artifacts-detected" if external_available else "awaiting-external-artifacts"
        elif execution_mode == "planned":
            status = "planned"
        else:
            status = "internal-self-check-generated"
        execution = {
            "schema_version": 1,
            "profile": name,
            "execution_mode": execution_mode,
            "status": status,
            "deployment_profile": deployment.profile,
            "counterpart_id": counterpart_id,
            "counterpart_class": counterpart.get("counterpart_class"),
            "required_targets": payload.get("required_targets", []),
            "required_artifacts": payload.get("required_artifacts", []),
            "required_peer_artifacts": counterpart.get("required_artifacts", []),
            "required_identity_fields": counterpart.get("required_identity_fields", []),
            "required_container_fields": counterpart.get("required_container_fields", []),
            "scenario_ids": scenario_ids,
            "contract_profiles": payload.get("contract_profiles", []),
            "preferred_runtime_profile": payload.get("preferred_runtime_profile", deployment.profile),
            "peer_verification_class": payload.get("peer_verification_class"),
            "attestation_class_required": counterpart.get("attestation_class_required"),
            "external_artifacts_root": str(ext_dir.relative_to(repo_root)) if external_available and ext_dir is not None and ext_dir.is_relative_to(repo_root) else (str(ext_dir) if external_available and ext_dir is not None else None),
            "independent_peer_validation": execution_mode == "external" and external_available,
            "notes": (
                "External peer artifacts were detected for normalization into preserved Tier 4 bundles."
                if execution_mode == "external" and external_available
                else "Independent external peer artifacts are still required for Tier 4 claims."
            ),
        }
        _write_yaml(execution_dir / f"{name}.{deployment.profile}.yaml", execution)
        executed.append(name)
    if selected:
        for name in selected - known_profiles:
            failures.append(f"Unknown peer profile: {name}")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": warnings,
        "summary": {
            "deployment_profile": deployment.profile,
            "execution_mode": execution_mode,
            "executed_profile_count": len(executed),
            "peer_profile_count": len(peer_profiles),
            "counterpart_catalog_count": len(counterparts),
            "retained_target_count": len(retained_targets),
            "mapped_retained_target_count": len([target for target in retained_targets if target in target_to_peer]),
            "retained_target_coverage_complete": not missing_target_mappings,
            "external_artifact_root": str(external_root) if external_root else None,
        },
        "details": executed,
    }
    _write_report(repo_root / "docs" / "compliance", "peer_profile_execution_report", payload, "Peer Profile Execution Report")
    return payload


def _run_release_signing_gate(repo_root: Path) -> int:
    repo_root = repo_root.resolve()
    profiles = ("baseline", "production", "hardening", "fapi2-security", "peer-claim")
    failures: list[str] = []
    details: list[dict[str, Any]] = []
    shared_signer = load_signer(signing_key=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY"), signer_id=os.environ.get("TIGRBL_AUTH_RELEASE_SIGNER_ID"))
    shared_signing_key = shared_signer.private_key_pem()
    for profile in profiles:
        deployment = deployment_from_options(profile=profile)
        bundle = build_release_bundle(repo_root, deployment, require_clean_checkout=True)
        signed = sign_release_bundle(bundle, signing_key=shared_signing_key, signer_id=shared_signer.identity.signer_id)
        verified = verify_release_bundle_signatures(bundle)
        passed = bool(signed.get("verification", {}).get("passed", False)) and bool(verified.get("passed", False))
        details.append({
            "profile": profile,
            "bundle_dir": str(bundle.relative_to(repo_root)),
            "signed": signed.get("status"),
            "verified": bool(verified.get("passed", False)),
            "signing_key_id": signed.get("signer", {}).get("key_id"),
        })
        if not passed:
            failures.append(f"Release signing verification failed for profile: {profile}")
    payload = {
        "passed": not failures,
        "failures": failures,
        "warnings": [],
        "summary": {
            "profile_count": len(profiles),
            "signed_bundle_count": len(details),
        },
        "details": details,
    }
    _write_report(repo_root / "docs" / "compliance", "release_signing_report", payload, "Release Signing Report")
    return 0 if payload["passed"] else 1
