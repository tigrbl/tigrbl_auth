from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

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
