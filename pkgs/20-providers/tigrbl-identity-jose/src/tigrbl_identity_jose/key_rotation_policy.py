from __future__ import annotations

from dataclasses import replace
from typing import Callable, Iterable, Mapping

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.normalization import normal_tuple
from tigrbl_identity_concrete.key_rotation_policy import (
    EffectiveKeyRotationPolicy,
    KeyRotationPolicyVersion,
)
from tigrbl_identity_contracts.evidence.key_rotation import (
    KeyRotationAuditEvidence as _KeyRotationAuditEvidence,
)


class KeyRotationPolicyOverlapError(RuntimeError):
    pass


class KeyRotationPolicyGovernance:
    """Governance-plane store for immutable key rotation policy versions."""

    def __init__(self) -> None:
        self._versions: dict[tuple[str, str], KeyRotationPolicyVersion] = {}
        self._published: dict[tuple[str, str, str, str, str, str], tuple[str, str]] = {}

    @property
    def versions(self) -> Mapping[tuple[str, str], KeyRotationPolicyVersion]:
        return dict(self._versions)

    def create_policy_version(
        self,
        policy_id: str,
        version_id: str,
        *,
        tenant_id: str,
        issuer: str,
        profile: str,
        key_class: str,
        key_use: str,
        algorithm: str,
        cadence_days: int,
        max_key_age_days: int,
        overlap_seconds: int,
        retirement_seconds: int,
        emergency_triggers: Iterable[str],
        created_by: str,
        reason: str,
        approval_required: bool = True,
        jwks_publish_required: bool = True,
    ) -> KeyRotationPolicyVersion:
        if (policy_id, version_id) in self._versions:
            raise ValueError("policy version already exists")
        if cadence_days <= 0 or max_key_age_days <= 0:
            raise ValueError("rotation cadence and max key age must be positive")
        if max_key_age_days < cadence_days:
            raise ValueError("max key age must be at least the rotation cadence")
        if overlap_seconds < 0 or retirement_seconds < 0:
            raise ValueError("overlap and retirement windows must be non-negative")
        if not policy_id or not version_id or not tenant_id or not issuer:
            raise ValueError("policy id, version id, tenant, and issuer are required")
        policy = KeyRotationPolicyVersion(
            policy_id=policy_id,
            version_id=version_id,
            tenant_id=tenant_id,
            issuer=issuer,
            profile=profile,
            key_class=key_class,
            key_use=key_use,
            algorithm=algorithm,
            cadence_days=cadence_days,
            max_key_age_days=max_key_age_days,
            overlap_seconds=overlap_seconds,
            retirement_seconds=retirement_seconds,
            emergency_triggers=normal_tuple(emergency_triggers),
            approval_required=approval_required,
            jwks_publish_required=jwks_publish_required,
            created_by=created_by,
            reason=reason,
            created_at=utc_now_iso(),
        )
        self._versions[(policy_id, version_id)] = policy
        return policy

    def approve_policy_version(self, policy_id: str, version_id: str, *, actor: str) -> KeyRotationPolicyVersion:
        policy = self._get(policy_id, version_id)
        if policy.status not in {"draft", "approved"}:
            raise ValueError("only draft policy versions can be approved")
        approved = replace(policy, status="approved", approved_by=actor, approved_at=utc_now_iso())
        self._versions[(policy_id, version_id)] = approved
        return approved

    def publish_policy_version(self, policy_id: str, version_id: str, *, actor: str) -> KeyRotationPolicyVersion:
        policy = self._get(policy_id, version_id)
        if policy.approval_required and policy.status != "approved":
            raise PermissionError("policy version must be approved before publication")
        scope = self._scope_key(policy)
        current_ref = self._published.get(scope)
        supersedes = current_ref[1] if current_ref else None
        if current_ref:
            current = self._get(*current_ref)
            self._versions[current_ref] = replace(current, status="retired")
        published = replace(
            policy,
            status="published",
            approved_by=policy.approved_by or actor,
            approved_at=policy.approved_at or utc_now_iso(),
            published_at=utc_now_iso(),
            supersedes=supersedes,
        )
        self._versions[(policy_id, version_id)] = published
        self._published[scope] = (policy_id, version_id)
        return published

    def effective_policy(
        self,
        *,
        tenant_id: str,
        issuer: str,
        profile: str,
        key_class: str,
        key_use: str,
        algorithm: str,
    ) -> EffectiveKeyRotationPolicy | None:
        ref = self._published.get((tenant_id, issuer, profile, key_class, key_use, algorithm))
        if ref is None:
            return None
        policy = self._get(*ref)
        return EffectiveKeyRotationPolicy(
            policy_id=policy.policy_id,
            version_id=policy.version_id,
            tenant_id=policy.tenant_id,
            issuer=policy.issuer,
            profile=policy.profile,
            key_class=policy.key_class,
            key_use=policy.key_use,
            algorithm=policy.algorithm,
            cadence_days=policy.cadence_days,
            max_key_age_days=policy.max_key_age_days,
            overlap_seconds=policy.overlap_seconds,
            retirement_seconds=policy.retirement_seconds,
            emergency_triggers=policy.emergency_triggers,
            jwks_publish_required=policy.jwks_publish_required,
        )

    def require_effective_policy(self, **scope: str) -> EffectiveKeyRotationPolicy:
        policy = self.effective_policy(**scope)
        if policy is None:
            raise PermissionError("key rotation requires an effective governance policy")
        return policy

    def assert_administration_does_not_own_policy(self, administration: object) -> None:
        forbidden = {"create_policy_version", "approve_policy_version", "publish_policy_version", "policy_store"}
        overlap = sorted(name for name in forbidden if hasattr(administration, name))
        if overlap:
            raise KeyRotationPolicyOverlapError("administration plane exposes governance policy authority")

    def _get(self, policy_id: str, version_id: str) -> KeyRotationPolicyVersion:
        try:
            return self._versions[(policy_id, version_id)]
        except KeyError as exc:
            raise KeyError("unknown key rotation policy version") from exc

    @staticmethod
    def _scope_key(policy: KeyRotationPolicyVersion) -> tuple[str, str, str, str, str, str]:
        return (policy.tenant_id, policy.issuer, policy.profile, policy.key_class, policy.key_use, policy.algorithm)


