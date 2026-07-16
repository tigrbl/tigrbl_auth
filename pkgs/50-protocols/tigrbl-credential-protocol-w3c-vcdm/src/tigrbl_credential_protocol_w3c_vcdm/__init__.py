from .compatibility import VcdmCompatibility, compatibility
from .contexts import VCDM_2_RECOMMENDATION, VC_CONTEXT_V2, validate_contexts
from .features import FEATURES_BY_VERSION, supports
from .errors import VcdmProtocolError
from .migrations import migrate_document
from .schemas import parse_verifiable_credential, parse_verifiable_presentation
from .schema_references import CredentialSchemaReference, parse_credential_schema
from .status import CredentialStatusEntry, parse_credential_status
from .validation import validate_verifiable_credential, validate_verifiable_presentation
from .versions import CURRENT_VERSION, VERSION_HISTORY, VcdmVersion, select_version
from tigrbl_verifiable_credential_concrete import VerifiableCredential
from tigrbl_verifiable_presentation_concrete import VerifiablePresentation

__all__ = [
    "CURRENT_VERSION",
    "CAPABILITY_REQUIREMENTS",
    "CredentialSchemaReference",
    "CredentialStatusEntry",
    "FEATURES_BY_VERSION",
    "VCDM_2_RECOMMENDATION",
    "VC_CONTEXT_V2",
    "VERSION_HISTORY",
    "VcdmCompatibility",
    "VcdmProtocolError",
    "VcdmVersion",
    "VerifiableCredential",
    "VerifiablePresentation",
    "compatibility",
    "credential_subject_claims",
    "migrate_document",
    "parse_credential_schema",
    "parse_credential_status",
    "parse_verifiable_credential",
    "parse_verifiable_presentation",
    "select_version",
    "supports",
    "validate_contexts",
    "validate_verifiable_credential",
    "validate_verifiable_presentation",
]
from .bindings import CAPABILITY_REQUIREMENTS
from .claims import credential_subject_claims
