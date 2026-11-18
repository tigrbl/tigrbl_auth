from __future__ import annotations

import ast
import asyncio
import base64
import json
import sys
from pathlib import Path
from time import time
from urllib.parse import parse_qs, urlparse

import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tba_protocol_oidc_relying_party import (  # noqa: E402
    CAPABILITY_REQUIREMENTS,
    CURRENT_VERSION,
    RP_ID_TOKEN_CLAIMS,
    BrowserMemorySession,
    BrowserStoragePolicy,
    DiscoveryClient,
    JwksCache,
    LoginRequest,
    PkceVerifier,
    RPConfiguration,
    RPError,
    RPSession,
    RelyingParty,
    UserInfoClient,
    assert_browser_no_client_secret,
    capability_report,
    compatibility,
    example_app_manifest,
    framework_callback_adapter,
    framework_login_adapter,
    migrate_configuration,
    pkce_s256_challenge,
    shared_vector_manifest,
    supports,
    validate_browser_storage_policy,
    validate_id_token_claims,
)
from tba_provider_replay_memory import MemoryRPSessionProvider, MemoryRPStateProvider


def _rp(*, secret: str | None = "secret") -> RelyingParty:
    return RelyingParty(
        RPConfiguration(
            issuer="https://issuer.example.test/",
            client_id="client-a",
            client_secret=secret,
            redirect_uri="https://rp.example.test/callback",
            post_logout_redirect_uri="https://rp.example.test/logout",
            scopes=("openid", "profile", "email"),
        ),
        state_store=MemoryRPStateProvider(),
        session_store=MemoryRPSessionProvider(),
    )


