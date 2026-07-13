"""Authorization governance-extension public surface."""

from __future__ import annotations
# ruff: noqa: F403,F405

from dataclasses import replace
from datetime import datetime, timedelta
from typing import Any, Callable, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now, utc_now_iso
from tigrbl_identity_core.versions import version_in_range
from tigrbl_identity_contracts.governance import *


class SDKEcosystemCatalog:
    def __init__(self) -> None:
        self._packages: dict[str, SDKPackage] = {}

    @property
    def packages(self) -> Mapping[str, SDKPackage]:
        return dict(self._packages)

    def register_sdk(
        self,
        sdk_id: str,
        *,
        package_name: str,
        language: str,
        version: str,
        compatible_runtime_range: tuple[str, str],
        generated_contracts: Mapping[str, str],
        auth_helpers: Iterable[str],
        supported_errors: Iterable[str],
        release_channel: str = "stable",
    ) -> SDKPackage:
        if not generated_contracts:
            raise ValueError("sdk package must declare generated contract alignment")
        helper_tuple = tuple(sorted(set(auth_helpers)))
        error_tuple = tuple(sorted(set(supported_errors)))
        if not helper_tuple:
            raise ValueError("sdk package must declare authentication helpers")
        if not error_tuple:
            raise ValueError("sdk package must declare supported errors")
        package = SDKPackage(
            sdk_id=sdk_id,
            package_name=package_name,
            language=language,
            version=version,
            compatible_runtime_range=compatible_runtime_range,
            generated_contracts=dict(generated_contracts),
            auth_helpers=helper_tuple,
            supported_errors=error_tuple,
            release_channel=release_channel,
        )
        self._packages[sdk_id] = package
        return package

    def compatible_sdk_ids(self, *, runtime_version: str, language: str | None = None) -> tuple[str, ...]:
        compatible: list[str] = []
        for package in self._packages.values():
            if language is not None and package.language != language:
                continue
            if version_in_range(runtime_version, package.compatible_runtime_range):
                compatible.append(package.sdk_id)
        return tuple(sorted(compatible))

    def build_alignment_report(
        self,
        *,
        runtime_version: str,
        expected_contracts: Mapping[str, str],
    ) -> dict[str, Any]:
        aligned_sdk_ids: list[str] = []
        mismatches: dict[str, dict[str, str]] = {}
        for package in self._packages.values():
            if not version_in_range(runtime_version, package.compatible_runtime_range):
                mismatches[package.sdk_id] = {"runtime": runtime_version, "reason": "runtime version out of range"}
                continue
            contract_mismatch = {
                kind: f"expected {expected_version}, got {package.generated_contracts.get(kind, 'missing')}"
                for kind, expected_version in expected_contracts.items()
                if package.generated_contracts.get(kind) != expected_version
            }
            if contract_mismatch:
                mismatches[package.sdk_id] = contract_mismatch
                continue
            aligned_sdk_ids.append(package.sdk_id)
        return {
            "runtime_version": runtime_version,
            "expected_contracts": dict(expected_contracts),
            "compatible_sdk_ids": list(self.compatible_sdk_ids(runtime_version=runtime_version)),
            "aligned_sdk_ids": sorted(aligned_sdk_ids),
            "mismatches": mismatches,
        }

    def summary(self) -> dict[str, Any]:
        languages = sorted({package.language for package in self._packages.values()})
        return {
            "package_count": len(self._packages),
            "languages": languages,
            "release_channels": sorted({package.release_channel for package in self._packages.values()}),
        }


class PluginRuntimeRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginDescriptor] = {}
        self._hook_handlers: dict[str, dict[str, Callable[[Mapping[str, Any]], Mapping[str, Any]]]] = {}
        self._events: list[PluginLifecycleEvent] = []

    @property
    def plugins(self) -> Mapping[str, PluginDescriptor]:
        return dict(self._plugins)

    @property
    def events(self) -> tuple[PluginLifecycleEvent, ...]:
        return tuple(self._events)

    def register_plugin(
        self,
        plugin_id: str,
        *,
        name: str,
        version: str,
        extension_points: Iterable[str],
        hooks: Mapping[str, Callable[[Mapping[str, Any]], Mapping[str, Any]]],
        compatible_sdk_ids: Iterable[str],
        isolation_mode: str = "process",
        operator_controls: Iterable[str] = ("audit", "disable"),
        fail_behavior: str = "disable_on_error",
    ) -> PluginDescriptor:
        descriptor = PluginDescriptor(
            plugin_id=plugin_id,
            name=name,
            version=version,
            extension_points=tuple(sorted(set(extension_points))),
            lifecycle_hooks=tuple(sorted(set(hooks))),
            compatible_sdk_ids=tuple(sorted(set(compatible_sdk_ids))),
            isolation_mode=isolation_mode,
            operator_controls=tuple(sorted(set(operator_controls))),
            fail_behavior=fail_behavior,
            registered_at=utc_now_iso(),
        )
        self._plugins[plugin_id] = descriptor
        self._hook_handlers[plugin_id] = dict(hooks)
        return descriptor

    def disable_plugin(self, plugin_id: str) -> PluginDescriptor:
        descriptor = self._plugins[plugin_id]
        updated = replace(descriptor, enabled=False)
        self._plugins[plugin_id] = updated
        return updated

    def enable_plugin(self, plugin_id: str) -> PluginDescriptor:
        descriptor = self._plugins[plugin_id]
        updated = replace(descriptor, enabled=True)
        self._plugins[plugin_id] = updated
        return updated

    def run_hook(self, plugin_id: str, hook_name: str, context: Mapping[str, Any]) -> Mapping[str, Any]:
        descriptor = self._plugins.get(plugin_id)
        if descriptor is None:
            raise KeyError(f"unknown plugin {plugin_id!r}")
        if not descriptor.enabled:
            raise PermissionError("plugin is disabled")
        handler = self._hook_handlers.get(plugin_id, {}).get(hook_name)
        if handler is None:
            raise KeyError(f"plugin {plugin_id!r} does not expose hook {hook_name!r}")
        try:
            result = dict(handler(dict(context)))
        except Exception as exc:  # pragma: no cover - exact exceptions are plugin-defined.
            message = f"{type(exc).__name__}: {exc}"
            self._events.append(
                PluginLifecycleEvent(
                    event_id=f"plg-{uuid4().hex}",
                    plugin_id=plugin_id,
                    hook_name=hook_name,
                    outcome="failed",
                    message=message,
                    recorded_at=utc_now_iso(),
                )
            )
            if descriptor.fail_behavior == "disable_on_error" or "disable" in descriptor.operator_controls:
                self.disable_plugin(plugin_id)
            raise RuntimeError(f"plugin hook failed in isolated execution: {message}") from exc
        self._events.append(
            PluginLifecycleEvent(
                event_id=f"plg-{uuid4().hex}",
                plugin_id=plugin_id,
                hook_name=hook_name,
                outcome="succeeded",
                message="hook completed",
                recorded_at=utc_now_iso(),
            )
        )
        return result

    def summary(self) -> dict[str, Any]:
        enabled = [plugin.plugin_id for plugin in self._plugins.values() if plugin.enabled]
        return {
            "plugin_count": len(self._plugins),
            "enabled_plugin_ids": sorted(enabled),
            "event_count": len(self._events),
            "isolation_modes": sorted({plugin.isolation_mode for plugin in self._plugins.values()}),
        }


