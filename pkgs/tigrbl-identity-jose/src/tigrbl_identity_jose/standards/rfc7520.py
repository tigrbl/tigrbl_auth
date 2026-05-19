"""JOSE composition helpers for RFC 7520 compliance."""

from __future__ import annotations

from typing import Final

from tigrbl_auth.config.settings import settings
from tigrbl_auth.standards.jose.rfc7515 import sign_jws, verify_jws
from tigrbl_auth.standards.jose.rfc7516 import decrypt_jwe, encrypt_jwe

RFC7520_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7520"


async def jws_then_jwe(payload: str, key: dict) -> str:
    if not settings.enable_rfc7520:
        raise RuntimeError(f"RFC 7520 support disabled: {RFC7520_SPEC_URL}")
    jws_token = await sign_jws(payload, key)
    return await encrypt_jwe(jws_token, key)


async def jwe_then_jws(token: str, key: dict) -> str:
    if not settings.enable_rfc7520:
        raise RuntimeError(f"RFC 7520 support disabled: {RFC7520_SPEC_URL}")
    jws_token = await decrypt_jwe(token, key)
    return await verify_jws(jws_token, key)


__all__ = ["RFC7520_SPEC_URL", "jws_then_jwe", "jwe_then_jws"]
