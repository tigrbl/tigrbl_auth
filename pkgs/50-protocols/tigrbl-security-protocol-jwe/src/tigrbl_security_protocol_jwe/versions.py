from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JWEVersion:
    identifier: str
    status: str
    published: str
    specification_uri: str


CURRENT_VERSION = JWEVersion(
    "RFC7516",
    "standards-track",
    "2015-05",
    "https://www.rfc-editor.org/rfc/rfc7516.html",
)
VERSION_HISTORY = (CURRENT_VERSION,)


def select_version(identifier: str = "RFC7516") -> JWEVersion:
    if identifier != CURRENT_VERSION.identifier:
        raise ValueError(f"unsupported JWE version: {identifier}")
    return CURRENT_VERSION
