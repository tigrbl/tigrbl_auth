"""Standalone OIDC ID Token structural object."""
from dataclasses import dataclass
from typing import Mapping
from tigrbl_jwt_concrete import JwtObject

@dataclass(frozen=True, slots=True)
class OidcIdToken:
    jwt: JwtObject
    def __post_init__(self) -> None:
        claims=self.jwt.claims
        missing=[name for name in ("iss","sub","aud","exp","iat") if name not in claims]
        if missing: raise ValueError(f"ID Token missing required claims: {', '.join(missing)}")
    @property
    def claims(self) -> Mapping[str, object]: return self.jwt.claims
    @property
    def serialized(self) -> str: return self.jwt.serialized

__all__=["OidcIdToken"]