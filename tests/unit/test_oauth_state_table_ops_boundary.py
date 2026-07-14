from __future__ import annotations


import pytest

from tigrbl_identity_storage.tables import (
    AuthCode,
    Client,
    ClientRegistration,
    PushedAuthorizationRequest,
    RevokedToken,
)
from tigrbl_identity_storage_runtime import (
    AuthCodeRuntimeSpec,
    ClientRegistrationRuntimeSpec,
    PushedAuthorizationRequestRuntimeSpec,
    RevokedTokenRuntimeSpec,
    create_client_registration,
    disable_client_registration,
    initializeIdentityRuntimeTables,
    is_token_hash_revoked,
    persist_authorization_code,
    persist_pushed_authorization_request,
    read_client_registration,
    record_revoked_token_hash,
    update_client_registration,
    upsert_client_registration,
)


def _activate_test_handlers(monkeypatch, storage) -> None:
    initializeIdentityRuntimeTables(
        (
            AuthCodeRuntimeSpec,
            ClientRegistrationRuntimeSpec,
            PushedAuthorizationRequestRuntimeSpec,
            RevokedTokenRuntimeSpec,
        )
    )
    for model in (
        AuthCode,
        Client,
        ClientRegistration,
        PushedAuthorizationRequest,
        RevokedToken,
    ):
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

    aggregate = await create_client_registration(
        {
            "payload": {
                "client_id": "00000000-0000-0000-0000-000000000301",
                "tenant_id": "00000000-0000-0000-0000-000000000201",
                "client_secret_hash": "hashed-secret",
                "redirect_uris": ("https://client.example/cb",),
                "grant_types": ("authorization_code",),
                "response_types": ("code",),
                "metadata": {"client_name": "Example"},
                "registration_access_token_hash": "hashed-access-token",
                "registration_client_uri": "https://issuer.example/register/client",
            },
            "db": administrator_storage,
        }
    )
    assert aggregate["client"]["redirect_uris"] == "https://client.example/cb"
    assert aggregate["registration"]["registration_metadata"] == {
        "client_name": "Example"
    }

    fetched = await read_client_registration(
        {
            "payload": {"client_id": aggregate["client"]["id"]},
            "db": administrator_storage,
        }
    )
    assert fetched is not None
    assert fetched["registration"]["registration_access_token_hash"] == (
        "hashed-access-token"
    )

    changed = await update_client_registration(
        {
            "payload": {
                "client_id": aggregate["client"]["id"],
                "redirect_uris": ("https://client.example/new",),
                "grant_types": ("authorization_code", "refresh_token"),
                "response_types": ("code",),
                "metadata": {"client_name": "Changed"},
            },
            "db": administrator_storage,
        }
    )
    assert changed["client"]["redirect_uris"] == "https://client.example/new"
    assert changed["registration"]["registration_access_token_hash"] == (
        "hashed-access-token"
    )

    disabled = await disable_client_registration(
        {
            "payload": {"client_id": aggregate["client"]["id"]},
            "db": administrator_storage,
        }
    )
    assert disabled["client"]["is_active"] is False
    assert disabled["registration"]["disabled_at"] is not None

    pushed = await persist_pushed_authorization_request(
        {
            "payload": {
                "client_id": "00000000-0000-0000-0000-000000000101",
                "tenant_id": "00000000-0000-0000-0000-000000000201",
                "params": {"scope": "openid", "redirect_uri": "https://client.example/cb"},
                "request_uri": "urn:ietf:params:oauth:request_uri:example",
                "expires_in": 90,
            },
            "db": administrator_storage,
        }
    )
    assert pushed["params"] == {
        "scope": "openid",
        "redirect_uri": "https://client.example/cb",
    }
    assert pushed["request_uri"] == "urn:ietf:params:oauth:request_uri:example"

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
            PushedAuthorizationRequestRuntimeSpec,
            RevokedTokenRuntimeSpec,
        )
    }
    assert operations == {
        "AuthCode": {"authorize"},
        "ClientRegistration": {
            "disable_registration",
            "get_registration",
            "register",
            "update_registration",
            "upsert",
        },
        "PushedAuthorizationRequest": {"push_authorization_request"},
        "RevokedToken": {"is_hash_revoked", "record_hash"},
    }


@pytest.mark.asyncio
async def test_pushed_authorization_persistence_rejects_unnormalized_shape(
    administrator_storage,
) -> None:
    with pytest.raises(ValueError, match="requires client_id"):
        await persist_pushed_authorization_request(
            {"payload": {"params": {}}, "db": administrator_storage}
        )
    with pytest.raises(TypeError, match="params must be a mapping"):
        await persist_pushed_authorization_request(
            {
                "payload": {"client_id": "client-a", "params": "openid"},
                "db": administrator_storage,
            }
        )
