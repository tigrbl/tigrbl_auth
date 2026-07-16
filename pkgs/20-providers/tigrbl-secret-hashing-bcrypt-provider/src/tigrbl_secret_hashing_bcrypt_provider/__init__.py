"""Bcrypt shared-secret hashing and verification provider."""

from __future__ import annotations

import bcrypt

from tigrbl_identity_contracts.shared_secrets import (
    EncodedSecretHash,
    SecretHash,
    SecretHashPolicy,
    SecretVerificationResult,
)


class BcryptSecretHasher:
    algorithm = "bcrypt"

    def __init__(self, *, rounds: int = 12, maximum_input_bytes: int = 72) -> None:
        if rounds < 4 or rounds > 31:
            raise ValueError("bcrypt rounds must be between 4 and 31")
        if maximum_input_bytes <= 0 or maximum_input_bytes > 72:
            raise ValueError("bcrypt maximum input bytes must be between 1 and 72")
        self.policy = SecretHashPolicy(
            algorithm=self.algorithm,
            work_factor=rounds,
            maximum_input_bytes=maximum_input_bytes,
        )

    def _presented_bytes(self, presented: str | bytes) -> bytes:
        value = presented.encode("utf-8") if isinstance(presented, str) else bytes(presented)
        maximum = self.policy.maximum_input_bytes
        if maximum is not None and len(value) > maximum:
            raise ValueError(f"shared secret exceeds bcrypt's {maximum}-byte limit")
        if not value:
            raise ValueError("shared secret is required")
        return value

    @staticmethod
    def _encoded_bytes(expected: SecretHash | EncodedSecretHash | None) -> bytes | None:
        if expected is None:
            return None
        value = expected.encoded if isinstance(expected, SecretHash) else expected
        return value.encode("utf-8") if isinstance(value, str) else bytes(value)

    def hash_secret(self, presented: str | bytes, /) -> SecretHash:
        encoded = bcrypt.hashpw(
            self._presented_bytes(presented),
            bcrypt.gensalt(rounds=self.policy.work_factor),
        )
        return SecretHash(encoded=encoded, algorithm=self.algorithm)

    def verify_secret(
        self,
        presented: str | bytes,
        expected: SecretHash | EncodedSecretHash | None,
        /,
    ) -> SecretVerificationResult:
        encoded = self._encoded_bytes(expected)
        if encoded is None:
            return SecretVerificationResult(False)
        try:
            verified = bcrypt.checkpw(self._presented_bytes(presented), encoded)
            rounds = int(encoded.split(b"$", 3)[2])
        except (TypeError, ValueError, IndexError):
            return SecretVerificationResult(False)
        return SecretVerificationResult(
            verified=verified,
            algorithm=self.algorithm,
            needs_rehash=verified and rounds != self.policy.work_factor,
        )


def _legacy_bcrypt_bytes(plain: str) -> bytes:
    value = plain.encode("utf-8")
    return value[:72]


def hash_pw(plain: str) -> bytes:
    """Deprecated bytes-oriented bcrypt compatibility helper."""

    return bcrypt.hashpw(_legacy_bcrypt_bytes(plain), bcrypt.gensalt(12))


def verify_pw(plain: str, hashed: bytes | None) -> bool:
    """Deprecated bytes-oriented bcrypt compatibility helper."""

    if hashed is None:
        return False
    try:
        return bcrypt.checkpw(_legacy_bcrypt_bytes(plain), hashed)
    except (TypeError, ValueError):
        return False


__all__ = ["BcryptSecretHasher", "hash_pw", "verify_pw"]
