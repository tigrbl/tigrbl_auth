"""Owned mapped-table inventory."""

from .credential_webauthn_passkey import CredentialWebAuthnPasskey
from .webauthn_attestation_record import WebAuthnAttestationRecord
from .webauthn_ceremony import WebAuthnCeremony
from .webauthn_relying_party import WebAuthnRelyingParty

TABLE_MODELS = (
    CredentialWebAuthnPasskey,
    WebAuthnAttestationRecord,
    WebAuthnCeremony,
    WebAuthnRelyingParty,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
