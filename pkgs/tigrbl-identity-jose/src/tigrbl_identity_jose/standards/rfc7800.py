"""Proof-of-possession helpers for RFC 7800 compliance."""

from __future__ import annotations

from typing import Any, Final, Mapping

from tigrbl_auth.config.settings import settings
from tigrbl_auth.standards.jose.rfc7638 import jwk_thumbprint

RFC7800_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7800"


def add_cnf_claim(payload: Mapping[str, Any], jwk: Mapping[str, Any]) -> dict[str, Any]:
    augmented = dict(payload)
    cnf = dict(augmented.get("cnf", {}))
    cnf["jkt"] = jwk_thumbprint(jwk, enabled=True)
    augmented["cnf"] = cnf
    return augmented


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
    cnf = payload.get("cnf", {})
    jkt = cnf.get("jkt")
    if not jkt:
        return False
    expected = jwk_thumbprint(jwk, enabled=True)
    return jkt == expected


__all__ = ["RFC7800_SPEC_URL", "add_cnf_claim", "verify_proof_of_possession"]
