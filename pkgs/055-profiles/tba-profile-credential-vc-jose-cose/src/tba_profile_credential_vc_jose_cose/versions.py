from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VcJoseCoseVersion:
    identifier: str
    status: str
    published: str
    specification_uri: str


CURRENT_VERSION = VcJoseCoseVersion(
    "VC-JOSE-COSE-1.0",
    "W3C-Recommendation",
    "2025-05-15",
    "https://www.w3.org/TR/vc-jose-cose/",
)
VERSION_HISTORY = (CURRENT_VERSION,)
