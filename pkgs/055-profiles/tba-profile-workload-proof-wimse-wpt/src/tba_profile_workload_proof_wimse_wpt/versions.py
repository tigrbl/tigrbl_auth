from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WptVersion:
    identifier: str
    status: str
    specification_uri: str


LEGACY_VERSION = WptVersion(
    "draft-ietf-wimse-wpt-01",
    "IETF-draft",
    "https://datatracker.ietf.org/doc/draft-ietf-wimse-wpt/01/",
)
CURRENT_VERSION = WptVersion(
    "draft-ietf-wimse-wpt-02",
    "IETF-draft",
    "https://datatracker.ietf.org/doc/html/draft-ietf-wimse-wpt-02",
)
VERSION_HISTORY = (LEGACY_VERSION, CURRENT_VERSION)
