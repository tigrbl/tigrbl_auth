from __future__ import annotations

import ast
import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def _imports_for(package: str) -> set[str]:
    package_root = next((ROOT / "pkgs").glob(f"02-contracts/*/src/{package}"))
    imports: set[str] = set()
    for path in package_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
    return imports


def test_user_plane_contracts_own_authn_resource_and_security_surfaces() -> None:
    import tba_contracts_identity as contracts
    import tba_contracts_security_trust as security_trust
    from tba_credentials.lifecycle import Credential
    from tba_credentials.proof_bindings import ProofBinding

    assert contracts.CredentialKind.PASSWORD.value == "password"
    assert Credential is contracts.Credential
    assert ProofBinding is contracts.ProofBinding
    assert contracts.AccessTokenClaims(
        iss="issuer",
        sub="subject",
        aud=("api",),
        exp=1,
        iat=1,
    ).aud == ("api",)
    assert security_trust.Artifact(kind="token", format="jwt").kind == "token"


def test_management_plane_contracts_own_admin_and_governance_surfaces() -> None:
    import tba_contracts_identity as control_contracts
    import tba_contracts_identity as contracts
    from tba_runtime_authorization_policy.control_plane import Role
    from tba_runtime_authorization_policy.governance_extension import SDKPackage

    assert Role is control_contracts.Role
    assert SDKPackage is contracts.SDKPackage
    assert (
        control_contracts.Role(name="admin", permissions=("tenant.read",)).name
        == "admin"
    )
    assert contracts.AdminResourceKind.PRINCIPAL.value == "principal"


def test_control_plane_contracts_own_control_plane_correctness_dtos() -> None:
    import tba_contracts_identity as contracts
    from tba_runtime_authorization_policy import (
        ControlPlaneCorrectnessReport,
        CorrectnessProofSection,
    )

    assert CorrectnessProofSection is contracts.CorrectnessProofSection
    assert ControlPlaneCorrectnessReport is contracts.ControlPlaneCorrectnessReport


def test_control_plane_contracts_do_not_export_executable_boundary_helpers() -> None:
    import tba_contracts_identity as contracts

    executable_helpers = {
        "provisioning_governance_ecosystem_boundary_manifest",
        "provisioning_governance_ecosystem_boundary_integrity",
        "".join(("pha", "se5_governance_extension_boundary_manifest")),
        "".join(("pha", "se5_governance_extension_boundary_integrity")),
        "build_control_plane_correctness_report",
    }

    assert not (executable_helpers & set(dir(contracts)))


def test_control_plane_contract_modules_have_no_top_level_functions() -> None:
    package_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )
    checked_modules = {
        "admin.py",
        "adaptive_access.py",
        "correctness/authorization.py",
        "correctness/reports.py",
    }
    offenders: list[str] = []

    for name in checked_modules:
        path = package_root / name
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}:{node.name}")

    assert offenders == []


def test_control_plane_executable_helpers_stay_in_authz_policy_capability() -> None:
    import tba_contracts_identity as contracts
    import tba_contracts_identity as management_contracts
    import tba_runtime_authorization_policy.control_plane as admin_models
    import tba_runtime_authorization_policy.governance_extension as governance_models

    assert admin_models.Role is contracts.Role
    assert governance_models.SDKPackage is management_contracts.SDKPackage
    assert set(admin_models.PUBLIC_CLIENT_FIELDS) < set(
        admin_models.ADMIN_CLIENT_FIELDS
    )
    assert "client_secret" not in admin_models.PUBLIC_CLIENT_FIELDS
    assert not hasattr(
        governance_models, "provisioning_governance_ecosystem_boundary_manifest"
    )
    assert not hasattr(
        governance_models, "provisioning_governance_ecosystem_boundary_integrity"
    )


