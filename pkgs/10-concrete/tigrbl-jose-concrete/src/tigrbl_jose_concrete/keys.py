from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class JoseKeyStatus(str, Enum):
    ACTIVE = "active"
    NEXT = "next"
    RETIRED = "retired"
    DISABLED = "disabled"


class JoseKeyUse(str, Enum):
    SIGN = "sig"
    ENCRYPT = "enc"


def public_jwk_material(jwk: Mapping[str, Any]) -> dict[str, Any]:
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


def validate_public_jwk_material(jwk: Mapping[str, Any]) -> None:
    if not jwk.get("kid"):
        raise ValueError("JWK kid is required")
    if jwk.get("kty") not in {"OKP", "RSA", "EC"}:
        raise ValueError("public JWKS publication requires OKP, RSA, or EC keys")
    public_jwk_material(jwk)


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
        validate_public_jwk_material(self.jwk)
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
class JoseKeyRotationResult:
    tenant_id: str
    current_kid: str | None
    next_kid: str
    retired_kids: tuple[str, ...]
    published_kids: tuple[str, ...]
    reason: str
    rotated_at: str


__all__ = [
    "JoseKey",
    "JoseKeyRotationResult",
    "JoseKeyStatus",
    "JoseKeyUse",
    "public_jwk_material",
    "validate_public_jwk_material",
]
