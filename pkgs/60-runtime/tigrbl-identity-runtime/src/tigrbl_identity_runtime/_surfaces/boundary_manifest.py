from __future__ import annotations
# ruff: noqa: F403,F405

from typing import Any, Final

from .schema import *
from .public_capabilities import *
from .registries import *

SURFACE_BASELINE_BOUNDARY_FEATURES: Final[tuple[SurfaceBoundaryClassification, ...]] = (
    SurfaceBoundaryClassification(
        feature_id="feat:uix-admin-boundary",
        surface_name="admin-uix",
        family="uix",
        audience="admin",
        surface_set="admin-rest",
        contract_kind="react-admin-uix",
        auth_required=True,
        public_visible=False,
        admin_visible=True,
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:uix-public-boundary",
        surface_name="public-uix",
        family="uix",
        audience="public",
        surface_set="public-rest",
        contract_kind="react-public-uix",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:surface-applicability-classification",
        surface_name="surface-applicability",
        family="governance",
        audience="mixed",
        surface_set=None,
        contract_kind="runtime-manifest",
        auth_required=False,
        public_visible=True,
        admin_visible=True,
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-admin-boundary",
        surface_name="admin-api",
        family="api",
        audience="admin",
        surface_set="admin-rest",
        contract_kind="openapi",
        auth_required=True,
        public_visible=False,
        admin_visible=True,
        owned_resources=tuple(SURFACE_REGISTRY["admin_control_plane"]["target_resources"]),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-admin-contract-publication-boundary",
        surface_name="admin-api-contract-publication",
        family="api",
        audience="admin",
        surface_set="admin-rest",
        contract_kind="openapi",
        auth_required=True,
        public_visible=False,
        admin_visible=True,
        owned_resources=tuple(SURFACE_REGISTRY["admin_control_plane"]["target_resources"]),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-admin-authz-gate",
        surface_name="admin-api-authz-gate",
        family="api",
        audience="admin",
        surface_set="admin-rest",
        contract_kind="runtime-gate",
        auth_required=True,
        public_visible=False,
        admin_visible=True,
        owned_paths=("/admin",),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-admin-resource-management-boundary",
        surface_name="admin-api-resource-management",
        family="api",
        audience="admin",
        surface_set="admin-rest",
        contract_kind="openapi-resource-management",
        auth_required=True,
        public_visible=False,
        admin_visible=True,
        owned_resources=tuple(SURFACE_REGISTRY["admin_control_plane"]["target_resources"]),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-admin-policy-control-plane-boundary",
        surface_name="admin-api-policy-control-plane",
        family="api",
        audience="admin",
        surface_set="admin-rest",
        contract_kind="openapi-policy-control",
        auth_required=True,
        public_visible=False,
        admin_visible=True,
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-admin-public-surface-exclusion",
        surface_name="admin-api-public-exclusion",
        family="api",
        audience="admin",
        surface_set="admin-rest",
        contract_kind="exclusion-guard",
        auth_required=True,
        public_visible=False,
        admin_visible=True,
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-public-boundary",
        surface_name="public-api",
        family="api",
        audience="public",
        surface_set="public-rest",
        contract_kind="openapi",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
        owned_paths=tuple(public_contract_paths()),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-public-oauth-boundary",
        surface_name="public-api-oauth",
        family="api",
        audience="public",
        surface_set="public-rest",
        contract_kind="openapi-oauth",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
        owned_paths=(
            "/authorize",
            "/token",
            "/revoke",
            "/introspect",
            "/device_authorization",
            "/par",
            "/token/exchange",
        ),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-public-oidc-boundary",
        surface_name="public-api-oidc",
        family="api",
        audience="public",
        surface_set="public-rest",
        contract_kind="openapi-oidc",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
        owned_paths=("/userinfo", "/logout", "/.well-known/openid-configuration"),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-public-discovery-boundary",
        surface_name="public-api-discovery",
        family="api",
        audience="public",
        surface_set="public-rest",
        contract_kind="well-known-discovery",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
        owned_paths=(
            "/.well-known/openid-configuration",
            "/.well-known/oauth-authorization-server",
            "/.well-known/oauth-protected-resource",
            "/.well-known/jwks.json",
        ),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-public-registration-boundary",
        surface_name="public-api-registration",
        family="api",
        audience="public",
        surface_set="public-rest",
        contract_kind="dynamic-client-registration",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
        owned_paths=("/register", "/register/{client_id}"),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-public-logout-boundary",
        surface_name="public-api-logout",
        family="api",
        audience="public",
        surface_set="public-rest",
        contract_kind="oidc-logout",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
        owned_paths=("/logout",),
    ),
    SurfaceBoundaryClassification(
        feature_id="feat:api-public-admin-surface-exclusion",
        surface_name="public-api-admin-exclusion",
        family="api",
        audience="public",
        surface_set="public-rest",
        contract_kind="exclusion-guard",
        auth_required=False,
        public_visible=True,
        admin_visible=False,
    ),
)


