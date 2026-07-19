"""Standalone WIMSE Workload Identity Token object."""
from dataclasses import dataclass
from typing import Mapping
from tigrbl_jwt_concrete import JwtObject

@dataclass(frozen=True, slots=True)
class WorkloadIdentityToken:
    jwt: JwtObject
    def __post_init__(self) -> None:
        missing=[name for name in ("sub","cnf","exp") if name not in self.jwt.claims]
        if missing: raise ValueError(f"WIT missing structural claims: {', '.join(missing)}")
    @property
    def claims(self) -> Mapping[str, object]: return self.jwt.claims

__all__=["WorkloadIdentityToken"]