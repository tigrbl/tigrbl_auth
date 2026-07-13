"""Neutral capability and protocol-requirement mapping contracts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProtocolCapabilityRequirement:
    protocol: str
    revision: str
    requirement_id: str
    wire_element: str
    capability_id: str
    operation: str
    normalized_namespace: str
    required: bool = True


__all__ = ["ProtocolCapabilityRequirement"]
