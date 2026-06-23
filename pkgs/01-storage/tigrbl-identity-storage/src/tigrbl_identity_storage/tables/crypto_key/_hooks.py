"""Storage-owned crypto key lifecycle hooks."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_storage.framework import hook_ctx

from .._ops import field, record_id
from ._usage import normalize_payload_key_usage
from ._table import CryptoKey

_TIGRBL_HOOK_STAGE_KEY = "".join(("pha", "se"))
_JWK_SECRET_FIELDS = {"d", "p", "q", "dp", "dq", "qi"}


def _scrub_public_material(material: Any) -> Any:
    if isinstance(material, dict):
        return {key: value for key, value in material.items() if key not in _JWK_SECRET_FIELDS}
    return material


def scrub_key_material(payload: Any) -> Any:
    if isinstance(payload, dict):
        cleaned = dict(payload)
        cleaned.pop("provider_key_ref", None)
        cleaned["public_material"] = _scrub_public_material(cleaned.get("public_material"))
        return cleaned
    if hasattr(payload, "provider_key_ref"):
        try:
            setattr(payload, "provider_key_ref", None)
        except Exception:
            pass
    if hasattr(payload, "public_material"):
        try:
            setattr(payload, "public_material", _scrub_public_material(getattr(payload, "public_material")))
        except Exception:
            pass
    return payload


@hook_ctx(**{"ops": ("create", "update"), _TIGRBL_HOOK_STAGE_KEY: "PRE_HANDLER"})
async def normalize_key_usage_policy(ctx: Mapping[str, Any]) -> None:
    payload = ctx.get("payload")
    if not isinstance(payload, Mapping):
        return
    normalized = normalize_payload_key_usage(payload)
    if isinstance(ctx, dict):
        ctx["payload"] = normalized


@hook_ctx(**{"ops": "create", _TIGRBL_HOOK_STAGE_KEY: "POST_HANDLER"})
async def seed_primary_key_version(ctx: Mapping[str, Any]) -> None:
    db = ctx.get("db") or ctx.get("session")
    row = ctx.get("result") or ctx.get("object") or ctx.get("item")
    if db is None or row is None:
        return
    from ..crypto_key_version import CryptoKeyVersion

    version = int(field(row, "primary_version", 1) or 1)
    existing = await CryptoKeyVersion.lookup(db, key_id=record_id(row), version=version)
    if existing is not None:
        return
    await CryptoKeyVersion.create_version(
        db,
        key_id=record_id(row),
        version=version,
        status="active",
        public_material=field(row, "public_material"),
        public_material_format=field(row, "public_material_format"),
        provider_key_ref=field(row, "provider_key_ref"),
        provider=field(row, "provider"),
        allowed_ops=field(row, "allowed_ops"),
        fingerprint=field(row, "fingerprint"),
    )


@hook_ctx(**{"ops": ("rotate_record",), _TIGRBL_HOOK_STAGE_KEY: "PRE_HANDLER"})
async def ensure_key_enabled(ctx: Mapping[str, Any]) -> None:
    db = ctx.get("db") or ctx.get("session")
    payload = ctx.get("payload") or {}
    kid = payload.get("kid") if isinstance(payload, Mapping) else None
    if db is None or not kid:
        return
    row = await CryptoKey.lookup_by_kid(db, kid=str(kid))
    if row is None or field(row, "status") != "active":
        raise LookupError("active crypto key not found")
    if isinstance(ctx, dict):
        ctx["crypto_key"] = row


__all__ = ["ensure_key_enabled", "normalize_key_usage_policy", "scrub_key_material", "seed_primary_key_version"]
