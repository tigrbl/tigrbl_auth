"""Standalone WIMSE Workload Proof Token object."""
from dataclasses import dataclass
from typing import Mapping
from tigrbl_jwt_concrete import JwtObject

@dataclass(frozen=True, slots=True)
class WorkloadProofToken:
    jwt: JwtObject
    def __post_init__(self) -> None:
        missing=[name for name in ("aud","exp","jti","wth") if name not in self.jwt.claims]
        if missing: raise ValueError(f"WPT missing structural claims: {', '.join(missing)}")
    @property
    def claims(self) -> Mapping[str, object]: return self.jwt.claims

__all__=["WorkloadProofToken"]