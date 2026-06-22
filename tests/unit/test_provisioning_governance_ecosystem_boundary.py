from __future__ import annotations

import ast
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from tigrbl_authz_policy.governance_extension import (
    AccessReviewWorkflow,
    EntitlementManager,
    PluginRuntimeRegistry,
    SDKEcosystemCatalog,
    ScimPatchOperation,
    ScimProvisioningPlane,
    build_provisioning_governance_ecosystem_delivery_summary,
)


ROOT = Path(__file__).resolve().parents[2]


def _sdk_catalog() -> SDKEcosystemCatalog:
    catalog = SDKEcosystemCatalog()
    catalog.register_sdk(
        "sdk-python",
        package_name="tigrbl-auth-python",
        language="python",
        version="0.3.4",
        compatible_runtime_range=("0.3.0", "0.3.9"),
        generated_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
        auth_helpers=("pkce", "client_secret_basic"),
        supported_errors=("problem+json", "json-rpc"),
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
    return catalog


def _plugins() -> PluginRuntimeRegistry:
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
    return registry


def _scim() -> ScimProvisioningPlane:
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
    return plane


def _entitlements() -> tuple[EntitlementManager, str]:
    manager = EntitlementManager()
    manager.define_entitlement(
        "ent-admin-console",
        tenant_id="tenant-a",
        name="Admin Console Access",
        owner="security-team",
        description="Grants access to the tenant administration console.",
    )
    assignment = manager.assign_entitlement(
        "ent-admin-console",
        subject_id="alice",
        justification="supports incident response",
        assigned_by="owner:security-team",
        expires_at=(datetime.now(tz=timezone.utc) + timedelta(days=30)).isoformat(),
    )
    return manager, assignment.assignment_id


def test_provisioning_governance_ecosystem_boundary_inventory_is_ssot_owned():
    import tigrbl_authz_policy.governance_extension as governance_extension
    import tigrbl_identity_contracts as management_contracts

    removed_inline_surfaces = {
        "GovernanceExtensionBoundaryFeature",
        "PHASE5_GOVERNANCE_EXTENSION_FEATURES",
        "PROVISIONING_GOVERNANCE_ECOSYSTEM_FEATURES",
        "phase5_governance_extension_boundary_integrity",
        "phase5_governance_extension_boundary_manifest",
        "provisioning_governance_ecosystem_boundary_integrity",
        "provisioning_governance_ecosystem_boundary_manifest",
    }

    assert not (removed_inline_surfaces & set(dir(governance_extension)))
    assert not (removed_inline_surfaces & set(dir(management_contracts)))


def test_contracts_and_authz_policy_use_identity_core_time_and_version_primitives():
    helper_names = {"_utc_now", "_utc_now_iso", "_semver_key", "_version_in_range"}
    roots = (
        ROOT
        / "pkgs"
        / "01-contracts"
        / "tigrbl-identity-contracts"
        / "src"
        / "tigrbl_identity_contracts",
        ROOT
        / "pkgs"
        / "40-capabilities"
        / "tigrbl-authz-policy"
        / "src"
        / "tigrbl_authz_policy",
    )

    for root in roots:
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            defined = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
            assert not (defined & helper_names), path


def test_provisioning_governance_ecosystem_boundary_t1_composes_sdk_plugins_scim_entitlements_and_reviews():
    catalog = _sdk_catalog()
    plugins = _plugins()
    scim = _scim()
    entitlements, assignment_id = _entitlements()
    reviews = AccessReviewWorkflow(entitlement_manager=entitlements)

    alignment = catalog.build_alignment_report(
        runtime_version="0.3.4",
        expected_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
    )
    hook_result = plugins.run_hook("plugin-audit-export", "before-export", {"tenant_id": "tenant-a"})
    user = scim.provision_user(
        "user-1",
        tenant_id="tenant-a",
        user_name="alice",
        attributes={"displayName": "Alice", "userName": "alice"},
    )
    scim.provision_group("group-1", tenant_id="tenant-a", display_name="admins", members=(user.user_id,))
    campaign = reviews.create_campaign(
        "campaign-q2",
        tenant_id="tenant-a",
        name="Quarterly privileged access review",
        reviewer_ids=("reviewer-bob",),
        assignment_ids=(assignment_id,),
    )
    decision = reviews.record_decision(
        "campaign-q2",
        item_id=campaign.item_ids[0],
        reviewer_id="reviewer-bob",
        decision="approve",
        reason="access still justified",
    )
    closed = reviews.close_campaign("campaign-q2")
    summary = build_provisioning_governance_ecosystem_delivery_summary(
        sdk_catalog=catalog,
        plugin_registry=plugins,
        scim_plane=scim,
        entitlement_manager=entitlements,
        access_reviews=reviews,
        runtime_version="0.3.4",
        expected_contracts={"openapi": "3.1.0", "openrpc": "1.3.2"},
    )

    assert alignment["aligned_sdk_ids"] == ["sdk-python", "sdk-typescript"]
    assert hook_result == {"accepted": "tenant-a"}
    assert decision.decision == "approve"
    assert closed.status == "closed"
    assert summary["sdk_ecosystem"]["package_count"] == 2
    assert summary["extensibility"]["event_count"] == 1
    assert summary["scim_provisioning"]["user_count"] == 1
    assert summary["entitlement_management"]["active_assignment_count"] == 1
    assert summary["access_review_workflows"]["decision_count"] == 1


def test_provisioning_governance_ecosystem_boundary_t2_fails_closed_for_drift_and_unsafe_operations():
    catalog = _sdk_catalog()
    plugins = _plugins()
    scim = _scim()
    entitlements, assignment_id = _entitlements()
    reviews = AccessReviewWorkflow(entitlement_manager=entitlements)

    mismatch = catalog.build_alignment_report(
        runtime_version="0.3.4",
        expected_contracts={"openapi": "3.1.1", "openrpc": "1.3.2"},
    )
    assert sorted(mismatch["mismatches"]) == ["sdk-python", "sdk-typescript"]

    with pytest.raises(ValueError, match="generated contract alignment"):
        catalog.register_sdk(
            "sdk-empty",
            package_name="empty",
            language="python",
            version="0.3.4",
            compatible_runtime_range=("0.3.0", "0.3.9"),
            generated_contracts={},
            auth_helpers=("pkce",),
            supported_errors=("problem+json",),
        )
    with pytest.raises(RuntimeError, match="isolated execution"):
        plugins.run_hook("plugin-faulty", "before-export", {"tenant_id": "tenant-a"})
    assert plugins.plugins["plugin-faulty"].enabled is False
    with pytest.raises(PermissionError, match="plugin is disabled"):
        plugins.run_hook("plugin-faulty", "before-export", {"tenant_id": "tenant-a"})

    with pytest.raises(ValueError, match="missing required fields"):
        scim.provision_user(
            "user-1",
            tenant_id="tenant-a",
            user_name="alice",
            attributes={"userName": "alice"},
        )
    scim.provision_user(
        "user-1",
        tenant_id="tenant-a",
        user_name="alice",
        attributes={"displayName": "Alice", "userName": "alice"},
    )
    with pytest.raises(PermissionError, match="user tenant mismatch"):
        scim.patch_user(
            "user-1",
            tenant_id="tenant-b",
            operations=(ScimPatchOperation(op="replace", path="active", value=False),),
        )
    with pytest.raises(ValueError, match="unsupported SCIM patch operation"):
        scim.patch_user(
            "user-1",
            tenant_id="tenant-a",
            operations=(ScimPatchOperation(op="remove", path="displayName", value=None),),
        )

    campaign = reviews.create_campaign(
        "campaign-q2",
        tenant_id="tenant-a",
        name="Quarterly privileged access review",
        reviewer_ids=("reviewer-bob",),
        assignment_ids=(assignment_id,),
        due_in_days=-1,
    )
    with pytest.raises(PermissionError, match="pending review items"):
        reviews.close_campaign("campaign-q2")
    escalated = reviews.escalate_overdue(reference_time=datetime.now(tz=timezone.utc))
    assert escalated == campaign.item_ids
    with pytest.raises(PermissionError, match="reviewer mismatch"):
        reviews.record_decision(
            "campaign-q2",
            item_id=campaign.item_ids[0],
            reviewer_id="reviewer-eve",
            decision="approve",
            reason="wrong reviewer",
        )
    revoked = entitlements.revoke_assignment(assignment_id, reason="access no longer justified")
    assert revoked.active is False

    expired = entitlements.assign_entitlement(
        "ent-admin-console",
        subject_id="bob",
        justification="temporary project access",
        assigned_by="owner:security-team",
        expires_at=(datetime.now(tz=timezone.utc) - timedelta(days=1)).isoformat(),
    )
    assert entitlements.expire_assignments(reference_time=datetime.now(tz=timezone.utc)) == (expired.assignment_id,)
