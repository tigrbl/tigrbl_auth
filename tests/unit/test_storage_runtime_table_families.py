from __future__ import annotations

import asyncio

import pytest
from tigrbl_identity_storage.tables import (
    AttestationEvidence,
    CredentialIssuanceTransaction,
    CredentialOffer,
    CredentialStatusEntry,
    GnapClientInstance,
    GnapContinuation,
    GnapGrant,
    GnapInteraction,
    PresentationConsent,
    PresentationReplay,
    PresentationTransaction,
    SecurityEvent,
    SecurityEventDelivery,
    SecurityEventReplay,
    SpiffeTrustBundle,
    SvidRecord,
)
from tigrbl_identity_storage_runtime import (
    AttestationEvidenceRuntimeSpec,
    CredentialIssuanceTransactionRuntimeSpec,
    CredentialOfferRuntimeSpec,
    CredentialStatusEntryRuntimeSpec,
    GnapClientInstanceRuntimeSpec,
    GnapContinuationRuntimeSpec,
    GnapGrantRuntimeSpec,
    GnapInteractionRuntimeSpec,
    PresentationConsentRuntimeSpec,
    PresentationReplayRuntimeSpec,
    PresentationTransactionRuntimeSpec,
    SecurityEventDeliveryRuntimeSpec,
    SecurityEventReplayRuntimeSpec,
    SecurityEventRuntimeSpec,
    SpiffeTrustBundleRuntimeSpec,
    SvidRecordRuntimeSpec,
    make_attestation_appraisal_recorder,
)
from tigrbl_identity_contracts.attestation import (
    AppraisalResult,
    AttestationEvidence as AttestationEvidenceContract,
    VerifiedAttestationEvidence,
)
from tigrbl_identity_contracts.tokens import (
    ProtectedTokenEnvelope,
    TokenEnvelopeFormat,
    TokenProfile,
    VerifiedTokenEnvelope,
)


def _operation(spec, alias: str):
    return next(operation for operation in spec.ops if operation.alias == alias)


def test_runtime_specs_target_authoritative_layer_01_tables() -> None:
    pairs = (
        (CredentialOfferRuntimeSpec, CredentialOffer),
        (CredentialIssuanceTransactionRuntimeSpec, CredentialIssuanceTransaction),
        (CredentialStatusEntryRuntimeSpec, CredentialStatusEntry),
        (GnapClientInstanceRuntimeSpec, GnapClientInstance),
        (GnapGrantRuntimeSpec, GnapGrant),
        (GnapContinuationRuntimeSpec, GnapContinuation),
        (GnapInteractionRuntimeSpec, GnapInteraction),
        (PresentationTransactionRuntimeSpec, PresentationTransaction),
        (PresentationConsentRuntimeSpec, PresentationConsent),
        (PresentationReplayRuntimeSpec, PresentationReplay),
        (AttestationEvidenceRuntimeSpec, AttestationEvidence),
        (SecurityEventRuntimeSpec, SecurityEvent),
        (SecurityEventDeliveryRuntimeSpec, SecurityEventDelivery),
        (SecurityEventReplayRuntimeSpec, SecurityEventReplay),
        (SvidRecordRuntimeSpec, SvidRecord),
        (SpiffeTrustBundleRuntimeSpec, SpiffeTrustBundle),
    )

    for spec, table in pairs:
        assert spec.model is table
        assert table.__module__.startswith("tigrbl_identity_storage.tables")


def test_family_operations_are_carrier_neutral_table_operations() -> None:
    operations = (
        _operation(CredentialOfferRuntimeSpec, "create_offer"),
        _operation(PresentationTransactionRuntimeSpec, "begin_presentation"),
        _operation(AttestationEvidenceRuntimeSpec, "record_evidence"),
        _operation(SecurityEventRuntimeSpec, "record_event"),
        _operation(SvidRecordRuntimeSpec, "record_svid"),
        _operation(GnapGrantRuntimeSpec, "create_grant"),
    )
    for operation in operations:
        assert operation.target == "custom"
        assert operation.tx_scope == "read_write"
        assert operation.bindings == ()
        assert operation.handler is operation.core


def test_table_operation_refuses_sensitive_raw_values_before_persistence() -> None:
    operation = _operation(CredentialOfferRuntimeSpec, "create_offer")
    for field in (
        "raw_nonce",
        "pre_authorized_code",
        "presentation_disclosures",
        "raw_payload",
    ):
        with pytest.raises(ValueError, match="sensitive raw fields"):
            asyncio.run(
                operation.handler({"payload": {field: "secret"}, "db": object()})
            )


def test_gnap_continuation_runtime_refuses_raw_tokens() -> None:
    operation = _operation(GnapContinuationRuntimeSpec, "record_continuation")

    with pytest.raises(ValueError, match="raw GNAP continuation"):
        asyncio.run(
            operation.handler(
                {
                    "payload": {
                        "grant_id": "grant-1",
                        "continuation_id": "continue-1",
                        "continuation_token": "secret",
                    },
                    "db": object(),
                }
            )
        )


def test_attestation_recorder_adapts_verified_evidence_to_durable_operations(
    monkeypatch,
) -> None:
    from tigrbl_identity_storage_runtime.ops import attestation as operations

    recorded = []

    async def capture_evidence(ctx):
        recorded.append(("evidence", ctx))
        return ctx["payload"]

    async def capture_result(ctx):
        recorded.append(("result", ctx))
        return ctx["payload"]

    monkeypatch.setattr(operations, "record_attestation_evidence", capture_evidence)
    monkeypatch.setattr(operations, "record_attestation_result", capture_result)
    envelope = ProtectedTokenEnvelope(
        "signed.eat.token",
        TokenEnvelopeFormat.JWT,
        TokenProfile.ENTITY_ATTESTATION_TOKEN,
    )
    evidence = AttestationEvidenceContract(
        "urn:example:eat-profile", {"eat_profile": "urn:example:eat-profile"}
    )
    verified = VerifiedAttestationEvidence(
        evidence, VerifiedTokenEnvelope(envelope, evidence.claims)
    )
    recorder = make_attestation_appraisal_recorder(
        db="db",
        evidence_id="eat-1",
        artifact_locator="vault://eat/1",
        evidence_digest="sha256:abc",
        issuer="https://attester.example",
        policy_id="policy-1",
    )

    result = asyncio.run(
        recorder(verified, AppraisalResult(True, "approved", {"risk": "low"}))
    )

    assert result["evidence_id"] == "eat-1"
    assert [kind for kind, _ in recorded] == ["evidence", "result"]
    assert recorded[0][1]["payload"]["format"] == "jwt"
    assert recorded[1][1]["payload"]["result_claims"] == {"risk": "low"}
