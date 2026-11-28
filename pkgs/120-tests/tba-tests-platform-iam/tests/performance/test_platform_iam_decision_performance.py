from time import perf_counter

from tba_contracts_authorization import ActionDefinition, AuthorizationRequest, PrincipalRef, ResourceRef
from tba_provider_authorization_policy_decision_engine import PlatformPolicyDecisionEngine


def test_default_deny_evaluation_1000_requests_under_half_second() -> None:
    engine = PlatformPolicyDecisionEngine(actions=[ActionDefinition("tenant.read", "tenant")])
    request = AuthorizationRequest(
        principal=PrincipalRef("alice", "user", tenant_id="tenant-a"),
        action="tenant.read",
        resource=ResourceRef("tenant", "tenant-a", "tenant-a"),
    )
    started = perf_counter()
    for _ in range(1000):
        assert not engine.evaluate(request).allowed
    assert perf_counter() - started < 0.5
