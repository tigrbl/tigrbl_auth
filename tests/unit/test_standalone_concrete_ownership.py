from __future__ import annotations

import tigrbl_identity_credentials_concrete as credentials
import tigrbl_identity_identities_concrete as identities
import tigrbl_oidc_claims_concrete as claims


def test_identity_classes_have_standalone_layer_10_owners() -> None:
    expected = {
        "UserIdentity": "tigrbl_user_identity_concrete",
        "AdminIdentity": "tigrbl_admin_identity_concrete",
        "ServiceIdentity": "tigrbl_service_identity_concrete",
        "ClientIdentity": "tigrbl_client_identity_concrete",
        "MachineIdentity": "tigrbl_machine_identity_concrete",
        "WorkloadIdentity": "tigrbl_workload_identity_concrete",
        "DeviceIdentity": "tigrbl_device_identity_concrete",
    }
    assert {name: getattr(identities, name).__module__ for name in expected} == expected


def test_credential_classes_have_standalone_layer_10_owners() -> None:
    expected = {
        "PasswordCredential": "tigrbl_password_credential_concrete",
        "PasswordResetCredential": "tigrbl_password_reset_credential_concrete",
        "ApiKeyCredential": "tigrbl_api_key_credential_concrete",
        "ServiceKeyCredential": "tigrbl_service_key_credential_concrete",
        "ClientSecretCredential": "tigrbl_client_secret_credential_concrete",
        "MfaCredential": "tigrbl_mfa_credential_concrete",
        "PasskeyCredential": "tigrbl_passkey_credential_concrete",
        "ServiceCredential": "tigrbl_service_credential_concrete",
        "WebAuthnCredential": "tigrbl_webauthn_credential_concrete",
        "PasswordlessCredential": "tigrbl_passwordless_credential_concrete",
        "MfaFactor": "tigrbl_mfa_factor_concrete",
        "MtlsCertificateCredential": "tigrbl_mtls_certificate_credential_concrete",
        "DpopKeyCredential": "tigrbl_dpop_key_credential_concrete",
        "SdJwtVc": "tigrbl_sd_jwt_vc_concrete",
        "Mdoc": "tigrbl_mdoc_concrete",
    }
    assert {
        name: getattr(credentials, name).__module__.split(".", 1)[0]
        for name in expected
    } == expected


def test_claims_classes_have_standalone_layer_10_owners() -> None:
    assert not hasattr(claims, "LocalClaimsProvider")
