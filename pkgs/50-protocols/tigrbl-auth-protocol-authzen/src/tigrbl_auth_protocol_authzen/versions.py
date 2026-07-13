from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthzenVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    AuthzenVersion("draft-00", "superseded-draft", "2024-08"),
    AuthzenVersion("implementers-draft-1", "superseded-implementers-draft", "2024"),
    AuthzenVersion("1.0", "final", "2026-01-11"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "1.0") -> AuthzenVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported AuthZEN version: {identifier}")


__all__ = ["AuthzenVersion", "CURRENT_VERSION", "VERSION_HISTORY", "select_version"]
