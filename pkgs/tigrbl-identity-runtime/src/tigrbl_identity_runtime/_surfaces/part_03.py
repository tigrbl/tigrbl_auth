DIAGNOSTICS_CAPABILITIES: Final[tuple[dict[str, Any], ...]] = (
    {
        "capability": "diagnostics-health",
        "kind": "diagnostics",
        "surface_set": "diagnostics",
        "mount_group": "diagnostics",
        "paths": ("/system/health",),
        "methods": ("get",),
        "flags": (),
        "summary": "Diagnostics health endpoint",
        "tags": ("diagnostics",),
        "contract_visible": False,
        "discovery_visible": False,
    },
)

ALL_SURFACE_CAPABILITIES: Final[tuple[dict[str, Any], ...]] = PUBLIC_CAPABILITIES + DIAGNOSTICS_CAPABILITIES


def public_capability_registry() -> dict[str, dict[str, Any]]:
    return {str(item["capability"]): dict(item) for item in PUBLIC_CAPABILITIES}


def diagnostics_capability_registry() -> dict[str, dict[str, Any]]:
    return {str(item["capability"]): dict(item) for item in DIAGNOSTICS_CAPABILITIES}


def all_surface_capability_registry() -> dict[str, dict[str, Any]]:
    return {str(item["capability"]): dict(item) for item in ALL_SURFACE_CAPABILITIES}


def capability_mount_groups() -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for item in ALL_SURFACE_CAPABILITIES:
        groups.setdefault(str(item.get("mount_group", "default")), []).append(str(item["capability"]))
    return groups


def route_registry() -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for item in ALL_SURFACE_CAPABILITIES:
        for path in item.get("paths", ()):  # type: ignore[union-attr]
            registry[str(path)] = {
                "surface_set": item.get("surface_set"),
                "methods": tuple(str(method) for method in item.get("methods", ())),
                "flags": tuple(str(flag) for flag in item.get("flags", ())),
                "summary": item.get("summary", str(path)),
                "tags": tuple(str(tag) for tag in item.get("tags", ())),
                "capability": item.get("capability"),
                "kind": item.get("kind"),
                "mount_group": item.get("mount_group"),
                "contract_visible": bool(item.get("contract_visible", True)),
                "discovery_visible": bool(item.get("discovery_visible", False)),
                "router_ref": item.get("router_ref"),
                "publisher_ref": item.get("publisher_ref"),
                "artifact_name": item.get("artifact_name"),
                "targets": tuple(str(target) for target in item.get("targets", ())),
            }
    return registry


def public_contract_paths() -> list[str]:
    paths: list[str] = []
    for item in PUBLIC_CAPABILITIES:
        if not bool(item.get("contract_visible", True)):
            continue
        for path in item.get("paths", ()):  # type: ignore[union-attr]
            if str(path) not in paths:
                paths.append(str(path))
    return paths


SURFACE_REGISTRY: dict[str, dict[str, Any]] = {
    "public_auth_plane": {
        "settings_flag": "surface_public_enabled",
        "surface_set": "public-rest",
        "capability_registry": "tigrbl_auth.config.surfaces.PUBLIC_CAPABILITIES",
        "current_routes": public_contract_paths(),
        "target_routes": public_contract_paths(),
    },
    "admin_control_plane": {
        "settings_flag": "surface_admin_enabled",
        "surface_set": "admin-rpc",
        "current_resources": [
            "Tenant",
            "User",
            "Client",
            "ClientRegistration",
            "ApiKey",
            "Service",
            "ServiceKey",
            "AuthSession",
            "AuthCode",
            "TokenRecord",
            "PushedAuthorizationRequest",
            "RevokedToken",
            "Consent",
            "LogoutState",
            "AuditEvent",
            "KeyRotationEvent",
        ],
        "target_resources": [
            "Tenant",
            "User",
            "Client",
            "ClientRegistration",
            "ApiKey",
            "Service",
            "ServiceKey",
            "AuthSession",
            "AuthCode",
            "TokenRecord",
            "PushedAuthorizationRequest",
            "RevokedToken",
            "Consent",
            "LogoutState",
            "AuditEvent",
            "KeyRotationEvent",
        ],
    },
    "operator_plane": {
        "settings_flag": "surface_operator_enabled",
        "current_commands": [
            "serve",
            "bootstrap",
            "migrate",
            "verify",
            "gate",
            "spec",
            "claims",
            "evidence",
            "adr",
            "doctor",
            "release",
            "tenant",
            "client",
            "identity",
            "flow",
            "session",
            "token",
            "keys",
            "discovery",
            "import",
            "export",
        ],
        "target_commands": [
            "bootstrap",
            "migrate",
            "serve",
            "verify",
            "gate",
            "spec",
            "evidence",
            "claims",
            "adr",
            "doctor",
            "release",
            "tenant",
            "client",
            "identity",
            "flow",
            "session",
            "token",
            "keys",
            "discovery",
            "import",
            "export",
        ],
    },
    "rpc_control_plane": {
        "settings_flag": "surface_rpc_enabled",
        "surface_set": "admin-rpc",
        "current_prefix": "/rpc",
        "target_prefix": "/rpc",
        "required_method": "rpc.discover",
    },
    "diagnostics_plane": {
        "settings_flag": "surface_diagnostics_enabled",
        "current_prefix": "/system",
        "target_prefix": "/system",
    },
    "plugin_plane": {
        "settings_flag": "surface_plugin_mode",
        "current_modes": ["mixed"],
        "target_modes": ["public-only", "admin-only", "mixed", "diagnostics-only"],
    },
}


@dataclass(frozen=True, slots=True)
class SurfaceBoundaryClassification:
    feature_id: str
    surface_name: str
    family: str
    audience: str
    surface_set: str | None
    contract_kind: str
    auth_required: bool
    public_visible: bool
    admin_visible: bool
    owned_paths: tuple[str, ...] = ()
    owned_resources: tuple[str, ...] = ()


