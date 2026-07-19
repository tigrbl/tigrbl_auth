from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class WitSvidVersion:
    identifier: str
    status: str
    specification_uri: str
CURRENT_VERSION = WitSvidVersion("SPIFFE-v1.15.1-WIT-SVID", "Incubating", "https://github.com/spiffe/spiffe/blob/v1.15.1/standards/WIT-SVID.md")
VERSION_HISTORY = (CURRENT_VERSION,)