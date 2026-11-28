from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JwtVersion:
    identifier: str
    status: str
    published: str


VERSION_HISTORY = (
    JwtVersion("draft-ietf-oauth-json-web-token-32", "superseded-draft", "2015-02"),
    JwtVersion("RFC7519", "standards-track", "2015-05"),
)
CURRENT_VERSION = VERSION_HISTORY[-1]


def select_version(identifier: str = "RFC7519") -> JwtVersion:
    for version in VERSION_HISTORY:
        if version.identifier == identifier:
            return version
    raise ValueError(f"unsupported JWT version: {identifier}")


__all__ = ["CURRENT_VERSION", "VERSION_HISTORY", "JwtVersion", "select_version"]
