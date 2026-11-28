"""Verify refresh rotation against the actual token table on SQLite."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from threading import Event
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.schema import CreateTable

from tba_durability_token.operations.tokens import claim_refresh_token_rotation
from tba_storage_token.tables import TokenRecord


@pytest.fixture
def token_store(tmp_path):
    table = TokenRecord.__table__
    engine = create_engine(
        f"sqlite:///{tmp_path / 'rotation.sqlite'}",
        execution_options={"schema_translate_map": {"authn": None}},
    )
    now = datetime.now(timezone.utc)
    payload = {
        "token_hash": "current",
        "tenant_id": uuid4(),
        "client_id": uuid4(),
        "refresh_family_id": "family",
    }
    with engine.begin() as db:
        db.execute(CreateTable(table, include_foreign_key_constraints=[]))
        db.execute(
            table.insert().values(
                **payload,
                id=uuid4(),
                token_kind="refresh",
                subject="fixture-account",
                issued_at=now,
                created_at=now,
                updated_at=now,
                expires_at=now + timedelta(minutes=5),
            )
        )
    try:
        yield engine, table, payload
    finally:
        engine.dispose()


def _claim(db, binding, successor):
    return asyncio.run(
        claim_refresh_token_rotation(
            {"db": db, "payload": {**binding, "successor_hash": successor}}
        )
    )


def test_competing_sqlite_rotations_have_one_committed_successor(token_store):
    engine, table, binding = token_store
    started = Event()

    def compete():
        with engine.begin() as db:
            started.set()
            return _claim(db, binding, "competing-successor")

    with ThreadPoolExecutor(max_workers=1) as workers:
        with engine.begin() as db:
            assert _claim(db, binding, "winning-successor")
            contender = workers.submit(compete)
            assert started.wait(timeout=5)
        assert not contender.result(timeout=5)

    with engine.begin() as db:
        row = db.execute(select(table)).mappings().one()
        assert row["refresh_successor_hash"] == "winning-successor"
        assert row["used_at"] is not None
        assert row["active"] is False
        assert row["token_status"] == "rotated"


def test_failed_issuance_restores_refresh_record(token_store):
    engine, table, binding = token_store

    class IssuanceFailed(Exception):
        pass

    with pytest.raises(IssuanceFailed), engine.begin() as db:
        assert _claim(db, binding, "rolled-back-successor")
        raise IssuanceFailed

    with engine.begin() as db:
        row = db.execute(select(table)).mappings().one()
        assert row["active"] is True
        assert row["refresh_successor_hash"] is None
        assert _claim(db, binding, "successful-retry")


def test_refresh_claim_rechecks_durable_binding_and_expiry(token_store):
    engine, table, binding = token_store
    with engine.begin() as db:
        assert not _claim(db, {**binding, "client_id": uuid4()}, "wrong-client")
        assert not _claim(db, {**binding, "tenant_id": uuid4()}, "wrong-tenant")
        assert not _claim(db, {**binding, "refresh_family_id": "other"}, "wrong-family")
        db.execute(table.update().values(expires_at=datetime.now(timezone.utc)))
        assert not _claim(db, binding, "expired")
