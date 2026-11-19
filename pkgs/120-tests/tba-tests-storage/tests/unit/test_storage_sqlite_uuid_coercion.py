from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from tigrbl import (
    delete_table_record,
    list_table_records,
    read_table_record,
    update_table_record,
)


class _Core:
    def __init__(self, func):
        self.core = func


@pytest.mark.unit
@pytest.mark.asyncio
async def test_bound_record_list_preserves_schema_materialized_filters():
    session_id = uuid4()
    captured: dict[str, object] = {}

    async def list_core(ctx):
        captured.update(ctx["payload"]["filters"])
        return [SimpleNamespace(id=uuid4(), session_id=session_id)]

    model = SimpleNamespace(handlers=SimpleNamespace(list=_Core(list_core)))

    rows = await list_table_records(
        model,
        db=object(),
        filters={"session_id": str(session_id)},
    )

    assert rows
    assert captured["session_id"] == str(session_id)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_bound_record_ops_preserve_schema_materialized_identifiers():
    row_id = uuid4()
    captured: dict[str, object] = {}

    async def read_core(ctx):
        captured["read"] = ctx["path_params"]["record_key"]
        return SimpleNamespace(id=row_id)

    async def update_core(ctx):
        captured["update"] = ctx["path_params"]["record_key"]
        return SimpleNamespace(item=SimpleNamespace(id=row_id))

    async def delete_core(ctx):
        captured["delete"] = ctx["path_params"]["record_key"]
        return None

    model = SimpleNamespace(
        __table__=SimpleNamespace(
            primary_key=SimpleNamespace(columns=(SimpleNamespace(name="record_key"),))
        ),
        ops=SimpleNamespace(
            by_alias={
                alias: SimpleNamespace(target=alias)
                for alias in ("read", "update", "delete")
            }
        ),
        handlers=SimpleNamespace(
            read=_Core(read_core),
            update=_Core(update_core),
            delete=_Core(delete_core),
        ),
    )

    await read_table_record(model, db=object(), ident=str(row_id))
    await update_table_record(model, db=object(), ident=str(row_id), payload={})
    await delete_table_record(model, db=object(), ident=str(row_id))

    assert captured == {
        "read": str(row_id),
        "update": str(row_id),
        "delete": str(row_id),
    }