def test_release_contracts_own_release_posture_surfaces() -> None:
    import tba_contracts_release as contracts
    from tba_certification_release.release_posture.models import (
        TransportPosture,
    )

    assert TransportPosture is contracts.TransportPosture


def test_management_plane_contracts_own_residency_and_evidence_surfaces() -> None:
    import tba_contracts_identity as contracts
    from tba_contracts_identity.evidence.key_rotation import KeyRotationAuditEvidence
    from tba_runtime_authorization_policy import ResidencyZone

    assert ResidencyZone is contracts.ResidencyZone
    assert KeyRotationAuditEvidence.__name__ == "KeyRotationAuditEvidence"
    assert not hasattr(contracts, "KeyRotationAuditEvidence")


def test_admin_capability_models_are_contract_reexports() -> None:
    from tba_contracts_identity.audit.admin import AdminAuditEvent
    import tba_contracts_identity as control_contracts
    import tba_contracts_identity as management_contracts
    import tba_contracts_identity as user_contracts
    import tigrbl_identity_credentials_concrete as credential_concrete
    import tigrbl_identity_identities_concrete as identity_concrete
    from tba_runtime_identity_administration._advanced_identity_plane import models as advanced_models
    from tba_runtime_identity_administration._control_plane import models as legacy_admin_models
    from tba_runtime_identity_administration_control_plane import models as admin_models

    assert admin_models.AdminResource is management_contracts.AdminResource
    assert admin_models.App is management_contracts.App
    assert legacy_admin_models.AdminResource is management_contracts.AdminResource
    assert not hasattr(admin_models, "PrincipalRecord")
    assert not hasattr(admin_models, "AdminAuditEvent")
    assert AdminAuditEvent.__name__ == "AdminAuditEvent"
    assert not hasattr(admin_models, "AdminUiView")
    assert advanced_models.AdaptiveContext is control_contracts.AdaptiveContext
    assert (
        advanced_models.AccessDecisionRequest is control_contracts.AccessDecisionRequest
    )
    assert advanced_models.TrustPath is control_contracts.TrustPath
    assert (
        advanced_models.PasswordlessCredential
        is credential_concrete.PasswordlessCredential
    )
    assert (
        advanced_models.AuthenticationChallenge
        is user_contracts.AuthenticationChallenge
    )
    assert advanced_models.WorkloadIdentity is identity_concrete.WorkloadIdentity
    assert not hasattr(advanced_models, "AdvancedIdentityBoundaryFeature")


def test_advanced_identity_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "advanced_identity.py").exists()
    assert (contracts_root / "authentication" / "__init__.py").exists()
    assert (contracts_root / "authentication" / "challenges.py").exists()
    assert not (contracts_root / "credentials" / "passwordless.py").exists()
    assert not (contracts_root / "credentials" / "webauthn.py").exists()
    assert not (contracts_root / "credentials" / "factors.py").exists()
    assert (contracts_root / "federation" / "__init__.py").exists()
    assert (contracts_root / "federation" / "providers.py").exists()
    assert (contracts_root / "federation" / "sessions.py").exists()
    assert not (contracts_root / "principals" / "devices.py").exists()
    assert not (contracts_root / "principals" / "workloads.py").exists()
    concrete_root = (
        ROOT
        / "pkgs"
        / "deprecated"
        / "tigrbl-identity-identities-concrete"
        / "src"
        / "tigrbl_identity_identities_concrete"
    )
    credential_root = (
        ROOT
        / "pkgs"
        / "deprecated"
        / "tigrbl-identity-credentials-concrete"
        / "src"
        / "tigrbl_identity_credentials_concrete"
    )
    assert (credential_root / "__init__.py").exists()
    assert (concrete_root / "__init__.py").exists()


def test_application_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert (contracts_root / "applications" / "__init__.py").exists()
    assert (contracts_root / "applications" / "models.py").exists()


