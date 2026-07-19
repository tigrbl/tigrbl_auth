from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DidCoreVersion:
    identifier: str
    status: str
    published: str
    specification_uri: str

CURRENT_VERSION = DidCoreVersion("DID-Core-1.0", "W3C-Recommendation", "2022-07-19", "https://www.w3.org/TR/did-core/")
VERSION_HISTORY = (CURRENT_VERSION,)