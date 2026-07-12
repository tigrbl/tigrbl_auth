from dataclasses import dataclass, field
from tigrbl_identity_contracts.principals import PrincipalKind
from tigrbl_identity_model_bases import IdentityBase, new_model_id


@dataclass(frozen=True, slots=True, kw_only=True)
class ClientIdentity(IdentityBase):
    id: str = field(default_factory=new_model_id)
    kind: PrincipalKind = field(default=PrincipalKind.CLIENT_IDENTITY, init=False)


__all__ = ["ClientIdentity"]
