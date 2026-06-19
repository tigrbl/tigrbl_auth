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
    package_root = next((ROOT / "pkgs").glob(f"00-core/*/src/{package}"))
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
    import tigrbl_user_plane_contracts as contracts
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
    assert contracts.Artifact(kind="token", format="jwt").kind == "token"


def test_management_plane_contracts_own_admin_and_governance_surfaces() -> None:
    import tigrbl_control_plane_contracts as control_contracts
    import tigrbl_management_plane_contracts as contracts
    from tigrbl_authz_policy._control_plane.models import Role
    from tigrbl_authz_policy._governance_extension.models import SDKPackage

    assert Role is control_contracts.Role
    assert SDKPackage is contracts.SDKPackage
    assert control_contracts.Role(name="admin", permissions=("tenant.read",)).name == "admin"
    assert contracts.AdminResourceKind.PRINCIPAL.value == "principal"


def test_control_plane_contracts_own_control_plane_correctness_dtos() -> None:
    import tigrbl_control_plane_contracts as contracts
    import tigrbl_user_plane_contracts as user_contracts
    from tigrbl_authz_policy import ControlPlaneCorrectnessReport, CorrectnessProofSection

    assert CorrectnessProofSection is contracts.CorrectnessProofSection
    assert ControlPlaneCorrectnessReport is contracts.ControlPlaneCorrectnessReport
    assert not hasattr(user_contracts, "ControlPlaneCorrectnessReport")
    assert not hasattr(user_contracts, "CorrectnessProofSection")


def test_control_plane_contracts_do_not_export_executable_boundary_helpers() -> None:
    import tigrbl_control_plane_contracts as contracts

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
    package_root = next((ROOT / "pkgs").glob("00-core/tigrbl-control-plane-contracts/src/tigrbl_control_plane_contracts"))
    offenders: list[str] = []

    for path in package_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                offenders.append(f"{path.relative_to(ROOT)}:{node.lineno}:{node.name}")

    assert offenders == []


def test_control_plane_executable_helpers_stay_in_authz_policy_capability() -> None:
    import tigrbl_control_plane_contracts as contracts
    import tigrbl_management_plane_contracts as management_contracts
    from tigrbl_authz_policy._control_plane import models as admin_models
    from tigrbl_authz_policy._governance_extension import models as governance_models

    assert admin_models.Role is contracts.Role
    assert governance_models.SDKPackage is management_contracts.SDKPackage
    assert admin_models.admin_policy_boundary_integrity()["passed"] is True
    assert governance_models.provisioning_governance_ecosystem_boundary_integrity()["passed"] is True
    assert "feat:f13-rbac" in admin_models.admin_policy_boundary_manifest()
    assert (
        "feat:f39-sdk-ecosystem"
        in governance_models.provisioning_governance_ecosystem_boundary_manifest()
    )


def test_release_contracts_own_release_posture_surfaces() -> None:
    import tigrbl_release_contracts as contracts
    from tigrbl_authz_policy._release_posture.models import TransportPosture

    assert TransportPosture is contracts.TransportPosture


def test_management_plane_contracts_own_residency_and_evidence_surfaces() -> None:
    import tigrbl_management_plane_contracts as contracts
    from tigrbl_authz_policy import ResidencyZone
    from tigrbl_identity_jose import KeyRotationAuditEvidence

    assert ResidencyZone is contracts.ResidencyZone
    assert KeyRotationAuditEvidence is contracts.KeyRotationAuditEvidence


def test_admin_capability_models_are_00_core_contract_reexports() -> None:
    import tigrbl_control_plane_contracts as control_contracts
    import tigrbl_management_plane_contracts as management_contracts
    import tigrbl_user_plane_contracts as user_contracts
    from tigrbl_identity_admin._advanced_identity_plane import models as advanced_models
    from tigrbl_identity_admin._control_plane import models as admin_models

    assert admin_models.AdminResource is management_contracts.AdminResource
    assert admin_models.PrincipalRecord is management_contracts.PrincipalRecord
    assert admin_models.AdminAuditEvent is management_contracts.AdminAuditEvent
    assert admin_models.AdminUiView is management_contracts.AdminUiView
    assert advanced_models.AdaptiveContext is control_contracts.AdaptiveContext
    assert advanced_models.AccessDecisionRequest is control_contracts.AccessDecisionRequest
    assert advanced_models.TrustPath is control_contracts.TrustPath
    assert advanced_models.PasswordlessCredential is user_contracts.PasswordlessCredential
    assert advanced_models.AuthenticationChallenge is user_contracts.AuthenticationChallenge
    assert advanced_models.WorkloadIdentity is user_contracts.WorkloadIdentity
    assert not hasattr(advanced_models, "AdvancedIdentityBoundaryFeature")


def test_user_plane_security_reexports_security_trust_contracts() -> None:
    sys.modules.pop("tigrbl_user_plane_contracts.security", None)

    security_trust = importlib.import_module("tigrbl_security_trust_contracts")
    user_security = importlib.import_module("tigrbl_user_plane_contracts.security")

    assert user_security.Artifact is security_trust.Artifact
    assert user_security.IArtifactVerifier is security_trust.IArtifactVerifier


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
        "tigrbl_user_plane_contracts",
        "tigrbl_control_plane_contracts",
        "tigrbl_management_plane_contracts",
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
