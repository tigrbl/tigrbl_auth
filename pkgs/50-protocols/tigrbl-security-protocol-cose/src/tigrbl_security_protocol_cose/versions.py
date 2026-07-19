from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class COSEVersion:
    identifier: str
    status: str
    published: str
    specification_uri: str


CURRENT_VERSION = COSEVersion(
    "RFC9052",
    "standards-track",
    "2022-08",
    "https://www.rfc-editor.org/rfc/rfc9052.html",
)
VERSION_HISTORY = (CURRENT_VERSION,)


def select_version(identifier: str = "RFC9052") -> COSEVersion:
    if identifier != CURRENT_VERSION.identifier:
        raise ValueError(f"unsupported COSE version: {identifier}")
    return CURRENT_VERSION
