from __future__ import annotations

import warnings
from dataclasses import dataclass
from importlib import import_module
from typing import Any, Callable, Mapping


class TbaAuthFacadeWarning(DeprecationWarning):
    """Warning emitted when a legacy ``tba_auth`` compatibility surface is used."""


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
    "build_application_runtime_plan": StableEntrypoint(
        "build_application_runtime_plan",
        "tba_server_identity.app",
        "build_application_runtime_plan",
        "tba-server-identity",
        deprecated=True,
    ),
    "build_gateway_runtime_plan": StableEntrypoint(
        "build_gateway_runtime_plan",
        "tba_server_identity.gateway",
        "build_gateway_runtime_plan",
        "tba-server-identity",
        deprecated=True,
    ),
    "resolve_gateway_deployment": StableEntrypoint(
        "resolve_gateway_deployment",
        "tba_server_identity.gateway",
        "resolve_gateway_deployment",
        "tba-server-identity",
        deprecated=True,
    ),
    "plugin_install": StableEntrypoint(
        "plugin_install",
        "tba_plugin_tigrbl",
        "install",
        "tba-plugin-tigrbl",
        deprecated=True,
    ),
    "TbaPlugin": StableEntrypoint(
        "TbaPlugin",
        "tba_plugin_tigrbl",
        "TbaPlugin",
        "tba-plugin-tigrbl",
        deprecated=True,
    ),
    "cli_main": StableEntrypoint(
        "cli_main",
        "tba_cli_identity.cli.main",
        "main",
        "tba-cli-identity",
        deprecated=True,
    ),
}


FACADE_EXTRAS: Mapping[str, tuple[str, ...]] = {
    "server": (
        "tba-server-identity",
        "tba-plugin-tigrbl",
        "tba-runtime-identity",
        "tba-storage-core",
    ),
    "operator": ("tba-operator-identity", "tba-testkit-identity"),
    "oauth": (
        "tba-protocol-oauth",
        "tba-protocol-oidc",
        "tba-provider-identity-jose",
    ),
    "consumer": ("tba-protocol-authorization-resource-server", "tba-protocol-oidc-relying-party"),
    "all": (
        "tba-primitives-identity",
        "tba-contracts-identity",
        "tba-concrete-identity-principals",
        "tba-credentials",
        "tba-provider-identity-jose",
        "tba-runtime-authorization-policy",
        "tba-protocol-oauth",
        "tba-protocol-oidc",
        "tba-runtime-identity-administration",
        "tba-storage-core",
        "tba-server-identity",
        "tba-plugin-tigrbl",
        "tba-runtime-identity",
        "tba-operator-identity",
        "tba-protocol-authorization-resource-server",
        "tba-protocol-oidc-relying-party",
        "tba-testkit-identity",
    ),
}


def warn_legacy_import(name: str, *, stacklevel: int = 2) -> None:
    warnings.warn(
        f"{name} is a tba-auth compatibility facade; import the split tba_identity_* package directly for new code.",
        TbaAuthFacadeWarning,
        stacklevel=stacklevel,
    )


def extras_for(extra: str) -> tuple[str, ...]:
    try:
        return FACADE_EXTRAS[extra]
    except KeyError as exc:
        raise FacadeImportError(f"unknown tba-auth extra: {extra}") from exc


def stable_entrypoints() -> Mapping[str, StableEntrypoint]:
    return dict(STABLE_ENTRYPOINTS)


def resolve_entrypoint(name: str, *, warn: bool = True) -> Any:
    try:
        entrypoint = STABLE_ENTRYPOINTS[name]
    except KeyError as exc:
        raise FacadeImportError(
            f"unknown tba-auth facade entrypoint: {name}"
        ) from exc
    if warn and entrypoint.deprecated:
        warn_legacy_import(f"tba_auth.{name}", stacklevel=3)
    try:
        module = import_module(entrypoint.module)
        return getattr(module, entrypoint.target)
    except (
        Exception
    ) as exc:  # pragma: no cover - message is asserted through the public wrapper
        raise FacadeImportError(
            f"tba-auth facade entrypoint {name!r} requires {entrypoint.package} "
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
    "TbaAuthFacadeWarning",
    "extras_for",
    "resolve_entrypoint",
    "stable_entrypoints",
    "warn_legacy_import",
]
