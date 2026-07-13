from __future__ import annotations

import datetime as dt

import pytest

from tigrbl_identity_storage.tables import TokenRecord
from tigrbl_identity_storage_runtime import (
    TokenRecordRuntimeSpec,
    initializeIdentityRuntimeTables,
    introspect_token_record,
    mark_refresh_token_rotated,
    persist_issued_token,
    revoke_refresh_token_family,
)


def _activate(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables((TokenRecordRuntimeSpec,))
    runtime_handlers = TokenRecord.handlers
    handlers = storage.handlers_for(TokenRecord)
    for name, value in vars(runtime_handlers).items():
        if not hasattr(handlers, name):
            setattr(handlers, name, value)
    monkeypatch.setattr(TokenRecord, "handlers", handlers, raising=False)


async def _persist(storage, **payload):
    return await persist_issued_token({"payload": payload, "db": storage})


@pytest.mark.asyncio
async def test_profiled_token_lifecycle_is_runtime_owned(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    now = dt.datetime.now(dt.timezone.utc)
    access = await _persist(
        administrator_storage,
        token_hash="access-digest",
        token_kind="access",
        token_profile="oauth-access-token",
        sender_constraint_kind="dpop",
        claims={
            "sub": "alice",
            "scope": "openid profile",
            "iss": "https://issuer.example",
            "exp": int((now + dt.timedelta(minutes=5)).timestamp()),
        },
    )
    assert access["token_profile"] == "oauth-access-token"
    assert access["sender_constraint_kind"] == "dpop"
    introspected = await introspect_token_record(
        {
            "payload": {"token_hash": "access-digest"},
            "db": administrator_storage,
        }
    )
    assert introspected["active"] is True
    assert introspected["sub"] == "alice"
    assert introspected["scope"] == "openid profile"

    family = "family-a"
    await _persist(
        administrator_storage,
        token_hash="refresh-one",
        token_kind="refresh",
        token_profile="oauth-refresh-token",
        refresh_family_id=family,
        claims={"sub": "alice"},
    )
    await _persist(
        administrator_storage,
        token_hash="refresh-two",
        token_kind="refresh",
        token_profile="oauth-refresh-token",
        refresh_family_id=family,
        claims={"sub": "alice"},
    )
    rotated = await mark_refresh_token_rotated(
        {
            "payload": {
                "token_hash": "refresh-one",
                "successor_hash": "refresh-two",
            },
            "db": administrator_storage,
        }
    )
    assert rotated["active"] is False
    assert rotated["token_status"] == "rotated"
    assert rotated["refresh_successor_hash"] == "refresh-two"

    revoked = await revoke_refresh_token_family(
        {
            "payload": {
                "refresh_family_id": family,
                "reuse_token_hash": "refresh-one",
            },
            "db": administrator_storage,
        }
    )
    assert len(revoked) == 2
    assert all(row["token_status"] == "revoked" for row in revoked)
    reused = next(row for row in revoked if row["token_hash"] == "refresh-one")
    assert reused["reuse_detected_at"] is not None


@pytest.mark.asyncio
async def test_expired_token_introspection_fails_closed(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    await _persist(
        administrator_storage,
        token_hash="expired-digest",
        token_kind="access",
        token_profile="oauth-access-token",
        expires_at=dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=1),
        claims={"sub": "alice"},
    )
    assert await introspect_token_record(
        {
            "payload": {"token_hash": "expired-digest"},
            "db": administrator_storage,
        }
    ) == {"active": False}


def test_token_record_runtime_spec_preserves_operation_identity() -> None:
    operations = {
        operation.alias: operation
        for operation in TokenRecordRuntimeSpec.ops
        if operation.extra.get("owner_layer") == "30-storage-runtime"
    }
    assert set(operations) == {
        "introspect",
        "mark_rotated",
        "persist_issued",
        "revoke_family",
    }
    assert all(operation.arity == "collection" for operation in operations.values())
