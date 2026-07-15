from __future__ import annotations

import asyncio
import time

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
    CapabilityContextError,
    CapabilityDeadlineExceededError,
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
    ICapability,
)
from tigrbl_identity_runtime import CapabilityRegistry
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
    assert nested.context is not None
    assert nested.context.parent_call_id == "parent-call"
    assert nested.context.capability_id == "test.child"
    assert nested.context.operation == "execute"

    with pytest.raises(RuntimeError, match="delegation cycle"):
        asyncio.run(
            parent.subcall(
                parent,
                "execute",
                3,
                context=CapabilityCallContext(call_id="cyclic-call"),
            )
        )


def test_call_context_is_populated_validated_and_deadline_preserved() -> None:
    capability = Capability(
        _definition("test.context"),
        operations={"execute": CapabilityOperation(target=lambda: "ok")},
    )
    context = CapabilityCallContext(
        call_id="call-1",
        tenant_id="tenant-1",
        trace_id="trace-1",
        authority=("read", "write"),
        deadline=time.time() + 30,
    )

    result = asyncio.run(capability.call("execute", context=context))
    assert result.context is not None
    assert result.context.capability_id == "test.context"
    assert result.context.operation == "execute"
    assert result.context.tenant_id == "tenant-1"
    assert result.context.trace_id == "trace-1"
    assert result.context.deadline == context.deadline

    with pytest.raises(CapabilityContextError, match="capability_id"):
        asyncio.run(
            capability.call(
                "execute",
                context=CapabilityCallContext(
                    call_id="bad-capability",
                    capability_id="other.capability",
                ),
            )
        )
    with pytest.raises(CapabilityContextError, match="operation"):
        asyncio.run(
            capability.call(
                "execute",
                context=CapabilityCallContext(
                    call_id="bad-operation",
                    operation="other",
                ),
            )
        )
    with pytest.raises(CapabilityDeadlineExceededError):
        asyncio.run(
            capability.call(
                "execute",
                context=CapabilityCallContext(
                    call_id="expired",
                    deadline=time.time() - 1,
                ),
            )
        )


def test_subcall_propagates_trace_and_tenant_and_narrows_authority() -> None:
    parent = Capability(
        _definition("test.parent-authority"),
        operations={"execute": CapabilityOperation(target=lambda: None)},
    )
    child = Capability(
        _definition("test.child-authority"),
        operations={
            "execute": CapabilityOperation(target=lambda: "child", delegated=True)
        },
    )
    context = CapabilityCallContext(
        call_id="parent-authority-call",
        tenant_id="tenant-1",
        trace_id="trace-1",
        authority=("read", "write"),
    )

    result = asyncio.run(
        parent.subcall(
            child,
            "execute",
            context=context,
            authority=("read",),
        )
    )
    assert result.context is not None
    assert result.context.tenant_id == "tenant-1"
    assert result.context.trace_id == "trace-1"
    assert result.context.authority == ("read",)

    with pytest.raises(CapabilityContextError, match="narrow"):
        asyncio.run(
            parent.subcall(
                child,
                "execute",
                context=context,
                authority=("admin",),
            )
        )


def test_runtime_capability_registry_validates_indexes_calls_and_reports() -> None:
    first = Capability(
        _definition("test.registry.first"),
        operations={"execute": CapabilityOperation(target=lambda value: value + 1)},
    )
    optional = Capability(
        _definition("test.registry.optional"),
        operations={
            "execute": CapabilityOperation(target=None, required=False),
        },
    )
    registry = CapabilityRegistry((first, optional))

    assert registry.capability_ids() == (
        "test.registry.first",
        "test.registry.optional",
    )
    assert asyncio.run(
        registry.call("test.registry.first", "execute", 2)
    ).value == 3
    report = registry.report()
    assert report["capability_ids"] == registry.capability_ids()
    assert report["capabilities"]["test.registry.optional"][
        "unavailable_optional_operations"
    ] == ("execute",)

    with pytest.raises(ValueError, match="duplicate"):
        registry.register(first)
    with pytest.raises(LookupError, match="unavailable"):
        registry.require("test.registry.optional", operations=("execute",))


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
    configurations = {}
    capabilities = (
        AttestationAppraisalCapability(_EvidenceVerifier(), _Appraiser()),
        DigitalCredentialIssuanceCapability(
            _Issuer(),
            lambda value: configurations.__setitem__(value.identifier, value),
            configurations.get,
            lambda offer: None,
            lambda request, result: None,
        ),
        DigitalCredentialPresentationCapability(
            _PresentationVerifier(),
            lambda audience, key: True,
            lambda holder, request: True,
            lambda holder, request: None,
            lambda holder, request, result: None,
        ),
        AdminControlPlane(),
        ReplayProtectionCapability(_ReplayProvider()),
        SecurityEventsCapability(
            _Transmitter(),
            _Receiver(),
            lambda event: None,
            lambda subscriber, event: object(),
            lambda delivery: None,
            lambda event: True,
        ),
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
