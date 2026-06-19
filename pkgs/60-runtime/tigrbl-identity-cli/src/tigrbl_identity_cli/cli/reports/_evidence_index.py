from __future__ import annotations

def sign_release_bundle(
    bundle_root: Path,
    *,
    signing_key: str | None = None,
    signer_id: str | None = None,
) -> dict[str, Any]:
    bundle_root = bundle_root.resolve()
    manifest_path = bundle_root / "release-bundle.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"release bundle not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    package = str(manifest.get("package", "tigrbl_auth"))
    version = str(manifest.get("version", _current_version(bundle_root.parents[3] if len(bundle_root.parents) >= 4 else bundle_root)))
    profile = str(manifest.get("profile", bundle_root.name))
    attest_root = bundle_root / "attestations"
    if attest_root.exists():
        shutil.rmtree(attest_root)
    attest_root.mkdir(parents=True, exist_ok=True)
    signer = load_signer(signing_key=signing_key or os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY"), signer_id=signer_id)
    verification_refs = write_public_key_artifacts(bundle_root, signer)

    contract_manifest = build_contract_set_manifest(bundle_root)
    contract_manifest_rel = "attestations/contract-set.manifest.json"
    _write_json(bundle_root / contract_manifest_rel, contract_manifest)

    signed_artifacts: list[dict[str, Any]] = []
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="release-bundle",
            artifact_rel_path="release-bundle.json",
            package=package,
            version=version,
            profile=profile,
            artifact_kind="release-bundle-manifest",
            media_type="application/json",
        )
    )
    claim_rel = next((item.get("path") for item in manifest.get("artifacts", []) if str(item.get("path", "")).startswith("compliance/claims/effective-target-claims.")), None)
    if not claim_rel:
        raise ValueError("release bundle is missing an effective claim manifest")
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="claim-manifest",
            artifact_rel_path=str(claim_rel),
            package=package,
            version=version,
            profile=profile,
            artifact_kind="claim-manifest",
            media_type=_artifact_media_type(str(claim_rel)),
        )
    )
    evidence_rel = next((item.get("path") for item in manifest.get("artifacts", []) if str(item.get("path", "")).startswith("compliance/evidence/effective-release-evidence.")), None)
    if not evidence_rel:
        raise ValueError("release bundle is missing an effective evidence manifest")
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="evidence-manifest",
            artifact_rel_path=str(evidence_rel),
            package=package,
            version=version,
            profile=profile,
            artifact_kind="evidence-manifest",
            media_type=_artifact_media_type(str(evidence_rel)),
        )
    )
    signed_artifacts.append(
        write_artifact_attestation(
            bundle_root,
            signer=signer,
            label="contract-set",
            artifact_rel_path=contract_manifest_rel,
            package=package,
            version=version,
            profile=profile,
            artifact_kind="contract-set-manifest",
            media_type="application/json",
        )
    )
    release_attestation = write_bundle_attestation(
        bundle_root,
        signer=signer,
        package=package,
        version=version,
        profile=profile,
        signed_artifacts=signed_artifacts,
    )
    result = {
        "status": "signed-ed25519-attested",
        "algorithm": "Ed25519",
        "package": package,
        "version": version,
        "profile": profile,
        "signer": signer.identity.to_manifest(),
        "verification_material": verification_refs,
        "release_attestation": release_attestation["attestation_path"],
        "signed_artifacts": signed_artifacts,
        "verification": {"passed": False, "failures": ["verification pending"], "warnings": [], "details": {}},
    }
    _write_json(bundle_root / "signature.json", result)
    verification = verify_bundle_attestations(bundle_root).to_manifest()
    result["verification"] = verification
    _write_json(bundle_root / "signature.json", result)
    return result


def verify_release_bundle_signatures(bundle_root: Path) -> dict[str, Any]:
    bundle_root = bundle_root.resolve()
    result = verify_bundle_attestations(bundle_root)
    payload = result.to_manifest()
    _write_report(
        bundle_root,
        "verification",
        payload,
        "Release Signing Verification Report",
    )
    return payload


def run_recertification(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    watched_paths = [
        repo_root / "pyproject.toml",
        repo_root / "docker" / "Dockerfile",
        repo_root / "compliance" / "targets" / "boundaries.yaml",
        repo_root / "compliance" / "targets" / "boundary-decisions.yaml",
        repo_root / "compliance" / "targets" / "rfc-targets.yaml",
        repo_root / "compliance" / "targets" / "oidc-targets.yaml",
        repo_root / "constraints" / "runner-uvicorn.txt",
        repo_root / "constraints" / "runner-hypercorn.txt",
        repo_root / "constraints" / "runner-tigrcorn.txt",
        repo_root / "uv.lock",
        repo_root / "docs" / "runbooks" / "INSTALLATION_PROFILES.md",
        repo_root / "docs" / "runbooks" / "CLEAN_CHECKOUT_REPRO.md",
        repo_root / ".github" / "workflows" / "ci-install-profiles.yml",
    ]
    joined = b""
    for path in watched_paths:
        if path.exists():
            joined += path.read_bytes()
    fingerprint = _hash_bytes(joined)
    state_path = repo_root / "compliance" / "claims" / "recertification-state.yaml"
    previous = _load_yaml(state_path).get("fingerprint") if state_path.exists() else None
    changed = previous is not None and previous != fingerprint
    state = {
        "schema_version": 1,
        "fingerprint": fingerprint,
        "previous_fingerprint": previous,
        "changed_since_last_run": changed,
        "version": _current_version(repo_root),
        "watched_dependency_artifact_count": len([path for path in watched_paths if path.exists()]),
    }
    _write_yaml(state_path, state)
    payload = {
        "passed": True,
        "failures": [],
        "warnings": ["Boundary, dependency, or reproducibility inputs changed; recertification review required."] if changed else [],
        "summary": state,
    }
    _write_report(repo_root / "docs" / "compliance", "recertification_report", payload, "Recertification Report")
    return payload


__all__ = [
    "build_adr_index",
    "build_evidence_bundle",
    "build_release_bundle",
    "diff_contracts",
    "execute_peer_profiles",
    "generate_state_reports",
    "load_validated_execution_status",
    "run_final_release_readiness_gate",
    "run_release_gates",
    "run_test_execution_gate",
    "run_recertification",
    "sign_release_bundle",
    "verify_release_bundle_signatures",
    "verify_peer_bundle_completeness",
    "summarize_evidence_status",
    "validate_openapi_contract",
    "validate_openrpc_contract",
    "verify_test_classification",
]
