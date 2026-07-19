from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WptVersion:
    identifier: str
    status: str
    specification_uri: str


CURRENT_VERSION = WptVersion(
    "draft-ietf-wimse-wpt-01",
    "IETF-draft",
    "https://datatracker.ietf.org/doc/draft-ietf-wimse-wpt/01/",
)
VERSION_HISTORY = (CURRENT_VERSION,)