def test_authority_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "authz" / "authority_graph.py").exists()
    assert not (contracts_root / "authz" / "authority_roles.py").exists()
    assert not (contracts_root / "authz" / "authority_semantics.py").exists()
    assert not (contracts_root / "trust_domains.py").exists()
    assert (contracts_root / "authority" / "__init__.py").exists()
    assert (contracts_root / "authority" / "graph.py").exists()
    assert (contracts_root / "authority" / "roles.py").exists()
    assert (contracts_root / "authority" / "semantics.py").exists()
    assert (contracts_root / "authority" / "trust_domains.py").exists()
    assert not hasattr(__import__("tba_contracts_identity.admin").admin, "Role")

    from tba_contracts_identity.authority import Role

    assert Role.__module__ == "tba_contracts_identity.authority.roles"


def test_correctness_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "correctness.py").exists()
    assert not (contracts_root / "authz" / "correctness.py").exists()
    assert not (contracts_root / "authz" / "correctness_report.py").exists()
    assert (contracts_root / "correctness" / "__init__.py").exists()
    assert (contracts_root / "correctness" / "authorization.py").exists()
    assert (contracts_root / "correctness" / "reports.py").exists()


def test_invariant_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "authz" / "invariants.py").exists()
    assert (contracts_root / "invariants" / "__init__.py").exists()


def test_liveness_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "authz" / "liveness.py").exists()
    assert (contracts_root / "liveness" / "__init__.py").exists()
    assert not (
        ROOT
        / "pkgs"
        / "00-primitives"
        / "tba-primitives-identity"
        / "src"
        / "tba_primitives_identity"
        / "liveness.py"
    ).exists()

    import tba_contracts_identity.liveness as liveness

    assert liveness.ConvergenceEvent.__module__ == "tba_contracts_identity.liveness"
    assert liveness.ConvergenceState.__module__ == "tba_contracts_identity.liveness"
    assert (
        liveness.LivenessConvergenceReport.__module__
        == "tba_contracts_identity.liveness"
    )
    sys.modules.pop("tba_primitives_identity.liveness", None)
    try:
        importlib.import_module("tba_primitives_identity.liveness")
    except ModuleNotFoundError:
        pass
    else:  # pragma: no cover - fail if core starts owning liveness records again.
        raise AssertionError("tba_primitives_identity.liveness should not exist")


def test_replay_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "authz" / "replay.py").exists()
    assert (contracts_root / "replay" / "__init__.py").exists()


def test_governance_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "governance.py").exists()
    assert (contracts_root / "governance" / "__init__.py").exists()
    assert (contracts_root / "governance" / "plugin" / "__init__.py").exists()
    assert (contracts_root / "governance" / "scim" / "__init__.py").exists()
    assert (contracts_root / "governance" / "entitlement" / "__init__.py").exists()
    assert (contracts_root / "governance" / "accessreview" / "__init__.py").exists()


def test_service_identity_contracts_are_placed_with_owning_domains() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "service_identity.py").exists()
    assert not (contracts_root / "service_identity").exists()
    assert not (contracts_root / "principals" / "services.py").exists()
    assert not (contracts_root / "credentials" / "services.py").exists()
    assert (contracts_root / "authentication" / "services.py").exists()
    assert (contracts_root / "delegation" / "admin.py").exists()


def test_delegation_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "authz" / "delegation_lifecycle_models.py").exists()
    assert not (contracts_root / "authz" / "delegation_proofs.py").exists()
    assert (contracts_root / "delegation" / "__init__.py").exists()
    assert (contracts_root / "delegation" / "lifecycle.py").exists()
    assert (contracts_root / "delegation" / "proofs.py").exists()


def test_residency_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "residency.py").exists()
    assert not (contracts_root / "authz" / "residency.py").exists()
    assert (contracts_root / "residency" / "__init__.py").exists()
    assert (contracts_root / "residency" / "errors.py").exists()
    assert (contracts_root / "residency" / "zones.py").exists()
    assert (contracts_root / "residency" / "records.py").exists()
    assert (contracts_root / "residency" / "decisions.py").exists()


