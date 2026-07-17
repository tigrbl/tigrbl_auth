import pytest
from types import SimpleNamespace

from tigrbl_auth.config.deployment import DEFAULT_VALUES
from tigrbl_auth.security.certification import (
    CertificationError,
    RealmState,
    assert_realm_isolation,
    deterministic_issuer,
)
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.services.tenant_discovery import (
    build_realm_openid_config,
    build_tenant_openid_config,
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


def test_realm_isolation_t2_integrates_with_realm_and_tenant_metadata() -> None:
    values = dict(DEFAULT_VALUES)
    values.update(
        issuer="https://auth.example.test",
        protected_resource_identifier="https://auth.example.test/resource",
    )
    deployment = resolve_deployment(
        SimpleNamespace(**values),
        profile="production",
        product_surface="resource-validation-app",
    )

    realm_a = build_realm_openid_config(deployment, "realm-a")
    realm_b = build_realm_openid_config(deployment, "realm-b")
    tenant_a = build_tenant_openid_config(deployment, "tenant-a")
    tenant_b = build_tenant_openid_config(deployment, "tenant-b")

    assert realm_a["issuer"] != realm_b["issuer"]
    assert realm_a["jwks_uri"] != realm_b["jwks_uri"]
    assert tenant_a["issuer"] != tenant_b["issuer"]
    assert tenant_a["jwks_uri"] != tenant_b["jwks_uri"]
    assert tenant_a["issuer"] not in {realm_a["issuer"], realm_b["issuer"]}
