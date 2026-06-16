from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from tigrbl_identity_server.security.handler_records import read_handler_record


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