class ScimProvisioningPlane:
    def __init__(self) -> None:
        self._schemas: dict[str, ScimSchema] = {}
        self._users: dict[str, ScimUser] = {}
        self._groups: dict[str, ScimGroup] = {}

    @property
    def schemas(self) -> Mapping[str, ScimSchema]:
        return dict(self._schemas)

    @property
    def users(self) -> Mapping[str, ScimUser]:
        return dict(self._users)

    @property
    def groups(self) -> Mapping[str, ScimGroup]:
        return dict(self._groups)

    def register_schema(self, schema_id: str, *, resource_kind: str, required_fields: Iterable[str]) -> ScimSchema:
        schema = ScimSchema(
            schema_id=schema_id,
            resource_kind=resource_kind,
            required_fields=tuple(sorted(set(required_fields))),
            registered_at=utc_now_iso(),
        )
        self._schemas[schema_id] = schema
        return schema

    def provision_user(
        self,
        user_id: str,
        *,
        tenant_id: str,
        user_name: str,
        attributes: Mapping[str, Any],
    ) -> ScimUser:
        schema = next((item for item in self._schemas.values() if item.resource_kind == "User"), None)
        if schema is None:
            raise RuntimeError("user schema must be registered before provisioning users")
        missing_fields = [field for field in schema.required_fields if field not in attributes]
        if missing_fields:
            raise ValueError(f"user payload missing required fields: {', '.join(missing_fields)}")
        user = ScimUser(
            user_id=user_id,
            tenant_id=tenant_id,
            user_name=user_name,
            attributes=dict(attributes),
            created_at=utc_now_iso(),
        )
        self._users[user_id] = user
        return user

    def patch_user(
        self,
        user_id: str,
        *,
        tenant_id: str,
        operations: Iterable[ScimPatchOperation],
    ) -> ScimUser:
        user = self._users[user_id]
        if user.tenant_id != tenant_id:
            raise PermissionError("user tenant mismatch")
        attributes = dict(user.attributes)
        active = user.active
        for operation in operations:
            if operation.op not in {"add", "replace"}:
                raise ValueError(f"unsupported SCIM patch operation {operation.op!r}")
            if operation.path == "active":
                active = bool(operation.value)
            else:
                attributes[operation.path] = operation.value
        updated = ScimUser(
            user_id=user.user_id,
            tenant_id=user.tenant_id,
            user_name=str(attributes.get("userName", user.user_name)),
            attributes=attributes,
            created_at=user.created_at,
            active=active,
        )
        self._users[user_id] = updated
        return updated

    def provision_group(
        self,
        group_id: str,
        *,
        tenant_id: str,
        display_name: str,
        members: Iterable[str] = (),
    ) -> ScimGroup:
        schema = next((item for item in self._schemas.values() if item.resource_kind == "Group"), None)
        if schema is None:
            raise RuntimeError("group schema must be registered before provisioning groups")
        group = ScimGroup(
            group_id=group_id,
            tenant_id=tenant_id,
            display_name=display_name,
            members=tuple(sorted(set(members))),
            created_at=utc_now_iso(),
        )
        self._groups[group_id] = group
        return group

    def add_group_member(self, group_id: str, *, tenant_id: str, member_id: str) -> ScimGroup:
        group = self._groups[group_id]
        if group.tenant_id != tenant_id:
            raise PermissionError("group tenant mismatch")
        updated = replace(group, members=tuple(sorted(set(group.members + (member_id,)))))
        self._groups[group_id] = updated
        return updated

    def tenant_snapshot(self, tenant_id: str) -> dict[str, Any]:
        users = [user for user in self._users.values() if user.tenant_id == tenant_id]
        groups = [group for group in self._groups.values() if group.tenant_id == tenant_id]
        return {
            "tenant_id": tenant_id,
            "schema_ids": sorted(self._schemas),
            "users": [
                {
                    "id": user.user_id,
                    "user_name": user.user_name,
                    "active": user.active,
                }
                for user in sorted(users, key=lambda item: item.user_id)
            ],
            "groups": [
                {
                    "id": group.group_id,
                    "display_name": group.display_name,
                    "member_count": len(group.members),
                }
                for group in sorted(groups, key=lambda item: item.group_id)
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "schema_count": len(self._schemas),
            "user_count": len(self._users),
            "group_count": len(self._groups),
        }


class EntitlementManager:
    def __init__(self) -> None:
        self._definitions: dict[str, EntitlementDefinition] = {}
        self._assignments: dict[str, EntitlementAssignment] = {}

    @property
    def definitions(self) -> Mapping[str, EntitlementDefinition]:
        return dict(self._definitions)

    @property
    def assignments(self) -> Mapping[str, EntitlementAssignment]:
        return dict(self._assignments)

    def define_entitlement(
        self,
        entitlement_id: str,
        *,
        tenant_id: str,
        name: str,
        owner: str,
        description: str,
    ) -> EntitlementDefinition:
        definition = EntitlementDefinition(
            entitlement_id=entitlement_id,
            tenant_id=tenant_id,
            name=name,
            owner=owner,
            description=description,
            created_at=utc_now_iso(),
        )
        self._definitions[entitlement_id] = definition
        return definition

    def assign_entitlement(
        self,
        entitlement_id: str,
        *,
        subject_id: str,
        justification: str,
        assigned_by: str,
        expires_at: str | None = None,
    ) -> EntitlementAssignment:
        definition = self._definitions[entitlement_id]
        assignment = EntitlementAssignment(
            assignment_id=f"ent-{uuid4().hex}",
            entitlement_id=entitlement_id,
            tenant_id=definition.tenant_id,
            subject_id=subject_id,
            justification=justification,
            assigned_by=assigned_by,
            created_at=utc_now_iso(),
            expires_at=expires_at,
        )
        self._assignments[assignment.assignment_id] = assignment
        return assignment

    def revoke_assignment(self, assignment_id: str, *, reason: str) -> EntitlementAssignment:
        assignment = self._assignments[assignment_id]
        updated = replace(assignment, active=False, revoked_reason=reason)
        self._assignments[assignment_id] = updated
        return updated

    def expire_assignments(self, *, reference_time: datetime | None = None) -> tuple[str, ...]:
        now = reference_time or utc_now()
        expired: list[str] = []
        for assignment_id, assignment in list(self._assignments.items()):
            if not assignment.active or assignment.expires_at is None:
                continue
            if datetime.fromisoformat(assignment.expires_at) <= now:
                self.revoke_assignment(assignment_id, reason="entitlement expired")
                expired.append(assignment_id)
        return tuple(sorted(expired))

    def tenant_inventory(self, tenant_id: str) -> dict[str, Any]:
        definitions = [definition for definition in self._definitions.values() if definition.tenant_id == tenant_id]
        assignments = [assignment for assignment in self._assignments.values() if assignment.tenant_id == tenant_id]
        return {
            "tenant_id": tenant_id,
            "entitlements": [
                {
                    "id": definition.entitlement_id,
                    "name": definition.name,
                    "owner": definition.owner,
                }
                for definition in sorted(definitions, key=lambda item: item.entitlement_id)
            ],
            "assignments": [
                {
                    "id": assignment.assignment_id,
                    "entitlement_id": assignment.entitlement_id,
                    "subject_id": assignment.subject_id,
                    "active": assignment.active,
                    "expires_at": assignment.expires_at,
                }
                for assignment in sorted(assignments, key=lambda item: item.assignment_id)
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "definition_count": len(self._definitions),
            "assignment_count": len(self._assignments),
            "active_assignment_count": sum(1 for assignment in self._assignments.values() if assignment.active),
        }


class AccessReviewWorkflow:
    def __init__(self, *, entitlement_manager: EntitlementManager) -> None:
        self._entitlement_manager = entitlement_manager
        self._campaigns: dict[str, AccessReviewCampaign] = {}
        self._items: dict[str, AccessReviewItem] = {}
        self._decisions: dict[str, AccessReviewDecision] = {}

    @property
    def campaigns(self) -> Mapping[str, AccessReviewCampaign]:
        return dict(self._campaigns)

    @property
    def items(self) -> Mapping[str, AccessReviewItem]:
        return dict(self._items)

    @property
    def decisions(self) -> Mapping[str, AccessReviewDecision]:
        return dict(self._decisions)

    def create_campaign(
        self,
        campaign_id: str,
        *,
        tenant_id: str,
        name: str,
        reviewer_ids: Iterable[str],
        assignment_ids: Iterable[str],
        due_in_days: int = 7,
    ) -> AccessReviewCampaign:
        reviewers = tuple(sorted(set(reviewer_ids)))
        if not reviewers:
            raise ValueError("access review campaign requires at least one reviewer")
        item_ids: list[str] = []
        due_at = (utc_now() + timedelta(days=due_in_days)).isoformat()
        assignments = [self._entitlement_manager.assignments[assignment_id] for assignment_id in assignment_ids]
        for index, assignment in enumerate(assignments):
            if assignment.tenant_id != tenant_id:
                raise PermissionError("assignment tenant mismatch in review campaign")
            reviewer_id = reviewers[index % len(reviewers)]
            item = AccessReviewItem(
                item_id=f"arw-{uuid4().hex}",
                assignment_id=assignment.assignment_id,
                subject_id=assignment.subject_id,
                entitlement_id=assignment.entitlement_id,
                reviewer_id=reviewer_id,
                status="pending",
                due_at=due_at,
            )
            self._items[item.item_id] = item
            item_ids.append(item.item_id)
        campaign = AccessReviewCampaign(
            campaign_id=campaign_id,
            tenant_id=tenant_id,
            name=name,
            reviewer_ids=reviewers,
            item_ids=tuple(item_ids),
            created_at=utc_now_iso(),
            due_at=due_at,
        )
        self._campaigns[campaign_id] = campaign
        return campaign

    def record_decision(
        self,
        campaign_id: str,
        *,
        item_id: str,
        reviewer_id: str,
        decision: str,
        reason: str,
    ) -> AccessReviewDecision:
        if decision not in {"approve", "revoke"}:
            raise ValueError("access review decision must be approve or revoke")
        campaign = self._campaigns[campaign_id]
        item = self._items[item_id]
        if item.item_id not in campaign.item_ids:
            raise KeyError("review item does not belong to campaign")
        if item.reviewer_id != reviewer_id:
            raise PermissionError("reviewer mismatch")
        updated_status = "approved" if decision == "approve" else "revoked"
        self._items[item_id] = replace(item, status=updated_status)
        if decision == "revoke":
            self._entitlement_manager.revoke_assignment(item.assignment_id, reason=reason)
        review_decision = AccessReviewDecision(
            decision_id=f"ard-{uuid4().hex}",
            item_id=item_id,
            reviewer_id=reviewer_id,
            decision=decision,
            reason=reason,
            recorded_at=utc_now_iso(),
        )
        self._decisions[review_decision.decision_id] = review_decision
        return review_decision

    def escalate_overdue(self, *, reference_time: datetime | None = None) -> tuple[str, ...]:
        now = reference_time or utc_now()
        escalated_ids: list[str] = []
        for item_id, item in list(self._items.items()):
            if item.status != "pending":
                continue
            if datetime.fromisoformat(item.due_at) >= now:
                continue
            self._items[item_id] = replace(item, status="escalated", escalation_count=item.escalation_count + 1)
            escalated_ids.append(item_id)
        return tuple(sorted(escalated_ids))

    def close_campaign(self, campaign_id: str) -> AccessReviewCampaign:
        campaign = self._campaigns[campaign_id]
        open_items = [self._items[item_id] for item_id in campaign.item_ids if self._items[item_id].status == "pending"]
        if open_items:
            raise PermissionError("cannot close campaign with pending review items")
        updated = replace(campaign, closed_at=utc_now_iso(), status="closed")
        self._campaigns[campaign_id] = updated
        return updated

    def summary(self) -> dict[str, Any]:
        return {
            "campaign_count": len(self._campaigns),
            "open_campaign_count": sum(1 for campaign in self._campaigns.values() if campaign.status == "open"),
            "decision_count": len(self._decisions),
            "escalated_item_count": sum(1 for item in self._items.values() if item.status == "escalated"),
        }


def build_provisioning_governance_ecosystem_delivery_summary(
    *,
    sdk_catalog: SDKEcosystemCatalog,
    plugin_registry: PluginRuntimeRegistry,
    scim_plane: ScimProvisioningPlane,
    entitlement_manager: EntitlementManager,
    access_reviews: AccessReviewWorkflow,
    runtime_version: str,
    expected_contracts: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "sdk_ecosystem": {
            **sdk_catalog.summary(),
            "alignment": sdk_catalog.build_alignment_report(
                runtime_version=runtime_version,
                expected_contracts=expected_contracts,
            ),
        },
        "extensibility": plugin_registry.summary(),
        "scim_provisioning": scim_plane.summary(),
        "entitlement_management": entitlement_manager.summary(),
        "access_review_workflows": access_reviews.summary(),
    }


build_phase5_delivery_summary = build_provisioning_governance_ecosystem_delivery_summary


__all__ = [
    "AccessReviewCampaign",
    "AccessReviewDecision",
    "AccessReviewItem",
    "AccessReviewWorkflow",
    "EntitlementAssignment",
    "EntitlementDefinition",
    "EntitlementManager",
    "PluginDescriptor",
    "PluginLifecycleEvent",
    "PluginRuntimeRegistry",
    "SDKPackage",
    "SDKEcosystemCatalog",
    "ScimGroup",
    "ScimPatchOperation",
    "ScimProvisioningPlane",
    "ScimSchema",
    "ScimUser",
    "build_provisioning_governance_ecosystem_delivery_summary",
    "build_phase5_delivery_summary",
]
