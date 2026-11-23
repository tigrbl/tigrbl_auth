from dataclasses import dataclass
from typing import Callable, Mapping

@dataclass(frozen=True)
class AuthorizationAdminClient:
    request: Callable[[str, str, Mapping[str, object] | None], Mapping[str, object]]
    def list_roles(self, tenant_id: str) -> Mapping[str, object]:
        return self.request("GET", f"/v1/tenants/{tenant_id}/authorization/roles", None)
    def create_grant(self, tenant_id: str, payload: Mapping[str, object]) -> Mapping[str, object]:
        return self.request("POST", f"/v1/tenants/{tenant_id}/authorization/grants", payload)

__all__ = ["AuthorizationAdminClient"]
