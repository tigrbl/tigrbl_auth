from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OAuthVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    OAuthVersion("RFC6749", "standards-track", "2012-10"),
    OAuthVersion("draft-ietf-oauth-v2-1-13", "active-draft-profile", "2024-09"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "draft-ietf-oauth-v2-1-13") -> OAuthVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported OAuth version/profile: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "OAuthVersion", "select_version"]
