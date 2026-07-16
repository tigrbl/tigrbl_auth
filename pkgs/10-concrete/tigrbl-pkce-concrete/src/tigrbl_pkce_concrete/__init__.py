from __future__ import annotations

import base64
import hashlib
import re
import secrets
from dataclasses import dataclass
from hmac import compare_digest
from typing import Any, Final, Mapping

from tigrbl_proof_of_possession_bases import (
    PkceVerifierBase,
    ProofOfPossessionDomainBase,
)
from tigrbl_security_trust_contracts import (
    Artifact,
    CapabilityMap,
    IssueRequest,
    VerificationResult,
    VerifyRequest,
)

PKCE_SPEC_URL: Final = "https://www.rfc-editor.org/rfc/rfc7636"
PKCE_CHALLENGE_METHOD: Final = "S256"
PKCE_VERIFIER_CHARS: Final = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
PKCE_VERIFIER_RE: Final = re.compile(r"^[A-Za-z0-9\-._~]{43,128}$")


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def make_pkce_verifier(length: int = 64) -> str:
    if not 43 <= length <= 128:
        raise ValueError("PKCE verifier length must be between 43 and 128 characters")
    return "".join(secrets.choice(PKCE_VERIFIER_CHARS) for _ in range(length))


def validate_pkce_verifier(verifier: str) -> str:
    value = str(verifier)
    if not PKCE_VERIFIER_RE.fullmatch(value):
        raise ValueError("invalid PKCE code_verifier")
    return value


def pkce_s256_challenge(verifier: str) -> str:
    if not verifier:
        raise ValueError("PKCE verifier is required")
    return b64url(hashlib.sha256(str(verifier).encode("ascii")).digest())


def verify_pkce_s256_challenge(
    verifier: str,
    challenge: str,
    *,
    enabled: bool = True,
    validate_verifier: bool = True,
) -> bool:
    if not enabled:
        return True
    try:
        value = validate_pkce_verifier(verifier) if validate_verifier else str(verifier)
        expected = pkce_s256_challenge(value)
    except (UnicodeEncodeError, ValueError):
        return False
    return compare_digest(expected, str(challenge))


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


class PkceProofProvider(PkceVerifierBase, ProofOfPossessionDomainBase):
    """Compatibility implementation of the PKCE proof-domain bases."""

    def supports(self) -> CapabilityMap:
        return CapabilityMap(
            ops={"issue": (PKCE_CHALLENGE_METHOD,), "verify": (PKCE_CHALLENGE_METHOD,)},
            algs=(PKCE_CHALLENGE_METHOD,),
            modes=("pkce",),
            features=("rfc7636", "proof-key", "code-challenge"),
        )

    def verify_challenge(self, *, verifier: str, challenge: str) -> bool:
        return verify_pkce_s256_challenge(verifier, challenge)

    async def issue(self, request: IssueRequest) -> Artifact:
        verifier = make_pkce_verifier(int(request.opts.get("length", 64)))
        challenge = pkce_s256_challenge(verifier)
        return Artifact(
            kind="pkce",
            format="oauth-parameters",
            structured={
                "code_verifier": verifier,
                "code_challenge": challenge,
                "code_challenge_method": PKCE_CHALLENGE_METHOD,
            },
            meta={"spec": PKCE_SPEC_URL},
        )

    async def verify(self, request: VerifyRequest) -> VerificationResult:
        verifier = _select_text(
            request.context, "code_verifier", fallback=request.payload
        )
        challenge = _select_text(
            request.context,
            "code_challenge",
            fallback=_artifact_challenge(request.artifact),
        )
        valid = verify_pkce_s256_challenge(
            verifier,
            challenge,
            enabled=bool(request.policy.get("enabled", True)),
            validate_verifier=bool(request.policy.get("validate_verifier", True)),
        )
        return VerificationResult(
            valid=valid,
            reason=None if valid else "PKCE code challenge mismatch",
            claims={
                "code_challenge": challenge,
                "code_challenge_method": PKCE_CHALLENGE_METHOD,
            },
            meta={"method": PKCE_CHALLENGE_METHOD, "spec": PKCE_SPEC_URL},
        )


def _select_text(
    values: Mapping[str, Any], key: str, *, fallback: Any | None = None
) -> str:
    value = values.get(key, fallback)
    return "" if value is None else str(value)


def _artifact_challenge(artifact: Artifact) -> str:
    if artifact.structured and "code_challenge" in artifact.structured:
        return str(artifact.structured["code_challenge"])
    if artifact.text_value is not None:
        return artifact.text_value
    return ""


__all__ = [
    "PKCE_CHALLENGE_METHOD",
    "PKCE_SPEC_URL",
    "PKCE_VERIFIER_CHARS",
    "PKCE_VERIFIER_RE",
    "PkceProofProvider",
    "PkceVerifier",
    "b64url",
    "make_pkce_verifier",
    "pkce_s256_challenge",
    "validate_pkce_verifier",
    "verify_pkce_s256_challenge",
]
