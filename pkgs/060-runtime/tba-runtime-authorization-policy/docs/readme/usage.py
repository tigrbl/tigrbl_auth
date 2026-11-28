from tba_runtime_authorization_policy import AuthorityRole, AuthorityScope
from tba_runtime_authorization_policy import (
    AdminGate,
    ABACAdministrator,
    DelegatedAdministrator,
)
from tba_runtime_authorization_policy import (
    PolicyEngine,
    RBACAdministrator,
    ServiceIdentityRegistry,
)
from tba_runtime_authorization_policy import (
    AuthorityDerivationGraph,
    PolicyDecisionEngine,
)
from tba_runtime_authorization_policy import (
    AuthorizationInvariant,
    AuthorizationSafetyPropertyEvaluator,
)


def configure_authorization(*, app, db, deployment):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    assert AuthorityRole.ADMIN.value == "admin"
    scope = AuthorityScope("tenant-a", "client.read")
    graph = AuthorityDerivationGraph()
    abac = ABACAdministrator(db)
    delegated = DelegatedAdministrator(db)
    engine = PolicyDecisionEngine()
    gate = AdminGate(app, deployment=deployment)
    orchestrator = PolicyEngine(db=db)
    invariants = (
        AuthorizationInvariant(
            invariant_id="authz.non_escalation",
            title="No escalation",
            property_family="safety",
            statement="Effective authority cannot exceed granted closure.",
            verification_method="graph",
        ),
    )
    rbac = RBACAdministrator(db)
    services = ServiceIdentityRegistry()
