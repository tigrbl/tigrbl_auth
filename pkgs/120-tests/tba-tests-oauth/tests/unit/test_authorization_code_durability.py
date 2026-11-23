"""Transaction and binding checks for an already-validated authorization code."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from threading import Barrier
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.schema import CreateTable

from tba_durability_oauth_state import consume_authorization_code
from tba_storage_oauth.tables import AuthCode


@pytest.fixture
def code_store(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'oauth.db'}",
        execution_options={"schema_translate_map": {"authn": None}},
    )
    table = AuthCode.__table__
    now = datetime.now(timezone.utc)
    binding = {
        "code_id": uuid4(),
        "tenant_id": uuid4(),
        "client_id": uuid4(),
        "redirect_uri": "https://client.example/callback",
        "code_challenge": "authenticated-code-challenge",
    }
    row = {
        key: value for key, value in binding.items() if key != "code_id"
    }
    with engine.begin() as db:
        db.execute(CreateTable(table, include_foreign_key_constraints=[]))
        db.execute(table.insert().values(
            **row,
            id=binding["code_id"],
            user_id=uuid4(),
            created_at=now,
            updated_at=now,
            expires_at=now + timedelta(minutes=5),
        ))
    try:
        yield engine, binding
    finally:
        engine.dispose()


def consume(db, binding):
    return asyncio.run(consume_authorization_code({"db": db, "payload": binding}))


@pytest.mark.unit
def test_authorization_code_can_be_consumed_only_once_across_transactions(code_store):
    engine, binding = code_store
    ready = Barrier(2, timeout=10)

    def redeem():
        with engine.begin() as db:
            ready.wait()
            return consume(db, binding)

    with ThreadPoolExecutor(max_workers=2) as workers:
        attempts = [workers.submit(redeem) for _ in range(2)]
        assert sorted(attempt.result(timeout=15) for attempt in attempts) == [False, True]


@pytest.mark.unit
@pytest.mark.parametrize(
    "field,value",
    [
        ("tenant_id", uuid4()),
        ("client_id", uuid4()),
        ("redirect_uri", "https://client.example/other"),
        ("code_challenge", "another-challenge"),
    ],
)
def test_code_stays_available_after_mismatched_binding(code_store, field, value):
    engine, binding = code_store
    with engine.begin() as db:
        assert not consume(db, {**binding, field: value})
    with engine.begin() as db:
        assert consume(db, binding)


@pytest.mark.unit
def test_expired_code_is_not_consumed(code_store):
    engine, binding = code_store
    table = AuthCode.__table__
    with engine.begin() as db:
        db.execute(table.update().values(expires_at=datetime.now(timezone.utc) - timedelta(seconds=1)))
        assert not consume(db, binding)
        assert db.execute(select(table.c.id)).scalar_one() == binding["code_id"]


@pytest.mark.unit
def test_rollback_after_consumption_preserves_code(code_store):
    engine, binding = code_store
    with pytest.raises(RuntimeError, match="token creation failed"):
        with engine.begin() as db:
            assert consume(db, binding)
            raise RuntimeError("token creation failed")
    with engine.begin() as db:
        assert consume(db, binding)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_consumption_accepts_an_async_database_connection(code_store):
    engine, binding = code_store
    async_engine = create_async_engine(
        engine.url.set(drivername="sqlite+aiosqlite"),
        execution_options={"schema_translate_map": {"authn": None}},
    )
    try:
        async with async_engine.begin() as db:
            assert await consume_authorization_code({"db": db, "payload": binding})
        async with async_engine.begin() as db:
            assert not await consume_authorization_code({"db": db, "payload": binding})
    finally:
        await async_engine.dispose()
