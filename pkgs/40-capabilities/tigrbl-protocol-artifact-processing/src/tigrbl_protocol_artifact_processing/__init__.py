from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.protocol_processing import (
    ArtifactProcessingRequest,
    ArtifactProcessingResult,
    ArtifactProcessorPort,
)


class ProtocolArtifactProcessingCapability(Capability):
    def __init__(self, processor: ArtifactProcessorPort):
        super().__init__(
            CapabilityDefinition(
                capability_id="artifact.processing",
                version="1.0",
            ),
            operations={
                name: CapabilityOperation(
                    target=getattr(processor, name),
                    delegated=True,
                )
                for name in ("decode", "validate", "encode", "map_error")
            },
            state=CapabilityState(ready=True, healthy=True, status="ready"),
        )
        self._processor = processor


__all__ = [
    "ArtifactProcessingRequest", "ArtifactProcessingResult",
    "ProtocolArtifactProcessingCapability",
]
