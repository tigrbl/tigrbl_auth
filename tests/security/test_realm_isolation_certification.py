import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    RealmState,
    assert_realm_isolation,
    deterministic_issuer,
)


def _realm(realm_id: str, slug: str) -> RealmState:
    issuer = deterministic_issuer(
        "https://auth.example.test",
        realm_slug=slug,
    )
    return RealmState(
        realm_id=realm_id,
        slug=slug,
        issuer=issuer,
        jwks_uri=f"{issuer}/.well-known/jwks.json",
        key_ids=frozenset({f"key-{realm_id}"}),
        tenant_ids=frozenset({f"tenant-{realm_id}"}),
        client_ids=frozenset({f"client-{realm_id}"}),
        policy_ids=frozenset({f"policy-{realm_id}"}),
        token_ids=frozenset({f"token-{realm_id}"}),
        cache_namespace=f"realm:{realm_id}",
        admin_authorities=frozenset({f"admin-{realm_id}"}),
    )


def test_realm_isolation_t0_contract_exports_runtime_check() -> None:
    assert callable(assert_realm_isolation)


def test_realm_isolation_t1_accepts_disjoint_realms() -> None:
    assert_realm_isolation((_realm("a", "realm-a"), _realm("b", "realm-b")))


def test_realm_isolation_t2_rejects_cross_realm_tenant_leakage() -> None:
    realm_a = _realm("a", "realm-a")
    realm_b = _realm("b", "realm-b")
    compromised = RealmState(
        **{**realm_b.__dict__, "tenant_ids": frozenset({"tenant-a"})}
    )

    with pytest.raises(CertificationError, match="tenant"):
        assert_realm_isolation((realm_a, compromised))
