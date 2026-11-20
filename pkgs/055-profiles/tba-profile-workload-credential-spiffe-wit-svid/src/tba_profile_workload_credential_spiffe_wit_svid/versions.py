from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WitSvidVersion:
    identifier: str
    status: str
    specification_uri: str


CURRENT_VERSION = WitSvidVersion(
    "SPIFFE-v1.15.1-WIT-SVID",
    "Incubating",
    "https://github.com/spiffe/spiffe/blob/5d15e3ee8782e205048d1f206fbf944e075f7bae/standards/WIT-SVID.md",
)
VERSION_HISTORY = (CURRENT_VERSION,)
