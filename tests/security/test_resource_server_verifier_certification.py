import time
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[2]
PKG_SRC = ROOT / "pkgs" / "50-protocols" / "tigrbl-authz-resource-server" / "src"
if str(PKG_SRC) not in sys.path:
    sys.path.insert(0, str(PKG_SRC))

from tigrbl_auth.security.certification import (  # noqa: E402
    CertificationError,
    VerifierPolicy,
    assert_verifier_accepts,
)
from tigrbl_auth.config.deployment import resolve_deployment  # noqa: E402
from tigrbl_auth.config.deployment import DEFAULT_VALUES  # noqa: E402
from tigrbl_auth.standards.oauth2.resource_verifier_contract import (  # noqa: E402
    build_protected_resource_verifier_contract,
)
from tigrbl_authz_resource_server import (  # noqa: E402
    AccessTokenClaims,
    ResourceServerVerifier,
    verifier_contract_from_metadata,
)


def _policy() -> VerifierPolicy:
    return VerifierPolicy(
        issuer="https://auth.example.test/realms/acme",
        audiences=frozenset({"api://notes"}),
        required_scopes=frozenset({"notes:read"}),
        max_authz_staleness_seconds=60,
    )


def _claims(**overrides: object) -> dict[str, object]:
    now = int(time.time())
    claims: dict[str, object] = {
        "iss": "https://auth.example.test/realms/acme",
        "aud": "api://notes",
        "scope": "notes:read notes:write",
        "iat": now,
        "authz_iat": now,
        "exp": now + 300,
    }
    claims.update(overrides)
    return claims


def _deployment():
    values = dict(DEFAULT_VALUES)
    values.update(
        issuer="https://auth.example.test",
        protected_resource_identifier="https://auth.example.test/resource",
    )
    return resolve_deployment(
        SimpleNamespace(**values),
        profile="production",
        product_surface="resource-validation-api",
    )


def test_resource_server_verifier_t0_contract_exports_verifier_policy() -> None:
    assert callable(assert_verifier_accepts)


def test_resource_server_verifier_t1_accepts_matching_claims() -> None:
    assert_verifier_accepts(_policy(), _claims())


@pytest.mark.parametrize(
    "overrides,match",
    [
        ({"iss": "https://other.example.test"}, "issuer"),
        ({"aud": "api://other"}, "audience"),
        ({"scope": "notes:write"}, "scope"),
        ({"exp": 1}, "expired"),
        ({"authz_iat": int(time.time()) - 120}, "stale"),
    ],
)
def test_resource_server_verifier_t2_fails_closed_for_bad_claims(
    overrides: dict[str, object],
    match: str,
) -> None:
    with pytest.raises(CertificationError, match=match):
        assert_verifier_accepts(_policy(), _claims(**overrides))


def test_verifier_contract_t1_projects_resource_validation_profile() -> None:
    deployment = _deployment()

    contract = build_protected_resource_verifier_contract(deployment)
    metadata = contract.as_metadata_projection()
    profile = verifier_contract_from_metadata(metadata)

    assert metadata["issuer"] == "https://auth.example.test"
    assert metadata["jwks_uri"] == "https://auth.example.test/.well-known/jwks.json"
    assert metadata["introspection_endpoint"] == "https://auth.example.test/introspect"
    assert metadata["fail_closed"] is True
    assert profile.resource_requirement().issuer == "https://auth.example.test"


def test_verifier_contract_t2_rejects_stale_authorization_snapshot() -> None:
    metadata = build_protected_resource_verifier_contract(
        _deployment()
    ).as_metadata_projection()
    profile = verifier_contract_from_metadata(metadata)
    requirement = profile.resource_requirement()
    verifier = ResourceServerVerifier(now=lambda: 1_000)
    claims = AccessTokenClaims(
        iss=profile.issuer,
        sub="user-1",
        aud=profile.audiences,
        exp=2_000,
        iat=1,
        scope=profile.required_scopes,
    )

    result = verifier.verify_claims(claims, requirement)

    assert not result.allowed
    assert "stale" in result.reason
