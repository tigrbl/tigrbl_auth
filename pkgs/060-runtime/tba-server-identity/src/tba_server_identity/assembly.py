from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping


class SurfacePlane(str, Enum):
    PUBLIC = "public"
    ADMIN = "admin"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class RouteSurface:
    name: str
    path: str
    plane: SurfacePlane
    methods: tuple[str, ...] = ("GET",)
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.name or not self.path.startswith("/"):
            raise ValueError("route surface requires a name and absolute path")
        object.__setattr__(self, "plane", SurfacePlane(self.plane))
        object.__setattr__(self, "methods", tuple(sorted({method.upper() for method in self.methods})))


@dataclass(frozen=True, slots=True)
class ServerProfile:
    name: str
    enabled_planes: tuple[SurfacePlane, ...]
    feature_flags: Mapping[str, bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "enabled_planes", tuple(SurfacePlane(plane) for plane in self.enabled_planes))
        object.__setattr__(self, "feature_flags", dict(self.feature_flags))


@dataclass(frozen=True, slots=True)
class AssemblyManifest:
    profile: ServerProfile
    routes: tuple[RouteSurface, ...]

    @property
    def public_routes(self) -> tuple[RouteSurface, ...]:
        return tuple(route for route in self.routes if route.plane == SurfacePlane.PUBLIC)

    @property
    def admin_routes(self) -> tuple[RouteSurface, ...]:
        return tuple(route for route in self.routes if route.plane == SurfacePlane.ADMIN)

    def route_names(self) -> tuple[str, ...]:
        return tuple(route.name for route in self.routes)


DEFAULT_ROUTE_SURFACES: tuple[RouteSurface, ...] = (
    RouteSurface("authorize", "/authorize", SurfacePlane.PUBLIC, ("GET", "POST")),
    RouteSurface("token", "/token", SurfacePlane.PUBLIC, ("POST",)),
    RouteSurface("jwks", "/.well-known/jwks.json", SurfacePlane.PUBLIC, ("GET",)),
    RouteSurface("admin-principals", "/admin/principals", SurfacePlane.ADMIN, ("GET", "POST", "PATCH", "DELETE")),
    RouteSurface("admin-credentials", "/admin/credentials", SurfacePlane.ADMIN, ("GET", "POST", "PATCH", "DELETE")),
    RouteSurface("health", "/health", SurfacePlane.SYSTEM, ("GET",)),
)


def build_route_surface_registry(routes: Iterable[RouteSurface] = DEFAULT_ROUTE_SURFACES) -> dict[str, RouteSurface]:
    registry: dict[str, RouteSurface] = {}
    for route in routes:
        if route.name in registry:
            raise ValueError(f"duplicate route surface {route.name!r}")
        registry[route.name] = route
    return registry


def compose_server_manifest(
    profile: ServerProfile,
    routes: Iterable[RouteSurface] = DEFAULT_ROUTE_SURFACES,
) -> AssemblyManifest:
    enabled_planes = set(profile.enabled_planes)
    selected = tuple(route for route in routes if route.enabled and route.plane in enabled_planes)
    return AssemblyManifest(profile=profile, routes=selected)


def assert_public_admin_separation(manifest: AssemblyManifest) -> None:
    public_paths = {route.path for route in manifest.public_routes}
    admin_paths = {route.path for route in manifest.admin_routes}
    overlap = public_paths.intersection(admin_paths)
    if overlap:
        raise ValueError(f"public/admin route overlap: {sorted(overlap)}")
    leaked = [route.path for route in manifest.public_routes if route.path.startswith("/admin")]
    if leaked:
        raise ValueError(f"admin routes exposed on public plane: {sorted(leaked)}")


def provider_server_profile() -> ServerProfile:
    return ServerProfile(
        name="provider",
        enabled_planes=(SurfacePlane.PUBLIC, SurfacePlane.ADMIN, SurfacePlane.SYSTEM),
        feature_flags={"surface_public_enabled": True, "surface_admin_enabled": True},
    )


__all__ = [
    "AssemblyManifest",
    "DEFAULT_ROUTE_SURFACES",
    "RouteSurface",
    "ServerProfile",
    "SurfacePlane",
    "assert_public_admin_separation",
    "build_route_surface_registry",
    "compose_server_manifest",
    "provider_server_profile",
]
