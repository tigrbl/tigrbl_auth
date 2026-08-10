"""Deprecated compatibility façade for standalone credential concretes."""

from tigrbl_credential_api_key_concrete import ApiKeyCredential
from tigrbl_credential_client_secret_concrete import ClientSecretCredential
from tigrbl_credential_dpop_key_concrete import DpopKeyCredential
from tigrbl_credential_mfa_concrete import MfaCredential
from tigrbl_mfa_factor_concrete import MfaFactor
from tigrbl_credential_mtls_certificate_concrete import MtlsCertificateCredential
from tigrbl_credential_passkey_concrete import PasskeyCredential
from tigrbl_credential_password_concrete import PasswordCredential
from tigrbl_credential_password_reset_concrete import PasswordResetCredential
from tigrbl_passwordless_credential_concrete import PasswordlessCredential
from tigrbl_service_credential_concrete import ServiceCredential
from tigrbl_credential_service_key_concrete import ServiceKeyCredential
from tigrbl_webauthn_credential_concrete import WebAuthnCredential
from tigrbl_corim_concrete import parse_corim
from tigrbl_eat_concrete import parse_eat
from tigrbl_credential_profile_sd_jwt_vc import parse_sd_jwt_vc
from tigrbl_credential_protocol_iso_mdoc import parse_mdoc
from tigrbl_credential_protocol_w3c_vcdm import (
    validate_verifiable_credential,
    validate_verifiable_presentation,
)
from tigrbl_mdoc_credential_concrete import MdocCredential
from tigrbl_sd_jwt_vc_credential_concrete import SdJwtVcCredential

Mdoc = MdocCredential
SdJwtVc = SdJwtVcCredential
__all__ = [
    "ApiKeyCredential",
    "ClientSecretCredential",
    "DpopKeyCredential",
    "MfaCredential",
    "MfaFactor",
    "MtlsCertificateCredential",
    "PasskeyCredential",
    "PasswordCredential",
    "PasswordResetCredential",
    "PasswordlessCredential",
    "ServiceCredential",
    "ServiceKeyCredential",
    "WebAuthnCredential",
    "Mdoc",
    "SdJwtVc",
    "parse_corim",
    "parse_eat",
    "parse_mdoc",
    "parse_sd_jwt_vc",
    "validate_verifiable_credential",
    "validate_verifiable_presentation",
]
