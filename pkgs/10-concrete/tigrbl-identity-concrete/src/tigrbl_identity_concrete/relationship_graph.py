from __future__ import annotations

from collections import deque
from typing import Iterable, Mapping

from tigrbl_identity_contracts.adaptive_access import (
    GraphDecision,
    RelationshipDefinition,
    RelationshipTuple,
)
from tigrbl_identity_core.entity_keys import normalize_entity


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


__all__ = ["RelationshipGraph"]
