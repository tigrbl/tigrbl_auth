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

from tigrbl_identity_testkit import (  # noqa: E402
    FakeIdentityProvider,
    FakeResourceServer,
    MatrixCellStatus,
    PackageMatrixHarness,
    SeededClient,
    TestkitError,
    build_fake_flow,
    cross_language_vectors,
    default_seed_set,
    provider_runtime_profile,
)


@pytest.mark.unit
def test_testkit_t0_public_surfaces_are_importable() -> None:
    profile = provider_runtime_profile()
    seeds = default_seed_set()
    vectors = cross_language_vectors()

    assert profile.name == "testkit-provider-runtime"
    assert "/authorize" in profile.routes
    assert profile.feature_flags["device_flow"] is True
    assert seeds.tenant.tenant_id == "test"
    assert seeds.client("test-rp").client_id == "test-rp"
    assert vectors["pkce_s256"]


@pytest.mark.unit
def test_testkit_t1_fake_idp_rp_and_resource_server_flow() -> None:
    idp, rp, resource_server = build_fake_flow()
    params = rp.authorization_params()
    authorization_url = rp.authorization_url()
    parsed = parse_qs(urlparse(authorization_url).query)
    code = idp.authorize(
        client_id=params["client_id"],
        redirect_uri=params["redirect_uri"],
        subject="user:123",
        scope=params["scope"].split(),
        code_challenge=params["code_challenge"],
        nonce=params["nonce"],
    )
    callback = rp.parse_callback(f"https://rp.example.test/callback?code={code.code}&state={rp.state}")
    token = idp.token(code=callback["code"], code_verifier=rp.code_verifier, client_id="test-rp")
    verified = resource_server.verify(f"Bearer {token.access_token}")
    userinfo = idp.userinfo(token.access_token)

    assert parsed["client_id"] == ["test-rp"]
    assert parsed["code_challenge_method"] == ["S256"]
    assert token.token_type == "Bearer"
    assert token.subject == "user:123"
    assert verified["active"] is True
    assert userinfo["preferred_username"] == "alice"


@pytest.mark.unit
def test_testkit_t1_seeded_fixtures_vectors_and_package_matrix() -> None:
    seeds = default_seed_set()
    vectors = cross_language_vectors()
    harness = PackageMatrixHarness()
    cells = harness.cells_for(
        "tigrbl-identity-testkit",
        test_paths=("tests/integration", "tests/interop", "tests/unit/test_testkit_cross_cutting_boundary.py"),
        cross_cutting=True,
    )

    harness.assert_complete(cells, package="tigrbl-identity-testkit")

    assert seeds.user("user:123").username == "alice"
    assert vectors["authorization_required_params"] == (
        "client_id",
        "code_challenge",
        "code_challenge_method",
        "nonce",
        "redirect_uri",
        "response_type",
        "scope",
        "state",
    )
    assert {cell.python_version for cell in cells} == {"3.10", "3.11", "3.12", "3.13", "3.14"}
    assert all(cell.cross_cutting for cell in cells)
    assert all(cell.status is MatrixCellStatus.PLANNED for cell in cells)


@pytest.mark.unit
def test_testkit_t2_fail_closed_runtime_seed_and_flow_guards() -> None:
    seeds = default_seed_set()
    idp = FakeIdentityProvider(seeds=seeds)
    client = SeededClient(client_id="bad", tenant_id="test", redirect_uri="https://rp.example.test/callback")

    with pytest.raises(TestkitError, match="route"):
        profile = provider_runtime_profile()
        profile.require_route("/missing")
    with pytest.raises(TestkitError, match="client"):
        seeds.client("missing-client")
    with pytest.raises(TestkitError, match="not allowed"):
        idp.authorize(
            client_id="test-rp",
            redirect_uri="https://rp.example.test/callback",
            subject="user:123",
            scope=("admin",),
            code_challenge="challenge",
            nonce="nonce",
        )
    with pytest.raises(TestkitError, match="redirect URI"):
        idp.authorize(
            client_id="test-rp",
            redirect_uri="https://evil.example.test/callback",
            subject="user:123",
            scope=("openid",),
            code_challenge="challenge",
            nonce="nonce",
        )
    with pytest.raises(TestkitError, match="seeded client"):
        FakeIdentityProvider(seeds=seeds).authorize(
            client_id=client.client_id,
            redirect_uri=client.redirect_uri,
            subject="user:123",
            scope=("openid",),
            code_challenge="challenge",
            nonce="nonce",
        )


@pytest.mark.unit
def test_testkit_t2_rejects_replay_bad_pkce_resource_server_and_matrix_gaps() -> None:
    idp, rp, resource_server = build_fake_flow()
    params = rp.authorization_params()
    code = idp.authorize(
        client_id=params["client_id"],
        redirect_uri=params["redirect_uri"],
        subject="user:123",
        scope=params["scope"].split(),
        code_challenge=params["code_challenge"],
        nonce=params["nonce"],
    )
    with pytest.raises(TestkitError, match="PKCE"):
        idp.token(code=code.code, code_verifier="wrong", client_id="test-rp")
    token = idp.token(code=code.code, code_verifier=rp.code_verifier, client_id="test-rp")
    with pytest.raises(TestkitError, match="already used"):
        idp.token(code=code.code, code_verifier=rp.code_verifier, client_id="test-rp")
    with pytest.raises(TestkitError, match="missing authorization"):
        resource_server.verify(None)
    with pytest.raises(TestkitError, match="missing scopes"):
        FakeResourceServer(idp=idp, required_scopes=("admin",)).verify(f"Bearer {token.access_token}")
    with pytest.raises(TestkitError, match="missing Python versions"):
        PackageMatrixHarness().assert_complete([], package="tigrbl-identity-testkit")


@pytest.mark.unit
def test_testkit_t2_public_boundary_imports_are_package_safe() -> None:
    files = [
        Path("pkgs/120-tests/tigrbl-identity-testkit/src/tigrbl_identity_testkit/__init__.py"),
        Path("pkgs/120-tests/tigrbl-identity-testkit/src/tigrbl_identity_testkit/cross_cutting.py"),
    ]
    forbidden = {
        "tigrbl_auth",
        "tigrbl_identity_admin",
        "tigrbl_identity_server",
        "tigrbl_identity_runtime",
        "sqlalchemy",
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
