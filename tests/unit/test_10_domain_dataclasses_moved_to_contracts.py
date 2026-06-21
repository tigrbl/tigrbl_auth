from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_ROOT = ROOT / "pkgs" / "10-domain"

ALLOWED_DOMAIN_DATACLASSES = {
    "tigrbl-identity-principals/src/tigrbl_identity_principals/service.py::PrincipalDirectory",
}


def _dataclass_defs(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for decorator in node.decorator_list:
            target = decorator.func if isinstance(decorator, ast.Call) else decorator
            if getattr(target, "id", getattr(target, "attr", "")) == "dataclass":
                names.add(node.name)
    return names


def test_10_domain_reusable_dataclasses_are_core_contract_reexports() -> None:
    import tigrbl_security_trust_contracts as security_trust_contracts
    import tigrbl_identity_contracts as user_contracts
    from tigrbl_identity_contracts.evidence.key_rotation import KeyRotationAuditEvidence
    from tigrbl_identity_contracts.policy.key_rotation import (
        EffectiveKeyRotationPolicy,
        KeyRotationPolicyVersion,
    )
    from tigrbl_identity_jose import boundary, key_rotation_policy, pqc
    from tigrbl_identity_jose.standards import rfc7516
    from tigrbl_identity_principals import models, tenant_discovery

    assert boundary.JoseKey is user_contracts.JoseKey
    assert boundary.KeyRotationContract is user_contracts.KeyRotationContract
    assert key_rotation_policy.KeyRotationPolicyVersion is KeyRotationPolicyVersion
    assert key_rotation_policy.EffectiveKeyRotationPolicy is EffectiveKeyRotationPolicy
    assert not hasattr(key_rotation_policy, "KeyRotationAuditEvidence")
    audit = key_rotation_policy.KeyRotationAdministration(
        key_rotation_policy.KeyRotationPolicyGovernance()
    )
    assert audit.audit_records == ()
    assert KeyRotationAuditEvidence.__name__ == "KeyRotationAuditEvidence"
    assert pqc.PQCSignatureKeyPair is security_trust_contracts.PQCSignatureKeyPair
    assert rfc7516.JWEPolicy is user_contracts.JWEPolicy
    assert models.Realm is user_contracts.Realm
    assert models.TenantBoundary is user_contracts.TenantBoundary
    assert models.Principal is user_contracts.Principal
    assert models.TenantMembership is user_contracts.TenantMembership
    assert models.SubjectAlias is user_contracts.SubjectAlias
    assert tenant_discovery.TenantTrustDomainAuthority is user_contracts.TenantTrustDomainAuthority
    assert tenant_discovery.RealmTrustDomainAuthority is user_contracts.RealmTrustDomainAuthority
    assert not hasattr(tenant_discovery, "TenantPublicDiscoveryBoundaryFeature")


def test_10_domain_only_keeps_implementation_local_dataclasses() -> None:
    offenders: list[str] = []
    for path in DOMAIN_ROOT.rglob("*.py"):
        relative = path.relative_to(DOMAIN_ROOT).as_posix()
        for name in sorted(_dataclass_defs(path)):
            entry = f"{relative}::{name}"
            if entry not in ALLOWED_DOMAIN_DATACLASSES:
                offenders.append(entry)

    assert offenders == []
