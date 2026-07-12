"""Proof-of-possession helpers for RFC 7800 compliance."""

from __future__ import annotations

from typing import Any, Final, Mapping

from tigrbl_identity_runtime.settings import settings
from tigrbl_jose_concrete import add_cnf_claim as _add_cnf_claim
from tigrbl_jose_concrete import verify_proof_of_possession as _verify_pop

RFC7800_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7800"


def add_cnf_claim(payload: Mapping[str, Any], jwk: Mapping[str, Any]) -> dict[str, Any]:
    return _add_cnf_claim(payload, jwk)


def verify_proof_of_possession(
    payload: Mapping[str, Any],
    jwk: Mapping[str, Any],
    *,
    enabled: bool | None = None,
) -> bool:
    if enabled is None:
        enabled = settings.enable_rfc7800
    if not enabled:
        return True
    return _verify_pop(payload, jwk)


__all__ = ["RFC7800_SPEC_URL", "add_cnf_claim", "verify_proof_of_possession"]
