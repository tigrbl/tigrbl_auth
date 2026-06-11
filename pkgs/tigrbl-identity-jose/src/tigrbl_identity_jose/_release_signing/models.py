from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat

from .utils import STATEMENT_VERSION, _b64url_encode, _canonical_json, _utc_now, sha256_bytes


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
