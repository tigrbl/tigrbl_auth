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
from tigrbl_identity_contracts.attestation import EvidenceVerificationResult
from tigrbl_identity_contracts.capabilities import (
    CapabilityCallContext,
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
    ICapability,
)
from tigrbl_replay_protection_capability import ReplayProtectionCapability
from tigrbl_security_events import SecurityEventsCapability
from tigrbl_workload_identity import WorkloadIdentityCapability


class _Appraiser:
    def appraise(self, evidence):
        return evidence


class _EvidenceVerifier:
    def verify_evidence(self, evidence):
        return EvidenceVerificationResult(False, "test verifier")


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


def _definition(capability_id: str = "test.capability") -> CapabilityDefinition:
    return CapabilityDefinition(capability_id, "1.0")


def test_capability_inheritance_order_is_contract_base_10_1_then_10_2() -> None:
    assert ICapability in CapabilityBase.__mro__
    assert Capability.__bases__ == (CapabilityBase,)
    assert DefaultCapability.__bases__ == (Capability,)


def test_capability_is_neutral_explicit_and_has_no_implicit_settings() -> None:
    capability = Capability(
        _definition(),
        operations={
            "execute": CapabilityOperation(target=None, required=False),
        },
    )

    assert capability.definition() == _definition()
    assert tuple(capability.operations()) == ("execute",)
    assert capability.attributes() == {}
    assert capability.callables() == {}
    assert capability.state().ready is None
    assert capability.state().healthy is None
    report = capability.capability_report()
    assert report["operations"] == ("execute",)
    assert report["bound_operations"] == ()
    assert report["optional_operations"] == ("execute",)
    assert report["unavailable_optional_operations"] == ("execute",)

    with pytest.raises(LookupError, match="unbound optional"):
        asyncio.run(capability.call("execute"))


def test_required_operation_without_target_fails_during_construction() -> None:
    with pytest.raises(NotImplementedError, match="required.*execute"):
        Capability(
            _definition(),
            operations={"execute": CapabilityOperation(target=None)},
        )


def test_capability_operation_registry_supports_calls_and_delegated_subcalls() -> None:
    parent = Capability(
        _definition("test.parent"),
        operations={
            "execute": CapabilityOperation(target=lambda value: value + 1),
        },
    )
    child = Capability(
        _definition("test.child"),
        operations={
            "execute": CapabilityOperation(
                target=lambda value: value * 2,
                delegated=True,
            ),
        },
    )

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


def test_state_provider_is_evaluated_when_state_and_report_are_requested() -> None:
    states = [
        CapabilityState(ready=False, healthy=True, status="initializing"),
        CapabilityState(ready=True, healthy=True, status="ready"),
    ]
    capability = Capability(
        _definition("test.dynamic-state"),
        operations={"execute": CapabilityOperation(target=lambda: None)},
        state=lambda: states.pop(0),
    )

    assert capability.state().status == "initializing"
    assert capability.capability_report()["state"]["status"] == "ready"


def test_default_capability_applies_only_its_documented_default_state() -> None:
    capability = DefaultCapability(
        _definition("test.default"),
        operations={"execute": CapabilityOperation(target=lambda: None)},
    )

    assert capability.definition() == _definition("test.default")
    assert capability.state() == DefaultCapability.DEFAULT_STATE


def test_every_layer_40_capability_has_one_effective_operation_registry() -> None:
    capabilities = (
        AttestationAppraisalCapability(_EvidenceVerifier(), _Appraiser()),
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
        definition = capability.definition()
        operations = capability.operations()
        report = capability.capability_report()
        assert capability.__class__.__bases__ == (Capability,)
        assert isinstance(capability, ICapability)
        assert definition.capability_id
        assert definition.version
        required_operations = {
            name for name, operation in operations.items() if operation.required
        }
        assert required_operations <= set(capability.callables()) <= set(operations)
        assert report["capability_id"] == definition.capability_id
        assert report["version"] == definition.version
        assert report["operations"] == tuple(operations)
        assert "state" in report
        for removed_field in (
            "ready",
            "healthy",
            "guarantees",
            "optional_features",
            "dependencies",
            "limitations",
            "unsupported",
            "implementation",
        ):
            assert removed_field not in report
        assert report["bound_operations"] == tuple(sorted(capability.callables()))
        capability_ids.add(definition.capability_id)

    assert len(capability_ids) == len(capabilities)
