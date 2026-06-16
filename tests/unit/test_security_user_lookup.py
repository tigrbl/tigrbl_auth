"""Tests for handler-backed user lookup helpers."""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from tigrbl_auth.security import user_lookup
from tigrbl_identity_server.security import user_lookup as identity_server_user_lookup


@pytest.fixture(params=[user_lookup, identity_server_user_lookup])
def lookup_module(request):
    return request.param


@pytest.mark.unit
@pytest.mark.asyncio
async def test_first_user_by_filters_coerces_uuid_subject_before_handler(monkeypatch, lookup_module):
    user_id = uuid.uuid4()
    user = SimpleNamespace(id=user_id, is_active=True)
    list_core = AsyncMock(return_value=[user])
    monkeypatch.setattr(lookup_module.User.handlers.list, "core", list_core)

    resolved = await lookup_module.first_user_by_filters(
        object(),
        {"id": str(user_id), "is_active": True},
    )

    assert resolved is user
    handler_filters = list_core.await_args.args[0]["payload"]["filters"]
    assert handler_filters == {"id": user_id, "is_active": True}


@pytest.mark.unit
@pytest.mark.asyncio
async def test_first_user_by_filters_keeps_non_uuid_subjects_for_mocks(monkeypatch, lookup_module):
    user = SimpleNamespace(id="user-1", is_active=True)
    list_core = AsyncMock(return_value=[user])
    monkeypatch.setattr(lookup_module.User.handlers.list, "core", list_core)

    resolved = await lookup_module.first_user_by_filters(
        object(),
        {"id": "user-1", "is_active": True},
    )

    assert resolved is user
    handler_filters = list_core.await_args.args[0]["payload"]["filters"]
    assert handler_filters == {"id": "user-1", "is_active": True}


@pytest.mark.unit
@pytest.mark.asyncio
async def test_first_user_by_filters_matches_uuid_rows_after_coercion(monkeypatch, lookup_module):
    user_id = uuid.uuid4()
    user = SimpleNamespace(id=user_id, is_active=True)
    list_core = AsyncMock(return_value={"items": [user]})
    monkeypatch.setattr(lookup_module.User.handlers.list, "core", list_core)

    resolved = await lookup_module.first_user_by_filters(
        object(),
        {"id": user_id.hex, "is_active": True},
    )

    assert resolved is user
