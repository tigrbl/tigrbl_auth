from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PQCSignatureKeyPair:
    algorithm: str
    public_key: bytes
    secret_key: bytes
    library: str = "pqcrypto"


__all__ = ["PQCSignatureKeyPair"]
