import pytest

from tigrbl_auth.security.certification import (
    AuthorizationSnapshot,
    AuthorizationState,
    CertificationError,
    assert_authorization_fresh,
)
from tigrbl_auth.standards.oauth2.introspection import (
    introspect_token,
    register_token,
    reset_tokens,
)


def test_authorization_mutation_t0_contract_exports_versioned_state() -> None:
    state = AuthorizationState("user-1")
    assert state.version == 1


def test_authorization_freshness_t1_accepts_current_snapshot() -> None:
    state = AuthorizationState("user-1")
    snapshot = AuthorizationSnapshot(
        subject_id="user-1",
        version=state.version,
        issued_at=100,
        max_staleness_seconds=30,
    )

    assert_authorization_fresh(snapshot, state, now=120)


def test_authorization_mutation_freshness_t2_rejects_stale_or_mutated_snapshot() -> None:
    state = AuthorizationState("user-1")
    snapshot = AuthorizationSnapshot("user-1", state.version, 100, 30)
    state.mutate("role removed")

    with pytest.raises(CertificationError, match="mutation version"):
        assert_authorization_fresh(snapshot, state, now=110)

    fresh_version = AuthorizationSnapshot("user-1", state.version, 100, 5)
    with pytest.raises(CertificationError, match="freshness window"):
        assert_authorization_fresh(fresh_version, state, now=106)


def test_authorization_mutation_freshness_t2_stale_marks_introspection() -> None:
    reset_tokens()
    register_token(
        "stale-token",
        {
            "sub": "user-1",
            "authz_version": 1,
            "current_authz_version": 2,
            "iat": 100,
            "exp": 9999999999,
        },
    )

    payload = introspect_token("stale-token")

    assert payload["active"] is False
    assert payload["inactive_reason"] == "authorization_snapshot_stale"
