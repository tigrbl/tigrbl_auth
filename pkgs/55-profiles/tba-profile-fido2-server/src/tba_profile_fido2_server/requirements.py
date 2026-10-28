from dataclasses import dataclass

from .algorithm_profile import REQUIRED_ALGORITHMS
from .attestation_profile import BASELINE_ATTESTATION_FORMATS
from .versions import CURRENT_VERSION


@dataclass(frozen=True, slots=True)
class Fido2ServerRequirements:
    revision: str = CURRENT_VERSION.identifier
    webauthn_revision: str = CURRENT_VERSION.webauthn_revision
    required_algorithms: tuple[int, ...] = REQUIRED_ALGORITHMS
    attestation_formats: tuple[str, ...] = BASELINE_ATTESTATION_FORMATS
    direct_ctap_transport: bool = False


DEFAULT_REQUIREMENTS = Fido2ServerRequirements()

__all__ = ["DEFAULT_REQUIREMENTS", "Fido2ServerRequirements"]
