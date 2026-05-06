from tigrbl_auth.uix import (
    ABACAdministration,
    ADMIN_CLIENT_FIELDS,
    PUBLIC_CLIENT_FIELDS,
    AttributePolicy,
    DelegatedAdministration,
    DynamicCondition,
    PolicyEngine,
    RBACAdministration,
    ServiceIdentityRegistry,
    assert_client_mutation_authority,
    build_compliance_report,
    expose_client_record,
    filter_visible_tenants,
    simulate_policy,
)


def test_service_identities_support_tenant_scoped_authentication_and_revocation():
    registry = ServiceIdentityRegistry()
    service = registry.register_service(
        "svc-notifier",
        tenant_id="tenant-a",
        name="notifier",
        scopes=("client.read", "client.update"),
    )
    credential = registry.issue_credential(service.service_id, label="primary")

    auth = registry.authenticate(credential.raw_key, tenant_id="tenant-a", required_permission="client.read")

    assert auth.service.service_id == "svc-notifier"
    assert auth.granted_permissions == ("client.read", "client.update")

    registry.revoke_credential(credential.credential_id)

    try:
        registry.authenticate(credential.raw_key, tenant_id="tenant-a", required_permission="client.read")
    except PermissionError as exc:
        assert "revoked" in str(exc)
    else:  # pragma: no cover - fail closed if the registry stops revoking.
        raise AssertionError("revoked service credential unexpectedly authenticated")


def test_rbac_supports_inheritance_tenant_scoping_and_fine_grained_denies():
    rbac = RBACAdministration()
    rbac.upsert_role("support-reader", ("tenant.read", "client.read"), tenant_id="tenant-a")
    rbac.upsert_role(
        "support-editor",
        ("client.update",),
        tenant_id="tenant-a",
        denied_permissions=("client.update.secret",),
        inherited_roles=("support-reader",),
    )
    rbac.assign_role("alice", "support-editor", tenant_id="tenant-a")

    allowed = rbac.decide("alice", "client.update", "tenant-a")
    denied = rbac.decide("alice", "client.update.secret", "tenant-a")
    wrong_tenant = rbac.decide("alice", "client.update", "tenant-b")

    assert allowed.allowed
    assert set(rbac.effective_permissions("alice", "tenant-a")) == {"client.read", "client.update", "tenant.read"}
    assert not denied.allowed
    assert "denied" in denied.reason
    assert not wrong_tenant.allowed


def test_policy_engine_supports_abac_dynamic_conditions_simulation_and_audit():
    rbac = RBACAdministration()
    rbac.upsert_role("security-admin", ("key.rotate",))
    rbac.assign_role("alice", "security-admin")

    abac = ABACAdministration()
    policy = abac.upsert_policy(
        "same-tenant-mfa-risk",
        permission="key.rotate",
        required_attributes={"tenant_id": "tenant-a", "mfa": True},
        dynamic_conditions=(DynamicCondition(field="risk", operator="lte", expected=2),),
    )

    allowed = simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk": 1},
    )
    denied = simulate_policy(
        rbac=rbac,
        abac=abac,
        subject="alice",
        permission="key.rotate",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk": 7},
    )

    engine = PolicyEngine(rbac=rbac, abac=abac)
    engine_decision = engine.evaluate(
        subject="alice",
        permission="key.rotate",
        tenant_id="tenant-a",
        attributes={"tenant_id": "tenant-a", "mfa": True, "risk": 1},
    )

    assert isinstance(policy, AttributePolicy)
    assert allowed.allowed
    assert not denied.allowed
    assert engine_decision.allowed
    assert len(engine.audit_events) == 1
    assert engine.audit_events[0].permission == "key.rotate"


