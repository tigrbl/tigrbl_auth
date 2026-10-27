from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RPBackendAppContract:
    mounted_router_packages: tuple[str, ...]

RP_BACKEND_APP_CONTRACT = RPBackendAppContract(("tigrbl-auth-router-rp-session",))

__all__ = ["RP_BACKEND_APP_CONTRACT", "RPBackendAppContract"]
