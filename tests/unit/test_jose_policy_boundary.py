from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for src in (ROOT / "pkgs").glob("*/src"):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)

from tigrbl_identity_jose import (
    RFC_TARGETS,
    JoseKey,
    JoseKeyRotationResult,
    JoseKeySet,
    JoseKeyStatus,
    JoseKeyUse,
    jwk_thumbprint,
    publish_tenant_jwks,
    rfc_vector_manifest,
)
from tigrbl_authz_policy import (
    AdminPolicy,
    AttributePolicy,
    DelegationPolicy,
    PermissionPolicy,
    PolicyDecisionEngine,
    PolicyKind,
    PolicyRequest,
    RolePolicy,
)
from tigrbl_authz_policy_decision_engine import PolicyDecisionEngine as CanonicalPolicyDecisionEngine


PUBLIC_JWK = {
    "kty": "OKP",
    "crv": "Ed25519",
    "kid": "kid-active",
    "x": "11qYAYKxCrfVS_3-f2Y7nDyxq5xT8uQv_Bf-8AIU7fo",
    "d": "private-material-is-not-published",
}


@pytest.mark.unit
def test_jose_policy_t0_public_surfaces_are_importable() -> None:
    assert RFC_TARGETS["jwk"] == "RFC 7517"
    assert rfc_vector_manifest()["jwt-bcp"] == "RFC 8725"
    assert PolicyKind.RBAC.value == "rbac"
    assert PolicyDecisionEngine is CanonicalPolicyDecisionEngine

    key = JoseKey(
        kid="kid-active",
        tenant_id="tenant-a",
        jwk=PUBLIC_JWK,
        algorithm="EdDSA",
        key_use=JoseKeyUse.SIGN,
        status=JoseKeyStatus.ACTIVE,
    )

    assert key.public_jwk()["kid"] == "kid-active"
    assert "d" not in key.public_jwk()


@pytest.mark.unit
def test_jose_t1_vectors_rotation_and_tenant_jwks_publication() -> None:
    active = JoseKey(
        kid="kid-active",
        tenant_id="tenant-a",
        jwk=PUBLIC_JWK,
        algorithm="EdDSA",
        status=JoseKeyStatus.ACTIVE,
    )
    other_tenant = JoseKey(
        kid="kid-other",
        tenant_id="tenant-b",
        jwk={**PUBLIC_JWK, "kid": "kid-other"},
        algorithm="EdDSA",
        status=JoseKeyStatus.ACTIVE,
    )
    keyset = JoseKeySet([active, other_tenant])

    rotation = keyset.rotate(
        tenant_id="tenant-a",
        next_key=JoseKey(
            kid="kid-next",
            tenant_id="tenant-a",
            jwk={**PUBLIC_JWK, "kid": "kid-next"},
            algorithm="EdDSA",
            status=JoseKeyStatus.NEXT,
        ),
        reason="scheduled rotation",
    )
    jwks = publish_tenant_jwks(keyset.keys.values(), tenant_id="tenant-a")

    assert jwk_thumbprint(PUBLIC_JWK)
    assert isinstance(rotation, JoseKeyRotationResult)
    assert rotation.current_kid == "kid-active"
    assert rotation.retired_kids == ("kid-active",)
    assert [key["kid"] for key in jwks["keys"]] == ["kid-next"]
    assert "kid-other" not in rotation.published_kids


@pytest.mark.unit
def test_policy_t1_rbac_abac_pbac_delegation_admin_and_trace() -> None:
    engine = PolicyDecisionEngine(
        roles=[
            RolePolicy(role="tenant-admin", tenant_id="tenant-a", permissions=("tenant.*",)),
        ],
        attributes=[
            AttributePolicy(
                policy_id="abac:same-region",
                tenant_id="tenant-a",
                action="tenant.update",
                required_attributes={"region": "us-sw"},
            )
        ],
        permissions=[
            PermissionPolicy(
                policy_id="pbac:tenant-update",
                tenant_id="tenant-a",
                permissions=("tenant.update",),
            )
        ],
        delegations=[
            DelegationPolicy(
                delegate="user:delegate",
                delegator="user:owner",
                tenant_ids=("tenant-a",),
                actions=("tenant.update",),
            )
        ],
        admins=[
            AdminPolicy(
                subject="user:delegate",
                tenant_ids=("tenant-a",),
                actions=("tenant.update",),
            )
        ],
    )
    request = PolicyRequest(
        subject="user:delegate",
        tenant_id="tenant-a",
        action="tenant.update",
        roles=("tenant-admin",),
        attributes={"region": "us-sw"},
        permissions=("tenant.update",),
        delegated_by="user:owner",
        admin=True,
    )

    decision = engine.evaluate(request)

    assert decision.allowed is True
    assert decision.trace_id == "poltrace:1"
    assert engine.traces[0].matched == ("abac:same-region", "pbac:tenant-update", "tenant-admin", "user:delegate", "user:owner")
    assert engine.traces[0].evaluated_kinds == (
        PolicyKind.DELEGATION,
        PolicyKind.ADMIN,
        PolicyKind.RBAC,
        PolicyKind.ABAC,
        PolicyKind.PBAC,
    )


@pytest.mark.unit
def test_policy_t2_denies_out_of_scope_delegation_and_admin() -> None:
    engine = PolicyDecisionEngine(
        roles=[RolePolicy(role="tenant-admin", tenant_id="tenant-a", permissions=("tenant.*",))],
        delegations=[
            DelegationPolicy(
                delegate="user:delegate",
                delegator="user:owner",
                tenant_ids=("tenant-a",),
                actions=("tenant.update",),
            )
        ],
        admins=[AdminPolicy(subject="user:delegate", tenant_ids=("tenant-a",), actions=("tenant.update",))],
    )

    delegated = engine.evaluate(
        PolicyRequest(
            subject="user:delegate",
            tenant_id="tenant-b",
            action="tenant.update",
            roles=("tenant-admin",),
            delegated_by="user:owner",
            admin=True,
        )
    )
    admin = engine.evaluate(
        PolicyRequest(
            subject="user:delegate",
            tenant_id="tenant-b",
            action="tenant.delete",
            roles=("tenant-admin",),
            admin=True,
        )
    )

    assert delegated.allowed is False
    assert delegated.reason == "delegation tenant scope denied"
    assert admin.allowed is False
    assert admin.reason == "admin policy denied"
    assert [trace.allowed for trace in engine.traces] == [False, False]


@pytest.mark.unit
def test_jose_policy_t2_public_boundary_has_no_forbidden_imports() -> None:
    root = Path("pkgs")
    files = [
        root / "30-providers/tigrbl-identity-jose/src/tigrbl_identity_jose/__init__.py",
        root / "30-providers/tigrbl-identity-jose/src/tigrbl_identity_jose/boundary.py",
        root / "40-capabilities/tigrbl-authz-policy-decision-engine/src/tigrbl_authz_policy_decision_engine/engine.py",
        root / "40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/__init__.py",
        root / "40-capabilities/tigrbl-authz-policy/src/tigrbl_authz_policy/decisions.py",
    ]
    forbidden = {"tigrbl_auth", "tigrbl_auth_protocol_oauth", "tigrbl_auth_protocol_oidc", "tigrbl_identity_server"}

    imports: set[str] = set()
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.level == 0:
                    imports.add(node.module.split(".")[0])

    assert imports.isdisjoint(forbidden)
