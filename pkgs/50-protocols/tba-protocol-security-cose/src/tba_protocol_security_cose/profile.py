from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class COSEProfile:
    name: str
    allowed_algorithms: frozenset[object]
    required_headers: frozenset[object] = frozenset()

    def validate_headers(self, headers: Mapping[object, object]) -> None:
        missing = self.required_headers.difference(headers)
        if missing:
            raise ValueError(
                f"missing required protected headers: {sorted(missing, key=str)}"
            )
        algorithm = headers.get(1, headers.get("alg"))
        if algorithm is not None and algorithm not in self.allowed_algorithms:
            raise ValueError(f"algorithm not allowed by {self.name}: {algorithm}")
