from __future__ import annotations

import importlib
import inspect
from pathlib import Path

import tigrbl_identity_credentials_concrete as credentials
import tigrbl_identity_identities_concrete as identities
from tba_bases_identity_claims import ClaimBase


ROOT = Path(__file__).resolve().parents[2]
CLAIM_PACKAGE_ROOT = ROOT / "pkgs" / "10-concrete"


def test_identity_classes_have_standalone_layer_10_owners() -> None:
    expected = {
        "UserIdentity": "tba_concrete_user_identity",
        "AdminIdentity": "tba_concrete_administrator_identity",
        "ServiceIdentity": "tba_concrete_service_identity",
        "ClientIdentity": "tba_concrete_client_identity",
        "MachineIdentity": "tba_concrete_machine_identity",
        "WorkloadIdentity": "tba_concrete_workload_identity",
        "DeviceIdentity": "tba_concrete_device_identity",
    }
    assert {name: getattr(identities, name).__module__ for name in expected} == expected


def test_credential_classes_have_standalone_layer_10_owners() -> None:
    expected = {
        "PasswordCredential": "tba_concrete_credential_password",
        "PasswordResetCredential": "tba_concrete_credential_password_reset",
        "ApiKeyCredential": "tba_concrete_credential_api_key",
        "ServiceKeyCredential": "tba_concrete_credential_service_key",
        "ClientSecretCredential": "tba_concrete_credential_client_secret",
        "MfaCredential": "tba_concrete_credential_mfa",
        "PasskeyCredential": "tba_concrete_credential_passkey",
        "ServiceCredential": "tba_concrete_service_credential",
        "WebAuthnCredential": "tba_concrete_webauthn_credential",
        "PasswordlessCredential": "tba_concrete_passwordless_credential",
        "MfaFactor": "tba_concrete_mfa_factor",
        "MtlsCertificateCredential": "tba_concrete_credential_mtls_certificate",
        "DpopKeyCredential": "tba_concrete_credential_dpop_key",
        "SdJwtVc": "tba_concrete_sd_jwt_vc_credential",
        "Mdoc": "tba_concrete_mdoc_credential",
    }
    assert {
        name: getattr(credentials, name).__module__.split(".", 1)[0]
        for name in expected
    } == expected


def test_claims_classes_have_standalone_layer_10_owners() -> None:
    ownership: dict[str, tuple[str, str | None]] = {}
    package_dirs = (
        path
        for path in CLAIM_PACKAGE_ROOT.glob("tba-claim-*-concrete")
        if (path / "pyproject.toml").is_file() and "tba-claim-cwt-" not in path.name
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
