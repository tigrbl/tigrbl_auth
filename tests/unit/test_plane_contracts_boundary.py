from __future__ import annotations

import ast
import importlib
import sys
import warnings
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


def test_control_plane_contracts_own_admin_and_governance_surfaces() -> None:
    import tigrbl_control_plane_contracts as contracts
    from tigrbl_authz_policy._control_plane.models import Role
    from tigrbl_authz_policy._governance_extension.models import SDKPackage

    assert Role is contracts.Role
    assert SDKPackage is contracts.SDKPackage
    assert contracts.Role(name="admin", permissions=("tenant.read",)).name == "admin"


def test_release_contracts_own_release_posture_surfaces() -> None:
    import tigrbl_release_contracts as contracts
    from tigrbl_authz_policy._release_posture.models import TransportPosture

    assert TransportPosture is contracts.TransportPosture


def test_security_trust_contracts_bridge_points_to_user_plane_security() -> None:
    sys.modules.pop("tigrbl_security_trust_contracts", None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        legacy = importlib.import_module("tigrbl_security_trust_contracts")

    import tigrbl_user_plane_contracts as user_plane

    assert legacy.Artifact is user_plane.Artifact
    assert any("tigrbl_user_plane_contracts.security" in str(item.message) for item in caught)


def test_contract_packages_do_not_import_capability_runtime_or_storage_packages() -> None:
    forbidden = {
        "tigrbl_auth",
        "tigrbl_authn_credentials",
        "tigrbl_authz_policy",
        "tigrbl_authz_resource_server",
        "tigrbl_identity_runtime",
        "tigrbl_identity_storage",
    }

    for package in ("tigrbl_user_plane_contracts", "tigrbl_control_plane_contracts"):
        assert not (_imports_for(package) & forbidden), package


def test_target_capability_packages_no_longer_own_contract_classes() -> None:
    capability_roots = [
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
