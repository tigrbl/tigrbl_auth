import asyncio

from tba_protocol_oid4vci import (
    CAPABILITY_REQUIREMENTS as OID4VCI_REQUIREMENTS,
    CURRENT_VERSION as OID4VCI_CURRENT,
    Oid4vciProtocol,
    capability_report as oid4vci_capability_report,
    compatibility as oid4vci_compatibility,
    migrate_request as migrate_issuance,
    supports as oid4vci_supports,
)
from tba_contracts_identity.digital_credentials import (
    CredentialIssuanceResult,
)


def test_oid4vci_pins_final_version_and_features():
    assert OID4VCI_CURRENT.identifier == "1.0"
    assert OID4VCI_CURRENT.published == "2025-09-16"
    assert oid4vci_supports("credential-configuration-id")


def test_oid4vci_migrates_the_legacy_proof_field():
    migrated = migrate_issuance(
        {"credential_configuration_id": "employee", "proof": {"jwt": "a.b.c"}},
        "draft-15",
    )
    assert "proofs" in migrated and "proof" not in migrated


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
