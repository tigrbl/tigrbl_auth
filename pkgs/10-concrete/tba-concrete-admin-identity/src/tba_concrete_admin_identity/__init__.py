from dataclasses import dataclass, field
from tba_contracts_identity.authority import AuthorityRole
from tba_contracts_identity.principals import PrincipalKind
from tba_bases_identity import IdentityBase
from tba_primitives_identity import new_model_id


@dataclass(frozen=True, slots=True, kw_only=True)
class AdminIdentity(IdentityBase):
    id: str = field(default_factory=new_model_id)
    kind: PrincipalKind = field(default=PrincipalKind.USER, init=False)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "roles", tuple(sorted({AuthorityRole.ADMIN.value, *self.roles}))
        )
        IdentityBase.__post_init__(self)


__all__ = ["AdminIdentity"]
