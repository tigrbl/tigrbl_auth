import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    TenantState,
    assert_tenant_isolation,
    deterministic_issuer,
)


def _tenant(realm_id: str, tenant_id: str, slug: str) -> TenantState:
    issuer = deterministic_issuer(
        "https://auth.example.test",
        realm_slug=f"realm-{realm_id}",
        tenant_slug=slug,
    )
    return TenantState(
        tenant_id=tenant_id,
        slug=slug,
        realm_id=realm_id,
        issuer=issuer,
        jwks_uri=f"{issuer}/.well-known/jwks.json",
        key_ids=frozenset({f"key-{tenant_id}"}),
        client_ids=frozenset({f"client-{tenant_id}"}),
        user_ids=frozenset({f"user-{tenant_id}"}),
        policy_ids=frozenset({f"policy-{tenant_id}"}),
        credential_ids=frozenset({f"cred-{tenant_id}"}),
        token_ids=frozenset({f"token-{tenant_id}"}),
        cache_namespace=f"tenant:{realm_id}:{tenant_id}",
    )


def test_tenant_isolation_t0_contract_exports_runtime_check() -> None:
    assert callable(assert_tenant_isolation)


def test_tenant_isolation_t1_accepts_same_and_cross_realm_tenants() -> None:
    assert_tenant_isolation(
        (
            _tenant("a", "tenant-a", "tenant-a"),
            _tenant("a", "tenant-b", "tenant-b"),
            _tenant("b", "tenant-c", "tenant-c"),
        )
    )


def test_tenant_isolation_t2_rejects_cross_tenant_client_collision() -> None:
    tenant_a = _tenant("a", "tenant-a", "tenant-a")
    tenant_b = _tenant("a", "tenant-b", "tenant-b")
    compromised = TenantState(
        **{**tenant_b.__dict__, "client_ids": frozenset({"client-tenant-a"})}
    )

    with pytest.raises(CertificationError, match="client"):
        assert_tenant_isolation((tenant_a, compromised))
