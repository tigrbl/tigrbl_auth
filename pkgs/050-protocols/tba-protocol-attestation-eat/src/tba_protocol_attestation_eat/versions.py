from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EatVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    EatVersion("draft-ietf-rats-eat-30", "superseded-draft", "2024-01"),
    EatVersion("RFC9711", "standards-track", "2025-04"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "RFC9711") -> EatVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported EAT version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "EatVersion", "select_version"]
