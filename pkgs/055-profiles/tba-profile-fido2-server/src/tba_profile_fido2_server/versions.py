from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Fido2ServerRevision:
    identifier: str
    webauthn_revision: str
    ctap_authenticator_revisions: tuple[str, ...]
    status: str
    specification_uri: str


FIDO2_SERVER_1_0 = Fido2ServerRevision(
    "fido2-server-1.0",
    "level-2",
    ("CTAP 2.0", "CTAP 2.1"),
    "implementation profile",
    "https://fidoalliance.org/specifications/",
)
CURRENT_VERSION = FIDO2_SERVER_1_0

__all__ = ["CURRENT_VERSION", "FIDO2_SERVER_1_0", "Fido2ServerRevision"]
