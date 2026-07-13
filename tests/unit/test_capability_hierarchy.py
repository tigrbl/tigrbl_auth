from __future__ import annotations

import asyncio

import pytest

from tigrbl_attestation_appraisal import AttestationAppraisalCapability
from tigrbl_capability import Capability
from tigrbl_capability_bases import CapabilityBase
from tigrbl_default_capability import DefaultCapability
from tigrbl_digital_credential_issuance import DigitalCredentialIssuanceCapability
from tigrbl_digital_credential_presentation import DigitalCredentialPresentationCapability
from tigrbl_identity_admin_control_plane import AdminControlPlane
from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityMetadata,
    ICapability,
)
from tigrbl_replay_protection_capability import ReplayProtectionCapability
from tigrbl_security_events import SecurityEventsCapability
from tigrbl_workload_identity import WorkloadIdentityCapability


class _Appraiser:
    def appraise(self, evidence):
        return evidence


class _Issuer:
    def issue(self, request):
        return request


class _PresentationVerifier:
    def verify(self, encoded, request):
        return (encoded, request)


class _Transmitter:
    def transmit(self, event, subscriber):
        return f"{subscriber}:{event}"


class _Receiver:
    def receive(self, encoded):
        return encoded


class _SvidProvider:
    def fetch_svid(self, audience=None):
        return audience


class _SvidVerifier:
    def verify_svid(self, svid, audience=None):
        return (svid, audience)


class _ReplayProvider:
    provider_id = "replay:test"
    persistence = "ephemeral-process-local"

    async def check_and_reserve(self, request):
        return request


def _metadata(capability_id: str = "test.capability") -> CapabilityMetadata:
    return CapabilityMetadata(capability_id, "1.0", ("execute",))


def test_capability_inheritance_order_is_contract_base_10_1_then_10_2() -> None:
    assert ICapability in CapabilityBase.__mro__
    assert Capability.__bases__ == (CapabilityBase,)
    assert DefaultCapability.__bases__ == (Capability,)


def test_capability_is_neutral_explicit_and_has_no_implicit_settings() -> None:
    capability = Capability(_metadata())

    assert capability.emit_capability_metadata() == _metadata()
    assert capability.attributes() == {}
    assert capability.callables() == {}
    assert capability.state().ready is None
    assert capability.state().healthy is None
    assert capability.emit_capability_metadata().effective_defaults == {}

    with pytest.raises(LookupError, match="unbound"):
        asyncio.run(capability.call("execute"))


def test_capability_supports_explicit_binding_calls_and_delegated_subcalls() -> None:
    parent = Capability(_metadata("test.parent"))
    child = Capability(_metadata("test.child"))
    parent.bind("execute", lambda value: value + 1)
    child.bind("execute", lambda value: value * 2, delegated=True)

    direct = asyncio.run(parent.call("execute", 2))
    nested = asyncio.run(
        parent.subcall(
            child,
            "execute",
            3,
            context=CapabilityCallContext(call_id="parent-call"),
        )
    )

    assert direct.value == 3
    assert direct.delegated is False
    assert nested.value == 6
    assert nested.delegated is True
    assert nested.capability_id == "test.child"

    with pytest.raises(RuntimeError, match="delegation cycle"):
        asyncio.run(
            parent.subcall(
                parent,
                "execute",
                3,
                context=CapabilityCallContext(call_id="cyclic-call"),
            )
        )


def test_default_capability_discloses_every_opinionated_default() -> None:
    capability = DefaultCapability(_metadata("test.default"))
    metadata = capability.emit_capability_metadata()

    assert metadata.implementation == "default-generic"
    assert metadata.ready is True
    assert metadata.healthy is True
    assert metadata.effective_defaults == DefaultCapability.DEFAULTS


def test_every_layer_40_capability_inherits_10_1_and_binds_declared_operations() -> None:
    capabilities = (
        AttestationAppraisalCapability(_Appraiser()),
        DigitalCredentialIssuanceCapability(_Issuer()),
        DigitalCredentialPresentationCapability(
            _PresentationVerifier(), lambda audience, key: True, lambda holder, request: True
        ),
        AdminControlPlane(),
        ReplayProtectionCapability(_ReplayProvider()),
        SecurityEventsCapability(_Transmitter(), _Receiver()),
        WorkloadIdentityCapability(_SvidProvider(), _SvidVerifier()),
    )

    capability_ids = set()
    for capability in capabilities:
        metadata = capability.emit_capability_metadata()
        assert capability.__class__.__bases__ == (Capability,)
        assert isinstance(capability, ICapability)
        assert metadata.capability_id
        assert metadata.version
        assert set(capability.callables()) == set(metadata.operations)
        capability_ids.add(metadata.capability_id)

    assert len(capability_ids) == len(capabilities)
