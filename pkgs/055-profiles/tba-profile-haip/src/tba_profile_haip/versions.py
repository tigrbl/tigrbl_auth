from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HaipVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    HaipVersion("draft-03", "superseded-draft", "2025-03"),
    HaipVersion("1.0", "final", "2025-12-24"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "1.0") -> HaipVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported HAIP version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "HaipVersion", "select_version"]
