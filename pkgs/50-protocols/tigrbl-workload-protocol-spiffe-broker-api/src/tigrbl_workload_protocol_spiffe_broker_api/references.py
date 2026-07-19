from dataclasses import dataclass
from typing import Mapping
@dataclass(frozen=True, slots=True)
class BrokerWorkloadReference:
    kind: str
    attributes: Mapping[str, object]

def normalize_reference(kind: str, attributes: Mapping[str, object]) -> BrokerWorkloadReference:
    if kind not in {"pid", "kubernetes"}: raise ValueError(f"unsupported broker workload reference: {kind}")
    if not attributes: raise ValueError("broker workload reference attributes are required")
    return BrokerWorkloadReference(kind, dict(attributes))