AuthorizationDecision = Callable[[Mapping[str, str]], str]


class KeyRotationAdministration:
    """Administration-plane consumer for effective policy projections."""

    def __init__(
        self,
        governance: KeyRotationPolicyGovernance,
        *,
        authorize: AuthorizationDecision | None = None,
    ) -> None:
        self._governance = governance
        self._authorize = authorize or (lambda request: "decision:allow")
        self._audit_records: list[_KeyRotationAuditEvidence] = []

    @property
    def audit_records(self) -> tuple[_KeyRotationAuditEvidence, ...]:
        return tuple(self._audit_records)

    def view_effective_policy(self, **scope: str) -> EffectiveKeyRotationPolicy:
        return self._governance.require_effective_policy(**scope)

    def execute_rotation(
        self,
        *,
        tenant_id: str,
        issuer: str,
        profile: str,
        key_class: str,
        key_use: str,
        algorithm: str,
        actor: str,
        old_kid: str,
        new_kid: str,
        jwks_published: bool,
        retired: bool,
        reason: str,
    ) -> _KeyRotationAuditEvidence:
        policy = self._governance.require_effective_policy(
            tenant_id=tenant_id,
            issuer=issuer,
            profile=profile,
            key_class=key_class,
            key_use=key_use,
            algorithm=algorithm,
        )
        decision = self._authorize(
            {
                "actor": actor,
                "action": "key.rotate",
                "tenant_id": tenant_id,
                "issuer": issuer,
                "policy_id": policy.policy_id,
                "policy_version_id": policy.version_id,
            }
        )
        if not decision:
            raise PermissionError("authorization decision reference is required")
        if policy.jwks_publish_required and not jwks_published:
            raise PermissionError("rotation policy requires JWKS publication")
        if not retired:
            raise PermissionError("rotation policy requires old key retirement evidence")
        audit = _KeyRotationAuditEvidence(
            audit_id=f"kra:{policy.policy_id}:{policy.version_id}:{new_kid}",
            tenant_id=tenant_id,
            issuer=issuer,
            profile=profile,
            policy_id=policy.policy_id,
            policy_version_id=policy.version_id,
            actor=actor,
            old_kid=old_kid,
            new_kid=new_kid,
            authorization_decision_ref=decision,
            jwks_published=jwks_published,
            retired=retired,
            reason=reason,
            recorded_at=utc_now_iso(),
        )
        self._audit_records.append(audit)
        return audit


__all__ = [
    "EffectiveKeyRotationPolicy",
    "KeyRotationAdministration",
    "KeyRotationPolicyGovernance",
    "KeyRotationPolicyOverlapError",
    "KeyRotationPolicyVersion",
]
