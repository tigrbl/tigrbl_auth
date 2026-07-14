from __future__ import annotations

from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from tigrbl_identity_storage_runtime.ops import common as table_ops
from tigrbl_identity_storage_runtime.ops.common import normalize_uuid_filters


class _Core:
    def __init__(self, func):
        self.core = func


@pytest.mark.unit
@pytest.mark.asyncio
async def test_handler_records_coerce_string_uuid_filters_before_list():
    session_id = uuid4()
    captured: dict[str, object] = {}

    async def list_core(ctx):
        captured.update(ctx["payload"]["filters"])
        return [SimpleNamespace(id=uuid4(), session_id=session_id)]

    model = SimpleNamespace(handlers=SimpleNamespace(list=_Core(list_core)))

    rows = await table_ops.list_handler_records(
        model,
        db=object(),
        filters={"session_id": str(session_id)},
    )

    assert rows
    assert captured["session_id"] == session_id
    assert isinstance(captured["session_id"], UUID)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_handler_records_coerce_string_uuid_identifiers_before_read_update_delete():
    row_id = uuid4()
    captured: dict[str, object] = {}

    async def read_core(ctx):
        captured["read"] = ctx["path_params"]["id"]
        return SimpleNamespace(id=row_id)

    async def update_core(ctx):
        captured["update"] = ctx["path_params"]["id"]
        return SimpleNamespace(item=SimpleNamespace(id=row_id))

    async def delete_core(ctx):
        captured["delete"] = ctx["path_params"]["id"]
        return None

    model = SimpleNamespace(
        handlers=SimpleNamespace(
            read=_Core(read_core),
            update=_Core(update_core),
            delete=_Core(delete_core),
        )
    )

    await table_ops.read_handler_record(model, db=object(), ident=str(row_id))
    await table_ops.update_handler_record(model, db=object(), ident=str(row_id), payload={})
    await table_ops.delete_handler_record(model, db=object(), ident=str(row_id))

    assert captured == {"read": row_id, "update": row_id, "delete": row_id}


@pytest.mark.unit
def test_uuid_filter_normalization_preserves_non_uuid_storage_keys():
    refresh_family_id = str(uuid4())
    normalized = normalize_uuid_filters(
        {
            "client_id": str(uuid4()),
            "refresh_family_id": refresh_family_id,
            "token_hash": "abc123",
        }
    )

    assert isinstance(normalized["client_id"], UUID)
    assert normalized["refresh_family_id"] == refresh_family_id
    assert isinstance(normalized["refresh_family_id"], str)
    assert normalized["token_hash"] == "abc123"
