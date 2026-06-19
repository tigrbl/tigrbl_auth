from __future__ import annotations

from .models import *
from .models import _utc_now, _utc_now_iso
from .sdk_plugins import *
from .provisioning import *

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
        due_at = (_utc_now() + timedelta(days=due_in_days)).isoformat()
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
            created_at=_utc_now_iso(),
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
            recorded_at=_utc_now_iso(),
        )
        self._decisions[review_decision.decision_id] = review_decision
        return review_decision

    def escalate_overdue(self, *, reference_time: datetime | None = None) -> tuple[str, ...]:
        now = reference_time or _utc_now()
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
        updated = replace(campaign, closed_at=_utc_now_iso(), status="closed")
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
    "GovernanceExtensionBoundaryFeature",
    "PROVISIONING_GOVERNANCE_ECOSYSTEM_FEATURES",
    "PHASE5_GOVERNANCE_EXTENSION_FEATURES",
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
    "provisioning_governance_ecosystem_boundary_integrity",
    "provisioning_governance_ecosystem_boundary_manifest",
    "phase5_governance_extension_boundary_integrity",
    "phase5_governance_extension_boundary_manifest",
]
