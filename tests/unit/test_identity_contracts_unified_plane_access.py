from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_identity_contracts_are_canonical_for_identity_and_admin_contracts() -> None:
    import tigrbl_identity_contracts as contracts
    from tigrbl_security_key_rotation_policy_contracts import KeyRotationPolicyVersion
    from tigrbl_identity_contracts.policy.requests import PolicyRequest

    assert contracts.Principal.__module__.startswith("tigrbl_identity_contracts")
    assert contracts.Identity.__module__.startswith("tigrbl_identity_contracts")
    assert contracts.Credential.__module__.startswith("tigrbl_identity_contracts")
    assert PolicyRequest.__module__.startswith("tigrbl_identity_contracts.policy")
    assert contracts.ProtectedResourceVerifierContract.__module__.startswith("tigrbl_identity_contracts")
    assert contracts.Role.__module__ == "tigrbl_identity_contracts.authority.roles"
    assert contracts.AccessDecisionRequest.__module__.startswith("tigrbl_identity_contracts")
    assert KeyRotationPolicyVersion.__module__ == "tigrbl_security_key_rotation_policy_contracts"
    assert not hasattr(contracts, "PolicyRequest")
    assert not hasattr(contracts, "KeyRotationPolicyVersion")
    assert contracts.AdminResource.__module__.startswith("tigrbl_identity_contracts")
    assert contracts.App.__module__ == "tigrbl_identity_contracts.applications.models"
    assert not hasattr(contracts, "ServiceIdentity")
    assert contracts.SDKPackage.__module__.startswith("tigrbl_identity_contracts")
    assert contracts.ResidencyZone.__module__.startswith("tigrbl_identity_contracts")


def test_plane_access_and_capability_are_metadata_declarations() -> None:
    from tigrbl_identity_contracts import (
        PlaneAccess,
        PlaneAccessDeclaration,
        PlaneCapability,
        PlaneCapabilityDeclaration,
    )

    declaration = PlaneAccessDeclaration(
        surface="tenant-admin",
        access=PlaneAccess.TENANT_ADMIN,
        capabilities=(PlaneCapability.MANAGE_PRINCIPALS, "manage_credentials"),
        default_audience="tigrbl-auth-admin",
        default_scopes=("principal.read", "credential.write"),
        network_segment="admin",
        deployment_profile="tenant-admin",
    )

    assert declaration.access is PlaneAccess.TENANT_ADMIN
    assert declaration.declares_capability(PlaneCapability.MANAGE_CREDENTIALS)
    assert declaration.declares_capability("manage_principals")
    assert declaration.default_scopes == ("principal.read", "credential.write")

    capability = PlaneCapabilityDeclaration(
        capability="verify_resource_access",
        access=(PlaneAccess.RESOURCE_VALIDATION, "internal"),
        audiences=("resource-api",),
        required_permissions=("token.introspect",),
    )

    assert capability.capability is PlaneCapability.VERIFY_RESOURCE_ACCESS
    assert capability.permits_access("resource_validation")
    assert capability.permits_access(PlaneAccess.INTERNAL)


def test_release_and_security_trust_stay_separate_contract_packages() -> None:
    import tigrbl_identity_contracts
    import tigrbl_release_contracts
    import tigrbl_security_trust_contracts

    assert not hasattr(tigrbl_identity_contracts, "TransportPosture")
    assert not hasattr(tigrbl_identity_contracts, "Artifact")
    assert tigrbl_release_contracts.TransportPosture.__module__.startswith("tigrbl_release_contracts")
    assert tigrbl_security_trust_contracts.Artifact.__module__.startswith("tigrbl_security_trust_contracts")


def test_legacy_plane_contract_packages_are_not_loaded() -> None:
    assert "tigrbl_user_plane_contracts" not in sys.modules
    assert "tigrbl_control_plane_contracts" not in sys.modules
    assert "tigrbl_management_plane_contracts" not in sys.modules
