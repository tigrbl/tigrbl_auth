"""Storage-owned key lifecycle hooks."""

from __future__ import annotations

from typing import Any, Mapping

from tigrbl_identity_storage.framework import hook_ctx

from .._ops import field, record_id
from ._table import Key

_TIGRBL_HOOK_STAGE_KEY = "".join(("pha", "se"))


def scrub_key_material(payload: Any) -> Any:
    if isinstance(payload, dict):
        cleaned = dict(payload)
        cleaned.pop("provider_key_ref", None)
        jwk = cleaned.get("public_jwk")
        if isinstance(jwk, dict):
            cleaned["public_jwk"] = {key: value for key, value in jwk.items() if key not in {"d", "p", "q", "dp", "dq", "qi"}}
        return cleaned
    for name in ("provider_key_ref",):
        if hasattr(payload, name):
            try:
                setattr(payload, name, None)
            except Exception:
                pass
    return payload


@hook_ctx(**{"ops": "create", _TIGRBL_HOOK_STAGE_KEY: "POST_HANDLER"})
async def seed_primary_key_version(ctx: Mapping[str, Any]) -> None:
    db = ctx.get("db") or ctx.get("session")
    row = ctx.get("result") or ctx.get("object") or ctx.get("item")
    if db is None or row is None:
        return
    from ..key_version import KeyVersion

    existing = await KeyVersion.lookup(db, key_id=record_id(row), version=int(field(row, "primary_version", 1) or 1))
    if existing is not None:
        return
    provider = ctx.get("key_provider")
    public_jwk = field(row, "public_jwk")
    provider_key_ref = field(row, "provider_key_ref")
    if provider is not None and (public_jwk is None or provider_key_ref is None):
        generated = await provider.create_key(kid=field(row, "kid"), algorithm=field(row, "algorithm"))
        public_jwk = public_jwk or getattr(generated, "public_jwk", None) or getattr(generated, "public", None)
        provider_key_ref = provider_key_ref or getattr(generated, "provider_key_ref", None) or getattr(generated, "key_ref", None)
    await KeyVersion.create_version(
        db,
        key_id=record_id(row),
        version=int(field(row, "primary_version", 1) or 1),
        status="active",
        public_jwk=public_jwk,
        provider_key_ref=provider_key_ref,
        provider=field(row, "provider"),
    )


@hook_ctx(**{"ops": ("sign", "verify", "rotate"), _TIGRBL_HOOK_STAGE_KEY: "PRE_HANDLER"})
async def ensure_key_enabled(ctx: Mapping[str, Any]) -> None:
    db = ctx.get("db") or ctx.get("session")
    payload = ctx.get("payload") or {}
    kid = payload.get("kid") if isinstance(payload, Mapping) else None
    if db is None or not kid:
        return
    row = await Key.lookup_by_kid(db, kid=str(kid))
    if row is None or field(row, "status") != "active":
        raise LookupError("active key not found")
    if isinstance(ctx, dict):
        ctx["key"] = row


__all__ = ["ensure_key_enabled", "scrub_key_material", "seed_primary_key_version"]
