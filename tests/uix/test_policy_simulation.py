from tigrbl_auth.uix import ABACAdministration, RBACAdministration, simulate_policy


def test_policy_simulation_returns_allow_deny_and_explanations():
    rbac = RBACAdministration()
    rbac.upsert_role("security-admin", ("key.rotate",))
    rbac.assign_role("alice", "security-admin")

    abac = ABACAdministration()
    abac.upsert_policy(
        "same-tenant-mfa",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )

    allowed = simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": True},
    )
    denied = simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-b", "mfa": True},
    )

    assert allowed.allowed
    assert allowed.matched == ("security-admin", "same-tenant-mfa")
    assert not denied.allowed
    assert "ABAC attributes" in denied.reason
