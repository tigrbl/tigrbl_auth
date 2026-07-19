from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True, slots=True)
class JWEProfile:
    name: str
    allowed_algorithms: frozenset[str]
    required_headers: frozenset[str] = frozenset()

    def validate_headers(self, headers: Mapping[str, object]) -> None:
        missing = self.required_headers.difference(headers)
        if missing:
            raise ValueError(f"missing required protected headers: {sorted(missing)}")
        algorithm = headers.get("alg")
        if algorithm is not None and algorithm not in self.allowed_algorithms:
            raise ValueError(f"algorithm not allowed by {self.name}: {algorithm}")
