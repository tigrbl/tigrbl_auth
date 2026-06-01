import time

import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    VerifierPolicy,
    assert_verifier_accepts,
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
