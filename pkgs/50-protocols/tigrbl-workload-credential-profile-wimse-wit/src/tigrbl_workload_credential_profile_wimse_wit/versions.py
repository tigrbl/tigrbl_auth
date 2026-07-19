from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WitVersion:
    identifier: str
    status: str
    specification_uri: str


CURRENT_VERSION = WitVersion(
    "draft-ietf-wimse-workload-creds-02",
    "IETF-draft",
    "https://datatracker.ietf.org/doc/draft-ietf-wimse-workload-creds/02/",
)
VERSION_HISTORY = (CURRENT_VERSION,)
