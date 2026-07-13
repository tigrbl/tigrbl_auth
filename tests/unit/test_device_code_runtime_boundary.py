from __future__ import annotations

import datetime as dt
import uuid

import pytest

from tigrbl_identity_storage.tables import DeviceCode
from tigrbl_identity_storage_runtime import (
    DeviceCodeRuntimeSpec,
    approve_device_code,
    create_table_record,
    deny_device_code,
    initializeIdentityRuntimeTables,
)


def _activate(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables((DeviceCodeRuntimeSpec,))
    runtime_handlers = DeviceCode.handlers
    handlers = storage.handlers_for(DeviceCode)
    for name, value in vars(runtime_handlers).items():
        if not hasattr(handlers, name):
            setattr(handlers, name, value)
    monkeypatch.setattr(DeviceCode, "handlers", handlers, raising=False)


async def _device_code(storage):
    return await create_table_record(
        DeviceCode,
        storage,
        {
            "device_code": "device-secret",
            "user_code": "ABCD-EFGH",
            "client_id": uuid.uuid4(),
            "expires_at": dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=5),
            "interval": 5,
            "authorized": False,
        },
    )


@pytest.mark.asyncio
async def test_device_code_approval_and_denial_are_runtime_owned(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    row = await _device_code(administrator_storage)
    user_id = uuid.uuid4()
    tenant_id = uuid.uuid4()

    approved = await approve_device_code(
        {
            "payload": {
                "device_code": row["device_code"],
                "sub": user_id,
                "tid": tenant_id,
            },
            "db": administrator_storage,
        }
    )
    assert approved["authorized"] is True
    assert approved["authorized_at"] is not None
    assert approved["user_id"] == user_id
    assert approved["tenant_id"] == tenant_id

    denied = await deny_device_code(
        {
            "payload": {"id": row["id"]},
            "db": administrator_storage,
        }
    )
    assert denied["authorized"] is False
    assert denied["denied_at"] is not None
    assert denied["denial_reason"] == "access_denied"


@pytest.mark.asyncio
async def test_device_code_transition_without_identity_is_noop(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    assert await approve_device_code(
        {"payload": {}, "db": administrator_storage}
    ) is None
    assert await deny_device_code(
        {"payload": {"device_code": "missing"}, "db": administrator_storage}
    ) is None


def test_device_code_runtime_spec_preserves_operation_identity() -> None:
    operations = {
        operation.alias: operation
        for operation in DeviceCodeRuntimeSpec.ops
        if operation.extra.get("owner_layer") == "30-storage-runtime"
    }
    assert set(operations) == {"approve", "deny"}
    assert all(operation.arity == "collection" for operation in operations.values())
    assert not hasattr(DeviceCode, "approve")
    assert not hasattr(DeviceCode, "deny")
