from dataclasses import asdict
from typing import Callable, Mapping

class PolicyDecisionRouter:
    path = "/v1/authorization/decisions"
    def __init__(self, decode: Callable[[Mapping[str, object]], object], engine: object) -> None:
        self.decode, self.engine = decode, engine
    def post(self, payload: Mapping[str, object]) -> dict[str, object]:
        decision = self.engine.evaluate(self.decode(payload))
        result = asdict(decision)
        result["effect"] = decision.effect.value
        result["allowed"] = decision.allowed
        return result

__all__ = ["PolicyDecisionRouter"]
