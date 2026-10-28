"""Context keys used to compose runtime key and token providers."""

from __future__ import annotations

from typing import Any, MutableMapping

KEY_PROVIDER_CTX = "key_provider"
SIGNER_CTX = "signer"
VERIFIER_CTX = "verifier"
JWT_CODER_CTX = "jwt_coder"
CLOCK_CTX = "clock"


def stash_security_providers(
    ctx: MutableMapping[str, Any],
    *,
    key_provider: Any | None = None,
    signer: Any | None = None,
    verifier: Any | None = None,
    jwt_coder: Any | None = None,
    clock: Any | None = None,
) -> MutableMapping[str, Any]:
    for key, value in (
        (KEY_PROVIDER_CTX, key_provider),
        (SIGNER_CTX, signer),
        (VERIFIER_CTX, verifier),
        (JWT_CODER_CTX, jwt_coder),
        (CLOCK_CTX, clock),
    ):
        if value is not None:
            ctx[key] = value
    return ctx


__all__ = [
    "CLOCK_CTX",
    "JWT_CODER_CTX",
    "KEY_PROVIDER_CTX",
    "SIGNER_CTX",
    "VERIFIER_CTX",
    "stash_security_providers",
]
