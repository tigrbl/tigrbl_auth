"""Typed HAIP component/profile schema descriptors."""

from dataclasses import dataclass

from .profile import HAIP_CREDENTIAL_FORMATS, HaipConfiguration


@dataclass(frozen=True, slots=True)
class HaipComponentVersions:
    oid4vci: str = "1.0"
    oid4vp: str = "1.0"


@dataclass(frozen=True, slots=True)
class HaipCredentialFormats:
    allowed: frozenset[str] = HAIP_CREDENTIAL_FORMATS


__all__ = [
    "HaipComponentVersions",
    "HaipConfiguration",
    "HaipCredentialFormats",
]
