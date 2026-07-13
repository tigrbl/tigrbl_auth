from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityMetadata, CapabilityState


class DefaultCapability(Capability):
    DEFAULTS: Mapping[str, object] = {
        "ready": True,
        "healthy": True,
        "binding_policy": "explicit-only",
    }

    def __init__(self, metadata: CapabilityMetadata, /) -> None:
        effective_defaults = dict(self.DEFAULTS)
        effective_defaults.update(metadata.effective_defaults)
        super().__init__(
            replace(
                metadata,
                ready=metadata.ready if metadata.ready is not None else True,
                healthy=metadata.healthy if metadata.healthy is not None else True,
                implementation="default-generic",
                effective_defaults=effective_defaults,
            ),
            state=CapabilityState(
                ready=metadata.ready if metadata.ready is not None else True,
                healthy=metadata.healthy if metadata.healthy is not None else True,
                status="ready",
            ),
        )


__all__ = ["DefaultCapability"]
