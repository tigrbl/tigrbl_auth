import asyncio

import pytest
from tigrbl_auth_protocol_authzen import (
    AuthzenProtocol,
    CURRENT_VERSION as AUTHZEN_CURRENT,
    migrate_evaluation,
    supports as authzen_supports,
)
from tigrbl_auth_protocol_oid4vci import (
    CAPABILITY_REQUIREMENTS as OID4VCI_REQUIREMENTS,
    CURRENT_VERSION as OID4VCI_CURRENT,
    Oid4vciProtocol,
    capability_report as oid4vci_capability_report,
    compatibility as oid4vci_compatibility,
    migrate_request as migrate_issuance,
    supports as oid4vci_supports,
)
from tigrbl_auth_protocol_oid4vp import (
    CAPABILITY_REQUIREMENTS as OID4VP_REQUIREMENTS,
    CURRENT_VERSION as OID4VP_CURRENT,
    Oid4vpProtocol,
    capability_report as oid4vp_capability_report,
    compatibility as oid4vp_compatibility,
    migrate_request as migrate_presentation,
    supports as oid4vp_supports,
)
from tigrbl_identity_contracts.digital_credentials import (
    CredentialIssuanceResult,
    PresentationResult,
)
from tigrbl_identity_contracts.policy import PolicyDecision, PolicyEvaluationResult


def test_protocol_packages_pin_independent_final_versions_and_features():
    assert (
        OID4VCI_CURRENT.identifier == "1.0"
        and OID4VCI_CURRENT.published == "2025-09-16"
    )
    assert (
        OID4VP_CURRENT.identifier == "1.0" and OID4VP_CURRENT.published == "2025-07-09"
    )
    assert (
        AUTHZEN_CURRENT.identifier == "1.0"
        and AUTHZEN_CURRENT.published == "2026-01-11"
    )
    assert oid4vci_supports("credential-configuration-id")
    assert oid4vp_supports("dcql")
    assert authzen_supports("search-resource")


def test_version_migrations_are_explicit_and_refuse_lossy_automatic_conversion():
    migrated = migrate_issuance(
        {"credential_configuration_id": "employee", "proof": {"jwt": "a.b.c"}},
        "draft-15",
    )
    assert "proofs" in migrated and "proof" not in migrated
    assert migrate_evaluation({"subject": {}}, "draft-00")["context"] == {}
    with pytest.raises(ValueError, match="losslessly"):
        migrate_presentation({"presentation_definition": {}}, "draft-20")


class _IssuanceCapability:
    def issue(self, request, **kwargs):
        self.request = request
        return CredentialIssuanceResult(transaction_id="deferred-1")


def test_oid4vci_wire_adapter_delegates_to_issuance_capability():
    capability = _IssuanceCapability()
    result = asyncio.run(
        Oid4vciProtocol(capability).credential(
            {
                "credential_configuration_id": "employee",
                "format": "dc+sd-jwt",
                "proofs": {"jwt": ["a.b.c"]},
            }
        )
    )
    assert result.transaction_id == "deferred-1"
    assert capability.request.configuration_id == "employee"


def test_oid4vci_maps_explicit_issuance_and_proof_operations():
    path = oid4vci_compatibility("draft-15")
    assert path.compatible and path.migration_required
    assert {item.operation for item in OID4VCI_REQUIREMENTS} == {
        "create_offer",
        "decode",
        "issue",
        "record_issuance",
        "register_configuration",
        "validate",
        "verify_wallet_attestation",
    }
    report = oid4vci_capability_report()
    assert report["required_capabilities"] == (
        "artifact.processing",
        "digital-credential.issuance",
    )


class _PresentationCapability:
    def present(self, holder, token, request):
        self.request = request
        return PresentationResult(True)


def test_oid4vp_binds_client_nonce_and_state_before_capability_dispatch():
    capability = _PresentationCapability()
    result = asyncio.run(
        Oid4vpProtocol(capability).verify(
            "alice",
            "vp-token",
            {
                "client_id": "https://verifier.example",
                "nonce": "nonce",
                "state": "transaction",
                "accepted_formats": ["dc+sd-jwt"],
            },
        )
    )
    assert result.valid
    assert capability.request.binding.transaction_id == "transaction"


def test_oid4vp_maps_explicit_presentation_and_replay_operations():
    path = oid4vp_compatibility("draft-25")
    assert path.compatible and path.lossless and path.migration_required
    assert {item.operation for item in OID4VP_REQUIREMENTS} == {
        "check_and_reserve",
        "check_consent",
        "decode",
        "present",
        "record_result",
        "record_transaction",
        "reserve_replay",
        "validate",
        "verify_presentation",
    }
    report = oid4vp_capability_report()
    assert report["required_capabilities"] == (
        "artifact.processing",
        "digital-credential.presentation",
        "security.replay-protection",
    )


class _Evaluator:
    def evaluate(self, request):
        self.request = request
        return PolicyEvaluationResult(PolicyDecision(True, "policy matched"))


def test_authzen_maps_wire_entities_to_neutral_policy_contracts():
    evaluator = _Evaluator()
    response = AuthzenProtocol(evaluator).access_evaluation(
        {
            "subject": {"type": "user", "id": "alice"},
            "action": {"type": "action", "id": "read"},
            "resource": {"type": "document", "id": "document-1"},
            "context": {"time": "day"},
        }
    )
    assert response == {"decision": True, "reason": "policy matched"}
    assert evaluator.request.subject.entities[0].identifier == "alice"