def surface_baseline_boundary_manifest() -> dict[str, dict[str, Any]]:
    return {
        item.feature_id: {
            "surface_name": item.surface_name,
            "family": item.family,
            "audience": item.audience,
            "surface_set": item.surface_set,
            "contract_kind": item.contract_kind,
            "auth_required": item.auth_required,
            "public_visible": item.public_visible,
            "admin_visible": item.admin_visible,
            "owned_paths": list(item.owned_paths),
            "owned_resources": list(item.owned_resources),
        }
        for item in SURFACE_BASELINE_BOUNDARY_FEATURES
    }


def surface_baseline_boundary_integrity() -> dict[str, Any]:
    routes = route_registry()
    public_paths = {
        path for path, meta in routes.items()
        if meta.get("surface_set") == "public-rest"
    }
    admin_paths = {"/tenant", "/client", "/user"}
    admin_prefixes = ("/tenant/", "/client/", "/user/")
    public_admin_leaks = sorted(path for path in public_paths if path in admin_paths)
    public_contract_leaks = sorted(
        path for path in public_contract_paths()
        if path in admin_paths or path.startswith(admin_prefixes)
    )
    admin_public_leaks = sorted(
        path for path in admin_paths
        if path in public_paths
    )
    return {
        "feature_count": len(SURFACE_BASELINE_BOUNDARY_FEATURES),
        "public_path_count": len(public_paths),
        "admin_resource_count": len(SURFACE_REGISTRY["admin_control_plane"]["target_resources"]),
        "public_admin_leaks": public_admin_leaks,
        "public_contract_leaks": public_contract_leaks,
        "admin_public_leaks": admin_public_leaks,
        "passed": not public_admin_leaks and not public_contract_leaks and not admin_public_leaks,
    }


PHASE1_SURFACE_BOUNDARY_FEATURES = SURFACE_BASELINE_BOUNDARY_FEATURES
phase1_surface_boundary_manifest = surface_baseline_boundary_manifest
phase1_surface_boundary_integrity = surface_baseline_boundary_integrity


def enabled_surface_summary(settings_obj: object) -> dict[str, bool | str]:
    from .deployment import resolve_deployment

    deployment = resolve_deployment(settings_obj)
    return dict(deployment.surfaces)


def surface_registry() -> dict[str, dict[str, Any]]:
    return SURFACE_REGISTRY


def surface_set_registry() -> dict[str, dict[str, bool]]:
    from .deployment import SURFACE_SET_REGISTRY

    return SURFACE_SET_REGISTRY


__all__ = [
    "ALL_SURFACE_CAPABILITIES",
    "DIAGNOSTICS_CAPABILITIES",
    "PHASE1_SURFACE_BOUNDARY_FEATURES",
    "PUBLIC_CAPABILITIES",
    "SURFACE_REGISTRY",
    "SURFACE_BASELINE_BOUNDARY_FEATURES",
    "SurfaceBoundaryClassification",
    "all_surface_capability_registry",
    "capability_mount_groups",
    "diagnostics_capability_registry",
    "enabled_surface_summary",
    "phase1_surface_boundary_integrity",
    "phase1_surface_boundary_manifest",
    "public_capability_registry",
    "public_contract_paths",
    "route_registry",
    "surface_registry",
    "surface_baseline_boundary_integrity",
    "surface_baseline_boundary_manifest",
    "surface_set_registry",
]
