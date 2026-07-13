from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GnapVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    GnapVersion("draft-13", "superseded-draft", "2023-03"),
    GnapVersion("draft-ietf-gnap-core-protocol-20", "superseded-draft", "2024-04"),
    GnapVersion("RFC9635", "standards-track", "2024-10"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "RFC9635") -> GnapVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported GNAP version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "GnapVersion", "select_version"]
