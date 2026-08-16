from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

import tigrbl_identity_server.security.handler_records as handler_records

from tigrbl_identity_server.security.handler_records import (
    delete_handler_record,
    read_handler_record,
    update_handler_record,
)


@pytest.mark.asyncio
async def test_read_handler_record_prefers_session_get() -> None:
    ident = uuid4()
    row = SimpleNamespace(id=ident)

    class Db:
        async def get(self, model, value):
            assert model is Model
            assert value == ident
            return row

    class _Read:
        @staticmethod
        async def core(envelope):
            raise AssertionError("handler read should not be used when db.get resolves")

    class Model:
        handlers = SimpleNamespace(read=_Read)

    assert await read_handler_record(Model, Db(), ident) is row


@pytest.mark.asyncio
async def test_update_handler_record_prefers_session_get_and_flushes() -> None:
    ident = uuid4()
    row = SimpleNamespace(id=ident, last_seen_at=None, ignored=None)
    flushed = False

    class Db:
        async def get(self, model, value):
            assert model is Model
            assert value == ident
            return row

        async def flush(self):
            nonlocal flushed
            flushed = True

    class _Update:
        @staticmethod
        async def core(envelope):
            raise AssertionError("handler update should not be used when db.get resolves")

    class Model:
        handlers = SimpleNamespace(update=_Update)

    payload = {"last_seen_at": "now", "missing_column": "ignored"}

    assert await update_handler_record(Model, Db(), ident, payload) is row
    assert row.last_seen_at == "now"
    assert not hasattr(row, "missing_column")
    assert flushed is True


@pytest.mark.parametrize(("update_last_seen", "expected_updates"), ((True, 1), (False, 0)))
@pytest.mark.asyncio
async def test_browser_session_resolution_can_skip_last_seen_flush(
    monkeypatch,
    update_last_seen: bool,
    expected_updates: int,
) -> None:
    session_id = uuid4()
    row = SimpleNamespace(
        id=session_id,
        ended_at=None,
        session_state="active",
        expires_at=None,
        cookie_secret_hash=None,
        last_seen_at=None,
    )
    updates: list[dict[str, object]] = []

    monkeypatch.setattr(
        handler_records,
        "parse_session_cookie_value",
        lambda value: SimpleNamespace(session_id=session_id, secret=None),
    )
    monkeypatch.setattr(handler_records, "extract_session_cookie", lambda request: "cookie")

    async def _read(model, db, ident):
        assert ident == session_id
        return row

    async def _update(model, db, ident, payload):
        assert ident == session_id
        updates.append(dict(payload))
        return row

    monkeypatch.setattr(handler_records, "read_handler_record", _read)
    monkeypatch.setattr(handler_records, "update_handler_record", _update)
    deployment = SimpleNamespace(flag_enabled=lambda name: True)

    resolved = await handler_records.resolve_browser_session_record(
        object(),
        object(),
        deployment=deployment,
        update_last_seen=update_last_seen,
    )

    assert resolved is row
    assert len(updates) == expected_updates
    if update_last_seen:
        assert updates[0]["last_seen_at"] is not None
    else:
        assert row.last_seen_at is None


@pytest.mark.asyncio
async def test_delete_handler_record_prefers_session_get_and_flushes() -> None:
    ident = uuid4()
    row = SimpleNamespace(id=ident)
    deleted_rows: list[object] = []
    flushed = False

    class Db:
        async def get(self, model, value):
            assert model is Model
            assert value == ident
            return row

        async def delete(self, value):
            deleted_rows.append(value)

        async def flush(self):
            nonlocal flushed
            flushed = True

    class _Delete:
        @staticmethod
        async def core(envelope):
            raise AssertionError("handler delete should not be used when db.get resolves")

    class Model:
        handlers = SimpleNamespace(delete=_Delete)

    assert await delete_handler_record(Model, Db(), ident) is row
    assert deleted_rows == [row]
    assert flushed is True
