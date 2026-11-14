import asyncio

import pytest
from tba_protocol_oid4vp import (
    CAPABILITY_REQUIREMENTS as OID4VP_REQUIREMENTS,
    CURRENT_VERSION as OID4VP_CURRENT,
    Oid4vpProtocol,
    capability_report as oid4vp_capability_report,
    compatibility as oid4vp_compatibility,
    migrate_request as migrate_presentation,
    supports as oid4vp_supports,
)
from tba_contracts_identity.digital_credentials import (
    PresentationResult,
)


def test_oid4vp_pins_final_version_and_features():
    assert OID4VP_CURRENT.identifier == "1.0"
    assert OID4VP_CURRENT.published == "2025-07-09"
    assert oid4vp_supports("dcql")


def test_oid4vp_refuses_lossy_presentation_migration():
    with pytest.raises(ValueError, match="losslessly"):
        migrate_presentation({"presentation_definition": {}}, "draft-20")


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
