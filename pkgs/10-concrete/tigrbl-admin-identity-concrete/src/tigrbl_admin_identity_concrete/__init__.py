from dataclasses import dataclass, field
from tigrbl_identity_contracts.authority import AuthorityRole
from tigrbl_identity_contracts.principals import PrincipalKind
from tigrbl_identity_bases import IdentityBase
from tigrbl_identity_core import new_model_id


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