def test_delegated_administration_controls_tenant_visibility_and_client_exposure():
    delegated = DelegatedAdministration()
    delegated.grant_scope(
        "operator:tenant-a",
        tenant_ids=("tenant-a",),
        permissions=("client.read", "client.update"),
        visible_client_fields=("id", "tenant_id", "name", "client_id", "redirect_uris", "type"),
        mutable_client_fields=("name", "redirect_uris"),
    )
    tenants = [
        {"id": "tenant-a", "name": "Tenant A"},
        {"id": "tenant-b", "name": "Tenant B"},
    ]
    client = {
        "id": "client-1",
        "tenant_id": "tenant-a",
        "name": "Portal",
        "client_id": "client-portal",
        "client_secret": "secret-value",
        "redirect_uris": ["https://portal.example/callback"],
        "type": "confidential",
        "created_at": "2026-05-05T00:00:00+00:00",
    }

    visible = filter_visible_tenants(tenants, subject="operator:tenant-a", delegated_admin=delegated)
    delegated_view = expose_client_record(client, plane="admin", subject="operator:tenant-a", delegated_admin=delegated)
    public_view = expose_client_record(client, plane="public")

    assert [tenant["id"] for tenant in visible] == ["tenant-a"]
    assert set(delegated_view) == {"id", "tenant_id", "name", "client_id", "redirect_uris", "type"}
    assert delegated_view["name"] == "Portal"
    assert "client_secret" not in delegated_view
    assert tuple(public_view) == PUBLIC_CLIENT_FIELDS

    assert_client_mutation_authority(
        subject="operator:tenant-a",
        tenant_id="tenant-a",
        patch={"name": "Portal 2"},
        delegated_admin=delegated,
    )
    try:
        assert_client_mutation_authority(
            subject="operator:tenant-a",
            tenant_id="tenant-a",
            patch={"client_secret": "rotated"},
            delegated_admin=delegated,
        )
    except PermissionError as exc:
        assert "delegated client mutation scope" in str(exc)
    else:  # pragma: no cover - fail closed if delegated mutation checks regress.
        raise AssertionError("delegated mutation unexpectedly allowed a secret rotation")


def test_compliance_report_summarizes_cross_plane_policy_state():
    registry = ServiceIdentityRegistry()
    registry.register_service(
        "svc-notifier",
        tenant_id="tenant-a",
        name="notifier",
        scopes=("client.read",),
    )
    rbac = RBACAdministration()
    rbac.upsert_role("auditor", ("audit.read",))
    rbac.assign_role("dana", "auditor")
    abac = ABACAdministration()
    abac.upsert_policy(
        "tenant-a-audit",
        permission="audit.read",
        required_attributes={"tenant_id": "tenant-a"},
    )
    delegated = DelegatedAdministration()
    delegated.grant_scope("delegate", tenant_ids=("tenant-a",), permissions=("client.read",))
    engine = PolicyEngine(rbac=rbac, abac=abac, delegated_admin=delegated)
    engine.evaluate(
        subject="dana",
        permission="audit.read",
        tenant_id="tenant-a",
        attributes={"tenant_id": "tenant-a"},
    )

    report = build_compliance_report(
        service_registry=registry,
        rbac=rbac,
        abac=abac,
        delegated_admin=delegated,
        audit_events=engine.audit_events,
        tenant_ids=("tenant-a", "tenant-b"),
        clients=(
            {
                "id": "client-1",
                "tenant_id": "tenant-a",
                "name": "Portal",
                "client_id": "client-portal",
                "client_secret": "hidden",
                "redirect_uris": ["https://portal.example/callback"],
                "type": "confidential",
                "created_at": "2026-05-05T00:00:00+00:00",
            },
        ),
    )

    assert report["tenant_isolation"]["enforced"]
    assert report["tenant_isolation"]["tenants"] == ["tenant-a", "tenant-b"]
    assert report["service_identities"]["active_service_count"] == 1
    assert report["policy_engine"]["role_count"] == 1
    assert report["policy_engine"]["policy_count"] == 1
    assert report["policy_engine"]["audit_event_count"] == 1
    assert report["client_exposure"]["admin_fields"] == list(ADMIN_CLIENT_FIELDS)
    assert report["recent_audit"][0]["subject"] == "dana"
