from dataclasses import dataclass, field
from tigrbl_identity_contracts.principals import PrincipalKind, PrincipalStatus
from tigrbl_identity_model_bases import IdentityBase, clean_tuple, required_text


@dataclass(frozen=True, slots=True, kw_only=True)
class ServiceIdentity(IdentityBase):
    id: str = ""
    subject: str = ""
    kind: PrincipalKind = field(default=PrincipalKind.SERVICE_IDENTITY, init=False)
    service_id: str = ""
    name: str = ""
    scopes: tuple[str, ...] = ()
    enabled: bool = True

    def __post_init__(self) -> None:
        service_id = required_text(
            self.service_id or self.subject or self.id, "service id"
        )
        object.__setattr__(self, "service_id", service_id)
        object.__setattr__(self, "id", self.id or service_id)
        object.__setattr__(self, "subject", self.subject or f"service:{service_id}")
        object.__setattr__(self, "name", self.name or self.display_name or service_id)
        object.__setattr__(self, "display_name", self.display_name or self.name)
        object.__setattr__(self, "scopes", clean_tuple(self.scopes))
        if not self.enabled:
            object.__setattr__(self, "status", PrincipalStatus.DISABLED)
        IdentityBase.__post_init__(self)


__all__ = ["ServiceIdentity"]
