"""Owned mapped-table inventory."""

from .authentication_challenge import AuthenticationChallenge
from .credential import Credential
from .credential_api_key import CredentialApiKey
from .credential_audit_event import CredentialAuditEvent
from .credential_client_secret import CredentialClientSecret
from .credential_dpop_key import CredentialDpopKey
from .credential_mfa_factor import CredentialMfaFactor
from .credential_mtls_certificate import CredentialMtlsCertificate
from .credential_password import CredentialPassword
from .credential_recovery_code import CredentialRecoveryCode
from .credential_service_key import CredentialServiceKey

TABLE_MODELS = (
    Credential,
    CredentialApiKey,
    CredentialServiceKey,
    CredentialAuditEvent,
    CredentialClientSecret,
    CredentialDpopKey,
    CredentialMfaFactor,
    CredentialMtlsCertificate,
    CredentialPassword,
    CredentialRecoveryCode,
    AuthenticationChallenge,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
