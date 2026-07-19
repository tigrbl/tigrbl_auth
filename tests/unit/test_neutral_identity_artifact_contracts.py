from datetime import datetime, timedelta, timezone

import pytest

from tigrbl_identity_core import (
    CredentialFormat,
    IdentityDocumentKind,
    ProtectedEnvelopeKind,
    TrustMaterialId,
    WorkloadCredentialId,
    WorkloadReferenceId,
)
from tigrbl_identity_document_contracts import IdentityDocument
from tigrbl_proof_of_possession_contracts import (
    ConfirmationKeyBinding,
    PossessionProof,
    PossessionProofContext,
)
from tigrbl_protected_envelope_contracts import ProtectedEnvelope
from tigrbl_token_contracts import TokenProfile
from tigrbl_workload_identity_contracts import (
    WorkloadCredential,
    WorkloadCredentialRequest,
    WorkloadCredentialSet,
    WorkloadIdentityRef,
    WorkloadReference,
    WorkloadTrustMaterial,
)


def test_identity_document_is_protocol_neutral_and_normalizes_kind() -> None:
    metadata = {"version_id": "7"}
    document = IdentityDocument(
        document_id="did:example:123#version-7",
        subject="did:example:123",
        kind="did-document",
        representation='{"id":"did:example:123"}',
        media_type="application/did+json",
        metadata=metadata,
    )
    metadata["version_id"] = "8"

    assert document.kind is IdentityDocumentKind.DID_DOCUMENT
    assert document.metadata == {"version_id": "7"}


def test_identity_document_rejects_missing_identity() -> None:
    with pytest.raises(ValueError, match="id, subject, and media type"):
        IdentityDocument(
            document_id="",
            subject="did:example:123",
            kind=IdentityDocumentKind.DID_DOCUMENT,
            representation=b"{}",
            media_type="application/did+json",
        )


def test_protected_envelope_distinguishes_jws_jwe_and_cose() -> None:
    for kind in (
        ProtectedEnvelopeKind.JWS,
        ProtectedEnvelopeKind.JWE,
        ProtectedEnvelopeKind.COSE_SIGN1,
        ProtectedEnvelopeKind.COSE_ENCRYPT0,
    ):
        envelope = ProtectedEnvelope(kind=kind.value, serialization=b"wire")
        assert envelope.kind is kind


def test_confirmation_binding_is_not_jose_specific() -> None:
    confirmation = {8: {1: 2, -1: 1, -2: b"x", -3: b"y"}}
    binding = ConfirmationKeyBinding(method=" CWT-COSE-Key ", confirmation=confirmation)
    confirmation[8][-2] = b"changed"

    assert binding.method == "cwt-cose-key"
    assert binding.confirmation[8][-2] == b"x"


def test_workload_credential_contracts_support_all_requested_formats() -> None:
    identity = WorkloadIdentityRef("spiffe://example.org/workload")
    reference = WorkloadReference(
        reference_id=WorkloadReferenceId("ref-1"),
        kind="process",
        scope="node-1",
        value={"pid": 42},
    )

    formats = (
        CredentialFormat.X509_SVID,
        CredentialFormat.JWT_SVID,
        CredentialFormat.WIT,
        CredentialFormat.WIT_SVID,
        CredentialFormat.CWT_SVID_EXTENSION,
    )
    credentials = tuple(
        WorkloadCredential(
            credential_id=WorkloadCredentialId(f"credential-{index}"),
            identity=identity,
            format=format_,
            artifact=b"artifact",
            valid_until=datetime.now(timezone.utc) + timedelta(minutes=5),
            trust_material_ref=TrustMaterialId("trust-1"),
        )
        for index, format_ in enumerate(formats)
    )

    request = WorkloadCredentialRequest(reference, CredentialFormat.WIT_SVID)
    result = WorkloadCredentialSet(credentials=credentials, version="1")
    trust = WorkloadTrustMaterial(
        material_id=TrustMaterialId("trust-1"),
        trust_domain="example.org",
        format="jwks",
        artifact=b"{}",
        version="1",
    )

    assert request.workload is reference
    assert tuple(item.format for item in result.credentials) == formats
    assert trust.trust_domain == "example.org"


def test_token_profiles_do_not_conflate_workload_tokens() -> None:
    assert TokenProfile.ID_TOKEN.value == "id-token"
    assert TokenProfile.JWT_ACCESS_TOKEN.value == "jwt-access-token"
    assert TokenProfile.WIT.value == "wit"
    assert TokenProfile.WIT_SVID.value == "wit-svid"
    assert TokenProfile.WPT.value == "wpt"
    assert TokenProfile.CWT_SVID_EXTENSION.value == "cwt-svid-extension"


def test_possession_proof_keeps_context_explicit() -> None:
    context = PossessionProofContext(
        audience="https://service.example",
        credential_digest="sha256:credential",
        accompanying_token_digests={"ath": "sha256:access-token"},
    )
    proof = PossessionProof(
        proof_id="proof-1",
        artifact="encoded-proof",
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=30),
        context=context,
        profile="wpt-pop",
    )

    assert proof.context.credential_digest == "sha256:credential"
    assert proof.profile == "wpt-pop"