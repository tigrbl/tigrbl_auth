from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PolicyDecisionBackendAppContract:
    mounted_router_packages: tuple[str, ...]

POLICY_DECISION_BACKEND_APP_CONTRACT = PolicyDecisionBackendAppContract(("tigrbl-auth-router-policy-decision",))

__all__ = ["POLICY_DECISION_BACKEND_APP_CONTRACT", "PolicyDecisionBackendAppContract"]
