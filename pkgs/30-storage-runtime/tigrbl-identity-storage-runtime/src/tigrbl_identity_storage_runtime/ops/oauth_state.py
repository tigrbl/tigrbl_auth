"""Durable OAuth authorization, registration, and revocation operations."""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from datetime import timezone
from typing import Any

from .common import (
    create_table_record,
    database_from_context,
    field_value,
    first_table_record,
    payload_from_context,
    update_table_record,
)


async def persist_authorization_code(ctx: Mapping[str, Any]) -> Any:
    """Persist an authorization code using the canonical create operation."""

    from tigrbl_identity_storage.tables import AuthCode

    return await create_table_record(
        AuthCode,
        database_from_context(ctx),
        payload_from_context(ctx),
    )


async def upsert_client_registration(ctx: Mapping[str, Any]) -> Any:
    """Create or merge durable dynamic-client registration metadata."""

    from tigrbl_identity_storage.tables import ClientRegistration

    db = database_from_context(ctx)
    payload = dict(payload_from_context(ctx))
    client_id = payload["client_id"]
    row = await first_table_record(
        ClientRegistration,
        db,
        {"client_id": client_id},
    )
    merged = {
        "client_id": client_id,
        "tenant_id": payload.get("tenant_id") or field_value(row, "tenant_id"),
        "registration_metadata": payload.get("metadata")
        or payload.get("registration_metadata")
        or field_value(row, "registration_metadata"),
        "contacts": list(payload["contacts"])
        if payload.get("contacts") is not None
        else field_value(row, "contacts"),
        "software_id": payload.get("software_id")
        or field_value(row, "software_id"),
        "software_version": payload.get("software_version")
        or field_value(row, "software_version"),
        "registration_access_token_hash": payload.get(
            "registration_access_token_hash"
        )
        or field_value(row, "registration_access_token_hash"),
        "registration_client_uri": payload.get("registration_client_uri")
        or field_value(row, "registration_client_uri"),
        "issued_at": field_value(row, "issued_at")
        or dt.datetime.now(timezone.utc),
    }
    if row is None:
        return await create_table_record(ClientRegistration, db, merged)
    return await update_table_record(
        ClientRegistration,
        db,
        field_value(row, "id"),
        merged,
    )


async def record_revoked_token_hash(ctx: Mapping[str, Any]) -> Any:
    """Idempotently record a revoked token digest and its durable metadata."""

    from tigrbl_identity_storage.tables import RevokedToken

    db = database_from_context(ctx)
    payload = dict(payload_from_context(ctx))
    digest = payload["token_hash"]
    row = await first_table_record(RevokedToken, db, {"token_hash": digest})
    record = {
        "token_hash": digest,
        "token_type_hint": payload.get("token_type_hint")
        or field_value(row, "token_type_hint"),
        "refresh_family_id": payload.get("refresh_family_id")
        or field_value(row, "refresh_family_id"),
        "subject": payload.get("subject") or field_value(row, "subject"),
        "tenant_id": payload.get("tenant_id") or field_value(row, "tenant_id"),
        "client_id": payload.get("client_id") or field_value(row, "client_id"),
        "revoked_reason": payload.get("reason")
        or payload.get("revoked_reason")
        or field_value(row, "revoked_reason")
        or "revoked",
        "expires_at": payload.get("expires_at")
        or field_value(row, "expires_at"),
    }
    if row is None:
        return await create_table_record(RevokedToken, db, record)
    return await update_table_record(
        RevokedToken,
        db,
        field_value(row, "id"),
        record,
    )


async def is_token_hash_revoked(ctx: Mapping[str, Any]) -> bool:
    """Return whether a token digest exists in the revocation ledger."""

    from tigrbl_identity_storage.tables import RevokedToken

    payload = payload_from_context(ctx)
    return (
        await first_table_record(
            RevokedToken,
            database_from_context(ctx),
            {"token_hash": payload["token_hash"]},
        )
        is not None
    )


__all__ = [
    "is_token_hash_revoked",
    "persist_authorization_code",
    "record_revoked_token_hash",
    "upsert_client_registration",
]
