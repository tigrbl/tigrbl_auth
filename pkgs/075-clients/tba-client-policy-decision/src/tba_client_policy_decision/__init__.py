from dataclasses import dataclass
from typing import Callable, Mapping

@dataclass(frozen=True)
class PolicyDecisionClient:
    request: Callable[[Mapping[str, object]], Mapping[str, object]]
    def decide(self, payload: Mapping[str, object]) -> Mapping[str, object]:
        return self.request(payload)

__all__ = ["PolicyDecisionClient"]
