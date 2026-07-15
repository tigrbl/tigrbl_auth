"""Composable protocol-neutral policy decision-point capability."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeAlias

from tigrbl_capability import Capability
from tigrbl_identity_contracts.capabilities import (
    CapabilityDefinition,
    CapabilityOperation,
    CapabilityState,
)
from tigrbl_identity_contracts.policy import (
    PolicyEntitySearchRequest,
    PolicyEntitySearchResult,
    PolicyEvaluationRequest,
    PolicyEvaluationResult,
    PolicyServiceCapabilities,
)

EvaluationTarget: TypeAlias = Callable[
    [PolicyEvaluationRequest], PolicyEvaluationResult
]
EntitySearchTarget: TypeAlias = Callable[
    [PolicyEntitySearchRequest], PolicyEntitySearchResult
]
DescriptionTarget: TypeAlias = Callable[[], PolicyServiceCapabilities]


class PolicyEvaluationCapability(Capability):
    """Expose one normalized policy decision point through reportable operations."""

    def __init__(
        self,
        evaluate: EvaluationTarget | None,
        *,
        search_entities: EntitySearchTarget | None = None,
        describe: DescriptionTarget | None = None,
    ) -> None:
        self._evaluate = evaluate
        self._search_entities = search_entities
        self._describe = describe
        super().__init__(
            CapabilityDefinition("policy.evaluation", "1.0"),
            operations={
                "evaluate": CapabilityOperation(
                    target=self.evaluate if evaluate is not None else None,
                    delegated=True,
                ),
                "evaluate_many": CapabilityOperation(
                    target=self.evaluate_many if evaluate is not None else None,
                    required=False,
                    delegated=True,
                ),
                "search_entities": CapabilityOperation(
                    target=(
                        self.search_entities if search_entities is not None else None
                    ),
                    required=False,
                    delegated=True,
                ),
                "describe": CapabilityOperation(
                    target=self.describe if describe is not None else None,
                    required=False,
                    delegated=True,
                ),
            },
            state=lambda: CapabilityState(
                ready=self._evaluate is not None,
                status="ready" if self._evaluate is not None else "unbound",
                details={
                    "search_bound": self._search_entities is not None,
                    "description_bound": self._describe is not None,
                },
            ),
        )

    def evaluate(self, request: PolicyEvaluationRequest) -> PolicyEvaluationResult:
        if not isinstance(request, PolicyEvaluationRequest):
            raise TypeError("request must be a PolicyEvaluationRequest")
        if self._evaluate is None:  # construction rejects this path
            raise NotImplementedError("policy evaluation target is not bound")
        result = self._evaluate(request)
        if not isinstance(result, PolicyEvaluationResult):
            raise TypeError("policy evaluator must return PolicyEvaluationResult")
        return result

    def evaluate_many(
        self, requests: Sequence[PolicyEvaluationRequest]
    ) -> tuple[PolicyEvaluationResult, ...]:
        return tuple(self.evaluate(request) for request in requests)

    def search_entities(
        self, request: PolicyEntitySearchRequest
    ) -> PolicyEntitySearchResult:
        if not isinstance(request, PolicyEntitySearchRequest):
            raise TypeError("request must be a PolicyEntitySearchRequest")
        if self._search_entities is None:
            raise NotImplementedError("policy entity-search target is not bound")
        result = self._search_entities(request)
        if not isinstance(result, PolicyEntitySearchResult):
            raise TypeError("policy search target must return PolicyEntitySearchResult")
        return result

    def describe(self) -> PolicyServiceCapabilities:
        if self._describe is None:
            raise NotImplementedError("policy description target is not bound")
        result = self._describe()
        if not isinstance(result, PolicyServiceCapabilities):
            raise TypeError("policy description target must return capabilities")
        return result


__all__ = [
    "DescriptionTarget",
    "EntitySearchTarget",
    "EvaluationTarget",
    "PolicyEvaluationCapability",
]
