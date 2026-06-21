from __future__ import annotations

from typing import Mapping, Sequence

from .base import CertificationError
from tigrbl_release_contracts import RealmState, TenantState


def _assert_disjoint(label: str, owners: Mapping[str, frozenset[str]]) -> None:
    seen: dict[str, str] = {}
    for owner, values in owners.items():
        for value in values:
            previous = seen.setdefault(value, owner)
            if previous != owner:
                raise CertificationError(
                    f"{label} {value!r} crosses from {previous!r} to {owner!r}"
                )


def assert_realm_isolation(realms: Sequence[RealmState]) -> None:
    """Prove realm-scoped objects and metadata do not cross realm boundaries."""

    if len(realms) < 2:
        raise CertificationError("realm isolation certification requires at least two realms")
    ids = [realm.realm_id for realm in realms]
    slugs = [realm.slug for realm in realms]
    issuers = [realm.issuer for realm in realms]
    jwks = [realm.jwks_uri for realm in realms]
    namespaces = [realm.cache_namespace for realm in realms if realm.cache_namespace]
    for label, values in {
        "realm id": ids,
        "realm slug": slugs,
        "issuer": issuers,
        "jwks_uri": jwks,
        "cache namespace": namespaces,
    }.items():
        if len(values) != len(set(values)):
            raise CertificationError(f"duplicate {label} in realm isolation set")

    _assert_disjoint("tenant", {r.realm_id: r.tenant_ids for r in realms})
    _assert_disjoint("client", {r.realm_id: r.client_ids for r in realms})
    _assert_disjoint("policy", {r.realm_id: r.policy_ids for r in realms})
    _assert_disjoint("token", {r.realm_id: r.token_ids for r in realms})
    _assert_disjoint("key", {r.realm_id: r.key_ids for r in realms})
    _assert_disjoint("admin authority", {r.realm_id: r.admin_authorities for r in realms})


def assert_tenant_isolation(tenants: Sequence[TenantState]) -> None:
    """Prove same-realm and cross-realm tenant state cannot overlap."""

    if len(tenants) < 2:
        raise CertificationError("tenant isolation certification requires at least two tenants")
    pairs = {(tenant.realm_id, tenant.tenant_id) for tenant in tenants}
    if len(pairs) != len(tenants):
        raise CertificationError("duplicate tenant id inside a realm")
    for label, values in {
        "issuer": [t.issuer for t in tenants],
        "jwks_uri": [t.jwks_uri for t in tenants],
        "cache namespace": [t.cache_namespace for t in tenants if t.cache_namespace],
    }.items():
        if len(values) != len(set(values)):
            raise CertificationError(f"duplicate tenant {label}")
    _assert_disjoint("tenant client", {t.tenant_id: t.client_ids for t in tenants})
    _assert_disjoint("tenant user", {t.tenant_id: t.user_ids for t in tenants})
    _assert_disjoint("tenant policy", {t.tenant_id: t.policy_ids for t in tenants})
    _assert_disjoint("tenant credential", {t.tenant_id: t.credential_ids for t in tenants})
    _assert_disjoint("tenant token", {t.tenant_id: t.token_ids for t in tenants})
    _assert_disjoint("tenant key", {t.tenant_id: t.key_ids for t in tenants})


def assert_issuer_consistency(
    *,
    expected_issuer: str,
    metadata_issuer: str,
    token_issuer: str | None = None,
    jwks_uri: str | None = None,
    allowed_jwks_uri: str | None = None,
) -> None:
    if metadata_issuer != expected_issuer:
        raise CertificationError("metadata issuer mismatch")
    if token_issuer is not None and token_issuer != expected_issuer:
        raise CertificationError("token issuer mismatch")
    if allowed_jwks_uri is not None and jwks_uri != allowed_jwks_uri:
        raise CertificationError("jwks_uri mismatch")
