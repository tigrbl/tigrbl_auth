from .contract import POLICY_DECISION_BACKEND_APP_CONTRACT, PolicyDecisionBackendAppContract

def build_app(router):
    return {"name": "tigrbl-policy-decision", "router": router, "health": "/health"}

__all__ = ["POLICY_DECISION_BACKEND_APP_CONTRACT", "PolicyDecisionBackendAppContract", "build_app"]
