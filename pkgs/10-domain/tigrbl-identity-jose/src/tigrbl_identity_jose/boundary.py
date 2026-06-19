from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from tigrbl_user_plane_contracts.security_jose import JoseKeyStatus, JoseKeyUse


RFC_TARGETS: Mapping[str, str] = {
    "jws": "RFC 7515",
    "jwe": "RFC 7516",
    "jwk": "RFC 7517",
    "jwa": "RFC 7518",
    "jwt": "RFC 7519",
    "jwk-thumbprint": "RFC 7638",
    "jwt-bcp": "RFC 8725",
}


def _utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _public_jwk_material(jwk: Mapping[str, Any]) -> dict[str, Any]:
    kty = jwk.get("kty")
    if kty == "OKP":
        return {key: jwk[key] for key in ("crv", "kty", "x") if key in jwk}
    if kty == "RSA":
        return {key: jwk[key] for key in ("e", "kty", "n") if key in jwk}
    if kty == "EC":
        return {key: jwk[key] for key in ("crv", "kty", "x", "y") if key in jwk}
    if kty == "oct":
        return {key: jwk[key] for key in ("k", "kty") if key in jwk}
    raise ValueError(f"unsupported JWK key type {kty!r}")


def jwk_thumbprint(jwk: Mapping[str, Any]) -> str:
    """Return the RFC 7638 SHA-256 JWK thumbprint."""
    return _b64url(hashlib.sha256(_canonical_json(_public_jwk_material(jwk))).digest())


def validate_public_jwk(jwk: Mapping[str, Any]) -> None:
    if not jwk.get("kid"):
        raise ValueError("JWK kid is required")
    if jwk.get("kty") not in {"OKP", "RSA", "EC"}:
        raise ValueError("public JWKS publication requires OKP, RSA, or EC keys")
    _public_jwk_material(jwk)


@dataclass(frozen=True, slots=True)
class JoseKey:
    kid: str
    tenant_id: str
    jwk: Mapping[str, Any]
    algorithm: str
    key_use: JoseKeyUse = JoseKeyUse.SIGN
    status: JoseKeyStatus = JoseKeyStatus.NEXT
    not_before: str = ""
    not_after: str | None = None
    created_at: str = ""
    rotated_from: str | None = None

    def public_jwk(self) -> dict[str, Any]:
        validate_public_jwk(self.jwk)
        public = dict(self.jwk)
        public.pop("d", None)
        public.pop("p", None)
        public.pop("q", None)
        public.pop("dp", None)
        public.pop("dq", None)
        public.pop("qi", None)
        public.pop("k", None)
        public["kid"] = self.kid
        public.setdefault("alg", self.algorithm)
        public.setdefault("use", self.key_use.value)
        return public


@dataclass(frozen=True, slots=True)
class KeyRotationContract:
    tenant_id: str
    current_kid: str | None
    next_kid: str
    retired_kids: tuple[str, ...]
    published_kids: tuple[str, ...]
    reason: str
    rotated_at: str


class JoseKeySet:
    def __init__(self, keys: Iterable[JoseKey] = ()) -> None:
        self._keys: dict[str, JoseKey] = {}
        for key in keys:
            self.add(key)

    @property
    def keys(self) -> Mapping[str, JoseKey]:
        return dict(self._keys)

    def add(self, key: JoseKey) -> JoseKey:
        validate_public_jwk(key.jwk)
        if key.kid in self._keys:
            raise ValueError("JWK kid already exists")
        created = key if key.created_at else replace(key, created_at=_utc_now())
        self._keys[key.kid] = created
        return created

    def rotate(
        self,
        *,
        tenant_id: str,
        next_key: JoseKey,
        reason: str,
        retire_current: bool = True,
    ) -> KeyRotationContract:
        active = [
            key
            for key in self._keys.values()
            if key.tenant_id == tenant_id and key.status == JoseKeyStatus.ACTIVE
        ]
        current = active[0] if active else None
        if next_key.tenant_id != tenant_id:
            raise ValueError("rotation key tenant mismatch")
        self.add(replace(next_key, status=JoseKeyStatus.ACTIVE, rotated_from=current.kid if current else None))
        retired: list[str] = []
        if current is not None and retire_current:
            self._keys[current.kid] = replace(current, status=JoseKeyStatus.RETIRED)
            retired.append(current.kid)
        published = tuple(key["kid"] for key in publish_tenant_jwks(self._keys.values(), tenant_id=tenant_id)["keys"])
        return KeyRotationContract(
            tenant_id=tenant_id,
            current_kid=current.kid if current else None,
            next_kid=next_key.kid,
            retired_kids=tuple(retired),
            published_kids=published,
            reason=reason,
            rotated_at=_utc_now(),
        )


def publish_tenant_jwks(
    keys: Iterable[JoseKey],
    *,
    tenant_id: str,
    include_next: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    publishable = []
    allowed_statuses = {JoseKeyStatus.ACTIVE}
    if include_next:
        allowed_statuses.add(JoseKeyStatus.NEXT)
    for key in keys:
        if key.tenant_id != tenant_id or key.status not in allowed_statuses:
            continue
        publishable.append(key.public_jwk())
    publishable.sort(key=lambda item: str(item["kid"]))
    return {"keys": publishable}


def rfc_vector_manifest() -> dict[str, str]:
    return dict(RFC_TARGETS)


__all__ = [
    "JoseKey",
    "JoseKeySet",
    "JoseKeyStatus",
    "JoseKeyUse",
    "KeyRotationContract",
    "RFC_TARGETS",
    "jwk_thumbprint",
    "publish_tenant_jwks",
    "rfc_vector_manifest",
    "validate_public_jwk",
]
