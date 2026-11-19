from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Oid4vpVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    Oid4vpVersion("draft-20", "superseded-draft", "2024-04"),
    Oid4vpVersion("draft-25", "superseded-draft", "2025-04"),
    Oid4vpVersion("1.0", "final", "2025-07-09"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "1.0") -> Oid4vpVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported OID4VP version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "Oid4vpVersion", "select_version"]
