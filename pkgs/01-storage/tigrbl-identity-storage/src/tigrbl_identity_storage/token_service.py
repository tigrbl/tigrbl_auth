from __future__ import annotations

from copy import deepcopy
import inspect
from typing import Any, Protocol
from uuid import uuid4

from tigrbl_identity_contracts.tokens import InvalidRefreshTokenError, RefreshTokenReuseError


class TokenCoder(Protocol):
    async def async_sign_pair(self, **kwargs: Any) -> tuple[str, str]: ...

    async def async_decode(self, token: str, **kwargs: Any) -> dict[str, Any]: ...


async def _decode_issued_claims(jwt: TokenCoder, token: str) -> dict[str, Any]:
    decode = jwt.async_decode
    try:
        parameters = inspect.signature(decode).parameters
    except (TypeError, ValueError):
        parameters = {}
    supports_skip = "verify_revocation" in parameters or any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    )
    if supports_skip:
        return await decode(token, verify_exp=False, verify_revocation=False)
    return await decode(token, verify_exp=False)


async def issue_persisted_token_pair(
    *,
    jwt: TokenCoder,
    sub: str,
    tid: str,
    client_id: str | None,
    cert_thumbprint: str | None = None,
    refresh_family_id: str | None = None,
    refresh_parent_token: str | None = None,
    authorization_trace: dict[str, Any] | None = None,
    delegation_provenance: dict[str, Any] | None = None,
    **extra: Any,
) -> tuple[str, str]:
    from tigrbl_identity_storage.tables._ops import token_hash
    from tigrbl_identity_storage.tables.token_record._lifecycle import upsert_token_record_async

    access_token, refresh_token = await jwt.async_sign_pair(
        sub=sub,
        tid=tid,
        cert_thumbprint=cert_thumbprint,
        persist_token=False,
        **extra,
    )
    access_claims = await _decode_issued_claims(jwt, access_token)
    refresh_claims = await _decode_issued_claims(jwt, refresh_token)
    if authorization_trace is not None:
        access_claims["authorization_trace"] = deepcopy(authorization_trace)
        refresh_claims["authorization_trace"] = deepcopy(authorization_trace)
    if delegation_provenance is not None:
        access_claims["delegation_provenance"] = deepcopy(delegation_provenance)
        refresh_claims["delegation_provenance"] = deepcopy(delegation_provenance)
    if client_id:
        access_claims["client_id"] = client_id
        refresh_claims["client_id"] = client_id
    family_id = refresh_family_id or str(uuid4())
    refresh_parent_hash = token_hash(refresh_parent_token) if refresh_parent_token else None
    await upsert_token_record_async(
        access_token,
        access_claims,
        token_kind="access",
        token_type_hint="access_token",
        refresh_family_id=family_id,
        refresh_parent_hash=refresh_parent_hash,
    )
    await upsert_token_record_async(
        refresh_token,
        refresh_claims,
        token_kind="refresh",
        token_type_hint="refresh_token",
        refresh_family_id=family_id,
        refresh_parent_hash=refresh_parent_hash,
    )
    return access_token, refresh_token


def _normalize_refresh_audience(value: Any) -> str | list[str] | None:
    if value is None or value == "":
        return None
    if isinstance(value, (str, list)):
        return value
    if isinstance(value, tuple):
        return list(value)
    return str(value)


async def redeem_refresh_token(
    *,
    jwt: TokenCoder,
    refresh_token: str,
    client_id: str,
    cert_thumbprint: str | None = None,
    requested_audience: str | None = None,
    token_type: str = "bearer",
) -> dict[str, Any]:
    from tigrbl_identity_storage.tables.token_record._lifecycle import (
        get_token_record_async,
        mark_token_used_async,
        revoke_refresh_family_async,
    )

    record = await get_token_record_async(refresh_token)
    if record is None:
        raise InvalidRefreshTokenError("refresh token was not issued by this repository")
    if record.token_kind != "refresh":
        raise InvalidRefreshTokenError("presented token is not a refresh token")
    if str(record.client_id or "") not in {"", client_id}:
        raise InvalidRefreshTokenError("refresh token client binding mismatch")
    family_id = str(record.refresh_family_id or "")
    if record.used_at is not None or record.refresh_successor_hash:
        if family_id:
            await revoke_refresh_family_async(family_id, reuse_token=refresh_token)
        raise RefreshTokenReuseError("refresh token replay detected")
    if not record.active or record.revoked_at is not None:
        raise InvalidRefreshTokenError("refresh token is inactive")

    claims = await jwt.async_decode(refresh_token, verify_exp=True, cert_thumbprint=cert_thumbprint)
    if claims.get("typ") != "refresh":
        raise InvalidRefreshTokenError("presented token is not a refresh token")
    if client_id and str(claims.get("client_id") or record.client_id or "") not in {"", client_id}:
        raise InvalidRefreshTokenError("refresh token client binding mismatch")

    stored_audience = _normalize_refresh_audience((record.claims or {}).get("aud") if isinstance(record.claims, dict) else None)
    if requested_audience and stored_audience not in {None, "", requested_audience}:
        raise InvalidRefreshTokenError("refresh token audience cannot be widened or changed")

    preserved_claims = deepcopy(record.claims or claims)
    preserved_claims.pop("iat", None)
    preserved_claims.pop("exp", None)
    preserved_claims.pop("nbf", None)
    preserved_claims.pop("jti", None)
    preserved_claims.pop("typ", None)

    next_audience = requested_audience or _normalize_refresh_audience(preserved_claims.pop("aud", None))
    next_scope = preserved_claims.pop("scope", None)
    next_issuer = preserved_claims.pop("iss", None)
    preserved_claims.pop("sub", None)
    preserved_claims.pop("tid", None)
    preserved_claims.pop("client_id", None)
    preserved_claims.pop("cnf", None)
    confirmation_claim = claims.get("cnf")
    extra_claims = preserved_claims or {}
    if confirmation_claim:
        extra_claims["cnf"] = confirmation_claim

    access_token, next_refresh_token = await issue_persisted_token_pair(
        jwt=jwt,
        sub=str(claims.get("sub") or record.subject),
        tid=str(claims.get("tid") or record.tenant_id or ""),
        client_id=client_id,
        cert_thumbprint=cert_thumbprint,
        refresh_family_id=family_id or None,
        refresh_parent_token=refresh_token,
        scope=next_scope,
        issuer=next_issuer,
        audience=next_audience,
        **extra_claims,
    )
    await mark_token_used_async(refresh_token, successor_token=next_refresh_token)
    return {
        "access_token": access_token,
        "refresh_token": next_refresh_token,
        "token_type": token_type,
    }


__all__ = [
    "TokenCoder",
    "issue_persisted_token_pair",
    "redeem_refresh_token",
]
