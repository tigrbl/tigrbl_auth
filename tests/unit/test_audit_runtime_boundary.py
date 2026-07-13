from __future__ import annotations

import uuid

import pytest

from tigrbl_identity_storage.tables import AuditEvent, Tenant
from tigrbl_identity_storage_runtime import (
    AuditEventRuntimeSpec,
    append_audit_event_record,
    create_table_record,
    initializeIdentityRuntimeTables,
    list_audit_event_records,
)


def _activate(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables((AuditEventRuntimeSpec,))
    for model in (AuditEvent, Tenant):
        runtime_handlers = model.handlers
        handlers = storage.handlers_for(model)
        for name, value in vars(runtime_handlers).items():
            if not hasattr(handlers, name):
                setattr(handlers, name, value)
        monkeypatch.setattr(model, "handlers", handlers, raising=False)


@pytest.mark.asyncio
async def test_audit_append_uses_explicit_tenant(monkeypatch, administrator_storage) -> None:
    _activate(monkeypatch, administrator_storage)
    tenant_id = uuid.uuid4()
    event = await append_audit_event_record(
        {
            "payload": {
                "tenant_id": tenant_id,
                "event_type": "identity.updated",
                "target_type": "identity",
                "target_id": "alice",
            },
            "db": administrator_storage,
        }
    )
    assert event["tenant_id"] == tenant_id
    assert event["event_type"] == "identity.updated"


@pytest.mark.asyncio
async def test_audit_append_preserves_tenant_fallback(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    tenant = await create_table_record(
        Tenant,
        administrator_storage,
        {"id": uuid.uuid4(), "slug": "default", "name": "Default"},
    )
    event = await append_audit_event_record(
        {
            "payload": {"event_type": "token.revoked"},
            "db": administrator_storage,
        }
    )
    assert event["tenant_id"] == tenant["id"]


@pytest.mark.asyncio
async def test_audit_list_filters_records(monkeypatch, administrator_storage) -> None:
    _activate(monkeypatch, administrator_storage)
    for event_type in ("token.issued", "token.revoked", "token.revoked"):
        await append_audit_event_record(
            {
                "payload": {"event_type": event_type},
                "db": administrator_storage,
            }
        )
    events = await list_audit_event_records(
        {
            "payload": {"event_type": "token.revoked"},
            "db": administrator_storage,
        }
    )
    assert len(events) == 2
    assert all(event["event_type"] == "token.revoked" for event in events)


def test_audit_runtime_spec_and_layer01_boundary() -> None:
    operations = {
        operation.alias: operation
        for operation in AuditEventRuntimeSpec.ops
        if operation.extra.get("owner_layer") == "30-storage-runtime"
    }
    assert set(operations) == {"append", "list_events"}
    assert operations["append"].tx_scope == "read_write"
    assert operations["list_events"].tx_scope == "read_only"
    assert not hasattr(AuditEvent, "append_audit_event")
    assert not hasattr(AuditEvent, "append_audit_event_async")
