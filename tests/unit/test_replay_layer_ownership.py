from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from tigrbl_auth_protocol_oauth import CAPABILITY_REQUIREMENTS as OAUTH_REQUIREMENTS
from tigrbl_auth_protocol_oid4vp import CAPABILITY_REQUIREMENTS as OID4VP_REQUIREMENTS
from tigrbl_auth_protocol_oidc import CAPABILITY_REQUIREMENTS as OIDC_REQUIREMENTS
from tigrbl_identity_contracts.replay import ReplayKey, ReplayReservationRequest
from tigrbl_identity_storage.tables import ReplayReservation
from tigrbl_identity_storage_runtime import SqlReplayReservationRepository
from tigrbl_replay_memory_provider import MemoryReplayProvider
from tigrbl_replay_protection_capability import ReplayProtectionCapability
from tigrbl_security_event_protocol_set import CAPABILITY_REQUIREMENTS as SET_REQUIREMENTS


def _request(value: str = "same") -> ReplayReservationRequest:
    return ReplayReservationRequest(
        ReplayKey("set:event-jti", value, issuer="https://issuer.example"),
        datetime.now(timezone.utc) + timedelta(minutes=5),
    )


def test_layer_01_owns_protocol_neutral_durable_replay_state():
    assert ReplayReservation.__tablename__ == "replay_reservations"
    assert ReplayReservation.__table__.c.key_digest.unique is True


def test_durable_replay_store_descriptor_is_operationally_explicit():
    descriptor = SqlReplayReservationRepository.descriptor
    assert descriptor.atomic_reservation is True
    assert descriptor.namespaces
    assert descriptor.tenant_isolation
    assert descriptor.expiry
    assert descriptor.retention
    assert descriptor.purge
    assert descriptor.audit
    assert descriptor.availability


def test_memory_provider_atomically_rejects_concurrent_duplicates():
    async def scenario():
        provider = MemoryReplayProvider()
        results = await asyncio.gather(
            *(provider.check_and_reserve(_request()) for _ in range(20))
        )
        assert sum(result.accepted for result in results) == 1
        assert sum(result.duplicate for result in results) == 19

    asyncio.run(scenario())


def test_layer_40_capability_reports_provider_identity_and_persistence():
    capability = ReplayProtectionCapability(
        MemoryReplayProvider(), namespaces=("set:event-jti",)
    )
    report = capability.capability_report()
    assert report["capability_id"] == "security.replay-protection"
    assert report["operations"] == ("check_and_reserve",)
    assert report["provider_id"] == "replay:memory"
    assert report["persistence"] == "ephemeral-process-local"
    assert "guarantees" not in report
    assert "limitations" not in report


def test_layer_50_maps_wire_requirements_to_replay_capability():
    requirements = SET_REQUIREMENTS + OAUTH_REQUIREMENTS + OIDC_REQUIREMENTS + OID4VP_REQUIREMENTS
    assert {item.protocol for item in requirements} == {
        "set", "oauth-dpop", "oidc-backchannel-logout", "oid4vp"
    }
    assert all(item.capability_id == "security.replay-protection" for item in requirements)
    assert all(item.operation == "check_and_reserve" for item in requirements)
    assert all(item.normalized_namespace for item in requirements)
