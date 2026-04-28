from tigrbl_auth.uix import ABACAdministration


def test_abac_administration_supports_policies_and_attributes():
    abac = ABACAdministration()
    policy = abac.upsert_policy(
        "same-tenant-key-rotation",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )

    decision = abac.decide(permission="key.rotate", attributes={"tenant_id": "tenant-a", "mfa": True})

    assert policy.required_attributes == {"tenant_id": "tenant-a", "mfa": True}
    assert decision.allowed
    assert decision.matched == ("same-tenant-key-rotation",)


def test_abac_administration_surfaces_denials():
    abac = ABACAdministration()
    abac.upsert_policy(
        "same-tenant-key-rotation",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
    )

    decision = abac.decide(permission="key.rotate", attributes={"tenant_id": "tenant-b", "mfa": True})

    assert not decision.allowed
    assert decision.reason == "permission denied by ABAC attributes"
