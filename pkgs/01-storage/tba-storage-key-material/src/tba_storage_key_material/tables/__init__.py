"""Owned mapped-table inventory."""

from .crypto_key import CryptoKey
from .crypto_key_version import CryptoKeyVersion
from .key_attestation_evidence import KeyAttestationEvidence
from .key_envelope import KeyEnvelope
from .key_rotation_event import KeyRotationEvent
from .key_rotation_policy import KeyRotationPolicy
from .principal_key_binding import PrincipalKeyBinding

TABLE_MODELS = (
    CryptoKey,
    CryptoKeyVersion,
    PrincipalKeyBinding,
    KeyEnvelope,
    KeyAttestationEvidence,
    KeyRotationEvent,
    KeyRotationPolicy,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
