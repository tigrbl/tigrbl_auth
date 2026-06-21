from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def _imports_for(package: str) -> set[str]:
    package_root = next((ROOT / "pkgs").glob(f"01-contracts/*/src/{package}"))
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
    import tigrbl_identity_contracts as contracts
    import tigrbl_security_trust_contracts as security_trust
    from tigrbl_authn_credentials.lifecycle import Credential
    from tigrbl_authn_credentials.proof_bindings import ProofBinding

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
    import tigrbl_identity_contracts as control_contracts
    import tigrbl_identity_contracts as contracts
    from tigrbl_authz_policy._control_plane.models import Role
    from tigrbl_authz_policy._governance_extension.models import SDKPackage

    assert Role is control_contracts.Role
    assert SDKPackage is contracts.SDKPackage
    assert control_contracts.Role(name="admin", permissions=("tenant.read",)).name == "admin"
    assert contracts.AdminResourceKind.PRINCIPAL.value == "principal"


def test_control_plane_contracts_own_control_plane_correctness_dtos() -> None:
    import tigrbl_identity_contracts as contracts
    from tigrbl_authz_policy import ControlPlaneCorrectnessReport, CorrectnessProofSection

    assert CorrectnessProofSection is contracts.CorrectnessProofSection
    assert ControlPlaneCorrectnessReport is contracts.ControlPlaneCorrectnessReport


def test_control_plane_contracts_do_not_export_executable_boundary_helpers() -> None:
    import tigrbl_identity_contracts as contracts

    executable_helpers = {
        "admin_policy_boundary_manifest",
        "admin_policy_boundary_integrity",
        "phase3_admin_policy_boundary_manifest",
        "phase3_admin_policy_boundary_integrity",
        "provisioning_governance_ecosystem_boundary_manifest",
        "provisioning_governance_ecosystem_boundary_integrity",
        "phase5_governance_extension_boundary_manifest",
        "phase5_governance_extension_boundary_integrity",
        "build_control_plane_correctness_report",
    }

    assert not (executable_helpers & set(dir(contracts)))


def test_control_plane_contract_modules_have_no_top_level_functions() -> None:
    package_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
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
    import tigrbl_identity_contracts as contracts
    import tigrbl_identity_contracts as management_contracts
    from tigrbl_authz_policy._control_plane import models as admin_models
    from tigrbl_authz_policy._governance_extension import models as governance_models

    assert admin_models.Role is contracts.Role
    assert governance_models.SDKPackage is management_contracts.SDKPackage
    assert admin_models.admin_policy_boundary_integrity()["passed"] is True
    assert "feat:f13-rbac" in admin_models.admin_policy_boundary_manifest()
    assert not hasattr(governance_models, "provisioning_governance_ecosystem_boundary_manifest")
    assert not hasattr(governance_models, "provisioning_governance_ecosystem_boundary_integrity")


def test_release_contracts_own_release_posture_surfaces() -> None:
    import tigrbl_release_contracts as contracts
    from tigrbl_authz_policy._release_posture.models import TransportPosture

    assert TransportPosture is contracts.TransportPosture


def test_management_plane_contracts_own_residency_and_evidence_surfaces() -> None:
    import tigrbl_identity_contracts as contracts
    from tigrbl_identity_contracts.evidence.key_rotation import KeyRotationAuditEvidence
    from tigrbl_authz_policy import ResidencyZone

    assert ResidencyZone is contracts.ResidencyZone
    assert KeyRotationAuditEvidence.__name__ == "KeyRotationAuditEvidence"
    assert not hasattr(contracts, "KeyRotationAuditEvidence")


def test_admin_capability_models_are_contract_reexports() -> None:
    from tigrbl_identity_contracts.audit.admin import AdminAuditEvent
    import tigrbl_identity_contracts as control_contracts
    import tigrbl_identity_contracts as management_contracts
    import tigrbl_identity_contracts as user_contracts
    from tigrbl_identity_admin._advanced_identity_plane import models as advanced_models
    from tigrbl_identity_admin._control_plane import models as admin_models

    assert admin_models.AdminResource is management_contracts.AdminResource
    assert admin_models.PrincipalRecord is management_contracts.PrincipalRecord
    assert not hasattr(admin_models, "AdminAuditEvent")
    assert AdminAuditEvent.__name__ == "AdminAuditEvent"
    assert admin_models.AdminUiView is management_contracts.AdminUiView
    assert advanced_models.AdaptiveContext is control_contracts.AdaptiveContext
    assert advanced_models.AccessDecisionRequest is control_contracts.AccessDecisionRequest
    assert advanced_models.TrustPath is control_contracts.TrustPath
    assert advanced_models.PasswordlessCredential is user_contracts.PasswordlessCredential
    assert advanced_models.AuthenticationChallenge is user_contracts.AuthenticationChallenge
    assert advanced_models.WorkloadIdentity is user_contracts.WorkloadIdentity
    assert not hasattr(advanced_models, "AdvancedIdentityBoundaryFeature")


