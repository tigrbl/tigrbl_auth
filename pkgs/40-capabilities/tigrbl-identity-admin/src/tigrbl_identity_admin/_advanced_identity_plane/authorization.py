from __future__ import annotations

from collections import deque
from dataclasses import replace
from typing import Any, Iterable, Mapping
from uuid import uuid4

from tigrbl_identity_core.clock import utc_now_iso
from tigrbl_identity_core.entity_keys import normalize_entity

from .models import (
    AccessDecisionRequest,
    AccessDecisionResponse,
    GraphDecision,
    PolicyDefinition,
    PolicyVersion,
    RelationshipDefinition,
    RelationshipTuple,
)


class RelationshipGraph:
    def __init__(self) -> None:
        self._definitions: dict[tuple[str, str], RelationshipDefinition] = {}
        self._tuples: list[RelationshipTuple] = []

    @property
    def definitions(self) -> Mapping[tuple[str, str], RelationshipDefinition]:
        return dict(self._definitions)

    @property
    def tuples(self) -> tuple[RelationshipTuple, ...]:
        return tuple(self._tuples)

    def define_relation(
        self,
        *,
        resource_type: str,
        relation: str,
        subject_types: Iterable[str],
    ) -> RelationshipDefinition:
        key = (resource_type, relation)
        prior = self._definitions.get(key)
        definition = RelationshipDefinition(
            resource_type=resource_type,
            relation=relation,
            subject_types=tuple(sorted(set(subject_types))),
            version=1 if prior is None else prior.version + 1,
        )
        self._definitions[key] = definition
        return definition

    def add_tuple(
        self,
        *,
        resource_type: str,
        resource_id: str,
        relation: str,
        subject_type: str,
        subject_id: str,
        tenant_id: str,
    ) -> RelationshipTuple:
        definition = self._definitions[(resource_type, relation)]
        if subject_type not in definition.subject_types:
            raise ValueError("relationship subject type is not allowed by schema")
        relationship = RelationshipTuple(
            resource=normalize_entity(resource_type, resource_id),
            relation=relation,
            subject=normalize_entity(subject_type, subject_id),
            tenant_id=tenant_id,
        )
        self._tuples.append(relationship)
        return relationship

    def check_access(
        self,
        *,
        tenant_id: str,
        subject: str,
        relation: str,
        resource: str,
        max_depth: int = 5,
    ) -> GraphDecision:
        queue: deque[tuple[str, int, tuple[str, ...]]] = deque(
            (tuple_.subject, 1, (f"{tuple_.resource}#{tuple_.relation}@{tuple_.subject}",))
            for tuple_ in self._tuples
            if tuple_.tenant_id == tenant_id and tuple_.resource == resource and tuple_.relation == relation
        )
        seen: set[tuple[str, int]] = set()
        while queue:
            candidate_subject, depth, explanation = queue.popleft()
            if candidate_subject == subject:
                return GraphDecision(True, "relationship tuple grants access", explanation)
            if depth >= max_depth or (candidate_subject, depth) in seen:
                continue
            seen.add((candidate_subject, depth))
            for tuple_ in self._tuples:
                if tuple_.tenant_id != tenant_id:
                    continue
                if tuple_.resource == candidate_subject and tuple_.relation == "member":
                    queue.append(
                        (
                            tuple_.subject,
                            depth + 1,
                            explanation + (f"{tuple_.resource}#{tuple_.relation}@{tuple_.subject}",),
                        )
                    )
        return GraphDecision(False, "no bounded relationship path grants access", ())


