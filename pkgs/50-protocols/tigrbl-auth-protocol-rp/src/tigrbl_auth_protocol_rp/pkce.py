from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from tigrbl_security_proof_pkce import (
    PKCE_CHALLENGE_METHOD,
    PKCE_SPEC_URL,
    make_pkce_verifier,
    pkce_s256_challenge,
    validate_pkce_verifier,
)


@dataclass(frozen=True, slots=True)
class PkceVerifier:
    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", validate_pkce_verifier(self.value))

    @classmethod
    def generate(cls, length: int = 64) -> "PkceVerifier":
        return cls(make_pkce_verifier(length))

    @property
    def code_challenge(self) -> str:
        return pkce_s256_challenge(self.value)

    @property
    def code_challenge_method(self) -> str:
        return PKCE_CHALLENGE_METHOD

    def authorization_params(self) -> Mapping[str, str]:
        return {
            "code_challenge": self.code_challenge,
            "code_challenge_method": self.code_challenge_method,
        }


__all__ = [
    "PKCE_CHALLENGE_METHOD",
    "PKCE_SPEC_URL",
    "PkceVerifier",
    "make_pkce_verifier",
    "pkce_s256_challenge",
    "validate_pkce_verifier",
]
