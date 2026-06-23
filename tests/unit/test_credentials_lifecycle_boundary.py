from __future__ import annotations

import ast
import sys
from datetime import timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for src in sorted((ROOT / "pkgs").glob("*/src")):
    value = str(src)
    if value not in sys.path:
        sys.path.insert(0, value)


def test_credentials_t0_exports_public_lifecycle_surface() -> None:
    import tigrbl_authn_credentials as credentials

    assert credentials.CredentialKind.PASSWORD.value == "password"
    assert credentials.CredentialStatus.ACTIVE.value == "active"
    assert str(credentials.new_credential_id())
    assert credentials.verify_secret("pw", credentials.hash_secret("pw"))


def test_credentials_t0_constructs_each_credential_kind() -> None:
    import tigrbl_authn_credentials as credentials

    password = credentials.create_password_credential("p1", "correct-horse")
    reset = credentials.create_password_reset_credential("p1")
    passkey = credentials.create_passkey_credential("p1", credential_id="passkey-1", public_key="pub")
    api_key = credentials.create_api_key_credential("p1")
    service_key = credentials.create_service_key_credential("svc1")
    client_secret = credentials.create_client_secret_credential("client1")
    mfa = credentials.create_mfa_factor_credential("p1", "123456")

    assert password.kind is credentials.CredentialKind.PASSWORD
    assert reset.credential.kind is credentials.CredentialKind.PASSWORD_RESET
    assert passkey.kind is credentials.CredentialKind.PASSKEY_WEBAUTHN
    assert api_key.credential.kind is credentials.CredentialKind.API_KEY
    assert service_key.credential.kind is credentials.CredentialKind.SERVICE_KEY
    assert client_secret.credential.kind is credentials.CredentialKind.CLIENT_SECRET
    assert mfa.kind is credentials.CredentialKind.MFA_FACTOR


def test_credentials_t1_verifies_password_keys_client_secret_and_mfa() -> None:
    import tigrbl_authn_credentials as credentials

    password = credentials.create_password_credential("p1", "pw")
    api_key = credentials.create_api_key_credential("p1", public_id="api-key-id")
    service_key = credentials.create_service_key_credential("svc1", public_id="service-key-id")
    client_secret = credentials.create_client_secret_credential("client1", public_id="client-secret-id")
    mfa = credentials.create_mfa_factor_credential("p1", "654321")

    assert credentials.verify_credential(password, "pw") is True
    assert credentials.verify_credential(api_key.credential, api_key.secret or "") is True
    assert credentials.verify_credential(service_key.credential, service_key.secret or "") is True
    assert credentials.verify_credential(client_secret.credential, client_secret.secret or "") is True
    assert credentials.verify_credential(mfa, "654321") is True
    assert credentials.verify_credential(password, "bad") is False


def test_credentials_t1_password_reset_and_passkey_behaviors() -> None:
    import pytest
    import tigrbl_authn_credentials as credentials

    reset = credentials.create_password_reset_credential("p1", ttl=timedelta(minutes=5))
    consumed = credentials.consume_one_time_credential(reset.credential, reset.secret or "")
    passkey = credentials.create_passkey_credential("p1", credential_id="credential-id", public_key="pub")

    assert consumed.status is credentials.CredentialStatus.CONSUMED
    assert credentials.verify_credential(passkey, "credential-id") is True
    with pytest.raises(credentials.CredentialStateError):
        credentials.consume_one_time_credential(passkey, "credential-id")


def test_credentials_t2_rotation_revocation_and_audit_events() -> None:
    import pytest
    import tigrbl_authn_credentials as credentials

    ledger = credentials.CredentialLedger()
    issued = credentials.create_api_key_credential("p1")
    ledger.add(issued.credential)
    assert ledger.verify(issued.credential.id, issued.secret or "") is True

    rotated = ledger.rotate(issued.credential.id, new_secret="new-secret")
    assert ledger.credentials[issued.credential.id].status is credentials.CredentialStatus.ROTATED
    assert rotated.credential.rotated_from == issued.credential.id
    assert ledger.verify(rotated.credential.id, "new-secret") is True

    revoked = ledger.revoke(rotated.credential.id, reason="compromised")
    assert revoked.status is credentials.CredentialStatus.REVOKED
    with pytest.raises(credentials.CredentialStateError):
        ledger.verify(revoked.id, "new-secret")

    actions = [event.action for event in ledger.audit_events]
    assert credentials.CredentialAuditAction.CREATED in actions
    assert credentials.CredentialAuditAction.VERIFIED in actions
    assert credentials.CredentialAuditAction.ROTATED in actions
    assert credentials.CredentialAuditAction.REVOKED in actions
    assert credentials.CredentialAuditAction.FAILED in actions


def test_credentials_t2_public_surface_import_dag_stays_clean() -> None:
    package_root = ROOT / "pkgs" / "40-capabilities" / "tigrbl-authn-credentials" / "src" / "tigrbl_authn_credentials"
    checked = [package_root / "__init__.py", package_root / "lifecycle.py"]
    forbidden = {"tigrbl_auth", "tigrbl_identity_server", "tigrbl_identity_storage", "tigrbl_identity_admin"}

    for path in checked:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert not (imports & forbidden), path


def test_credentials_contracts_are_packaged_by_domain() -> None:
    contracts_root = ROOT / "pkgs" / "02-contracts" / "tigrbl-identity-contracts" / "src" / "tigrbl_identity_contracts"

    from tigrbl_identity_contracts.audit.credentials import CredentialAuditEvent
    import tigrbl_identity_contracts.credentials as credential_contracts

    assert not (contracts_root / "authn.py").exists()
    assert (contracts_root / "credentials" / "__init__.py").exists()
    assert (contracts_root / "credentials" / "enums.py").exists()
    assert (contracts_root / "credentials" / "errors.py").exists()
    assert (contracts_root / "credentials" / "models.py").exists()
    assert (contracts_root / "audit" / "credentials.py").exists()
    assert CredentialAuditEvent.__module__ == "tigrbl_identity_contracts.audit.credentials"
    assert not hasattr(credential_contracts.models, "CredentialAuditEvent")
