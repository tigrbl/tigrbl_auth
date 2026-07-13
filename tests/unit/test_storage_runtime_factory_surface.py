from __future__ import annotations

from tigrbl import OpSpec, TableSpec
from tigrbl_identity_storage.tables import ReplayReservation
from tigrbl_identity_storage_runtime import (
    RUNTIME_OPERATION_BY_ALIAS,
    RUNTIME_TABLE_BY_NAME,
    RUNTIME_TABLE_SPEC_BY_NAME,
    activateRuntimeTableSpec,
    defineRuntimeTableSpec,
    deriveRuntimeTableSpec,
    makeRuntimeOperation,
)


async def _reserve(ctx):
    return ctx


def test_runtime_operation_is_carrier_neutral_and_transactional() -> None:
    operation = makeRuntimeOperation(alias="check_and_reserve", handler=_reserve)

    assert isinstance(operation, OpSpec)
    assert operation.alias == "check_and_reserve"
    assert operation.bindings == ()
    assert operation.expose_routes is False
    assert operation.expose_rpc is False
    assert operation.expose_method is True
    assert operation.tx_scope == "read_write"
    assert operation.handler is _reserve


def test_runtime_table_definition_uses_the_public_tigrbl_factory() -> None:
    operation = makeRuntimeOperation(alias="check_and_reserve", handler=_reserve)
    definition = defineRuntimeTableSpec(operations=(operation,))

    assert issubclass(definition, TableSpec)
    assert definition.OPS == (operation,)


def test_runtime_spec_derivation_preserves_model_and_overlays_operations() -> None:
    operation = makeRuntimeOperation(alias="check_and_reserve", handler=_reserve)
    derived = deriveRuntimeTableSpec(
        ReplayReservation,
        operations=(operation,),
    )

    assert derived.model is ReplayReservation
    assert derived.table_profile is not None
    assert derived.table_profile.kind == "rest_oltp"
    assert next(item for item in derived.ops if item.alias == "check_and_reserve") is operation
    assert {item.alias for item in derived.ops}.issuperset({"create", "read", "list"})


def test_runtime_inventory_indexes_canonical_tables_and_operations() -> None:
    assert RUNTIME_TABLE_BY_NAME["ReplayReservation"] is ReplayReservation
    spec = RUNTIME_TABLE_SPEC_BY_NAME["ReplayReservation"]
    assert spec.model is ReplayReservation
    assert RUNTIME_OPERATION_BY_ALIAS[("ReplayReservation", "create")].table is ReplayReservation


def test_runtime_activation_materializes_custom_operation_on_canonical_table() -> None:
    operation = makeRuntimeOperation(alias="runtime_probe", handler=_reserve)
    spec = deriveRuntimeTableSpec(ReplayReservation, operations=(operation,))
    original = tuple(getattr(ReplayReservation, "__tigrbl_ops__", ()) or ())
    try:
        activateRuntimeTableSpec(spec)
        assert ReplayReservation.ops.by_alias["runtime_probe"].alias == "runtime_probe"
        assert ReplayReservation.handlers.runtime_probe.core is not None
        assert ReplayReservation.schemas.runtime_probe is not None
    finally:
        ReplayReservation.__tigrbl_ops__ = original
        from tigrbl import rebind

        rebind(ReplayReservation)
