"""Injected configuration for the environment-backed JOSE provider.

The provider owns safe dependency-light defaults. Runtime composition may
replace the source object, but this package never imports the runtime layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DefaultJoseProviderSettings:
    issuer: str = "https://authn.example.com"
    protected_resource_identifier: str = "https://authn.example.com/resource"
    jwt_signing_alg: str = "EdDSA"
    enable_pqc_jose: bool = False
    enable_rfc7515: bool = True
    enable_rfc7516: bool = True
    enable_rfc7517: bool = True
    enable_rfc7518: bool = True
    enable_rfc7520: bool = True
    enable_rfc7638: bool = True
    enable_rfc7800: bool = False
    enable_rfc8037: bool = True
    enable_rfc8176: bool = True
    enable_rfc8705: bool = False
    enable_rfc8812: bool = False
    enable_rfc9068: bool = False
    enable_rfc9700: bool = True


_source: Any = DefaultJoseProviderSettings()


class _JoseProviderSettingsProxy:
    def __getattr__(self, name: str) -> Any:
        return getattr(_source, name)


settings = _JoseProviderSettingsProxy()


def configure_jose_provider(source: Any) -> None:
    """Use *source* for subsequent provider configuration reads."""

    global _source
    _source = source


def jose_provider_source() -> Any:
    """Return the currently injected configuration source."""

    return _source


__all__ = [
    "DefaultJoseProviderSettings",
    "configure_jose_provider",
    "jose_provider_source",
    "settings",
]
