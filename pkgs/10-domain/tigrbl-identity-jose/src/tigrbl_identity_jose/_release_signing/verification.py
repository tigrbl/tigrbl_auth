from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from .models import VerificationResult
from .utils import _b64url_decode, _canonical_json, sha256_bytes, sha256_file, sha256_text


def verify_statement(statement: dict[str, Any], *, public_key_pem: str | None = None) -> VerificationResult:
    failures: list[str] = []
    warnings: list[str] = []
    payload = statement.get("payload") if isinstance(statement, dict) else None
    signature_block = statement.get("signature") if isinstance(statement, dict) else None
    if not isinstance(payload, dict):
        failures.append("Statement missing payload object")
        return VerificationResult(False, failures, warnings, {})
    if not isinstance(signature_block, dict):
        failures.append("Statement missing signature block")
        return VerificationResult(False, failures, warnings, {})
    signer = payload.get("signer") if isinstance(payload.get("signer"), dict) else {}
    pem = public_key_pem or signer.get("public_key_pem")
    if not isinstance(pem, str) or not pem.strip():
        failures.append("Statement missing public key PEM")
        return VerificationResult(False, failures, warnings, {})
    key = load_pem_public_key(pem.encode("utf-8"))
    if not isinstance(key, Ed25519PublicKey):
        failures.append("Statement public key is not Ed25519")
        return VerificationResult(False, failures, warnings, {})
    sig_value = signature_block.get("value")
    if not isinstance(sig_value, str) or not sig_value:
        failures.append("Statement signature value is missing")
        return VerificationResult(False, failures, warnings, {})
    try:
        key.verify(_b64url_decode(sig_value), _canonical_json(payload))
    except Exception as exc:  # noqa: BLE001
        failures.append(f"Signature verification failed: {exc}")
        return VerificationResult(False, failures, warnings, {})
    payload_sha = signature_block.get("payload_sha256")
    actual_sha = sha256_bytes(_canonical_json(payload))
    if payload_sha != actual_sha:
        failures.append("Statement payload digest does not match signature block")
    embedded_sha = signer.get("public_key_sha256")
    if embedded_sha and embedded_sha != sha256_text(pem):
        failures.append("Embedded public key SHA-256 does not match public key PEM")
    details = {
        "statement_type": payload.get("statement_type"),
        "artifact_label": payload.get("subject", {}).get("artifact_label") if isinstance(payload.get("subject"), dict) else None,
        "key_id": signer.get("key_id"),
        "issued_at": payload.get("issued_at"),
    }
    return VerificationResult(not failures, failures, warnings, details)


def verify_bundle_attestations(bundle_root: Path) -> VerificationResult:
    bundle_root = bundle_root.resolve()
    failures: list[str] = []
    warnings: list[str] = []
    attest_root = bundle_root / "attestations"
    if not attest_root.exists():
        failures.append("Missing attestations directory")
        return VerificationResult(False, failures, warnings, {})
    summary_path = bundle_root / "signature.json"
    if not summary_path.exists():
        failures.append("Missing signature.json summary")
        return VerificationResult(False, failures, warnings, {})
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    signed_artifacts = summary.get("signed_artifacts", [])
    if not isinstance(signed_artifacts, list) or not signed_artifacts:
        failures.append("signature.json does not list signed artifacts")
        return VerificationResult(False, failures, warnings, {})
    verified_labels: list[str] = []
    key_ids: set[str] = set()
    for item in signed_artifacts:
        label = str(item.get("label"))
        artifact_rel_path = str(item.get("artifact_path"))
        attestation_rel_path = str(item.get("attestation_path"))
        artifact_path = bundle_root / artifact_rel_path
        attestation_path = bundle_root / attestation_rel_path
        if not artifact_path.exists():
            failures.append(f"Signed artifact missing: {artifact_rel_path}")
            continue
        if not attestation_path.exists():
            failures.append(f"Attestation missing for {label}: {attestation_rel_path}")
            continue
        statement = json.loads(attestation_path.read_text(encoding="utf-8"))
        result = verify_statement(statement)
        failures.extend(result.failures)
        warnings.extend(result.warnings)
        if not result.passed:
            continue
        payload = statement["payload"]
        subject = payload.get("subject", {}) if isinstance(payload.get("subject"), dict) else {}
        if subject.get("artifact_sha256") != sha256_file(artifact_path):
            failures.append(f"Artifact digest mismatch for {label}: {artifact_rel_path}")
            continue
        if subject.get("artifact_path") != artifact_rel_path:
            failures.append(f"Artifact path mismatch for {label}: {artifact_rel_path}")
            continue
        signer = payload.get("signer", {}) if isinstance(payload.get("signer"), dict) else {}
        if signer.get("key_id"):
            key_ids.add(str(signer.get("key_id")))
        verified_labels.append(label)
    release_attestation_path = attest_root / "release-attestation.json"
    if not release_attestation_path.exists():
        failures.append("Missing release-attestation.json")
    else:
        bundle_statement = json.loads(release_attestation_path.read_text(encoding="utf-8"))
        result = verify_statement(bundle_statement)
        failures.extend(result.failures)
        warnings.extend(result.warnings)
        if result.passed:
            subject = bundle_statement["payload"].get("subject", {})
            bundle_items = subject.get("signed_artifacts", []) if isinstance(subject, dict) else []
            if len(bundle_items) != len(signed_artifacts):
                failures.append("Release attestation signed_artifacts count does not match signature.json")
            for item in bundle_items:
                label = str(item.get("label"))
                if label not in verified_labels:
                    failures.append(f"Release attestation references unverified artifact: {label}")
            signer = bundle_statement["payload"].get("signer", {})
            if isinstance(signer, dict) and signer.get("key_id"):
                key_ids.add(str(signer.get("key_id")))
    if len(key_ids) > 1:
        failures.append("Multiple signing identities were used within one release bundle")
    details = {
        "bundle_root": str(bundle_root),
        "verified_artifact_count": len(verified_labels),
        "signing_key_id": sorted(key_ids)[0] if len(key_ids) == 1 else None,
        "artifact_labels": verified_labels,
    }
    return VerificationResult(not failures, failures, warnings, details)
