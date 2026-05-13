from __future__ import annotations

from datetime import datetime, timedelta, timezone

from tigrbl_auth.services.governance_extension_plane import (
    AccessReviewWorkflow,
    EntitlementManager,
    PluginRuntimeRegistry,
    SDKEcosystemCatalog,
    ScimPatchOperation,
    ScimProvisioningPlane,
    build_phase5_delivery_summary,
)


def test_sdk_ecosystem_tracks_runtime_compatibility_and_contract_alignment():
    catalog = SDKEcosystemCatalog()
    catalog.register_sdk(
        "sdk-python",
        package_name="tigrbl-auth-python",
        language="python",
        version="0.3.4",
        compatible_runtime_range=("0.3.0", "0.3.9"),
        generated_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
        auth_helpers=("pkce", "client_secret_basic"),
        supported_errors=("problem+json",),
    )
    catalog.register_sdk(
        "sdk-typescript",
        package_name="tigrbl-auth-ts",
        language="typescript",
        version="0.3.4",
        compatible_runtime_range=("0.3.0", "0.3.9"),
        generated_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
        auth_helpers=("pkce", "refresh_token"),
        supported_errors=("problem+json", "json-rpc"),
    )

    assert catalog.compatible_sdk_ids(runtime_version="0.3.4") == (
        "sdk-python",
        "sdk-typescript",
    )

    report = catalog.build_alignment_report(
        runtime_version="0.3.4",
        expected_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
    )

    assert report["aligned_sdk_ids"] == ["sdk-python", "sdk-typescript"]
    assert report["mismatches"] == {}


def test_plugin_runtime_registry_enforces_isolation_audit_and_operator_controls():
    registry = PluginRuntimeRegistry()
    registry.register_plugin(
        "plugin-audit-export",
        name="Audit Export",
        version="1.0.0",
        extension_points=("audit.export", "entitlement.snapshot"),
        hooks={"before-export": lambda payload: {"accepted": payload["tenant_id"]}},
        compatible_sdk_ids=("sdk-python",),
    )
    registry.register_plugin(
        "plugin-faulty",
        name="Faulty Plugin",
        version="1.0.0",
        extension_points=("audit.export",),
        hooks={"before-export": lambda payload: (_ for _ in ()).throw(RuntimeError(f"boom for {payload['tenant_id']}"))},
        compatible_sdk_ids=("sdk-python",),
    )

    result = registry.run_hook("plugin-audit-export", "before-export", {"tenant_id": "tenant-a"})
    assert result == {"accepted": "tenant-a"}

    try:
        registry.run_hook("plugin-faulty", "before-export", {"tenant_id": "tenant-a"})
    except RuntimeError as exc:
        assert "isolated execution" in str(exc)
    else:  # pragma: no cover - fail closed if faulty plugins stop raising.
        raise AssertionError("faulty plugin unexpectedly succeeded")

    assert not registry.plugins["plugin-faulty"].enabled
    assert registry.summary()["event_count"] == 2


def test_scim_provisioning_supports_schema_registration_patch_and_group_membership():
    plane = ScimProvisioningPlane()
    plane.register_schema(
        "urn:ietf:params:scim:schemas:core:2.0:User",
        resource_kind="User",
        required_fields=("displayName", "userName"),
    )
    plane.register_schema(
        "urn:ietf:params:scim:schemas:core:2.0:Group",
        resource_kind="Group",
        required_fields=("displayName",),
    )

    user = plane.provision_user(
        "user-1",
        tenant_id="tenant-a",
        user_name="alice",
        attributes={"displayName": "Alice", "userName": "alice", "email": "alice@example.com"},
    )
    assert user.attributes["displayName"] == "Alice"

    patched = plane.patch_user(
        "user-1",
        tenant_id="tenant-a",
        operations=(
            ScimPatchOperation(op="replace", path="displayName", value="Alice Example"),
            ScimPatchOperation(op="replace", path="active", value=False),
        ),
    )
    group = plane.provision_group("group-1", tenant_id="tenant-a", display_name="admins", members=("user-1",))
    updated_group = plane.add_group_member("group-1", tenant_id="tenant-a", member_id="user-2")

    snapshot = plane.tenant_snapshot("tenant-a")

    assert patched.attributes["displayName"] == "Alice Example"
    assert not patched.active
    assert group.members == ("user-1",)
    assert updated_group.members == ("user-1", "user-2")
    assert snapshot["schema_ids"] == [
        "urn:ietf:params:scim:schemas:core:2.0:Group",
        "urn:ietf:params:scim:schemas:core:2.0:User",
    ]
    assert snapshot["users"][0]["active"] is False
    assert snapshot["groups"][0]["member_count"] == 2


