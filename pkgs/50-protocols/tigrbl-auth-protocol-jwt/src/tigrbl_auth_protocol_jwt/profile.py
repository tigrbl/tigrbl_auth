from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True, slots=True)
class JwtProfile:
    name: str
    allowed_types: frozenset[str]
    required_claims: frozenset[str]
    allowed_algorithms: frozenset[str]

    def validate(self, headers: Mapping[str, object], claims: Mapping[str, object]) -> None:
        token_type = headers.get("typ")
        if token_type not in self.allowed_types:
            raise ValueError(f"unexpected token type for {self.name}: {token_type}")
        algorithm = headers.get("alg")
        if algorithm in {None, "none"} or algorithm not in self.allowed_algorithms:
            raise ValueError(f"algorithm not allowed by {self.name}: {algorithm}")
        missing = self.required_claims.difference(claims)
        if missing:
            raise ValueError(f"missing required claims: {sorted(missing)}")