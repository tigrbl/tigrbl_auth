from __future__ import annotations

import base64
import hashlib
import re
import secrets
from dataclasses import dataclass
from typing import Final, Mapping


PKCE_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc7636"
PKCE_CHALLENGE_METHOD: Final = "S256"
_VERIFIER_CHARS: Final = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
_VERIFIER_RE: Final = re.compile(r"^[A-Za-z0-9\-._~]{43,128}$")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_pkce_verifier(length: int = 64) -> str:
    if not 43 <= length <= 128:
        raise ValueError("PKCE verifier length must be between 43 and 128 characters")
    return "".join(secrets.choice(_VERIFIER_CHARS) for _ in range(length))


def validate_pkce_verifier(verifier: str) -> str:
    value = str(verifier)
    if not _VERIFIER_RE.fullmatch(value):
        raise ValueError("invalid PKCE code_verifier")
    return value


def pkce_s256_challenge(verifier: str) -> str:
    if not verifier:
        raise ValueError("PKCE verifier is required")
    return _b64url(hashlib.sha256(str(verifier).encode("ascii")).digest())


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