def test_advanced_identity_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "advanced_identity.py").exists()
    assert (contracts_root / "authentication" / "__init__.py").exists()
    assert (contracts_root / "authentication" / "challenges.py").exists()
    assert (contracts_root / "credentials" / "passwordless.py").exists()
    assert (contracts_root / "credentials" / "webauthn.py").exists()
    assert (contracts_root / "credentials" / "factors.py").exists()
    assert (contracts_root / "federation" / "__init__.py").exists()
    assert (contracts_root / "federation" / "providers.py").exists()
    assert (contracts_root / "federation" / "sessions.py").exists()
    assert (contracts_root / "principals" / "devices.py").exists()
    assert (contracts_root / "principals" / "workloads.py").exists()


def test_authority_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "authz" / "authority_graph.py").exists()
    assert not (contracts_root / "authz" / "authority_roles.py").exists()
    assert not (contracts_root / "authz" / "authority_semantics.py").exists()
    assert (contracts_root / "authority" / "__init__.py").exists()
    assert (contracts_root / "authority" / "graph.py").exists()
    assert (contracts_root / "authority" / "roles.py").exists()
    assert (contracts_root / "authority" / "semantics.py").exists()


def test_correctness_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
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
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "authz" / "invariants.py").exists()
    assert (contracts_root / "invariants" / "__init__.py").exists()


def test_liveness_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "authz" / "liveness.py").exists()
    assert (contracts_root / "liveness" / "__init__.py").exists()


def test_governance_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
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
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "service_identity.py").exists()
    assert not (contracts_root / "service_identity").exists()
    assert (contracts_root / "principals" / "services.py").exists()
    assert (contracts_root / "credentials" / "services.py").exists()
    assert (contracts_root / "authentication" / "services.py").exists()
    assert (contracts_root / "delegation" / "admin.py").exists()


def test_delegation_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
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
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
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
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "authz" / "decisions.py").exists()
    assert not (contracts_root / "key_rotation.py").exists()
    assert (contracts_root / "policy" / "__init__.py").exists()
    assert (contracts_root / "policy" / "conditions.py").exists()
    assert (contracts_root / "policy" / "decisions.py").exists()
    assert (contracts_root / "policy" / "effects.py").exists()
    assert (contracts_root / "policy" / "key_rotation.py").exists()
    assert (contracts_root / "policy" / "kinds.py").exists()
    assert (contracts_root / "policy" / "lifecycle.py").exists()
    assert (contracts_root / "policy" / "requests.py").exists()
    assert (contracts_root / "policy" / "rules.py").exists()


def test_plane_contracts_are_domain_packaged() -> None:
    contracts_root = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts"
    )

    assert not (contracts_root / "planes.py").exists()
    assert (contracts_root / "planes" / "__init__.py").exists()


def test_removed_plane_contract_import_roots_are_not_loaded() -> None:
    assert "tigrbl_user_plane_contracts" not in sys.modules
    assert "tigrbl_control_plane_contracts" not in sys.modules
    assert "tigrbl_management_plane_contracts" not in sys.modules


def test_contract_packages_do_not_import_capability_runtime_or_storage_packages() -> None:
    forbidden = {
        "tigrbl_auth",
        "tigrbl_authn_credentials",
        "tigrbl_authz_policy",
        "tigrbl_authz_resource_server",
        "tigrbl_identity_runtime",
        "tigrbl_identity_storage",
    }

    for package in (
        "tigrbl_identity_contracts",
        "tigrbl_release_contracts",
        "tigrbl_security_trust_contracts",
    ):
        assert not (_imports_for(package) & forbidden), package


def test_target_capability_packages_no_longer_own_contract_classes() -> None:
    capability_roots = [
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-identity-admin"
        / "src"
        / "tigrbl_identity_admin",
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-authn-credentials"
        / "src"
        / "tigrbl_authn_credentials",
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-authz-policy"
        / "src"
        / "tigrbl_authz_policy",
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-authz-resource-server"
        / "src"
        / "tigrbl_authz_resource_server",
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
                    if has_dataclass or "Enum" in base_names or "Protocol" in base_names or "BaseModel" in base_names:
                        offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}:{node.name}")

    assert offenders == []
