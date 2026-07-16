from __future__ import annotations

import importlib
import inspect
from pathlib import Path

import tigrbl_identity_credentials_concrete as credentials
import tigrbl_identity_identities_concrete as identities
from tigrbl_identity_claims_bases import ClaimBase


ROOT = Path(__file__).resolve().parents[2]
CLAIM_PACKAGE_ROOT = ROOT / "pkgs" / "10-concrete"


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
        "SdJwtVc": "tigrbl_sd_jwt_vc_credential_concrete",
        "Mdoc": "tigrbl_mdoc_credential_concrete",
    }
    assert {
        name: getattr(credentials, name).__module__.split(".", 1)[0]
        for name in expected
    } == expected


def test_claims_classes_have_standalone_layer_10_owners() -> None:
    ownership: dict[str, tuple[str, str | None]] = {}
    package_dirs = (
        path
        for path in CLAIM_PACKAGE_ROOT.glob("tigrbl-claim-*-concrete")
        if (path / "pyproject.toml").is_file() and "tigrbl-claim-cwt-" not in path.name
    )
    for package_dir in sorted(package_dirs):
        module_name = package_dir.name.replace("-", "_")
        module = importlib.import_module(module_name)
        claim_classes = [
            value
            for value in vars(module).values()
            if inspect.isclass(value)
            and issubclass(value, ClaimBase)
            and value is not ClaimBase
            and value.__module__ == module_name
        ]
        assert len(claim_classes) == 1, package_dir.name

        claim_class = claim_classes[0]
        canonical_name = claim_class.claim_name
        protocol_label = getattr(claim_class, "protocol_label", None)
        key = f"{canonical_name}:{protocol_label or ''}"
        assert key not in ownership, (key, ownership[key], package_dir.name)
        ownership[key] = (package_dir.name, protocol_label)

    assert {"at_hash:", "ath:", "iss:", "sub:"}.issubset(ownership)
