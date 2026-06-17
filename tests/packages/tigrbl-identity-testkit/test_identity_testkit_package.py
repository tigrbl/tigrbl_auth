from __future__ import annotations

import pytest

from tigrbl_identity_testkit import (
    PackageMatrixHarness,
    TestkitError,
    build_fake_flow,
    cross_language_vectors,
    default_seed_set,
    provider_runtime_profile,
)


def test_identity_testkit_package_exposes_seeded_runtime_vectors() -> None:
    profile = provider_runtime_profile()
    seeds = default_seed_set()
    vectors = cross_language_vectors()

    assert profile.name == "testkit-provider-runtime"
    assert profile.feature_flags["dpop"] is True
    assert seeds.client("test-rp").redirect_uri == "https://rp.example.test/callback"
    assert vectors["pkce_s256"]


def test_identity_testkit_package_runs_fake_oidc_flow() -> None:
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
    token = idp.token(
        code=code.code,
        code_verifier=rp.code_verifier,
        client_id=params["client_id"],
    )

    assert token.token_type == "Bearer"
    assert resource_server.verify(f"Bearer {token.access_token}")["active"] is True
    assert idp.userinfo(token.access_token)["preferred_username"] == "alice"


def test_identity_testkit_package_fails_closed_for_bad_vectors() -> None:
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
        idp.token(code=code.code, code_verifier="bad", client_id=params["client_id"])
    with pytest.raises(TestkitError, match="missing authorization"):
        resource_server.verify(None)
    with pytest.raises(TestkitError, match="missing Python versions"):
        PackageMatrixHarness().assert_complete([], package="tigrbl-identity-testkit")


def test_identity_testkit_package_matrix_cells_cover_supported_versions() -> None:
    cells = PackageMatrixHarness().cells_for(
        "tigrbl-identity-testkit",
        test_paths=("tests/packages/tigrbl-identity-testkit", "tests/interop"),
        cross_cutting=True,
    )

    assert {cell.python_version for cell in cells} == {
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    }
    assert all(cell.cross_cutting for cell in cells)
