from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SpiffeSvidVersion:
    identifier: str
    status: str
    specification_uris: tuple[str, ...]


CURRENT_VERSION = SpiffeSvidVersion(
    "SPIFFE-1.0",
    "stable",
    (
        "https://github.com/spiffe/spiffe/blob/main/standards/SPIFFE-ID.md",
        "https://github.com/spiffe/spiffe/blob/main/standards/X509-SVID.md",
        "https://github.com/spiffe/spiffe/blob/main/standards/JWT-SVID.md",
    ),
)
VERSION_HISTORY = (CURRENT_VERSION,)
