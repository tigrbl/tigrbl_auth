from __future__ import annotations

from types import SimpleNamespace

import pytest

from tigrbl_identity_storage.tables.token_record import _op as token_runtime
from tigrbl_identity_storage.tables.token_record._op import _persistence as token_persistence
from tigrbl_identity_server.security import handler_records


def test_storage_token_service_uses_provider_object_protocol():
    source = token_persistence.__loader__.get_source(token_persistence.__name__)

    assert "class TokenCoder(Protocol)" in source
    assert "from tigrbl_identity_jose" not in source
    assert "jwt: TokenCoder" in source


@pytest.mark.asyncio
async def test_load_client_defaults_registration_when_optional_store_is_absent(monkeypatch):
    client = SimpleNamespace(id="client-a")

    async def read_client(_model, _db, _client_id):
        return client

    async def missing_registration_store(_model, _db, _filters):
        raise AttributeError("'DummyDB' object has no attribute 'execute'")

    monkeypatch.setattr(token_runtime, "read_handler_record", read_client)
    monkeypatch.setattr(token_runtime, "first_handler_record", missing_registration_store)

    loaded, registration = await token_runtime._load_client(object(), "client-a")

    assert loaded is client
    assert registration is None
    assert token_runtime._registered_token_endpoint_auth_method(registration) == "client_secret_basic"


@pytest.mark.asyncio
async def test_issue_token_pair_records_decodes_minted_tokens_without_revocation(monkeypatch):
    class FakeJWT:
        def __init__(self):
            self.decode_kwargs = []

        async def async_sign_pair(self, **_kwargs):
            return "access-token", "refresh-token"

        async def async_decode(self, token, **kwargs):
            self.decode_kwargs.append((token, kwargs))
            return {"sub": "subject", "tid": "tenant"}

    created: list[tuple[str, dict]] = []

    async def record_token(_db, token, claims, **_kwargs):
        created.append((token, claims))

    jwt = FakeJWT()
    monkeypatch.setattr(handler_records, "create_token_record", record_token)

    access, refresh = await handler_records.issue_token_pair_records(
        object(),
        jwt=jwt,
        sub="subject",
        tid="tenant",
        client_id="client-a",
    )

    assert (access, refresh) == ("access-token", "refresh-token")
    assert [token for token, _claims in created] == ["access-token", "refresh-token"]
    assert [kwargs["verify_revocation"] for _token, kwargs in jwt.decode_kwargs] == [False, False]


@pytest.mark.asyncio
async def test_issue_persisted_token_pair_decodes_minted_tokens_without_revocation(monkeypatch):
    class FakeJWT:
        def __init__(self):
            self.decode_kwargs = []

        async def async_sign_pair(self, **_kwargs):
            return "access-token", "refresh-token"

        async def async_decode(self, token, **kwargs):
            self.decode_kwargs.append((token, kwargs))
            return {"sub": "subject", "tid": "tenant"}

    persisted: list[tuple[str, dict]] = []

    async def upsert_token_record_async(token, claims, **_kwargs):
        persisted.append((token, claims))

    monkeypatch.setattr(
        "tigrbl_identity_storage.tables.token_record._op.upsert_token_record_async",
        upsert_token_record_async,
    )
    monkeypatch.setattr("tigrbl_identity_storage.tables._ops.token_hash", lambda token: f"hash:{token}")

    jwt = FakeJWT()
    access, refresh = await token_persistence.issue_persisted_token_pair(
        jwt=jwt,
        sub="subject",
        tid="tenant",
        client_id="client-a",
    )

    assert (access, refresh) == ("access-token", "refresh-token")
    assert [token for token, _claims in persisted] == ["access-token", "refresh-token"]
    assert [kwargs["verify_revocation"] for _token, kwargs in jwt.decode_kwargs] == [False, False]
