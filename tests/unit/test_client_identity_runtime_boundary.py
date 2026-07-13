from __future__ import annotations

import uuid

import pytest

from tigrbl_identity_storage.tables import Client, User
from tigrbl_identity_storage_runtime import (
    ClientRuntimeSpec,
    UserRuntimeSpec,
    create_table_record,
    disable_client,
    enable_client,
    initializeIdentityRuntimeTables,
    lookup_client,
    lookup_identity_by_identifier,
    replace_client_secret_hash,
    replace_password_hash,
    set_identity_enabled,
)


def _activate(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables((ClientRuntimeSpec, UserRuntimeSpec))
    for model in (Client, User):
        runtime_handlers = model.handlers
        handlers = storage.handlers_for(model)
        for name, value in vars(runtime_handlers).items():
            if not hasattr(handlers, name):
                setattr(handlers, name, value)
        monkeypatch.setattr(model, "handlers", handlers, raising=False)


@pytest.mark.asyncio
async def test_client_record_lifecycle_is_runtime_owned(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    client_id = uuid.uuid4()
    await create_table_record(
        Client,
        administrator_storage,
        {
            "id": client_id,
            "tenant_id": uuid.uuid4(),
            "name": "runtime-client",
            "client_secret_hash": b"old-hash",
            "redirect_uris": "https://client.example/callback",
            "is_active": True,
        },
    )
    context = {"payload": {"client_id": client_id}, "db": administrator_storage}

    assert (await lookup_client(context))["id"] == client_id
    assert (await disable_client(context))["is_active"] is False
    assert (await enable_client(context))["is_active"] is True
    rotated = await replace_client_secret_hash(
        {**context, "payload": {"client_id": client_id, "client_secret_hash": b"new-hash"}}
    )
    assert rotated["client_secret_hash"] == b"new-hash"


@pytest.mark.asyncio
async def test_identity_lookup_and_password_state_are_runtime_owned(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    identity_id = uuid.uuid4()
    await create_table_record(
        User,
        administrator_storage,
        {
            "id": identity_id,
            "tenant_id": uuid.uuid4(),
            "username": "alice",
            "email": "alice@example.test",
            "password_hash": b"old-hash",
            "is_active": True,
        },
    )

    by_username = await lookup_identity_by_identifier(
        {"payload": {"identifier": "alice"}, "db": administrator_storage}
    )
    by_email = await lookup_identity_by_identifier(
        {"payload": {"identifier": "alice@example.test"}, "db": administrator_storage}
    )
    assert by_username["id"] == identity_id
    assert by_email["id"] == identity_id

    replaced = await replace_password_hash(
        {
            "payload": {"identity_id": identity_id, "password_hash": b"new-hash"},
            "db": administrator_storage,
        }
    )
    assert replaced["password_hash"] == b"new-hash"
    await set_identity_enabled(
        {
            "payload": {"identity_id": identity_id, "enabled": False},
            "db": administrator_storage,
        }
    )
    assert await lookup_identity_by_identifier(
        {"payload": {"identifier": "alice"}, "db": administrator_storage}
    ) is None


def test_client_and_identity_runtime_operation_identity() -> None:
    client_ops = {
        operation.alias: operation
        for operation in ClientRuntimeSpec.ops
        if operation.extra.get("owner_layer") == "30-storage-runtime"
    }
    identity_ops = {
        operation.alias: operation
        for operation in UserRuntimeSpec.ops
        if operation.extra.get("owner_layer") == "30-storage-runtime"
    }
    assert set(client_ops) == {"lookup_client", "enable", "disable", "rotate_secret_hash"}
    assert client_ops["lookup_client"].tx_scope == "read_only"
    assert client_ops["enable"].arity == "member"
    assert set(identity_ops) == {"lookup_by_identifier", "replace_password_hash", "set_enabled"}
    assert not hasattr(Client, "verify_secret")
    assert not hasattr(Client, "authenticate")
    assert not hasattr(Client, "rotate_secret")
