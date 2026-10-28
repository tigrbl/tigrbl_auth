from dataclasses import dataclass, field
from tba_contracts_identity.principals import PrincipalKind
from tba_bases_identity import IdentityBase
from tba_primitives_identity import new_model_id


@dataclass(frozen=True, slots=True, kw_only=True)
class UserIdentity(IdentityBase):
    id: str = field(default_factory=new_model_id)
    kind: PrincipalKind = field(default=PrincipalKind.USER, init=False)


__all__ = ["UserIdentity"]
