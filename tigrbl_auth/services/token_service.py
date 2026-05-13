"""JWT minting/verification and operator token wrappers."""

from __future__ import annotations

import asyncio
import base64
import json
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from threading import Thread
from typing import Any, Dict, Iterable, Optional, Tuple
from uuid import uuid4

from tigrbl_auth.errors import InvalidTokenError

from .key_management import _DEFAULT_KEY_PATH, _ensure_key, _provider
from .session_service import (
    exchange_token_for_context,
    get_token_for_context,
    introspect_token_for_context,
    list_tokens_for_context,
    revoke_all_tokens_for_context,
    revoke_token_for_context,
)

_ACCESS_TTL = timedelta(minutes=60)
_REFRESH_TTL = timedelta(days=7)


class RefreshTokenError(Exception):
    """Base class for refresh token lifecycle failures."""


class InvalidRefreshTokenError(RefreshTokenError):
    """The presented refresh token is invalid for the retained boundary."""


class RefreshTokenReuseError(RefreshTokenError):
    """A refresh token replay was detected and the family was revoked."""


def _load_runtime() -> dict[str, Any]:
    try:
        from tigrbl_auth.framework import ExportPolicy, FileKeyProvider, JWTTokenService, LocalKeyProvider, JWAAlg, KeyAlg, KeyClass, KeySpec, KeyUse
        from tigrbl_auth.config.settings import settings
        from tigrbl_auth.standards.oauth2.mtls import validate_certificate_binding
        from tigrbl_auth.standards.oauth2.revocation import is_revoked
        from tigrbl_auth.standards.oauth2.introspection import register_token
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("runtime token-service dependencies are unavailable") from exc
    return {
        "ExportPolicy": ExportPolicy,
        "FileKeyProvider": FileKeyProvider,
        "JWTTokenService": JWTTokenService,
        "LocalKeyProvider": LocalKeyProvider,
        "JWAAlg": JWAAlg,
        "KeyAlg": KeyAlg,
        "KeyClass": KeyClass,
        "KeySpec": KeySpec,
        "KeyUse": KeyUse,
        "settings": settings,
        "validate_certificate_binding": validate_certificate_binding,
        "is_revoked": is_revoked,
        "register_token": register_token,
    }


