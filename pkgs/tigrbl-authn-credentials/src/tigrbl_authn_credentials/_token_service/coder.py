from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, Optional, Tuple
from uuid import uuid4

from tigrbl_identity_core.errors import InvalidTokenError

from .runtime import _ACCESS_TTL, _REFRESH_TTL, _header_alg, _load_runtime, _run, _svc, _svc_async


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

    @classmethod
    async def async_default(cls) -> "JWTCoder":
        svc, kid = await _svc_async()
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
        persist_token: bool = True,
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
            from tigrbl_auth_protocol_oauth.standards.jwt_access_tokens import add_jwt_access_token_claims

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
        return token

    def sign(self, **kwargs: Any) -> str:
        return _run(self.async_sign(**kwargs))

    async def async_sign_pair(self, *, sub: str, tid: str, cert_thumbprint: Optional[str] = None, **extra: Any) -> Tuple[str, str]:
        access = await self.async_sign(sub=sub, tid=tid, cert_thumbprint=cert_thumbprint, **extra)
        refresh = await self.async_sign(sub=sub, tid=tid, ttl=_REFRESH_TTL, typ="refresh", cert_thumbprint=cert_thumbprint, **extra)
        return access, refresh

    def sign_pair(self, **kwargs: Any) -> Tuple[str, str]:
        return _run(self.async_sign_pair(**kwargs))

    async def async_verify(
        self,
        token: str,
        *,
        cert_thumbprint: Optional[str] = None,
        audience: Optional[Iterable[str] | str] = None,
        issuer: Optional[str] = None,
        verify_revocation: bool = True,
    ) -> Dict[str, Any]:
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
        if verify_revocation and await runtime["is_revoked_async"](token):
            raise InvalidTokenError("token revoked")
        return payload

    def verify(self, token: str, **kwargs: Any) -> Dict[str, Any]:
        return _run(self.async_verify(token, **kwargs))

    async def async_decode(
        self,
        token: str,
        *,
        verify_exp: bool = True,
        cert_thumbprint: Optional[str] = None,
        audience: Optional[Iterable[str] | str] = None,
        issuer: Optional[str] = None,
        verify_revocation: bool = True,
    ) -> Dict[str, Any]:
        payload = await self.async_verify(
            token,
            cert_thumbprint=cert_thumbprint,
            audience=audience,
            issuer=issuer,
            verify_revocation=verify_revocation,
        )
        if verify_exp:
            exp = payload.get("exp")
            if exp is not None and int(exp) < int(datetime.now(timezone.utc).timestamp()):
                raise InvalidTokenError("token expired")
        return payload

    def decode(
        self,
        token: str,
        *,
        verify_exp: bool = True,
        cert_thumbprint: Optional[str] = None,
        audience: Optional[Iterable[str] | str] = None,
        issuer: Optional[str] = None,
        verify_revocation: bool = True,
    ) -> Dict[str, Any]:
        return _run(
            self.async_decode(
                token,
                verify_exp=verify_exp,
                cert_thumbprint=cert_thumbprint,
                audience=audience,
                issuer=issuer,
                verify_revocation=verify_revocation,
            )
        )
