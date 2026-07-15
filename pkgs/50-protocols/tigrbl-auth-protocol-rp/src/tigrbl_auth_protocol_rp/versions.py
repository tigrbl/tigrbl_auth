"""Version ownership for the composed OIDC relying-party profile."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RpProfileVersion:
    identifier: str
    status: str
    published: str
    specifications: tuple[str, ...]


VERSION_HISTORY = (
    RpProfileVersion(
        "oidc-core-1.0+oauth2.0",
        "superseded-composite-profile",
        "2014-11-08",
        ("OIDC Core 1.0", "RFC6749"),
    ),
    RpProfileVersion(
        "oidc-core-1.0-errata2+oauth2.0+pkce",
        "current-composite-profile",
        "2023-12-15",
        ("OIDC Core 1.0 Errata 2", "RFC6749", "RFC7636"),
    ),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(
    identifier: str = CURRENT_VERSION.identifier,
) -> RpProfileVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported RP profile version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "RpProfileVersion", "select_version"]
