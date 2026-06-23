"""Context keys consumed by table-owned key and token operations."""

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
    if key_provider is not None:
        ctx[KEY_PROVIDER_CTX] = key_provider
    if signer is not None:
        ctx[SIGNER_CTX] = signer
    if verifier is not None:
        ctx[VERIFIER_CTX] = verifier
    if jwt_coder is not None:
        ctx[JWT_CODER_CTX] = jwt_coder
    if clock is not None:
        ctx[CLOCK_CTX] = clock
    return ctx


__all__ = [
    "CLOCK_CTX",
    "JWT_CODER_CTX",
    "KEY_PROVIDER_CTX",
    "SIGNER_CTX",
    "VERIFIER_CTX",
    "stash_security_providers",
]
