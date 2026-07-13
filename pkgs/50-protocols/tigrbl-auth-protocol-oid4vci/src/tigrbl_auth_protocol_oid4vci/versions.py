from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Oid4vciVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    Oid4vciVersion("draft-11", "superseded-draft", "2023-12"),
    Oid4vciVersion("draft-15", "superseded-draft", "2024-12"),
    Oid4vciVersion("1.0", "final", "2025-09-16"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "1.0") -> Oid4vciVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported OID4VCI version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "Oid4vciVersion", "select_version"]