class PolicyRegistry:
    def __init__(self, *, relationship_graph: RelationshipGraph) -> None:
        self.relationship_graph = relationship_graph
        self._definitions: dict[str, PolicyDefinition] = {}
        self._versions: dict[str, PolicyVersion] = {}
        self._versions_by_policy: dict[str, list[str]] = {}
        self._active_version_by_policy: dict[str, str] = {}

    @property
    def definitions(self) -> Mapping[str, PolicyDefinition]:
        return dict(self._definitions)

    @property
    def versions(self) -> Mapping[str, PolicyVersion]:
        return dict(self._versions)

    def create_policy(self, *, tenant_id: str, name: str, language: str = "tigrbl-conditions/v1") -> PolicyDefinition:
        if language != "tigrbl-conditions/v1":
            raise ValueError("unsupported policy language")
        definition = PolicyDefinition(
            policy_id=f"policy-{uuid4().hex}",
            name=name,
            tenant_id=tenant_id,
            language=language,
            created_at=utc_now_iso(),
        )
        self._definitions[definition.policy_id] = definition
        self._versions_by_policy[definition.policy_id] = []
        return definition

    def publish_version(self, *, policy_id: str, source: str, promote: bool = True) -> PolicyVersion:
        definition = self._definitions[policy_id]
        relation, context_equals = self._parse_policy_source(source)
        current_ids = self._versions_by_policy[policy_id]
        version = PolicyVersion(
            version_id=f"policy-version-{uuid4().hex}",
            policy_id=policy_id,
            version_number=len(current_ids) + 1,
            source=source,
            created_at=utc_now_iso(),
            relation=relation,
            context_equals=context_equals,
            promoted=False,
        )
        self._versions[version.version_id] = version
        current_ids.append(version.version_id)
        if promote:
            self.promote_version(version.version_id)
        return self._versions[version.version_id]

    def promote_version(self, version_id: str) -> PolicyVersion:
        version = self._versions[version_id]
        policy_id = version.policy_id
        for prior_id in self._versions_by_policy[policy_id]:
            prior = self._versions[prior_id]
            self._versions[prior_id] = replace(prior, promoted=False)
        updated = replace(version, promoted=True)
        self._versions[version_id] = updated
        self._active_version_by_policy[policy_id] = version_id
        return updated

    def rollback_policy(self, *, policy_id: str, version_id: str) -> PolicyVersion:
        if version_id not in self._versions_by_policy[policy_id]:
            raise KeyError("policy version does not belong to policy")
        return self.promote_version(version_id)

    def check_compatibility(self, *, left_version_id: str, right_version_id: str) -> bool:
        left = self._versions[left_version_id]
        right = self._versions[right_version_id]
        return left.relation == right.relation and set(left.context_equals).issubset(set(right.context_equals))

    def access_decision(self, request: AccessDecisionRequest) -> AccessDecisionResponse:
        policy_version = self._resolve_version(request)
        graph_decision = self.relationship_graph.check_access(
            tenant_id=request.tenant_id,
            subject=request.subject,
            relation=policy_version.relation,
            resource=request.resource,
        )
        if not graph_decision.allowed:
            return AccessDecisionResponse(
                allowed=False,
                reason=graph_decision.reason,
                correlation_id=request.correlation_id,
                policy_version_id=policy_version.version_id,
                explanation=graph_decision.explanation,
                idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
            )
        missing_context = [
            key for key, _value in policy_version.context_equals
            if key not in request.context
        ]
        if missing_context:
            return AccessDecisionResponse(
                allowed=False,
                reason="required policy context is missing",
                correlation_id=request.correlation_id,
                policy_version_id=policy_version.version_id,
                explanation=tuple(missing_context),
                idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
            )
        mismatched_context = [
            key for key, expected_value in policy_version.context_equals
            if request.context[key] != expected_value
        ]
        if mismatched_context:
            return AccessDecisionResponse(
                allowed=False,
                reason="policy context does not satisfy required values",
                correlation_id=request.correlation_id,
                policy_version_id=policy_version.version_id,
                explanation=tuple(mismatched_context),
                idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
            )
        return AccessDecisionResponse(
            allowed=True,
            reason="policy version and relationship graph grant access",
            correlation_id=request.correlation_id,
            policy_version_id=policy_version.version_id,
            explanation=graph_decision.explanation + tuple(
                f"context.{key}={request.context[key]!r}" for key, _value in policy_version.context_equals
            ),
            idempotency_key=f"{request.correlation_id}:{request.subject}:{request.action}:{request.resource}",
        )

    def _resolve_version(self, request: AccessDecisionRequest) -> PolicyVersion:
        if request.policy_version_id is not None:
            return self._versions[request.policy_version_id]
        for policy_id, definition in self._definitions.items():
            if definition.tenant_id == request.tenant_id and definition.name == request.action:
                active_version_id = self._active_version_by_policy[policy_id]
                return self._versions[active_version_id]
        raise KeyError(f"no active policy found for action {request.action!r}")

    def _parse_policy_source(self, source: str) -> tuple[str, tuple[tuple[str, Any], ...]]:
        normalized = " ".join(source.strip().split())
        if not normalized.startswith("allow if relation "):
            raise ValueError("policy must start with 'allow if relation <name>'")
        if any(token in normalized for token in ("import ", "exec", "lambda", ";", "__")):
            raise ValueError("unsafe construct detected in policy source")
        fragments = [fragment.strip() for fragment in normalized.split(" and ")]
        relation_fragment = fragments[0]
        relation = relation_fragment.removeprefix("allow if relation ").strip()
        if not relation:
            raise ValueError("policy relation is required")
        context_equals: list[tuple[str, Any]] = []
        for fragment in fragments[1:]:
            if not fragment.startswith("context.") or "==" not in fragment:
                raise ValueError("policy conditions must be 'context.<field> == <value>'")
            field, raw_value = [part.strip() for part in fragment.split("==", 1)]
            field = field.replace("context.", "").strip()
            if not field:
                raise ValueError("policy context field is required")
            if raw_value in {"true", "false"}:
                parsed_value: Any = raw_value == "true"
            elif raw_value.startswith('"') and raw_value.endswith('"'):
                parsed_value = raw_value[1:-1]
            else:
                try:
                    parsed_value = int(raw_value)
                except ValueError:
                    parsed_value = raw_value
            context_equals.append((field, parsed_value))
        return relation, tuple(context_equals)
