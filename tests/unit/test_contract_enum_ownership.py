from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKGS = ROOT / "pkgs"

ALLOWED_NON_CONTRACT_ENUMS = {
    "JoseKeyStatus",
    "JoseKeyUse",
    "MatrixCellStatus",
    "ReadinessStatus",
    "SurfacePlane",
}


def _enum_class_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = {
            base.id
            for base in node.bases
            if isinstance(base, ast.Name)
        } | {
            base.attr
            for base in node.bases
            if isinstance(base, ast.Attribute)
        }
        if "Enum" in base_names:
            names.add(node.name)
    return names


def test_reusable_enums_resolve_from_contract_packages() -> None:
    from tigrbl_identity_contracts import (
        AdminResourceKind,
        AdminResourceStatus,
    )
    from tigrbl_identity_admin._control_plane import models as legacy_admin_models
    from tigrbl_identity_admin_control_plane import models as admin_models
    from tigrbl_identity_jose import boundary, keys
    from tigrbl_identity_principals import factories as principal_factories
    from tigrbl_identity_contracts import (
        BrowserStoragePolicy,
        OAuthGrantStatus,
        OidcSessionStatus,
        PrincipalKind,
        PrincipalStatus,
        TokenType,
    )
    from tigrbl_auth_protocol_oauth import protocol as oauth_protocol
    from tigrbl_auth_protocol_oauth.standards._rfc8693 import runtime as token_exchange
    from tigrbl_auth_protocol_oidc import provider as oidc_provider
    from tigrbl_auth_protocol_rp import client as rp_client

    assert boundary.JoseKeyStatus is keys.JoseKeyStatus
    assert boundary.JoseKeyUse is keys.JoseKeyUse
    assert principal_factories.PrincipalKind is PrincipalKind
    assert principal_factories.PrincipalStatus is PrincipalStatus
    assert oauth_protocol.OAuthGrantStatus is OAuthGrantStatus
    assert token_exchange.TokenType is TokenType
    assert oidc_provider.OidcSessionStatus is OidcSessionStatus
    assert rp_client.BrowserStoragePolicy is BrowserStoragePolicy
    assert admin_models.AdminResourceKind is AdminResourceKind
    assert admin_models.AdminResourceStatus is AdminResourceStatus
    assert legacy_admin_models.AdminResourceKind is AdminResourceKind
    assert not hasattr(admin_models, "AdminUiState")


def test_reusable_enums_are_not_defined_outside_contract_packages() -> None:
    offenders: list[str] = []
    for path in PKGS.rglob("*.py"):
        relative = path.relative_to(PKGS)
        if relative.parts[0] == "01-contracts":
            continue
        for enum_name in sorted(_enum_class_names(path)):
            if enum_name in ALLOWED_NON_CONTRACT_ENUMS:
                continue
            offenders.append(f"{relative.as_posix()}::{enum_name}")

    assert offenders == []