def test_policy_contracts_are_domain_packaged_without_old_owners() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "authz" / "decisions.py").exists()
    assert not (contracts_root / "authz").exists()
    assert not (contracts_root / "key_rotation.py").exists()
    assert (contracts_root / "policy" / "__init__.py").exists()
    assert (contracts_root / "policy" / "conditions.py").exists()
    assert (contracts_root / "policy" / "decisions.py").exists()
    assert (contracts_root / "policy" / "definitions.py").exists()
    assert (contracts_root / "policy" / "effects.py").exists()
    assert (contracts_root / "policy" / "kinds.py").exists()
    assert (contracts_root / "policy" / "ports.py").exists()
    assert (contracts_root / "policy" / "requests.py").exists()
    assert (contracts_root / "policy" / "rules.py").exists()
    assert (contracts_root / "policy" / "versions.py").exists()
    assert (
        ROOT
        / "pkgs"
        / "10-concrete"
        / "tba-concrete-authorization-policy-rules"
        / "src"
        / "tba_concrete_authorization_policy_rules"
        / "__init__.py"
    ).exists()


def test_plane_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "02-contracts"
        / "tba-contracts-identity"
        / "src"
        / "tba_contracts_identity"
    )

    assert not (contracts_root / "planes.py").exists()
    assert (contracts_root / "planes" / "__init__.py").exists()


def test_removed_plane_contract_import_roots_are_not_loaded() -> None:
    assert "tba_user_plane_contracts" not in sys.modules
    assert "tba_control_plane_contracts" not in sys.modules
    assert "tba_management_plane_contracts" not in sys.modules


def test_contract_packages_do_not_import_capability_runtime_or_storage_packages() -> (
    None
):
    forbidden = {
        "tba_auth",
        "tba_credentials",
        "tba_authn_credentials",
        "tba_runtime_authorization_policy",
        "tba_protocol_authorization_resource_server",
        "tba_runtime_identity",
        "tba_storage_core",
        "tba_certification_release",
    }

    for package in (
        "tba_contracts_identity",
        "tba_contracts_release",
        "tba_contracts_security_trust",
    ):
        assert not (_imports_for(package) & forbidden), package


def test_target_capability_packages_no_longer_own_contract_classes() -> None:
    capability_roots = [
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-identity-admin-control-plane"
        / "src"
        / "tba_runtime_identity_administration_control_plane",
        ROOT
        / "pkgs"
        / "20-providers"
        / "tba-runtime-identity-administration"
        / "src"
        / "tba_runtime_identity_administration",
        ROOT
        / "pkgs"
        / "70-facade"
        / "tba-credentials"
        / "src"
        / "tba_credentials",
        ROOT
        / "pkgs"
        / "20-providers"
        / "tba-runtime-authorization-policy"
        / "src"
        / "tba_runtime_authorization_policy",
    ]
    offenders: list[str] = []

    for package_root in capability_roots:
        for path in package_root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            decorators = {
                node.lineno
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            }
            del decorators
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    base_names = {
                        getattr(base, "id", getattr(base, "attr", ""))
                        for base in node.bases
                    }
                    has_dataclass = any(
                        getattr(decorator, "id", getattr(decorator, "attr", ""))
                        == "dataclass"
                        or (
                            isinstance(decorator, ast.Call)
                            and getattr(
                                decorator.func,
                                "id",
                                getattr(decorator.func, "attr", ""),
                            )
                            == "dataclass"
                        )
                        for decorator in node.decorator_list
                    )
                    if (
                        has_dataclass
                        or "Enum" in base_names
                        or "Protocol" in base_names
                        or "BaseModel" in base_names
                    ):
                        offenders.append(
                            f"{path.relative_to(ROOT)}:{node.lineno}:{node.name}"
                        )

    assert offenders == []
