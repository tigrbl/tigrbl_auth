"""Authorization governance-extension public surface."""

from __future__ import annotations
# ruff: noqa: F403,F405

from dataclasses import replace
from datetime import datetime, timedelta
from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now, utc_now_iso
from tigrbl_identity_contracts.governance import *


from .governance_extension import PluginRuntimeRegistry, SDKEcosystemCatalog
from .governance_provisioning import ScimProvisioningPlane


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

    def revoke_assignment(
        self, assignment_id: str, *, reason: str
    ) -> EntitlementAssignment:
        assignment = self._assignments[assignment_id]
        updated = replace(assignment, active=False, revoked_reason=reason)
        self._assignments[assignment_id] = updated
        return updated

    def expire_assignments(
        self, *, reference_time: datetime | None = None
    ) -> tuple[str, ...]:
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
        definitions = [
            definition
            for definition in self._definitions.values()
            if definition.tenant_id == tenant_id
        ]
        assignments = [
            assignment
            for assignment in self._assignments.values()
            if assignment.tenant_id == tenant_id
        ]
        return {
            "tenant_id": tenant_id,
            "entitlements": [
                {
                    "id": definition.entitlement_id,
                    "name": definition.name,
                    "owner": definition.owner,
                }
                for definition in sorted(
                    definitions, key=lambda item: item.entitlement_id
                )
            ],
            "assignments": [
                {
                    "id": assignment.assignment_id,
                    "entitlement_id": assignment.entitlement_id,
                    "subject_id": assignment.subject_id,
                    "active": assignment.active,
                    "expires_at": assignment.expires_at,
                }
                for assignment in sorted(
                    assignments, key=lambda item: item.assignment_id
                )
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "definition_count": len(self._definitions),
            "assignment_count": len(self._assignments),
            "active_assignment_count": sum(
                1 for assignment in self._assignments.values() if assignment.active
            ),
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
        assignments = [
            self._entitlement_manager.assignments[assignment_id]
            for assignment_id in assignment_ids
        ]
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
            self._entitlement_manager.revoke_assignment(
                item.assignment_id, reason=reason
            )
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

    def escalate_overdue(
        self, *, reference_time: datetime | None = None
    ) -> tuple[str, ...]:
        now = reference_time or utc_now()
        escalated_ids: list[str] = []
        for item_id, item in list(self._items.items()):
            if item.status != "pending":
                continue
            if datetime.fromisoformat(item.due_at) >= now:
                continue
            self._items[item_id] = replace(
                item, status="escalated", escalation_count=item.escalation_count + 1
            )
            escalated_ids.append(item_id)
        return tuple(sorted(escalated_ids))

    def close_campaign(self, campaign_id: str) -> AccessReviewCampaign:
        campaign = self._campaigns[campaign_id]
        open_items = [
            self._items[item_id]
            for item_id in campaign.item_ids
            if self._items[item_id].status == "pending"
        ]
        if open_items:
            raise PermissionError("cannot close campaign with pending review items")
        updated = replace(campaign, closed_at=utc_now_iso(), status="closed")
        self._campaigns[campaign_id] = updated
        return updated

    def summary(self) -> dict[str, Any]:
        return {
            "campaign_count": len(self._campaigns),
            "open_campaign_count": sum(
                1 for campaign in self._campaigns.values() if campaign.status == "open"
            ),
            "decision_count": len(self._decisions),
            "escalated_item_count": sum(
                1 for item in self._items.values() if item.status == "escalated"
            ),
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
