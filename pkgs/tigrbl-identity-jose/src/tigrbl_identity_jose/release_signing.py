from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
    load_pem_public_key,
)

STATEMENT_VERSION = 1
STATEMENT_TYPE_ARTIFACT = "https://tigrbl.dev/attestations/release-artifact/v1"
STATEMENT_TYPE_BUNDLE = "https://tigrbl.dev/attestations/release-bundle/v1"
DEFAULT_SIGNER_ID = "tigrbl_auth.checkpoint.attestor"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _canonical_json(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(text: str) -> bytes:
    padding = "=" * ((4 - len(text) % 4) % 4)
    return base64.urlsafe_b64decode((text + padding).encode("ascii"))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(payload: str) -> str:
    return sha256_bytes(payload.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


@dataclass(slots=True)
class SignerIdentity:
    signer_id: str
    key_id: str
    public_key_pem: str
    public_key_sha256: str
    source: str
    algorithm: str = "Ed25519"
    identity_kind: str = "repository-release-attestor"

    def to_manifest(self) -> dict[str, Any]:
        return {
            "signer_id": self.signer_id,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
            "identity_kind": self.identity_kind,
            "public_key_pem": self.public_key_pem,
            "public_key_sha256": self.public_key_sha256,
            "source": self.source,
        }


@dataclass(slots=True)
class LoadedSigner:
    private_key: Ed25519PrivateKey
    identity: SignerIdentity

    def private_key_pem(self) -> str:
        return self.private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()).decode("utf-8")

    def sign_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        raw = _canonical_json(payload)
        signature = self.private_key.sign(raw)
        return {
            "algorithm": self.identity.algorithm,
            "encoding": "base64url",
            "value": _b64url_encode(signature),
            "payload_sha256": sha256_bytes(raw),
        }

    def sign_statement(self, statement_type: str, subject: dict[str, Any], *, issued_at: str | None = None) -> dict[str, Any]:
        payload = {
            "schema_version": STATEMENT_VERSION,
            "statement_type": statement_type,
            "issued_at": issued_at or _utc_now(),
            "signer": self.identity.to_manifest(),
            "subject": subject,
        }
        return {
            "schema_version": STATEMENT_VERSION,
            "payload": payload,
            "signature": self.sign_payload(payload),
        }


@dataclass(slots=True)
class VerificationResult:
    passed: bool
    failures: list[str]
    warnings: list[str]
    details: dict[str, Any]

    def to_manifest(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "failures": list(self.failures),
            "warnings": list(self.warnings),
            "details": dict(self.details),
        }


def _public_key_manifest(private_key: Ed25519PrivateKey, *, signer_id: str, source: str) -> SignerIdentity:
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo).decode("utf-8")
    public_sha = sha256_text(public_pem)
    key_id = f"ed25519:{public_sha[:24]}"
    return SignerIdentity(
        signer_id=signer_id,
        key_id=key_id,
        public_key_pem=public_pem,
        public_key_sha256=public_sha,
        source=source,
    )


