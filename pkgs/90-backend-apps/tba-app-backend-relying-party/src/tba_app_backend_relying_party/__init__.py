from dataclasses import dataclass
from .contract import RP_BACKEND_APP_CONTRACT, RPBackendAppContract

@dataclass(frozen=True)
class RPDeployment:
    client_id: str
    audience: str
    cookie_name: str
    redirect_allowlist: tuple[str, ...]
    required_acr: str | None = None

def validate_separation(customer: RPDeployment, internal: RPDeployment) -> None:
    if customer.client_id == internal.client_id or customer.cookie_name == internal.cookie_name:
        raise ValueError("customer and internal RP deployments must be isolated")

__all__ = ["RP_BACKEND_APP_CONTRACT", "RPBackendAppContract", "RPDeployment", "validate_separation"]
