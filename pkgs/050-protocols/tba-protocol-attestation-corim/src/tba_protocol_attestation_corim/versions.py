from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CorimVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    CorimVersion("draft-ietf-rats-corim-10", "superseded-draft", "2024-07"),
    CorimVersion("draft-ietf-rats-corim-11", "active-draft", "2025-03"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = CURRENT_VERSION.identifier) -> CorimVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported CoRIM version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "CorimVersion", "select_version"]
