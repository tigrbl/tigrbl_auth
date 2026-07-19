from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class JwtAccessTokenVersion:
    identifier: str
    status: str
    published: str
    specification_uri: str
CURRENT_VERSION = JwtAccessTokenVersion("RFC9068", "standards-track", "2021-10", "https://www.rfc-editor.org/rfc/rfc9068.html")
VERSION_HISTORY = (CURRENT_VERSION,)