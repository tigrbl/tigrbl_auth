import json
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import parse_qs, urlsplit

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from httpx import ASGITransport, AsyncClient
from tba_primitives_identity.base64url import base64url_encode
from tba_router_relying_party_session import workspace
from tba_runtime_relying_party_session.sqlite import SQLiteRPStore


def _encode_object(value):
    return base64url_encode(json.dumps(value).encode())


def _encode_number(value):
    return base64url_encode(value.to_bytes((value.bit_length() + 7) // 8, "big"))


@pytest.mark.asyncio
async def test_workspace_signed_login_durable_session_grant_and_logout(tmp_path, monkeypatch):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = key.public_key().public_numbers()
    nonce = ""
    pkce_challenge = ""
    allowed = True

    def google(host, path, *, form=None):
        if host == "www.googleapis.com":
            assert path == "/oauth2/v3/certs"
            return {"keys": [{"kid": "google-test", "kty": "RSA", "alg": "RS256",
                              "n": _encode_number(public.n), "e": _encode_number(public.e)}]}
        assert form["code"] == "test-code"
        from tba_protocol_oidc_relying_party import pkce_s256_challenge

        assert pkce_s256_challenge(form["code_verifier"]) == pkce_challenge
        now = int(time.time())
        claims = {
            "iss": "accounts.google.com", "sub": "google-principal", "aud": "client",
            "email": "operator@example.test", "email_verified": True, "hd": "example.test",
            "iat": now, "exp": now + 3600, "nonce": nonce,
        }
        header = {"alg": "RS256", "kid": "google-test"}
        payload = f"{_encode_object(header)}.{_encode_object(claims)}"
        signature = key.sign(payload.encode(), padding.PKCS1v15(), hashes.SHA256())
        return {"id_token": f"{payload}.{base64url_encode(signature)}",
                "refresh_token": "must-never-be-stored"}

    def authorize(identity):
        assert identity["sub"] == "google-principal"
        if not allowed:
            raise PermissionError("grant revoked")

    async def app(scope, receive, send):
        raise AssertionError("unexpected forwarded route")

    monkeypatch.setattr(workspace, "_google_json", google)
    database = tmp_path / "rp.sqlite3"
    options = {
        "client_id": "client",
        "client_secret": "test-secret",
        "redirect_uri": "https://ops.example.test/oauth2/callback",
        "application_path": "/ops",
        "signed_out_path": "/ops/session-ended",
        "database": database,
        "authorize": authorize,
    }
    first = workspace.WorkspaceLogin(**options)
    async with AsyncClient(
        transport=ASGITransport(app=first.wrap(app)),
        base_url="https://ops.example.test",
    ) as browser:
        assert (await browser.get("/auth/session")).status_code == 401
        destination = "/ops/invitations/review?id=selected"
        start = await browser.get("/auth/login", params={"return": destination})
        assert start.status_code == 302
        values = parse_qs(urlsplit(start.headers["location"]).query)
        state = values["state"][0]
        nonce = values["nonce"][0]
        pkce_challenge = values["code_challenge"][0]
        callback = await browser.get("/oauth2/callback", params={"code": "test-code", "state": state})
        assert callback.status_code == 303
        assert callback.headers["location"] == destination
        assert "HttpOnly" in callback.headers["set-cookie"]
        assert "Secure" in callback.headers["set-cookie"]
        assert "must-never-be-stored" not in database.read_bytes().decode("latin-1")
        copied = dict(browser.cookies)

    second = workspace.WorkspaceLogin(**options)
    async with AsyncClient(
        transport=ASGITransport(app=second.wrap(app)),
        base_url="https://ops.example.test", cookies=copied,
    ) as browser:
        assert (await browser.get("/auth/session")).status_code == 204
        allowed = False
        assert (await browser.get("/auth/session")).status_code == 401
        allowed = True
        assert (await browser.post("/auth/logout", headers={"Origin": "https://other.test"})).status_code == 403
        assert (await browser.get("/auth/session")).status_code == 204
        assert (await browser.post("/auth/logout", headers={"Origin": "https://ops.example.test"})).status_code == 303
        browser.cookies.update(copied)
        assert (await browser.get("/auth/session")).status_code == 401


def test_workspace_durable_state_can_only_be_consumed_once(tmp_path):
    database = tmp_path / "rp.sqlite3"
    first = SQLiteRPStore(database, realm="ops")
    second = SQLiteRPStore(database, realm="ops")
    separate = SQLiteRPStore(database, realm="customer")
    login = first.create(redirect_uri="https://ops.example.test/callback", scope=("openid",))
    with pytest.raises(ValueError):
        separate.consume(login.state)

    def take(store):
        try:
            return store.consume(login.state)
        except ValueError:
            return None

    with ThreadPoolExecutor(max_workers=2) as worker:
        results = list(worker.map(take, (first, second)))
    assert results.count(login) == 1
    assert results.count(None) == 1
