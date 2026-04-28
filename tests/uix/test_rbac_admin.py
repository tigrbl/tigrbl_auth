from tigrbl_auth.uix import RBACAdministration


def test_rbac_administration_supports_roles_permissions_and_assignments():
    rbac = RBACAdministration()
    role = rbac.upsert_role("support-admin", ("tenant.read", "client.disable"))
    rbac.assign_role("alice", "support-admin")

    decision = rbac.decide("alice", "client.disable")

    assert role.permissions == ("client.disable", "tenant.read")
    assert rbac.assignments["alice"] == ("support-admin",)
    assert decision.allowed
    assert decision.matched == ("support-admin",)


def test_rbac_administration_surfaces_denials():
    rbac = RBACAdministration()
    rbac.upsert_role("auditor", ("tenant.read",))
    rbac.assign_role("bob", "auditor")

    decision = rbac.decide("bob", "key.rotate")

    assert not decision.allowed
    assert decision.reason == "permission denied by RBAC role assignments"
