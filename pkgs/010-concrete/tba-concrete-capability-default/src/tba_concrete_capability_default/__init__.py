from __future__ import annotations

from collections.abc import Mapping

from tba_concrete_capability import Capability
from tba_contracts_identity.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
    CapabilityStateProvider,
)


class DefaultCapability(Capability):
    DEFAULT_STATE = CapabilityState(ready=True, healthy=True, status="ready")

    def __init__(
        self,
        definition: CapabilityDefinition,
        /,
        *,
        operations: Mapping[str, CapabilityOperation],
        attributes: Mapping[str, object] | None = None,
        state: CapabilityState | CapabilityStateProvider | None = None,
    ) -> None:
        super().__init__(
            definition,
            operations=operations,
            attributes=attributes,
            state=state if state is not None else self.DEFAULT_STATE,
        )


__all__ = ["DefaultCapability"]