def _load_private_key_from_pem(pem: str) -> Ed25519PrivateKey:
    key = load_pem_private_key(pem.encode("utf-8"), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("release signing key must be an Ed25519 private key")
    return key


def _private_key_from_material(signing_key: str | None) -> tuple[Ed25519PrivateKey, str]:
    env_file = os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY_FILE")
    env_pem = os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_KEY_PEM")
    env_seed = os.environ.get("TIGRBL_AUTH_RELEASE_SIGNING_SEED")
    material = signing_key or env_pem
    if env_file and not signing_key and not env_pem:
        pem = Path(env_file).read_text(encoding="utf-8")
        return _load_private_key_from_pem(pem), f"file:{env_file}"
    if material:
        if "BEGIN PRIVATE KEY" in material:
            return _load_private_key_from_pem(material), "inline-pem"
        maybe_path = Path(material)
        if maybe_path.exists() and maybe_path.is_file():
            pem = maybe_path.read_text(encoding="utf-8")
            return _load_private_key_from_pem(pem), f"file:{maybe_path}"
        seed = hashlib.sha256(material.encode("utf-8")).digest()
        return Ed25519PrivateKey.from_private_bytes(seed), "derived-inline-secret"
    if env_seed:
        seed = hashlib.sha256(env_seed.encode("utf-8")).digest()
        return Ed25519PrivateKey.from_private_bytes(seed), "derived-env-seed"
    return Ed25519PrivateKey.generate(), "generated-ephemeral-checkpoint-key"


def load_signer(*, signing_key: str | None = None, signer_id: str | None = None) -> LoadedSigner:
    private_key, source = _private_key_from_material(signing_key)
    identity = _public_key_manifest(private_key, signer_id=signer_id or os.environ.get("TIGRBL_AUTH_RELEASE_SIGNER_ID", DEFAULT_SIGNER_ID), source=source)
    return LoadedSigner(private_key=private_key, identity=identity)


def write_public_key_artifacts(bundle_root: Path, signer: LoadedSigner) -> dict[str, str]:
    attest_root = bundle_root / "attestations"
    key_dir = attest_root / "keys"
    key_dir.mkdir(parents=True, exist_ok=True)
    public_key_path = key_dir / f"{signer.identity.key_id.replace(':', '-')}.pub.pem"
    public_key_path.write_text(signer.identity.public_key_pem, encoding="utf-8")
    signer_identity_path = attest_root / "signer-identity.json"
    signer_identity_path.write_text(json.dumps(signer.identity.to_manifest(), indent=2) + "\n", encoding="utf-8")
    return {
        "public_key_path": str(public_key_path.relative_to(bundle_root)).replace("\\", "/"),
        "signer_identity_path": str(signer_identity_path.relative_to(bundle_root)).replace("\\", "/"),
    }


def build_contract_set_manifest(bundle_root: Path) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for path in sorted((bundle_root / "specs").rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(bundle_root)).replace("\\", "/")
        entries.append({
            "path": rel,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        })
    return {
        "schema_version": STATEMENT_VERSION,
        "kind": "contract-set",
        "contract_count": len(entries),
        "contracts": entries,
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_attestation(path: Path, attestation: dict[str, Any]) -> None:
    _write_json(path, attestation)


def _artifact_subject(
    *,
    label: str,
    artifact_path: str,
    artifact_sha256: str,
    package: str,
    version: str,
    profile: str,
    artifact_kind: str,
    media_type: str,
) -> dict[str, Any]:
    return {
        "package": package,
        "version": version,
        "profile": profile,
        "artifact_label": label,
        "artifact_kind": artifact_kind,
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "media_type": media_type,
    }


def write_artifact_attestation(
    bundle_root: Path,
    *,
    signer: LoadedSigner,
    label: str,
    artifact_rel_path: str,
    package: str,
    version: str,
    profile: str,
    artifact_kind: str,
    media_type: str,
) -> dict[str, Any]:
    artifact_path = bundle_root / artifact_rel_path
    subject = _artifact_subject(
        label=label,
        artifact_path=artifact_rel_path,
        artifact_sha256=sha256_file(artifact_path),
        package=package,
        version=version,
        profile=profile,
        artifact_kind=artifact_kind,
        media_type=media_type,
    )
    statement = signer.sign_statement(STATEMENT_TYPE_ARTIFACT, subject)
    attestation_path = bundle_root / "attestations" / f"{label}.attestation.json"
    write_attestation(attestation_path, statement)
    return {
        "label": label,
        "artifact_path": artifact_rel_path,
        "artifact_sha256": subject["artifact_sha256"],
        "attestation_path": str(attestation_path.relative_to(bundle_root)).replace("\\", "/"),
    }


def write_bundle_attestation(
    bundle_root: Path,
    *,
    signer: LoadedSigner,
    package: str,
    version: str,
    profile: str,
    signed_artifacts: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    subject = {
        "package": package,
        "version": version,
        "profile": profile,
        "bundle_root": str(bundle_root.name),
        "signed_artifacts": list(signed_artifacts),
    }
    statement = signer.sign_statement(STATEMENT_TYPE_BUNDLE, subject)
    attestation_path = bundle_root / "attestations" / "release-attestation.json"
    write_attestation(attestation_path, statement)
    return {
        "attestation_path": str(attestation_path.relative_to(bundle_root)).replace("\\", "/"),
        "statement": statement,
    }


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


__all__ = [
    "DEFAULT_SIGNER_ID",
    "LoadedSigner",
    "SignerIdentity",
    "VerificationResult",
    "build_contract_set_manifest",
    "load_signer",
    "sha256_bytes",
    "sha256_file",
    "verify_bundle_attestations",
    "verify_statement",
    "write_artifact_attestation",
    "write_attestation",
    "write_bundle_attestation",
    "write_public_key_artifacts",
]