def test_entitlement_management_and_access_reviews_support_revocation_escalation_and_closure():
    entitlements = EntitlementManager()
    entitlements.define_entitlement(
        "ent-admin-console",
        tenant_id="tenant-a",
        name="Admin Console Access",
        owner="security-team",
        description="Grants access to the tenant administration console.",
    )
    assignment = entitlements.assign_entitlement(
        "ent-admin-console",
        subject_id="alice",
        justification="supports incident response",
        assigned_by="owner:security-team",
        expires_at=(datetime.now(tz=timezone.utc) + timedelta(days=30)).isoformat(),
    )
    review = AccessReviewWorkflow(entitlement_manager=entitlements)
    campaign = review.create_campaign(
        "campaign-q2",
        tenant_id="tenant-a",
        name="Quarterly privileged access review",
        reviewer_ids=("reviewer-bob",),
        assignment_ids=(assignment.assignment_id,),
        due_in_days=-1,
    )

    escalated = review.escalate_overdue(reference_time=datetime.now(tz=timezone.utc))
    assert len(escalated) == 1

    item_id = campaign.item_ids[0]
    decision = review.record_decision(
        "campaign-q2",
        item_id=item_id,
        reviewer_id="reviewer-bob",
        decision="revoke",
        reason="access no longer justified",
    )
    closed = review.close_campaign("campaign-q2")
    inventory = entitlements.tenant_inventory("tenant-a")

    assert decision.decision == "revoke"
    assert not entitlements.assignments[assignment.assignment_id].active
    assert closed.status == "closed"
    assert inventory["assignments"][0]["active"] is False


def test_phase5_delivery_summary_aggregates_workflow_state():
    catalog = SDKEcosystemCatalog()
    catalog.register_sdk(
        "sdk-python",
        package_name="tigrbl-auth-python",
        language="python",
        version="0.3.4",
        compatible_runtime_range=("0.3.0", "0.3.9"),
        generated_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
        auth_helpers=("pkce",),
        supported_errors=("problem+json",),
    )
    plugins = PluginRuntimeRegistry()
    plugins.register_plugin(
        "plugin-audit-export",
        name="Audit Export",
        version="1.0.0",
        extension_points=("audit.export",),
        hooks={"before-export": lambda payload: payload},
        compatible_sdk_ids=("sdk-python",),
    )
    scim = ScimProvisioningPlane()
    scim.register_schema("user", resource_kind="User", required_fields=("displayName", "userName"))
    scim.register_schema("group", resource_kind="Group", required_fields=("displayName",))
    scim.provision_user(
        "user-1",
        tenant_id="tenant-a",
        user_name="alice",
        attributes={"displayName": "Alice", "userName": "alice"},
    )
    entitlements = EntitlementManager()
    entitlements.define_entitlement(
        "ent-admin-console",
        tenant_id="tenant-a",
        name="Admin Console Access",
        owner="security-team",
        description="Grants admin UI access.",
    )
    assignment = entitlements.assign_entitlement(
        "ent-admin-console",
        subject_id="alice",
        justification="supports incident response",
        assigned_by="owner:security-team",
    )
    reviews = AccessReviewWorkflow(entitlement_manager=entitlements)
    reviews.create_campaign(
        "campaign-q2",
        tenant_id="tenant-a",
        name="Quarterly privileged access review",
        reviewer_ids=("reviewer-bob",),
        assignment_ids=(assignment.assignment_id,),
    )

    summary = build_phase5_delivery_summary(
        sdk_catalog=catalog,
        plugin_registry=plugins,
        scim_plane=scim,
        entitlement_manager=entitlements,
        access_reviews=reviews,
        runtime_version="0.3.4",
        expected_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
    )

    assert summary["sdk_ecosystem"]["alignment"]["aligned_sdk_ids"] == ["sdk-python"]
    assert summary["extensibility"]["plugin_count"] == 1
    assert summary["scim_provisioning"]["user_count"] == 1
    assert summary["entitlement_management"]["active_assignment_count"] == 1
    assert summary["access_review_workflows"]["campaign_count"] == 1
