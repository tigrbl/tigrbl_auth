"""Normalized protocol-artifact processing and coverage contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol

from .capabilities import ProtocolCapabilityRequirement


@dataclass(frozen=True, slots=True)
class ArtifactProcessingRequest:
    artifact_kind: str
    encoded: str | bytes | Mapping[str, object]
    expected_profile: str
    context: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ArtifactProcessingResult:
    accepted: bool
    normalized: object = None
    errors: tuple[str, ...] = ()


class ArtifactProcessorPort(Protocol):
    def decode(self, request: ArtifactProcessingRequest, /) -> ArtifactProcessingResult: ...
    def validate(self, request: ArtifactProcessingRequest, /) -> ArtifactProcessingResult: ...
    def encode(self, request: ArtifactProcessingRequest, /) -> ArtifactProcessingResult: ...
    def map_error(self, error: object, /) -> ArtifactProcessingResult: ...


def build_protocol_capability_report(
    *,
    protocol: str,
    revision: str,
    features: tuple[str, ...],
    evidence_links: tuple[str, ...] = (),
    extra_requirements: tuple[ProtocolCapabilityRequirement, ...] = (),
) -> dict[str, object]:
    generated = tuple(
        ProtocolCapabilityRequirement(
            protocol=protocol,
            revision=revision,
            requirement_id=f"{protocol}:{feature}",
            wire_element=feature,
            capability_id="artifact.processing",
            operation="validate",
            normalized_namespace=f"protocol-artifact:{protocol}",
        )
        for feature in sorted(set(features))
    )
    requirements = generated + tuple(extra_requirements)
    return {
        "protocol": protocol,
        "selected_revision": revision,
        "features": tuple(sorted(set(features))),
        "required_capabilities": tuple(sorted({item.capability_id for item in requirements})),
        "requirements": requirements,
        "effective_coverage": {
            item.requirement_id: f"{item.capability_id}.{item.operation}" for item in requirements
        },
        "evidence_links": tuple(evidence_links),
    }


__all__ = [
    "ArtifactProcessingRequest", "ArtifactProcessingResult", "ArtifactProcessorPort",
    "build_protocol_capability_report",
]
