from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SdJwtVcVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    SdJwtVcVersion("draft-10", "superseded-draft", "2024-09"),
    SdJwtVcVersion("draft-13", "superseded-draft", "2025-02"),
    SdJwtVcVersion("draft-17", "active-draft", "2025-07"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "draft-17") -> SdJwtVcVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported SD-JWT VC version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "SdJwtVcVersion", "select_version"]
