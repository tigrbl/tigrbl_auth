from __future__ import annotations

import ast
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_identity_rp import (  # noqa: E402
    BrowserMemorySession,
    BrowserStoragePolicy,
    DiscoveryClient,
    JwksCache,
    RPConfiguration,
    RPError,
    RPSession,
    RelyingParty,
    UserInfoClient,
    assert_browser_no_client_secret,
    example_app_manifest,
    framework_callback_adapter,
    framework_login_adapter,
    pkce_s256_challenge,
    shared_vector_manifest,
    validate_browser_storage_policy,
    validate_id_token_claims,
)


def _rp(*, secret: str | None = "secret") -> RelyingParty:
    return RelyingParty(
        RPConfiguration(
            issuer="https://issuer.example.test/",
            client_id="client-a",
            client_secret=secret,
            redirect_uri="https://rp.example.test/callback",
            post_logout_redirect_uri="https://rp.example.test/logout",
            scopes=("openid", "profile", "email"),
        )
    )


@pytest.mark.unit
def test_rp_t0_public_surfaces_and_vectors_are_importable() -> None:
    rp = _rp()
    url, login = rp.build_authorization_url("https://issuer.example.test/authorize")
    values = parse_qs(urlparse(url).query)

    assert shared_vector_manifest()["callback_required_params"] == "code,state"
    assert values["client_id"] == ["client-a"]
    assert values["code_challenge_method"] == ["S256"]
    assert pkce_s256_challenge(login.code_verifier) == values["code_challenge"][0]


@pytest.mark.unit
def test_rp_t1_authorization_callback_confidential_exchange_and_refresh() -> None:
    rp = _rp()
    _url, login = rp.build_authorization_url("https://issuer.example.test/authorize")
    callback = rp.parse_callback(f"https://rp.example.test/callback?code=abc&state={login.state}&iss=https://issuer.example.test")

    session = rp.exchange_code_confidential(
        lambda payload: {
            "sub": "user:123",
            "id_token": "id-token",
            "access_token": "access-token",
            "refresh_token": "refresh-token",
            "code_verifier_seen": payload["code_verifier"],
        },
        callback,
    )
    refreshed = rp.refresh(lambda token: {"access_token": "access-token-2", "refresh_token": token}, login.state)

    assert session.subject == "user:123"
    assert refreshed.access_token == "access-token-2"
    assert rp.token_store.get(login.state).access_token == "access-token-2"


@pytest.mark.unit
def test_rp_t1_discovery_jwks_id_token_userinfo_logout_and_adapter() -> None:
    rp = _rp()
    discovery = DiscoveryClient(
        lambda _url: {
            "issuer": "https://issuer.example.test",
            "authorization_endpoint": "https://issuer.example.test/authorize",
            "token_endpoint": "https://issuer.example.test/token",
            "jwks_uri": "https://issuer.example.test/jwks.json",
            "userinfo_endpoint": "https://issuer.example.test/userinfo",
        }
    )
    metadata = discovery.discover("https://issuer.example.test")
    jwks = JwksCache()
    jwks.put({"keys": [{"kid": "kid-1", "kty": "OKP"}]})
    userinfo = UserInfoClient(lambda endpoint, token: {"endpoint": endpoint, "sub": "user:123", "token": token})
    callback = framework_callback_adapter(rp, "https://rp.example.test/callback?code=abc&state=state-1")
    claims = validate_id_token_claims(
        {"iss": "https://issuer.example.test", "aud": ["client-a"], "nonce": "nonce-1", "exp": 1},
        issuer="https://issuer.example.test",
        audience="client-a",
        nonce="nonce-1",
    )
    logout = rp.build_logout_url("https://issuer.example.test/logout", id_token_hint="id-token", state="bye")
    login_response = framework_login_adapter(rp, metadata["authorization_endpoint"])
    manifest = example_app_manifest()

    assert metadata["userinfo_endpoint"].endswith("/userinfo")
    assert jwks.get("kid-1")["kty"] == "OKP"
    assert userinfo.get("https://issuer.example.test/userinfo", "access-token")["sub"] == "user:123"
    assert callback.code == "abc"
    assert claims["aud"] == ["client-a"]
    assert "post_logout_redirect_uri=https%3A%2F%2Frp.example.test%2Flogout" in logout
    assert login_response["status"] == 302
    assert login_response["headers"]["location"].startswith("https://issuer.example.test/authorize?")
    assert manifest["browser_rp"]["client_secret"] is False


@pytest.mark.unit
def test_rp_t1_browser_memory_session_and_no_secret_guard() -> None:
    memory = BrowserMemorySession(policy=BrowserStoragePolicy.MEMORY_ONLY)
    session = RPSession(subject="user:123", id_token="id", access_token="at")
    memory.set(session)

    assert_browser_no_client_secret(_rp(secret=None).config)
    assert validate_browser_storage_policy(BrowserStoragePolicy.MEMORY_ONLY) is BrowserStoragePolicy.MEMORY_ONLY
    assert memory.get() == session
    memory.clear()
    assert memory.get() is None
    with pytest.raises(RPError, match="client secret"):
        BrowserMemorySession(client_secret="forbidden")


@pytest.mark.unit
def test_rp_t2_callback_replay_public_client_and_validation_failures() -> None:
    rp = _rp()
    _url, login = rp.build_authorization_url("https://issuer.example.test/authorize")
    callback = rp.parse_callback(f"https://rp.example.test/callback?code=abc&state={login.state}")
    rp.validate_callback(callback)

    with pytest.raises(RPError, match="already consumed"):
        rp.validate_callback(callback)
    with pytest.raises(RPError, match="client secret"):
        _rp(secret=None).exchange_code_confidential(lambda _payload: {}, callback)
    with pytest.raises(RPError, match="audience"):
        validate_id_token_claims(
            {"iss": "https://issuer.example.test", "aud": ["other"], "nonce": "nonce-1", "exp": 1},
            issuer="https://issuer.example.test",
            audience="client-a",
            nonce="nonce-1",
        )
    with pytest.raises(RPError, match="localStorage"):
        validate_browser_storage_policy(BrowserStoragePolicy.LOCAL_STORAGE)
    with pytest.raises(RPError, match="client secret"):
        assert_browser_no_client_secret(_rp(secret="not-browser-safe").config)
    with pytest.raises(RPError, match="missing required endpoints"):
        DiscoveryClient(lambda _url: {"issuer": "https://issuer.example.test"}).discover("https://issuer.example.test")


@pytest.mark.unit
def test_rp_t2_public_boundary_has_no_provider_imports() -> None:
    files = [
        Path("pkgs/tigrbl-identity-rp/src/tigrbl_identity_rp/__init__.py"),
        Path("pkgs/tigrbl-identity-rp/src/tigrbl_identity_rp/client.py"),
    ]
    forbidden = {
        "tigrbl_auth",
        "tigrbl_identity_oauth",
        "tigrbl_identity_oidc",
        "tigrbl_identity_server",
        "tigrbl_identity_runtime",
    }

    imports: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                imports.add(node.module.split(".")[0])

    assert imports.isdisjoint(forbidden)
