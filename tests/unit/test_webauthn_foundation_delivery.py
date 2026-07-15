from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from tigrbl_authenticator_attestation_capability import (
    AuthenticatorAttestationCapability,
)
from tigrbl_identity_contracts.capabilities import CapabilityOperationUnavailableError
from tigrbl_identity_contracts.public_key_authentication import (
    CeremonyBinding,
    CeremonyContext,
    CeremonyKind,
    CredentialBinding,
    CredentialRegistrationResult,
    PublicKeyAuthenticationIntent,
    PublicKeyAuthenticationOptions,
    PublicKeyAuthenticationResult,
    PublicKeyCredentialSource,
    PublicKeyRegistrationIntent,
    PublicKeyRegistrationOptions,
)
from tigrbl_identity_core import normalize_protocol_tag
from tigrbl_identity_storage.tables import (
    CredentialWebAuthnPasskey,
    WebAuthnAttestationRecord,
    WebAuthnCeremony,
    WebAuthnRelyingParty,
)
from tigrbl_identity_storage_runtime.tables.webauthn import (
    WebAuthnCeremonyRuntimeSpec,
    WebAuthnCredentialRuntimeSpec,
    WebAuthnRelyingPartyRuntimeSpec,
)
from tigrbl_public_key_authentication_capability import (
    PublicKeyAuthenticationCapability,
)
from tigrbl_public_key_credential_management_capability import (
    PublicKeyCredentialManagementCapability,
)
from tigrbl_public_key_registration_capability import PublicKeyRegistrationCapability
from tigrbl_webauthn_credential_concrete import WebAuthnCredential


def _context(kind: CeremonyKind) -> CeremonyContext:
    now = datetime.now(timezone.utc)
    return CeremonyContext(
        ceremony_id="ceremony-1",
        kind=kind,
        binding=CeremonyBinding(
            "tenant-1", "example.com", "https://example.com", "alice"
        ),
        challenge=b"0123456789abcdef0123456789abcdef",
        issued_at=now,
        expires_at=now + timedelta(minutes=5),
    )


def test_protocol_tags_cover_complete_fido_family() -> None:
    assert {
        normalize_protocol_tag(value)
        for value in (
            "fido",
            "fido2",
            "webauthn",
            "ctap",
            "ctap2",
            "passkey",
            "fido-mds",
        )
    }


def test_storage_tables_own_typed_webauthn_state() -> None:
    assert WebAuthnCeremony.__tablename__ == "webauthn_ceremonies"
    assert WebAuthnRelyingParty.__tablename__ == "webauthn_relying_parties"
    assert WebAuthnAttestationRecord.__tablename__ == "webauthn_attestation_records"
    columns = CredentialWebAuthnPasskey.__table__.columns
    for name in (
        "credential_external_id",
        "credential_public_key_cose",
        "cose_algorithm",
        "backup_eligible",
        "backup_state",
        "aaguid",
    ):
        assert name in columns


def test_layer30_specs_keep_semantic_operation_aliases() -> None:
    ceremony_ops = {op.alias for op in WebAuthnCeremonyRuntimeSpec.ops}
    credential_ops = {op.alias for op in WebAuthnCredentialRuntimeSpec.ops}
    rp_ops = {op.alias for op in WebAuthnRelyingPartyRuntimeSpec.ops}
    expected_ceremony_ops = {
        "reserve_registration_ceremony",
        "reserve_authentication_ceremony",
        "load_active_ceremony",
        "consume_ceremony",
        "fail_ceremony",
    }
    assert expected_ceremony_ops.issubset(ceremony_ops)
    assert "update_assertion_state" in credential_ops
    assert "resolve_relying_party_configuration" in rp_ops
    assert all(
        not op.bindings and not op.expose_routes
        for op in WebAuthnCeremonyRuntimeSpec.ops
        if op.alias in expected_ceremony_ops
    )


def test_concrete_webauthn_credential_validates_backup_and_aaguid() -> None:
    credential = WebAuthnCredential(
        credential_id="internal-1",
        subject_id="alice",
        tenant_id="tenant-1",
        rp_id="example.com",
        algorithm="ES256",
        cose_algorithm=-7,
        transports=("internal",),
        credential_external_id=b"credential-1",
        credential_public_key_cose=b"key",
        aaguid=b"\x00" * 16,
        backup_eligible=True,
        backup_state=True,
    )
    assert credential.metadata["cose_algorithm"] == -7
    with pytest.raises(ValueError, match="backup eligible"):
        WebAuthnCredential(
            credential_id="bad",
            subject_id="alice",
            tenant_id="tenant-1",
            rp_id="example.com",
            algorithm="ES256",
            transports=(),
            backup_state=True,
        )


@pytest.mark.asyncio
async def test_registration_and_authentication_capabilities_expose_one_operation_identity() -> (
    None
):
    registration_options = PublicKeyRegistrationOptions(
        _context(CeremonyKind.REGISTRATION), (-7,)
    )
    source = PublicKeyCredentialSource(
        credential_id="credential-1",
        external_id=b"external",
        public_key=b"key",
        algorithm=-7,
        binding=CredentialBinding("tenant-1", "example.com", "alice", b"alice"),
    )

    async def begin_registration(_intent):
        return registration_options

    async def complete_registration(_registration):
        return CredentialRegistrationResult(True, source)

    registration = PublicKeyRegistrationCapability(
        begin_registration, complete_registration
    )
    assert set(registration.operations()) == {
        "begin_public_key_registration",
        "complete_public_key_registration",
    }
    result = await registration.call(
        "begin_public_key_registration",
        PublicKeyRegistrationIntent(
            "tenant-1", "alice", "example.com", "https://example.com", b"alice"
        ),
    )
    assert result.value is registration_options

    authentication_options = PublicKeyAuthenticationOptions(
        _context(CeremonyKind.AUTHENTICATION)
    )

    async def begin_authentication(_intent):
        return authentication_options

    async def complete_authentication(_assertion):
        return PublicKeyAuthenticationResult(False, reason="test")

    authentication = PublicKeyAuthenticationCapability(
        begin_authentication, complete_authentication
    )
    result = await authentication.call(
        "begin_public_key_authentication",
        PublicKeyAuthenticationIntent("tenant-1", "example.com", "https://example.com"),
    )
    assert result.value is authentication_options


@pytest.mark.asyncio
async def test_optional_attestation_operations_report_unavailable() -> None:
    capability = AuthenticatorAttestationCapability(appraise=lambda value: value)
    report = capability.capability_report()
    assert report["unavailable_optional_operations"] == (
        "reappraise_registered_authenticator",
        "resolve_authenticator_metadata",
    )
    with pytest.raises(CapabilityOperationUnavailableError):
        await capability.call("resolve_authenticator_metadata", b"\x00" * 16)


def test_management_capability_requires_all_declared_operations() -> None:
    with pytest.raises(NotImplementedError, match="required capability operation"):
        PublicKeyCredentialManagementCapability(
            list_credentials=lambda: (),
            rename_credential=None,
            revoke_credential=lambda: None,
        )
