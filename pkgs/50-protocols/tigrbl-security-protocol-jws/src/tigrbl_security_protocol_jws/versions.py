from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class JWSVersion:
    identifier: str
    status: str
    published: str
    specification_uri: str

CURRENT_VERSION = JWSVersion("RFC7515", "standards-track", "2015-05", "https://www.rfc-editor.org/rfc/rfc7515.html")
VERSION_HISTORY = (CURRENT_VERSION,)

def select_version(identifier: str = "RFC7515") -> JWSVersion:
    if identifier != CURRENT_VERSION.identifier:
        raise ValueError(f"unsupported JWS version: {identifier}")
    return CURRENT_VERSION
