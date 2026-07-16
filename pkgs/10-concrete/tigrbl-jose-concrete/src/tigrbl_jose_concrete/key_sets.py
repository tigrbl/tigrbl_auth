from __future__ import annotations

import hashlib
from dataclasses import replace
from typing import Any, Iterable, Mapping

from tigrbl_jose_bases import JoseKeySetBase
from tigrbl_identity_core.base64url import base64url_encode
from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.json_canonicalization import canonical_json_bytes

from .keys import (
    JoseKey,
    JoseKeyRotationResult,
    JoseKeyStatus,
    JoseKeyUse,
    public_jwk_material,
    validate_public_jwk_material,
)


RFC_TARGETS: Mapping[str, str] = {
    "jws": "RFC 7515",
    "jwe": "RFC 7516",
    "jwk": "RFC 7517",
    "jwa": "RFC 7518",
    "jwt": "RFC 7519",
    "jwk-thumbprint": "RFC 7638",
    "jwt-bcp": "RFC 8725",
}


def _public_jwk_material(jwk: Mapping[str, Any]) -> dict[str, Any]:
    return public_jwk_material(jwk)


def jwk_thumbprint(jwk: Mapping[str, Any]) -> str:
    """Return the RFC 7638 SHA-256 JWK thumbprint."""
    return base64url_encode(
        hashlib.sha256(canonical_json_bytes(_public_jwk_material(jwk))).digest()
    )


def validate_public_jwk(jwk: Mapping[str, Any]) -> None:
    validate_public_jwk_material(jwk)


class JoseKeySet(JoseKeySetBase):
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
        created = key if key.created_at else replace(key, created_at=utc_now_iso())
        self._keys[key.kid] = created
        return created

    def rotate(
        self,
        *,
        tenant_id: str,
        next_key: JoseKey,
        reason: str,
        retire_current: bool = True,
    ) -> JoseKeyRotationResult:
        active = [
            key
            for key in self._keys.values()
            if key.tenant_id == tenant_id and key.status == JoseKeyStatus.ACTIVE
        ]
        current = active[0] if active else None
        if next_key.tenant_id != tenant_id:
            raise ValueError("rotation key tenant mismatch")
        self.add(
            replace(
                next_key,
                status=JoseKeyStatus.ACTIVE,
                rotated_from=current.kid if current else None,
            )
        )
        retired: list[str] = []
        if current is not None and retire_current:
            self._keys[current.kid] = replace(current, status=JoseKeyStatus.RETIRED)
            retired.append(current.kid)
        published = tuple(
            key["kid"]
            for key in publish_tenant_jwks(self._keys.values(), tenant_id=tenant_id)[
                "keys"
            ]
        )
        return JoseKeyRotationResult(
            tenant_id=tenant_id,
            current_kid=current.kid if current else None,
            next_kid=next_key.kid,
            retired_kids=tuple(retired),
            published_kids=published,
            reason=reason,
            rotated_at=utc_now_iso(),
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
    "JoseKeyRotationResult",
    "RFC_TARGETS",
    "jwk_thumbprint",
    "publish_tenant_jwks",
    "rfc_vector_manifest",
    "validate_public_jwk",
]
