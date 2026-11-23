from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OidcVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    OidcVersion("1.0", "final", "2014-11-08"),
    OidcVersion("1.0-errata2", "final-errata", "2023-12-15"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "1.0-errata2") -> OidcVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported OIDC version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "OidcVersion", "select_version"]
