from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import CapabilityMetadata
from tigrbl_identity_contracts.protocol_processing import (
    ArtifactProcessingRequest,
    ArtifactProcessingResult,
    ArtifactProcessorPort,
)


class ProtocolArtifactProcessingCapability(Capability):
    def __init__(self, processor: ArtifactProcessorPort):
        super().__init__(
            CapabilityMetadata(
                capability_id="artifact.processing",
                version="1.0",
                operations=("decode", "validate", "encode", "map_error"),
                guarantees=("profile-explicit", "fail-closed-validation"),
                dependencies=(type(processor).__name__,),
                ready=True,
                healthy=True,
                unsupported=("key-loading", "trust-selection", "persistence"),
            )
        )
        self._processor = processor
        for operation in self.emit_capability_metadata().operations:
            self.bind(operation, getattr(processor, operation), delegated=True)


__all__ = [
    "ArtifactProcessingRequest", "ArtifactProcessingResult",
    "ProtocolArtifactProcessingCapability",
]
