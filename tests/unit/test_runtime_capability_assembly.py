from __future__ import annotations

import pytest

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    ProtocolCapabilityRequirement,
)
from tigrbl_identity_server.api import runtime_assembly as server_runtime_assembly
from tigrbl_identity_runtime import (
    CapabilityFactory,
    CapabilityRegistry,
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


def test_request_scoped_factory_is_reported_validated_and_materialized() -> None:
    definition = CapabilityDefinition("example.processing", "1.0")
    registry = CapabilityRegistry(
        factories=(
            CapabilityFactory(
                definition,
                ("execute",),
                lambda dependency: Capability(
                    definition,
                    operations={
                        "execute": CapabilityOperation(
                            target=lambda value: dependency + value
                        ),
                    },
                ),
            ),
        )
    )

    assembly = build_runtime_capability_assembly(
        build_providers=dict,
        build_storage_runtime=lambda providers: {},
        build_capabilities=lambda providers, storage: registry,
        build_protocols=lambda capabilities: (
            {"requirements": (_requirement(),)},
        ),
    )
    report = assembly.capabilities.report()["capabilities"]["example.processing"]
    capability = assembly.capabilities.materialize("example.processing", 2)

    assert report["lifetime"] == "request-scoped"
    assert report["state"]["status"] == "requires-materialization"
    assert capability.definition() == definition


def test_request_scoped_factory_rejects_definition_and_operation_drift() -> None:
    definition = CapabilityDefinition("example.processing", "1.0")
    wrong_definition = CapabilityRegistry(
        factories=(
            CapabilityFactory(
                definition,
                ("execute",),
                lambda: Capability(
                    CapabilityDefinition("different", "1.0"),
                    operations={
                        "execute": CapabilityOperation(target=lambda: None),
                    },
                ),
            ),
        )
    )
    missing_operation = CapabilityRegistry(
        factories=(
            CapabilityFactory(
                definition,
                ("execute",),
                lambda: Capability(
                    definition,
                    operations={
                        "other": CapabilityOperation(target=lambda: None),
                    },
                ),
            ),
        )
    )

    with pytest.raises(ValueError, match="different capability definition"):
        wrong_definition.materialize("example.processing")
    with pytest.raises(NotImplementedError, match="did not bind"):
        missing_operation.materialize("example.processing")

@pytest.mark.asyncio
async def test_server_runtime_assembly_async_uses_event_loop_safe_jwt_provider(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    token_coder = object()

    async def async_default(*args: object, **kwargs: object) -> object:
        return token_coder

    def build_with_provider(
        settings_obj: object,
        *,
        token_coder: object,
    ) -> object:
        return token_coder

    monkeypatch.setattr(server_runtime_assembly.JWTCoder, "async_default", async_default)
    monkeypatch.setattr(
        server_runtime_assembly,
        "_build_server_runtime_assembly",
        build_with_provider,
    )

    assembly = await server_runtime_assembly.build_server_runtime_assembly_async(
        object()
    )

    assert assembly is token_coder
