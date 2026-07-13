from __future__ import annotations

import datetime as dt
import uuid

import pytest

from tigrbl_identity_storage.tables import AuthSession, Consent, LogoutState
from tigrbl_identity_storage_runtime import (
    AuthSessionRuntimeSpec,
    ConsentRuntimeSpec,
    LogoutStateRuntimeSpec,
    bind_session_client,
    create_table_record,
    ensure_logout_for_session,
    get_active_session,
    initializeIdentityRuntimeTables,
    latest_logout_for_session,
    list_consents_for_user,
    mark_logout_channel,
    revoke_consent_for_user,
    revoke_consents_for_client,
    rotate_session_cookie_secret,
    terminate_session,
    touch_session,
    update_logout_metadata,
)


def _activate(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables(
        (AuthSessionRuntimeSpec, ConsentRuntimeSpec, LogoutStateRuntimeSpec)
    )
    for model in (AuthSession, Consent, LogoutState):
        runtime_handlers = model.handlers
        handlers = storage.handlers_for(model)
        for name, value in vars(runtime_handlers).items():
            if not hasattr(handlers, name):
                setattr(handlers, name, value)
        monkeypatch.setattr(model, "handlers", handlers, raising=False)


@pytest.mark.asyncio
async def test_session_lifecycle_is_runtime_owned(monkeypatch, administrator_storage) -> None:
    _activate(monkeypatch, administrator_storage)
    session = await create_table_record(
        AuthSession,
        administrator_storage,
        {
            "session_state": "active",
            "cookie_issued_at": None,
            "expires_at": dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1),
        },
    )
    context = {
        "path_params": {"id": session["id"]},
        "payload": {},
        "db": administrator_storage,
    }

    assert await get_active_session(context) == session
    touched = await touch_session(context)
    assert touched["last_seen_at"] is not None
    bound = await bind_session_client(
        {**context, "payload": {"client_id": "client-a"}}
    )
    assert bound["client_id"] == "client-a"
    rotated = await rotate_session_cookie_secret(
        {**context, "payload": {"cookie_secret_hash": "digest-a"}}
    )
    assert rotated["cookie_secret_hash"] == "digest-a"
    assert rotated["cookie_issued_at"] is not None
    terminated = await terminate_session(
        {**context, "payload": {"reason": "logout"}}
    )
    assert terminated["session_state"] == "terminated"
    assert terminated["ended_at"] is not None
    assert await get_active_session(context) is None


@pytest.mark.asyncio
async def test_consent_lifecycle_is_runtime_owned(monkeypatch, administrator_storage) -> None:
    _activate(monkeypatch, administrator_storage)
    tenant_id = uuid.uuid4()
    user_id = uuid.uuid4()
    client_id = uuid.uuid4()
    other_client_id = uuid.uuid4()
    first = await create_table_record(
        Consent,
        administrator_storage,
        {
            "id": uuid.uuid4(),
            "tenant_id": tenant_id,
            "user_id": user_id,
            "client_id": client_id,
            "state": "active",
        },
    )
    await create_table_record(
        Consent,
        administrator_storage,
        {
            "id": uuid.uuid4(),
            "tenant_id": tenant_id,
            "user_id": user_id,
            "client_id": client_id,
            "state": "active",
        },
    )
    await create_table_record(
        Consent,
        administrator_storage,
        {
            "id": uuid.uuid4(),
            "tenant_id": tenant_id,
            "user_id": user_id,
            "client_id": other_client_id,
            "state": "active",
        },
    )

    principal = {
        "payload": {"tenant_id": str(tenant_id), "user_id": str(user_id)},
        "db": administrator_storage,
    }
    assert len(await list_consents_for_user(principal)) == 3
    revoked = await revoke_consent_for_user(
        {**principal, "path_params": {"id": first["id"]}}
    )
    assert revoked["state"] == "revoked"
    revoked_for_client = await revoke_consents_for_client(
        {
            **principal,
            "path_params": {"client_id": str(client_id)},
        }
    )
    assert len(revoked_for_client) == 2
    assert all(row["revoked_at"] is not None for row in revoked_for_client)


@pytest.mark.asyncio
async def test_logout_propagation_is_runtime_owned(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate(monkeypatch, administrator_storage)
    session_id = uuid.uuid4()
    context = {
        "payload": {
            "session_id": session_id,
            "frontchannel_required": True,
            "backchannel_required": True,
        },
        "db": administrator_storage,
    }
    logout = await ensure_logout_for_session(context)
    assert logout["status"] == "pending"
    assert await latest_logout_for_session(context) == logout

    updated = await update_logout_metadata(
        {
            "payload": {
                "logout_id": logout["id"],
                "metadata": {"initiator": "rp"},
            },
            "db": administrator_storage,
        }
    )
    assert updated["logout_metadata"] == {"initiator": "rp"}
    front = await mark_logout_channel(
        {
            "payload": {"logout_id": logout["id"], "channel": "frontchannel"},
            "db": administrator_storage,
        }
    )
    assert front["status"] == "pending"
    complete = await mark_logout_channel(
        {
            "payload": {"logout_id": logout["id"], "channel": "backchannel"},
            "db": administrator_storage,
        }
    )
    assert complete["status"] == "complete"
    assert complete["propagated_at"] is not None


def test_runtime_specs_preserve_operation_arity_and_schemas() -> None:
    session_ops = {operation.alias: operation for operation in AuthSessionRuntimeSpec.ops}
    consent_ops = {operation.alias: operation for operation in ConsentRuntimeSpec.ops}
    logout_ops = {operation.alias: operation for operation in LogoutStateRuntimeSpec.ops}

    assert session_ops["terminate"].arity == "member"
    assert session_ops["touch"].arity == "member"
    assert session_ops["get_active"].arity == "member"
    assert session_ops["rotate_cookie_secret"].arity == "member"
    assert session_ops["bind_client"].arity == "member"
    assert consent_ops["list_for_user"].response_model is Consent.schemas.list.out
    assert consent_ops["revoke_for_user"].arity == "member"
    assert consent_ops["revoke_for_user"].response_model is Consent.schemas.update.out
    assert logout_ops["update_metadata"].arity == "member"
    assert logout_ops["mark_channel"].arity == "member"
