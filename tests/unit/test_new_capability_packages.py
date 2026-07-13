from datetime import datetime, timezone

from tigrbl_attestation_appraisal import AttestationAppraisalCapability
from tigrbl_digital_credential_issuance import DigitalCredentialIssuanceCapability
from tigrbl_digital_credential_presentation import (
    DigitalCredentialPresentationCapability,
)
from tigrbl_identity_contracts.attestation import AppraisalResult, AttestationEvidence
from tigrbl_identity_contracts.digital_credentials import (
    CredentialConfiguration,
    CredentialFormat,
    CredentialIssuanceRequest,
    CredentialIssuanceResult,
    CredentialType,
    DigitalCredential,
    PresentationRequest,
    PresentationResult,
    TransactionBinding,
)
from tigrbl_identity_contracts.security_events import SecurityEvent
from tigrbl_identity_contracts.workloads import SpiffeId, Svid, SvidFormat
from tigrbl_security_events import SecurityEventsCapability
from tigrbl_workload_identity import WorkloadIdentityCapability


class _Issuer:
    def issue(self, request):
        return CredentialIssuanceResult(DigitalCredential(request.format, "encoded"))


class _WalletVerifier:
    def verify_wallet_attestation(self, value):
        return value == "valid-wallet"


def test_issuance_capability_composes_configuration_wallet_policy_and_issuer():
    format_ = CredentialFormat("dc+sd-jwt")
    configuration = CredentialConfiguration(
        "employee", CredentialType("urn:employee", format_), (format_,)
    )
    capability = DigitalCredentialIssuanceCapability(_Issuer(), _WalletVerifier())
    capability.register_configuration(configuration)
    assert capability.offer("https://issuer", ("employee",)).configuration_ids == (
        "employee",
    )
    result = capability.issue(
        CredentialIssuanceRequest("employee", format_),
        wallet_attestation="valid-wallet",
        require_wallet_attestation=True,
    )
    assert result.credential is not None


class _PresentationVerifier:
    def verify(self, value, request):
        return PresentationResult(value == "valid")


def test_presentation_capability_enforces_consent_and_replay_before_verification():
    consumed = set()
    capability = DigitalCredentialPresentationCapability(
        _PresentationVerifier(),
        lambda audience, key: (
            (audience, key) not in consumed and not consumed.add((audience, key))
        ),
        lambda holder, request: holder == "alice",
    )
    request = PresentationRequest(
        ("dc+sd-jwt",), TransactionBinding("nonce", "https://verifier")
    )
    assert capability.present("alice", "valid", request).valid
    assert not capability.present("alice", "valid", request).valid


class _Appraiser:
    def appraise(self, evidence):
        return AppraisalResult(True, "approved")


def test_attestation_capability_records_appraisal_outcome():
    records = []
    capability = AttestationAppraisalCapability(
        _Appraiser(), lambda evidence, result: records.append(result)
    )
    assert capability.appraise(AttestationEvidence("profile", {})).trusted
    assert records[0].reason == "approved"


def test_security_event_capability_composes_transmit_receive_and_recording():
    event = SecurityEvent(
        "https://example/event",
        "https://issuer",
        ("receiver",),
        "jti",
        datetime.now(timezone.utc),
    )
    records = []

    class _Transmitter:
        def transmit(self, event, subscriber):
            return "a.b.c"

    class _Receiver:
        def receive(self, encoded):
            return event

    capability = SecurityEventsCapability(
        _Transmitter(),
        _Receiver(),
        lambda action, value, subscriber: records.append(action),
    )
    assert capability.transmit(event, "receiver") == "a.b.c"
    assert capability.receive("a.b.c") is event
    assert records == ["transmitted", "received"]


def test_workload_capability_returns_verified_identity_not_raw_svid():
    identity = SpiffeId.parse("spiffe://example.org/workload/api")

    class _Provider:
        def fetch_svid(self, audience=None):
            return Svid(
                identity, SvidFormat.JWT if audience else SvidFormat.X509, "token"
            )

    class _Verifier:
        def verify_svid(self, svid, audience=None):
            return svid.spiffe_id

    capability = WorkloadIdentityCapability(_Provider(), _Verifier())
    assert capability.x509_identity() == identity
    assert capability.jwt_identity("service") == identity
