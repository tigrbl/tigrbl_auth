from dataclasses import dataclass

from .requirements import Fido2ServerRequirements


@dataclass(frozen=True, slots=True)
class Fido2ServerProfile:
    requirements: Fido2ServerRequirements = Fido2ServerRequirements()
    metadata_enabled: bool = False
    certification_evidence_uri: str | None = None


__all__ = ["Fido2ServerProfile"]
