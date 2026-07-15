from __future__ import annotations

import pytest

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    ProtocolCapabilityRequirement,
)
from tigrbl_identity_runtime import (
    ProtocolCapabilityBindingError,
    build_runtime_capability_assembly,
)


def _requirement(
    capability_id: str = "example.processing",
    operation: str = "execute",
    *,
    required: bool = True,
) -> ProtocolCapabilityRequirement:
    return ProtocolCapabilityRequirement(
        protocol="example",
        revision="1.0",
        requirement_id="example-execution",
        wire_element="example request",
        capability_id=capability_id,
        operation=operation,
        normalized_namespace="example-result",
        required=required,
    )


def _capability() -> Capability:
    return Capability(
        CapabilityDefinition("example.processing", "1.0"),
        operations={
            "execute": CapabilityOperation(target=lambda value: value),
        },
    )


def test_runtime_assembly_constructs_layers_in_dependency_order() -> None:
    calls: list[str] = []

    def providers():
        calls.append("providers")
        return {"signer": object()}

    def storage(provider_set):
        calls.append("storage-runtime")
        assert tuple(provider_set) == ("signer",)
        return {"tokens": object()}

    def capabilities(provider_set, storage_set):
        calls.append("capabilities")
        assert tuple(provider_set) == ("signer",)
        assert tuple(storage_set) == ("tokens",)
        return (_capability(),)

    def protocols(registry):
        calls.append("protocols")
        assert registry.capability_ids() == ("example.processing",)
        return (
            {
                "protocol": "example",
                "selected_revision": "1.0",
                "requirements": (_requirement(),),
            },
        )

    assembly = build_runtime_capability_assembly(
        build_providers=providers,
        build_storage_runtime=storage,
        build_capabilities=capabilities,
        build_protocols=protocols,
    )

    assert calls == ["providers", "storage-runtime", "capabilities", "protocols"]
    assert assembly.construction_order == tuple(calls)
    assert assembly.report()["capabilities"]["capability_ids"] == (
        "example.processing",
    )


@pytest.mark.parametrize(
    ("requirements", "message"),
    [
        ((_requirement("missing"),), "missing capability missing"),
        ((_requirement(operation="missing"),), "unavailable operation"),
    ],
)
def test_runtime_assembly_fails_closed_on_missing_required_targets(
    requirements: tuple[ProtocolCapabilityRequirement, ...],
    message: str,
) -> None:
    with pytest.raises(ProtocolCapabilityBindingError, match=message):
        build_runtime_capability_assembly(
            build_providers=dict,
            build_storage_runtime=lambda providers: {},
            build_capabilities=lambda providers, storage: (_capability(),),
            build_protocols=lambda registry: ({"requirements": requirements},),
        )


def test_runtime_assembly_allows_an_absent_optional_capability() -> None:
    assembly = build_runtime_capability_assembly(
        build_providers=dict,
        build_storage_runtime=lambda providers: {},
        build_capabilities=lambda providers, storage: (_capability(),),
        build_protocols=lambda registry: (
            {"requirements": (_requirement("optional", required=False),)},
        ),
    )

    assert assembly.capabilities.capability_ids() == ("example.processing",)
