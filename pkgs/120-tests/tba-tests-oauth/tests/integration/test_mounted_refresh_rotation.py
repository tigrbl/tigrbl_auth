"""Exercise refresh persistence through the mounted public ASGI application."""

import asyncio
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

import pytest


@pytest.mark.integration
def test_mounted_refresh_rotation_rollback_and_reuse(tmp_path):
    # Storage and signing resources are initialized on import. Start a fresh
    # process so it uses only this test's isolated database and local keys.
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("POSTGRES_", "PG_", "TBA_AUTH_", "AUTHN_"))
    }
    env.update(
        ASYNC_FALLBACK_DB=f"sqlite+aiosqlite:///{tmp_path.as_posix()}/identity.db",
        AUTHN_ISSUER="https://rotation.example.test",
        TBA_AUTH_BOOTSTRAP_ADMIN_USERNAME="fixture-admin",
        TBA_AUTH_BOOTSTRAP_ADMIN_TENANT_SLUG="fixture-tenant",
        TBA_AUTH_OPERATOR_STATE_DIR=str(tmp_path / "operator"),
        PYTHONDONTWRITEBYTECODE="1",
    )
    result = subprocess.run(
        [sys.executable, str(Path(__file__).resolve())],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=75,
    )
    assert result.returncode == 0, result.stdout + result.stderr


async def _exercise_refresh_routes():
    from httpx import ASGITransport, AsyncClient, BasicAuth
    from sqlalchemy import select, text

    from tba_app_backend_public import build_app
    from tba_primitives_identity.digests import token_hash
    from tba_provider_identity_jose.key_management import hash_pw
    from tba_runtime_identity_storage.migrations import apply_all_async
    from tba_runtime_identity_storage.session import storage_session
    from tba_runtime_identity_storage.token_persistence import issue_persisted_token_pair
    from tba_provider_identity_jose.jwt_coder import JWTCoder
    from tba_storage_oauth.tables import Client
    from tba_storage_principals.tables import User
    from tba_storage_tenancy.tables import Tenant
    from tba_storage_token.tables import TokenRecord

    app = build_app()
    await apply_all_async()
    async with storage_session() as db:
        tenant = Tenant(
            slug="fixture-tenant", name="Refresh fixture", email="tenant@example.test"
        )
        db.add(tenant)
        await db.flush()
        user = User(
            tenant_id=tenant.id,
            username="fixture-admin",
            email="admin@example.test",
            password_hash=hash_pw("Local fixture password!"),
            is_admin=True,
            is_superuser=True,
        )
        client = Client(
            id=uuid4(),
            tenant_id=tenant.id,
            client_secret_hash=hash_pw("local-fixture-client-secret"),
            redirect_uris="https://client.example.test/callback",
        )
        db.add_all([user, client])
        await db.flush()
        tenant_id, user_id, client_id = map(str, (tenant.id, user.id, client.id))

    incoming, outgoing = asyncio.Queue(), asyncio.Queue()
    await incoming.put({"type": "lifespan.startup"})
    lifespan = asyncio.create_task(app({"type": "lifespan"}, incoming.get, outgoing.put))
    try:
        started = await asyncio.wait_for(outgoing.get(), timeout=25)
        assert started["type"] == "lifespan.startup.complete", started
        _, refresh = await issue_persisted_token_pair(
            jwt=await JWTCoder.async_default(),
            sub=user_id,
            tid=tenant_id,
            client_id=client_id,
            issuer="https://rotation.example.test",
            scope="openid profile",
        )
        auth = BasicAuth(client_id, "local-fixture-client-secret")
        grant = {"grant_type": "refresh_token", "refresh_token": refresh}
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="https://rotation.example.test"
        ) as http:
            # Abort the second successor INSERT after the parent update and
            # access-token INSERT, leaving the real request transaction in charge.
            async with storage_session() as db:
                await db.execute(text("""
                    CREATE TRIGGER authn.fail_successor
                    BEFORE INSERT ON token_records
                    WHEN NEW.token_kind = 'refresh' AND NEW.refresh_parent_hash IS NOT NULL
                    BEGIN
                        SELECT RAISE(ABORT, 'fixture refuses refresh successor');
                    END
                """))
            failed = await http.post("/token", data=grant, auth=auth)
            assert failed.status_code == 409
            async with storage_session() as db:
                rows = (await db.execute(select(TokenRecord))).scalars().all()
                assert len(rows) == 2
                assert all(row.active and row.used_at is None for row in rows)
                await db.execute(text("DROP TRIGGER authn.fail_successor"))

            succeeded = await http.post("/token", data=grant, auth=auth)
            assert succeeded.status_code == 200
            pair = succeeded.json()
            async with storage_session() as db:
                rows = (await db.execute(select(TokenRecord))).scalars().all()
                by_digest = {row.token_hash: row for row in rows}
                assert len(rows) == 4
                parent = by_digest[token_hash(refresh)]
                successor = by_digest[token_hash(pair["refresh_token"])]
                assert parent.refresh_successor_hash == successor.token_hash
                assert successor.refresh_parent_hash == parent.token_hash
                assert successor.refresh_family_id == parent.refresh_family_id

            access = {"Authorization": f"Bearer {pair['access_token']}"}
            assert (await http.get("/userinfo", headers=access)).status_code == 200
            reused = await http.post("/token", data=grant, auth=auth)
            assert reused.status_code == 400 and reused.json()["error"] == "invalid_grant"
            async with storage_session() as db:
                rows = (await db.execute(select(TokenRecord))).scalars().all()
                assert len(rows) == 4
                assert all(not row.active for row in rows)
                assert all(row.revoked_reason == "refresh_token_reuse_detected" for row in rows)
            assert (await http.get("/userinfo", headers=access)).status_code == 401
    finally:
        await incoming.put({"type": "lifespan.shutdown"})
        await asyncio.wait_for(lifespan, timeout=15)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[5]
    sys.path[:0] = [str(root), *map(str, root.glob("pkgs/[0-9][0-9][0-9]-*/*/src"))]
    asyncio.run(_exercise_refresh_routes())