def _run(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    result = None

    def runner():
        nonlocal result
        result = asyncio.run(coro)

    thread = Thread(target=runner)
    thread.start()
    thread.join()
    return result


@lru_cache(maxsize=1)
def _svc() -> Tuple[Any, str]:
    runtime = _load_runtime()
    kp = _provider()
    if _DEFAULT_KEY_PATH.exists():
        kid = _DEFAULT_KEY_PATH.read_text().strip()
        if kid:
            try:
                _run(kp.get_key(kid, include_secret=False))
            except Exception:
                kid, _, _ = _run(_ensure_key())
        else:
            kid, _, _ = _run(_ensure_key())
    else:
        spec = runtime["KeySpec"](
            klass=runtime["KeyClass"].asymmetric,
            alg=runtime["KeyAlg"].ED25519,
            uses=(runtime["KeyUse"].SIGN, runtime["KeyUse"].VERIFY),
            export_policy=runtime["ExportPolicy"].SECRET_WHEN_ALLOWED,
            label="jwt_ed25519",
        )
        ref = _run(kp.create_key(spec))
        kid = ref.kid
        _DEFAULT_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        _DEFAULT_KEY_PATH.write_text(kid)
    service = runtime["JWTTokenService"](kp)
    return service, kid


def _header_alg(token: str) -> str:
    try:
        header_segment = token.split(".")[0]
        padded = header_segment + "=" * (-len(header_segment) % 4)
        header = json.loads(base64.urlsafe_b64decode(padded).decode())
        return str(header.get("alg", "")).lower()
    except Exception:
        return ""


class JWTCoder:
    __slots__ = ("_svc", "_kid")

    def __init__(self, arg1: Any, arg2: Any):
        runtime = _load_runtime()
        if isinstance(arg1, runtime["JWTTokenService"]) and isinstance(arg2, str):
            self._svc = arg1
            self._kid = arg2
            return
        if isinstance(arg1, (bytes, bytearray)) and isinstance(arg2, (bytes, bytearray)):
            kp = runtime["LocalKeyProvider"]()
            spec = runtime["KeySpec"](
                klass=runtime["KeyClass"].asymmetric,
                alg=runtime["KeyAlg"].ED25519,
                uses=(runtime["KeyUse"].SIGN, runtime["KeyUse"].VERIFY),
                export_policy=runtime["ExportPolicy"].SECRET_WHEN_ALLOWED,
                label="jwt_ed25519",
            )
            ref = _run(kp.import_key(spec, arg1, public=arg2))
            self._svc = runtime["JWTTokenService"](kp)
            self._kid = ref.kid
            return
        raise TypeError("JWTCoder requires (JWTTokenService, kid) or (private_pem, public_pem)")

    @classmethod
    def default(cls) -> "JWTCoder":
        svc, kid = _svc()
        return cls(svc, kid)

    async def async_sign(
        self,
        *,
        sub: str,
        tid: Optional[str] = None,
        ttl: timedelta = _ACCESS_TTL,
        typ: str = "access",
        issuer: Optional[str] = None,
        audience: Optional[Iterable[str] | str] = None,
        cert_thumbprint: Optional[str] = None,
        **extra: Any,
    ) -> str:
        runtime = _load_runtime()
        settings = runtime["settings"]
        now = datetime.now(timezone.utc)
        payload: Dict[str, Any] = {
            "sub": sub,
            "typ": typ,
            "iat": int(now.timestamp()),
            "exp": int((now + ttl).timestamp()),
            "jti": str(uuid4()),
            **extra,
        }
        if tid is not None:
            payload["tid"] = tid
        if getattr(settings, "enable_rfc8705", False) and cert_thumbprint is not None:
            payload["cnf"] = {"x5t#S256": cert_thumbprint}
        if getattr(settings, "enable_rfc9068", False) and typ == "access":
            effective_issuer = issuer or settings.issuer
            effective_audience = audience or settings.protected_resource_identifier
            from tigrbl_auth.standards.oauth2.jwt_access_tokens import add_jwt_access_token_claims

            payload = add_jwt_access_token_claims(payload, issuer=effective_issuer, audience=effective_audience)
            issuer = effective_issuer
            audience = effective_audience
        token = await self._svc.mint(
            payload,
            alg=runtime["JWAAlg"].EDDSA,
            kid=self._kid,
            lifetime_s=int(ttl.total_seconds()),
            subject=sub,
            issuer=issuer,
            audience=audience,
        )
        if getattr(settings, "enable_rfc7662", False):
            claims = dict(payload)
            claims.setdefault("sub", sub)
            claims.setdefault("kind", typ)
            if tid is not None:
                claims.setdefault("tid", tid)
            if issuer is not None:
                claims.setdefault("iss", issuer)
            if audience is not None:
                claims.setdefault("aud", list(audience) if isinstance(audience, (list, tuple, set)) else audience)
            runtime["register_token"](token, claims)
        return token

    def sign(self, **kwargs: Any) -> str:
        return _run(self.async_sign(**kwargs))

    async def async_sign_pair(self, *, sub: str, tid: str, cert_thumbprint: Optional[str] = None, **extra: Any) -> Tuple[str, str]:
        access = await self.async_sign(sub=sub, tid=tid, cert_thumbprint=cert_thumbprint, **extra)
        refresh = await self.async_sign(sub=sub, tid=tid, ttl=_REFRESH_TTL, typ="refresh", cert_thumbprint=cert_thumbprint, **extra)
        return access, refresh

    def sign_pair(self, **kwargs: Any) -> Tuple[str, str]:
        return _run(self.async_sign_pair(**kwargs))

    async def async_verify(self, token: str, *, cert_thumbprint: Optional[str] = None, audience: Optional[Iterable[str] | str] = None, issuer: Optional[str] = None) -> Dict[str, Any]:
        runtime = _load_runtime()
        settings = runtime["settings"]
        if _header_alg(token) == "none":
            raise InvalidTokenError("unsigned tokens are not accepted")
        try:
            payload = await self._svc.verify(token, audience=audience, issuer=issuer)
        except Exception as exc:
            raise InvalidTokenError("signature verification failed") from exc
        payload = dict(payload)
        if getattr(settings, "enable_rfc9700", False) and (audience is not None or issuer is not None):
            if payload.get("iss") in {None, "", "placeholder-issuer"}:
                raise InvalidTokenError("missing issuer")
            aud = payload.get("aud")
            if aud in {None, ""} or aud == []:
                raise InvalidTokenError("missing audience")
        cnf = payload.get("cnf") if isinstance(payload.get("cnf"), dict) else {}
        if getattr(settings, "enable_rfc8705", False) and cnf.get("x5t#S256") is not None:
            runtime["validate_certificate_binding"](payload, cert_thumbprint)
        if runtime["is_revoked"](token):
            raise InvalidTokenError("token revoked")
        return payload

    def verify(self, token: str, **kwargs: Any) -> Dict[str, Any]:
        return _run(self.async_verify(token, **kwargs))

    async def async_decode(self, token: str, *, verify_exp: bool = True, cert_thumbprint: Optional[str] = None, audience: Optional[Iterable[str] | str] = None, issuer: Optional[str] = None) -> Dict[str, Any]:
        payload = await self.async_verify(token, cert_thumbprint=cert_thumbprint, audience=audience, issuer=issuer)
        if verify_exp:
            exp = payload.get("exp")
            if exp is not None and int(exp) < int(datetime.now(timezone.utc).timestamp()):
                raise InvalidTokenError("token expired")
        return payload

    def decode(self, token: str, *, verify_exp: bool = True, cert_thumbprint: Optional[str] = None, audience: Optional[Iterable[str] | str] = None, issuer: Optional[str] = None) -> Dict[str, Any]:
        return _run(self.async_decode(token, verify_exp=verify_exp, cert_thumbprint=cert_thumbprint, audience=audience, issuer=issuer))


async def issue_persisted_token_pair(
    *,
    jwt: JWTCoder,
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
    from tigrbl_auth.services.persistence import token_hash, upsert_token_record_async

    access_token, refresh_token = await jwt.async_sign_pair(
        sub=sub,
        tid=tid,
        cert_thumbprint=cert_thumbprint,
        **extra,
    )
    access_claims = await jwt.async_decode(access_token, verify_exp=False)
    refresh_claims = await jwt.async_decode(refresh_token, verify_exp=False)
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
    jwt: JWTCoder,
    refresh_token: str,
    client_id: str,
    cert_thumbprint: str | None = None,
    requested_audience: str | None = None,
    token_type: str = "bearer",
) -> dict[str, Any]:
    from tigrbl_auth.services.persistence import (
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



# -----------------------------
# Operator-plane wrappers
# -----------------------------

def parse_token_patch(raw_patch: dict[str, Any] | None) -> dict[str, Any]:
    patch = dict(raw_patch or {})
    patch.setdefault("issued_at", patch.get("iat") or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"))
    if "token_type" not in patch and "typ" in patch:
        patch["token_type"] = patch["typ"]
    return patch


def list_operator_tokens_for_context(context, *, status_filter: str | None = None, filter_expr: str | None = None, sort: str = "id", offset: int = 0, limit: int = 50):
    return list_tokens_for_context(context, status_filter=status_filter, filter_expr=filter_expr, sort=sort, offset=offset, limit=limit)


def get_operator_token_for_context(context, *, record_id: str):
    return get_token_for_context(context, record_id=record_id)


def introspect_operator_token_for_context(context, *, record_id: str):
    return introspect_token_for_context(context, record_id=record_id)


def revoke_operator_token_for_context(context, *, record_id: str):
    return revoke_token_for_context(context, record_id=record_id)


def revoke_all_operator_tokens_for_context(context, *, status_filter: str | None = None, filter_expr: str | None = None):
    return revoke_all_tokens_for_context(context, status_filter=status_filter, filter_expr=filter_expr)


def exchange_operator_token_for_context(context, *, subject_token: str | None, requested_token_type: str | None = None, audience: str | None = None, resource: str | None = None, actor_token: str | None = None, extras: dict[str, Any] | None = None):
    return exchange_token_for_context(context, subject_token=subject_token, requested_token_type=requested_token_type, audience=audience, resource=resource, actor_token=actor_token, extras=extras)


__all__ = [
    "InvalidRefreshTokenError",
    "JWTCoder",
    "RefreshTokenError",
    "RefreshTokenReuseError",
    "exchange_operator_token_for_context",
    "get_operator_token_for_context",
    "introspect_operator_token_for_context",
    "issue_persisted_token_pair",
    "list_operator_tokens_for_context",
    "parse_token_patch",
    "redeem_refresh_token",
    "revoke_all_operator_tokens_for_context",
    "revoke_operator_token_for_context",
]
