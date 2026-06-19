from __future__ import annotations

import warnings
from dataclasses import dataclass
from importlib import import_module
from typing import Any, Callable, Mapping


class TigrblAuthFacadeWarning(DeprecationWarning):
    """Warning emitted when a legacy ``tigrbl_auth`` compatibility surface is used."""


class FacadeImportError(ImportError):
    """Raised when a facade target is unavailable in the installed package set."""


@dataclass(frozen=True, slots=True)
class StableEntrypoint:
    name: str
    module: str
    target: str
    package: str
    deprecated: bool = False

    @property
    def dotted_target(self) -> str:
        return f"{self.module}.{self.target}"


STABLE_ENTRYPOINTS: Mapping[str, StableEntrypoint] = {
    "app": StableEntrypoint("app", "tigrbl_identity_server.app", "app", "tigrbl-identity-server", deprecated=True),
    "build_app": StableEntrypoint("build_app", "tigrbl_identity_server.app", "build_app", "tigrbl-identity-server", deprecated=True),
    "build_application_runtime_plan": StableEntrypoint(
        "build_application_runtime_plan",
        "tigrbl_identity_server.app",
        "build_application_runtime_plan",
        "tigrbl-identity-server",
        deprecated=True,
    ),
    "gateway_app": StableEntrypoint("gateway_app", "tigrbl_identity_server.gateway", "app", "tigrbl-identity-server", deprecated=True),
    "build_gateway": StableEntrypoint(
        "build_gateway",
        "tigrbl_identity_server.gateway",
        "build_gateway",
        "tigrbl-identity-server",
        deprecated=True,
    ),
    "build_gateway_runtime_plan": StableEntrypoint(
        "build_gateway_runtime_plan",
        "tigrbl_identity_server.gateway",
        "build_gateway_runtime_plan",
        "tigrbl-identity-server",
        deprecated=True,
    ),
    "resolve_gateway_deployment": StableEntrypoint(
        "resolve_gateway_deployment",
        "tigrbl_identity_server.gateway",
        "resolve_gateway_deployment",
        "tigrbl-identity-server",
        deprecated=True,
    ),
    "plugin_install": StableEntrypoint("plugin_install", "tigrbl_identity_server.plugin", "install", "tigrbl-identity-server", deprecated=True),
    "TigrblAuthPlugin": StableEntrypoint(
        "TigrblAuthPlugin",
        "tigrbl_identity_server.plugin",
        "TigrblAuthPlugin",
        "tigrbl-identity-server",
        deprecated=True,
    ),
    "cli_main": StableEntrypoint("cli_main", "tigrbl_identity_cli.cli.main", "main", "tigrbl-identity-cli", deprecated=True),
}


FACADE_EXTRAS: Mapping[str, tuple[str, ...]] = {
    "server": ("tigrbl-identity-server", "tigrbl-identity-runtime", "tigrbl-identity-storage"),
    "operator": ("tigrbl-identity-operator", "tigrbl-identity-testkit"),
    "oauth": ("tigrbl-auth-protocol-oauth", "tigrbl-auth-protocol-oidc", "tigrbl-identity-jose"),
    "consumer": ("tigrbl-authz-resource-server", "tigrbl-auth-protocol-rp"),
    "all": (
        "tigrbl-identity-core",
        "tigrbl-identity-contracts",
        "tigrbl-identity-principals",
        "tigrbl-authn-credentials",
        "tigrbl-identity-jose",
        "tigrbl-authz-policy",
        "tigrbl-auth-protocol-oauth",
        "tigrbl-auth-protocol-oidc",
        "tigrbl-identity-admin",
        "tigrbl-identity-storage",
        "tigrbl-identity-server",
        "tigrbl-identity-runtime",
        "tigrbl-identity-operator",
        "tigrbl-authz-resource-server",
        "tigrbl-auth-protocol-rp",
        "tigrbl-identity-testkit",
    ),
}


def warn_legacy_import(name: str, *, stacklevel: int = 2) -> None:
    warnings.warn(
        f"{name} is a tigrbl-auth compatibility facade; import the split tigrbl_identity_* package directly for new code.",
        TigrblAuthFacadeWarning,
        stacklevel=stacklevel,
    )


def extras_for(extra: str) -> tuple[str, ...]:
    try:
        return FACADE_EXTRAS[extra]
    except KeyError as exc:
        raise FacadeImportError(f"unknown tigrbl-auth extra: {extra}") from exc


def stable_entrypoints() -> Mapping[str, StableEntrypoint]:
    return dict(STABLE_ENTRYPOINTS)


def resolve_entrypoint(name: str, *, warn: bool = True) -> Any:
    try:
        entrypoint = STABLE_ENTRYPOINTS[name]
    except KeyError as exc:
        raise FacadeImportError(f"unknown tigrbl-auth facade entrypoint: {name}") from exc
    if warn and entrypoint.deprecated:
        warn_legacy_import(f"tigrbl_auth.{name}", stacklevel=3)
    try:
        module = import_module(entrypoint.module)
        return getattr(module, entrypoint.target)
    except Exception as exc:  # pragma: no cover - message is asserted through the public wrapper
        raise FacadeImportError(
            f"tigrbl-auth facade entrypoint {name!r} requires {entrypoint.package} "
            f"to provide {entrypoint.dotted_target}"
        ) from exc


class LazyCompatEntrypoint:
    def __init__(self, name: str) -> None:
        self.name = name

    def resolve(self) -> Any:
        return resolve_entrypoint(self.name)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        target: Callable[..., Any] = self.resolve()
        return target(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.resolve(), name)

    def __repr__(self) -> str:
        entrypoint = STABLE_ENTRYPOINTS.get(self.name)
        target = entrypoint.dotted_target if entrypoint is not None else self.name
        return f"<LazyCompatEntrypoint {target}>"


__all__ = [
    "FACADE_EXTRAS",
    "FacadeImportError",
    "LazyCompatEntrypoint",
    "STABLE_ENTRYPOINTS",
    "StableEntrypoint",
    "TigrblAuthFacadeWarning",
    "extras_for",
    "resolve_entrypoint",
    "stable_entrypoints",
    "warn_legacy_import",
]
