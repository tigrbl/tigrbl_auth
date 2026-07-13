from __future__ import annotations

from collections.abc import Mapping

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
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