@pytest.fixture(scope="module")
def public_keys():
    return (
        rsa.generate_private_key(public_exponent=65537, key_size=2048),
        rsa.generate_private_key(public_exponent=65537, key_size=2048),
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "case",
    [
        "success",
        "issuer",
        "audience",
        "extra-audience",
        "nonce",
        "expired",
        "signature",
    ],
)
def test_public_callback_exchanges_pkce_and_requires_verified_identity(
    case, public_keys
) -> None:
    issuer = "https://issuer.example.test"
    rp = _rp(secret=None)
    signing_key, unrelated_key = public_keys

    def encode(value: bytes) -> str:
        return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")

    numbers = signing_key.public_key().public_numbers()
    jwk = {
        "kty": "RSA",
        "kid": "key-1",
        "alg": "RS256",
        "use": "sig",
        **{
            name: encode(number.to_bytes((number.bit_length() + 7) // 8, "big"))
            for name, number in (("n", numbers.n), ("e", numbers.e))
        },
    }
    metadata = {
        "issuer": issuer,
        "authorization_endpoint": issuer + "/authorize",
        "token_endpoint": issuer + "/token",
        "jwks_uri": issuer + "/jwks",
        "token_endpoint_auth_methods_supported": ["none"],
    }
    requests = []

    async def get_json(url):
        return {
            issuer + "/.well-known/openid-configuration": metadata,
            issuer + "/jwks": {"keys": [jwk]},
        }[url]

    async def exercise():
        url, login = await rp.begin_public_login(get_json)
        assert parse_qs(urlparse(url).query)["code_challenge"] == [
            pkce_s256_challenge(login.code_verifier)
        ]
        now = int(time())
        claims = {
            "iss": issuer,
            "aud": "client-a",
            "iat": now,
            "exp": now + 60,
            "nonce": login.nonce,
            "sub": "verified-subject",
        }
        overrides = {
            "issuer": {"iss": issuer + "/"},
            "audience": {"aud": "other"},
            "extra-audience": {"aud": ["client-a", "other"], "azp": "client-a"},
            "nonce": {"nonce": "other"},
            "expired": {"exp": now - 1},
        }
        claims.update(overrides.get(case, {}))
        signing_input = ".".join(
            encode(json.dumps(part).encode())
            for part in (
                {"alg": "RS256", "kid": "key-1"},
                claims,
            )
        )
        key = unrelated_key if case == "signature" else signing_key
        signature = key.sign(
            signing_input.encode(), padding.PKCS1v15(), hashes.SHA256()
        )

        async def post_form(url, form):
            requests.append((url, form))
            return {
                "access_token": "access",
                "id_token": signing_input + "." + encode(signature),
                "token_type": "Bearer",
                "sub": "untrusted-token-response-subject",
            }

        callback = rp.config.redirect_uri + "?code=code&state=" + login.state

        async def complete(url, state=login.state):
            return await rp.complete_public_callback(
                url,
                expected_state=state,
                get_json=get_json,
                post_form=post_form,
            )

        with pytest.raises(RPError, match="state mismatch"):
            await complete(callback, "another-browser")
        with pytest.raises(RPError, match="duplicate"):
            await complete(callback + "&state=second")
        assert not requests
        if case == "success":
            result = await complete(callback)
            assert (
                result.identity.subject == result.session.subject == "verified-subject"
            )
            assert rp.token_store.get(login.state) == result.session
        else:
            with pytest.raises(RPError):
                await complete(callback)
            with pytest.raises(ValueError, match="unknown RP session"):
                rp.token_store.get(login.state)
        with pytest.raises(RPError, match="already consumed"):
            await complete(callback)
        assert requests == [
            (
                issuer + "/token",
                {
                    "grant_type": "authorization_code",
                    "client_id": "client-a",
                    "redirect_uri": rp.config.redirect_uri,
                    "code": "code",
                    "code_verifier": login.code_verifier,
                },
            )
        ]

    asyncio.run(exercise())


@pytest.mark.unit
def test_rp_t0_public_surfaces_and_vectors_are_importable() -> None:
    rp = _rp()
    url, login = rp.build_authorization_url("https://issuer.example.test/authorize")
    values = parse_qs(urlparse(url).query)

    assert shared_vector_manifest()["callback_required_params"] == "code,state"
    assert isinstance(PkceVerifier(login.code_verifier), PkceVerifier)
    assert values["client_id"] == ["client-a"]
    assert values["code_challenge_method"] == ["S256"]
    assert pkce_s256_challenge(login.code_verifier) == values["code_challenge"][0]


@pytest.mark.unit
def test_rp_owns_composite_profile_history_claims_and_capability_bindings() -> None:
    assert CURRENT_VERSION.status == "current-composite-profile"
    assert supports("pkce-s256")
    path = compatibility("oidc-core-1.0+oauth2.0")
    assert path.compatible and path.migration_required
    assert migrate_configuration(
        {},
        source="oidc-core-1.0+oauth2.0",
    ) == {
        "browser_storage_policy": "memory_only",
        "pkce_method": "S256",
    }
    assert {claim.claim_name for claim in RP_ID_TOKEN_CLAIMS} >= {
        "aud",
        "exp",
        "iat",
        "iss",
        "nonce",
        "sub",
    }
    assert {item.operation for item in CAPABILITY_REQUIREMENTS} == {
        "check_and_reserve",
        "decode",
        "validate",
    }
    report = capability_report()
    assert report["selected_revision"] == CURRENT_VERSION.identifier
    assert report["required_capabilities"] == (
        "artifact.processing",
        "security.replay-protection",
    )


@pytest.mark.unit
def test_rp_t1_pkce_verifier_model_renders_authorization_params() -> None:
    verifier = PkceVerifier.generate()
    params = verifier.authorization_params()

    assert 43 <= len(verifier.value) <= 128
    assert params["code_challenge"] == pkce_s256_challenge(verifier.value)
    assert params["code_challenge_method"] == "S256"


@pytest.mark.unit
def test_rp_t1_authorization_callback_confidential_exchange_and_refresh() -> None:
    rp = _rp()
    _url, login = rp.build_authorization_url("https://issuer.example.test/authorize")
    callback = rp.parse_callback(
        f"https://rp.example.test/callback?code=abc&state={login.state}&iss=https://issuer.example.test"
    )

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
    refreshed = rp.refresh(
        lambda token: {"access_token": "access-token-2", "refresh_token": token},
        login.state,
    )

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
    userinfo = UserInfoClient(
        lambda endpoint, token: {
            "endpoint": endpoint,
            "sub": "user:123",
            "token": token,
        }
    )
    callback = framework_callback_adapter(
        rp, "https://rp.example.test/callback?code=abc&state=state-1"
    )
    claims = validate_id_token_claims(
        {
            "iss": "https://issuer.example.test",
            "aud": ["client-a"],
            "nonce": "nonce-1",
            "exp": 1,
        },
        issuer="https://issuer.example.test",
        audience="client-a",
        nonce="nonce-1",
    )
    logout = rp.build_logout_url(
        "https://issuer.example.test/logout", id_token_hint="id-token", state="bye"
    )
    login_response = framework_login_adapter(rp, metadata["authorization_endpoint"])
    manifest = example_app_manifest()

    assert metadata["userinfo_endpoint"].endswith("/userinfo")
    assert jwks.get("kid-1")["kty"] == "OKP"
    assert (
        userinfo.get("https://issuer.example.test/userinfo", "access-token")["sub"]
        == "user:123"
    )
    assert callback.code == "abc"
    assert claims["aud"] == ["client-a"]
    assert "post_logout_redirect_uri=https%3A%2F%2Frp.example.test%2Flogout" in logout
    assert login_response["status"] == 302
    assert login_response["headers"]["location"].startswith(
        "https://issuer.example.test/authorize?"
    )
    assert manifest["browser_rp"]["client_secret"] is False


@pytest.mark.unit
def test_rp_t1_browser_memory_session_and_no_secret_guard() -> None:
    memory = BrowserMemorySession(policy=BrowserStoragePolicy.MEMORY_ONLY)
    session = RPSession(subject="user:123", id_token="id", access_token="at")
    memory.set(session)

    assert_browser_no_client_secret(_rp(secret=None).config)
    assert (
        validate_browser_storage_policy(BrowserStoragePolicy.MEMORY_ONLY)
        is BrowserStoragePolicy.MEMORY_ONLY
    )
    assert memory.get() == session
    memory.clear()
    assert memory.get() is None
    with pytest.raises(RPError, match="client secret"):
        BrowserMemorySession(client_secret="forbidden")


@pytest.mark.unit
def test_rp_t2_callback_replay_public_client_and_validation_failures() -> None:
    rp = _rp()
    _url, login = rp.build_authorization_url("https://issuer.example.test/authorize")
    callback = rp.parse_callback(
        f"https://rp.example.test/callback?code=abc&state={login.state}"
    )
    rp.validate_callback(callback)

    with pytest.raises(RPError, match="already consumed"):
        rp.validate_callback(callback)
    with pytest.raises(RPError, match="client secret"):
        _rp(secret=None).exchange_code_confidential(lambda _payload: {}, callback)
    with pytest.raises(RPError, match="audience"):
        validate_id_token_claims(
            {
                "iss": "https://issuer.example.test",
                "aud": ["other"],
                "nonce": "nonce-1",
                "exp": 1,
            },
            issuer="https://issuer.example.test",
            audience="client-a",
            nonce="nonce-1",
        )
    with pytest.raises(RPError, match="localStorage"):
        validate_browser_storage_policy(BrowserStoragePolicy.LOCAL_STORAGE)
    with pytest.raises(RPError, match="client secret"):
        assert_browser_no_client_secret(_rp(secret="not-browser-safe").config)
    with pytest.raises(RPError, match="missing required endpoints"):
        DiscoveryClient(
            lambda _url: {"issuer": "https://issuer.example.test"}
        ).discover("https://issuer.example.test")


@pytest.mark.unit
def test_rp_t2_pkce_verifier_rejects_invalid_values_and_login_url_fails_closed() -> (
    None
):
    class BadStateStore:
        def create(self, *, redirect_uri: str, scope: tuple[str, ...]) -> LoginRequest:
            return LoginRequest(
                state="state-1",
                nonce="nonce-1",
                code_verifier="short",
                redirect_uri=redirect_uri,
                scope=scope,
            )

    with pytest.raises(ValueError, match="invalid PKCE code_verifier"):
        PkceVerifier("short")
    with pytest.raises(ValueError, match="invalid PKCE code_verifier"):
        PkceVerifier("a" * 129)
    with pytest.raises(ValueError, match="invalid PKCE code_verifier"):
        PkceVerifier(("a" * 42) + "!")
    with pytest.raises(ValueError, match="between 43 and 128"):
        PkceVerifier.generate(42)
    with pytest.raises(ValueError, match="invalid PKCE code_verifier"):
        RelyingParty(
            _rp().config,
            state_store=BadStateStore(),
            session_store=MemoryRPSessionProvider(),
        ).build_authorization_url("https://issuer.example.test/authorize")


@pytest.mark.unit
def test_rp_t2_public_boundary_has_no_upper_runtime_imports() -> None:
    files = [
        Path(
            "pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py"
        ),
        Path(
            "pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py"
        ),
        Path(
            "pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/pkce.py"
        ),
    ]
    forbidden = {
        "tba_auth",
        "tba_protocol_oauth",
        "tba_protocol_oidc",
        "tba_server_identity",
        "tba_runtime_identity",
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
