from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SetVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    SetVersion("draft-ietf-secevent-token-13", "superseded-draft", "2018-05"),
    SetVersion("RFC8417", "standards-track", "2018-07"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "RFC8417") -> SetVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported SET version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "SetVersion", "select_version"]
