"""Tests for RFC 7592 client management operations."""

import uuid

import pytest

from tigrbl_auth import rfc7592
from tigrbl_auth.tables import Client
from sqlalchemy.exc import NoResultFound
from tigrbl_identity_storage_runtime.ops.common import (
    create_record,
    delete_record,
    read_record,
    update_record,
)
from tigrbl_identity_jose.key_management import hash_pw


def test_rfc7592_spec_url() -> None:
    """Module exports the specification URL."""
    assert rfc7592.RFC7592_SPEC_URL.endswith("7592")


@pytest.mark.asyncio
async def test_update_and_delete_client_via_server(db_session):
    client = await create_record(Client, db_session, {
        "tenant_id": uuid.UUID("FFFFFFFF-0000-0000-0000-000000000000"),
        "client_id": str(uuid.uuid4()),
        "client_secret_hash": hash_pw("secret"),
        "redirect_uris": "https://a.example/cb",
    })
    client_id = client.id
    await update_record(Client, db_session, client_id, {"redirect_uris": "https://b.example/cb"})
    fetched = await read_record(Client, db_session, client_id)
    assert fetched is not None
    uris = fetched.redirect_uris
    if isinstance(uris, str):
        uris = uris.split()
    assert "https://b.example/cb" in uris
    await delete_record(Client, db_session, client_id)
    with pytest.raises(NoResultFound):
        await read_record(Client, db_session, client_id)
