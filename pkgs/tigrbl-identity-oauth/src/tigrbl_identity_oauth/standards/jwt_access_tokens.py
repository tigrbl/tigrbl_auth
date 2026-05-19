"""Domain-organized JWT access-token profile helpers."""

from __future__ import annotations

from typing import Any, Dict, Final, Iterable, Set

from tigrbl_auth.errors import InvalidTokenError

RFC9068_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc9068"


def add_jwt_access_token_claims(
    payload: Dict[str, Any], *, issuer: str, audience: Iterable[str] | str
) -> Dict[str, Any]:
    augmented = dict(payload)
    augmented["iss"] = issuer
    augmented["aud"] = audience if isinstance(audience, str) else list(audience)
    return augmented


def validate_jwt_access_token_claims(
    payload: Dict[str, Any], *, issuer: str, audience: Iterable[str] | str
) -> None:
    if payload.get("iss") != issuer:
        raise InvalidTokenError(f"issuer mismatch per RFC 9068: {RFC9068_SPEC_URL}")
    token_aud = payload.get("aud")
    expected: Set[str] = {audience} if isinstance(audience, str) else set(audience)
    presented: Set[str] = {token_aud} if isinstance(token_aud, str) else set(token_aud or [])
    if not (expected & presented):
        raise InvalidTokenError(f"audience mismatch per RFC 9068: {RFC9068_SPEC_URL}")
    for claim in ("sub", "exp"):
        if claim not in payload:
            raise InvalidTokenError(f"{claim} claim required by RFC 9068: {RFC9068_SPEC_URL}")


__all__ = ["RFC9068_SPEC_URL", "add_jwt_access_token_claims", "validate_jwt_access_token_claims"]
