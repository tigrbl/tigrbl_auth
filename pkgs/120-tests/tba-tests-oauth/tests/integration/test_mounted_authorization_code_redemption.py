"""Verify the authorization-code transaction through the public ASGI carrier."""

import asyncio
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

import pytest


@pytest.mark.integration
def test_mounted_code_redemption_consumes_only_after_committed_issuance(tmp_path):
    # A fresh process gives storage and signing initialization their own
    # configuration, SQLite database, and local keys.
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("POSTGRES_", "PG_", "TBA_AUTH_", "AUTHN_"))
    }
    env.update(
        ASYNC_FALLBACK_DB=f"sqlite+aiosqlite:///{tmp_path.as_posix()}/identity.db",
        AUTHN_ISSUER="https://redemption.example.test",
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


async def _exercise_code_redemption():
    from httpx import ASGITransport, AsyncClient, BasicAuth
    from sqlalchemy import select, text

    from tba_app_backend_public import build_app
    from tba_primitives_identity.digests import token_hash
    from tba_protocol_oauth.standards.proof_key_for_code_exchange import (
        makeCodeChallenge,
        makeCodeVerifier,
    )
    from tba_provider_identity_jose.key_management import hash_pw
    from tba_runtime_identity_storage.migrations import apply_all_async
    from tba_runtime_identity_storage.session import storage_session
    from tba_storage_oauth.tables import AuthCode, Client
    from tba_storage_principals.tables import User
    from tba_storage_tenancy.tables import Tenant
    from tba_storage_token.tables import TokenRecord

    app = build_app()
    await apply_all_async()
    callback = "https://client.example.test/callback"
    verifier = makeCodeVerifier()
    client_id, code_id = uuid4(), uuid4()
    async with storage_session() as db:
        tenant = Tenant(
            slug="fixture-tenant", name="Code fixture", email="tenant@example.test"
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
            id=client_id,
            tenant_id=tenant.id,
            client_secret_hash=hash_pw("local-fixture-client-secret"),
            redirect_uris=callback,
        )
        db.add_all([user, client])
        await db.flush()
        db.add(
            AuthCode(
                id=code_id,
                tenant_id=tenant.id,
                user_id=user.id,
                client_id=client_id,
                redirect_uri=callback,
                code_challenge=makeCodeChallenge(verifier),
                nonce="fixture-nonce",
                scope="openid",
                expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            )
        )

    incoming, outgoing = asyncio.Queue(), asyncio.Queue()
    await incoming.put({"type": "lifespan.startup"})
    lifespan = asyncio.create_task(app({"type": "lifespan"}, incoming.get, outgoing.put))
    try:
        started = await asyncio.wait_for(outgoing.get(), timeout=25)
        assert started["type"] == "lifespan.startup.complete", started
        auth = BasicAuth(str(client_id), "local-fixture-client-secret")
        grant = {
            "grant_type": "authorization_code",
            "code": str(code_id),
            "redirect_uri": callback,
            "code_verifier": verifier,
        }
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="https://redemption.example.test"
        ) as http:
            invalid = await http.post(
                "/token", data={**grant, "code_verifier": makeCodeVerifier()}, auth=auth
            )
            assert invalid.status_code == 400 and invalid.json()["error"] == "invalid_grant"
            async with storage_session() as db:
                assert await db.get(AuthCode, code_id) is not None
                await db.execute(text("""
                    CREATE TRIGGER authn.fail_token_pair
                    BEFORE INSERT ON token_records
                    WHEN NEW.token_kind = 'refresh'
                    BEGIN
                        SELECT RAISE(ABORT, 'fixture refuses refresh token insert');
                    END
                """))
            failed = await http.post("/token", data=grant, auth=auth)
            assert failed.status_code == 409
            async with storage_session() as db:
                assert await db.get(AuthCode, code_id) is not None
                assert not (await db.execute(select(TokenRecord))).scalars().all()
                await db.execute(text("DROP TRIGGER authn.fail_token_pair"))

            redeemed = await http.post("/token", data=grant, auth=auth)
            assert redeemed.status_code == 200, redeemed.status_code
            pair = redeemed.json()
            assert pair["id_token"]
            async with storage_session() as db:
                assert await db.get(AuthCode, code_id) is None
                rows = (await db.execute(select(TokenRecord))).scalars().all()
                assert {row.token_hash for row in rows} == {
                    token_hash(pair["access_token"]),
                    token_hash(pair["refresh_token"]),
                }
            replay = await http.post("/token", data=grant, auth=auth)
            assert replay.status_code == 400 and replay.json()["error"] == "invalid_grant"
    finally:
        await incoming.put({"type": "lifespan.shutdown"})
        await asyncio.wait_for(lifespan, timeout=15)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[5]
    sys.path[:0] = [str(root), *map(str, root.glob("pkgs/[0-9][0-9][0-9]-*/*/src"))]
    asyncio.run(_exercise_code_redemption())
