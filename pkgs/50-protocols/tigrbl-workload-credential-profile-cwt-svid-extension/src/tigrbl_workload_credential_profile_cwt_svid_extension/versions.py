from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CwtSvidExtensionVersion:
    identifier: str
    status: str
    specification_uris: tuple[str, ...]


CURRENT_VERSION = CwtSvidExtensionVersion(
    "TIGRBL-CWT-SVID-EXPERIMENT-1",
    "experimental-extension",
    (
        "https://www.rfc-editor.org/rfc/rfc8392.html",
        "https://www.rfc-editor.org/rfc/rfc8747.html",
        "https://www.rfc-editor.org/rfc/rfc9052.html",
    ),
)
VERSION_HISTORY = (CURRENT_VERSION,)
EXPERIMENTAL_EXTENSION = True
SPIFFE_CONFORMANT = False
