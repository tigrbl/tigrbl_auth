from __future__ import annotations


import pytest

from tigrbl_identity_storage.tables import AuthCode, ClientRegistration, RevokedToken
from tigrbl_identity_storage_runtime import (
    AuthCodeRuntimeSpec,
    ClientRegistrationRuntimeSpec,
    RevokedTokenRuntimeSpec,
    initializeIdentityRuntimeTables,
    is_token_hash_revoked,
    persist_authorization_code,
    record_revoked_token_hash,
    upsert_client_registration,
)


def _activate_test_handlers(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables(
        (
            AuthCodeRuntimeSpec,
            ClientRegistrationRuntimeSpec,
            RevokedTokenRuntimeSpec,
        )
    )
    for model in (AuthCode, ClientRegistration, RevokedToken):
        runtime_handlers = model.handlers
        handlers = storage.handlers_for(model)
        for name, value in vars(runtime_handlers).items():
            if not hasattr(handlers, name):
                setattr(handlers, name, value)
        monkeypatch.setattr(model, "handlers", handlers, raising=False)


@pytest.mark.asyncio
async def test_oauth_durable_state_operations_are_runtime_owned(
    monkeypatch,
    administrator_storage,
) -> None:
    _activate_test_handlers(monkeypatch, administrator_storage)

    code = await persist_authorization_code(
        {"payload": {"client_id": "client-a", "scope": "openid"}, "db": administrator_storage}
    )
    assert code["client_id"] == "client-a"

    registration = await upsert_client_registration(
        {
            "payload": {
                "client_id": "client-a",
                "contacts": ["first@example.com"],
                "metadata": {"token_endpoint_auth_method": "private_key_jwt"},
            },
            "db": administrator_storage,
        }
    )
    updated = await upsert_client_registration(
        {
            "payload": {
                "client_id": "client-a",
                "contacts": ["second@example.com"],
            },
            "db": administrator_storage,
        }
    )
    assert updated["id"] == registration["id"]
    assert updated["contacts"] == ["second@example.com"]
    assert updated["registration_metadata"] == {
        "token_endpoint_auth_method": "private_key_jwt"
    }

    assert not await is_token_hash_revoked(
        {"payload": {"token_hash": "digest-a"}, "db": administrator_storage}
    )
    recorded = await record_revoked_token_hash(
        {
            "payload": {"token_hash": "digest-a", "reason": "logout"},
            "db": administrator_storage,
        }
    )
    assert recorded["revoked_reason"] == "logout"
    assert await is_token_hash_revoked(
        {"payload": {"token_hash": "digest-a"}, "db": administrator_storage}
    )


def test_oauth_runtime_specs_expose_expected_custom_operations() -> None:
    operations = {
        spec.model.__name__: {
            operation.alias
            for operation in spec.ops
            if operation.extra.get("owner_layer") == "30-storage-runtime"
        }
        for spec in (
            AuthCodeRuntimeSpec,
            ClientRegistrationRuntimeSpec,
            RevokedTokenRuntimeSpec,
        )
    }
    assert operations == {
        "AuthCode": {"authorize"},
        "ClientRegistration": {"upsert"},
        "RevokedToken": {"is_hash_revoked", "record_hash"},
    }
