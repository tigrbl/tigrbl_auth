from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WitVersion:
    identifier: str
    status: str
    specification_uri: str


LEGACY_VERSION = WitVersion(
    "draft-ietf-wimse-workload-creds-02",
    "IETF-draft",
    "https://datatracker.ietf.org/doc/draft-ietf-wimse-workload-creds/02/",
)
CURRENT_VERSION = WitVersion(
    "draft-ietf-wimse-workload-creds-03",
    "IETF-draft",
    "https://datatracker.ietf.org/doc/html/draft-ietf-wimse-workload-creds-03",
)
VERSION_HISTORY = (LEGACY_VERSION, CURRENT_VERSION)
