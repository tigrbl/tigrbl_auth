"""PBKDF2-SHA256 shared-secret hashing for existing TBA consumer records."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

from tba_contracts_identity.shared_secrets import (
    EncodedSecretHash,
    SecretHash,
    SecretHashPolicy,
    SecretVerificationResult,
)


class Pbkdf2SecretHasher:
    """Use the padded base64url representation shared by existing consumers."""

    algorithm = "pbkdf2_sha256"

    def __init__(self, *, rounds: int = 310_000) -> None:
        if rounds < 1:
            raise ValueError("PBKDF2 rounds must be positive")
        self.policy = SecretHashPolicy(algorithm=self.algorithm, work_factor=rounds)

    def hash_secret(
        self, presented: str | bytes, /, *, salt: bytes | None = None
    ) -> SecretHash:
        if salt is None:
            salt = secrets.token_bytes(16)
        elif not salt:
            raise ValueError("PBKDF2 salt must be nonempty")
        rounds = self.policy.work_factor
        digest = _derive(presented, salt, rounds)
        salt_text = base64.urlsafe_b64encode(salt).decode("ascii")
        digest_text = base64.urlsafe_b64encode(digest).decode("ascii")
        return SecretHash(
            encoded=f"{self.algorithm}${rounds}${salt_text}${digest_text}",
            algorithm=self.algorithm,
        )

    def verify_secret(
        self,
        presented: str | bytes,
        expected: SecretHash | EncodedSecretHash | None,
        /,
    ) -> SecretVerificationResult:
        encoded = expected.encoded if isinstance(expected, SecretHash) else expected
        if encoded is None:
            return SecretVerificationResult(False)
        try:
            if isinstance(encoded, bytes):
                encoded = encoded.decode("ascii")
            algorithm, rounds_text, salt_text, digest_text = encoded.split("$", 3)
            if algorithm != self.algorithm or len(digest_text) != 44:
                return SecretVerificationResult(False)
            rounds = int(rounds_text)
            salt = base64.b64decode(salt_text, altchars=b"-_", validate=True)
            if not salt:
                return SecretVerificationResult(False)
            digest = base64.urlsafe_b64encode(_derive(presented, salt, rounds))
            verified = hmac.compare_digest(digest, digest_text.encode("ascii"))
        except (AttributeError, OverflowError, TypeError, ValueError):
            return SecretVerificationResult(False)
        return SecretVerificationResult(
            verified=verified,
            algorithm=self.algorithm,
            needs_rehash=verified and rounds < self.policy.work_factor,
        )


def _derive(presented: str | bytes, salt: bytes, rounds: int) -> bytes:
    secret = presented.encode("utf-8") if isinstance(presented, str) else presented
    return hashlib.pbkdf2_hmac("sha256", secret, salt, rounds)


__all__ = ["Pbkdf2SecretHasher"]
