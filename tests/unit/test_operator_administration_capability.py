from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from tba_runtime_identity_administration_control_plane import (
    OPERATOR_ADMINISTRATION_OPERATIONS,
    OperatorAdministrationCapability,
)
from tba_cli_identity.operator_administration import (
    operator_administration_registry,
)


ROOT = Path(__file__).resolve().parents[2]
HANDLERS = (
    ROOT / "pkgs/60-runtime/tba-cli-identity/src/tba_cli_identity/cli/handlers"
)


def _delegates(target):
    return {name: target for name in OPERATOR_ADMINISTRATION_OPERATIONS}


def test_operator_administration_authorizes_before_durable_delegation() -> None:
    events: list[str] = []

    def authorize(operation: str, context: object) -> None:
        events.append(f"authorize:{operation}:{context}")

    def delegate(context: object, **kwargs: object) -> dict[str, object]:
        events.append(f"delegate:{context}")
        return dict(kwargs)

    capability = OperatorAdministrationCapability(
        authorize=authorize,
        delegates=_delegates(delegate),
    )
    result = asyncio.run(
        capability.call("create_resource", "ctx", record_id="tenant-1")
    )

    assert result.value == {"record_id": "tenant-1"}
    assert events == ["authorize:create_resource:ctx", "delegate:ctx"]
    assert result.delegated is True


def test_operator_administration_denial_prevents_delegation() -> None:
    delegated = False

    def deny(operation: str, context: object) -> None:
        raise PermissionError(f"denied {operation}")

    def delegate(context: object, **kwargs: object) -> None:
        nonlocal delegated
        delegated = True

    capability = OperatorAdministrationCapability(
        authorize=deny,
        delegates=_delegates(delegate),
    )

    with pytest.raises(PermissionError, match="denied delete_resource"):
        asyncio.run(capability.call("delete_resource", "ctx", record_id="tenant-1"))
    assert delegated is False


def test_operator_administration_requires_every_declared_operation() -> None:
    delegates = _delegates(lambda context, **kwargs: None)
    delegates.pop("key_rotate")

    with pytest.raises(NotImplementedError, match="key_rotate"):
        OperatorAdministrationCapability(
            authorize=lambda operation, context: None,
            delegates=delegates,
        )


def test_cli_reports_the_effective_operator_capability_set() -> None:
    report = operator_administration_registry().report()
    capability = report["capabilities"]["identity-admin.operator"]

    assert capability["operations"] == OPERATOR_ADMINISTRATION_OPERATIONS
    assert capability["bound_operations"] == OPERATOR_ADMINISTRATION_OPERATIONS
    assert capability["delegated_operations"] == OPERATOR_ADMINISTRATION_OPERATIONS


def test_cli_handlers_do_not_import_durable_mutation_modules_directly() -> None:
    banned = (
        "tba_runtime_identity_storage.operator_store",
        "tba_runtime_identity_storage.resource_service",
        "tba_runtime_identity_storage.key_management",
    )
    sources = {path: path.read_text(encoding="utf-8") for path in HANDLERS.glob("*.py")}

    violations = {
        str(path.relative_to(ROOT)): tuple(name for name in banned if name in source)
        for path, source in sources.items()
        if any(name in source for name in banned)
    }
    assert violations == {}
