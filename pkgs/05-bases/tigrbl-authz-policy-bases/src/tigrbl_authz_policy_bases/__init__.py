"""Base classes for concrete authorization policy implementations."""

from abc import ABC
from typing import Any, Mapping
from tigrbl_identity_contracts.authorization_scopes import (
    ScopeMatcherPort,
    ScopeMatchRequest,
    ScopeMatchResult,
)


class ScopeMatcherBase(ScopeMatcherPort, ABC):
    def match(self, request: ScopeMatchRequest, /) -> ScopeMatchResult:
        raise NotImplementedError


from tigrbl_identity_contracts.policy import (
    AdviceHandlerPort,
    Advice,
    AttributeDesignator,
    AttributeResolverPort,
    AttributeSelector,
    AttributeSelectorPort,
    ConditionEvaluatorPort,
    DynamicCondition,
    Obligation,
    ObligationHandlerPort,
    PolicyCombineRequest,
    PolicyCombinerPort,
    PolicyDecision,
    PolicyRequest,
    PolicyRule,
    RuleEvaluatorPort,
)


class PolicyRuleBase(PolicyRule):
    """Base for concrete policy-rule dataclasses."""


class AttributeResolverBase(AttributeResolverPort, ABC):
    def resolve(
        self, designator: AttributeDesignator, request: PolicyRequest, /
    ) -> Any:
        raise NotImplementedError


class AttributeSelectorBase(AttributeSelectorPort, ABC):
    def select(self, selector: AttributeSelector, values: Mapping[str, Any], /) -> Any:
        raise NotImplementedError


class PolicyCombinerBase(PolicyCombinerPort, ABC):
    def combine(self, request: PolicyCombineRequest, /) -> PolicyDecision:
        raise NotImplementedError


class ConditionEvaluatorBase(ConditionEvaluatorPort, ABC):
    def evaluate_condition(
        self, condition: DynamicCondition, request: PolicyRequest, /
    ) -> bool:
        raise NotImplementedError


class RuleEvaluatorBase(RuleEvaluatorPort, ABC):
    def evaluate_rule(
        self, rule: PolicyRule, request: PolicyRequest, /
    ) -> PolicyDecision:
        raise NotImplementedError


class ObligationHandlerBase(ObligationHandlerPort, ABC):
    async def handle_obligation(
        self, obligation: Obligation, decision: PolicyDecision, /
    ) -> None:
        raise NotImplementedError


class AdviceHandlerBase(AdviceHandlerPort, ABC):
    async def handle_advice(self, advice: Advice, decision: PolicyDecision, /) -> None:
        raise NotImplementedError


__all__ = [
    "AdviceHandlerBase",
    "AttributeResolverBase",
    "AttributeSelectorBase",
    "ConditionEvaluatorBase",
    "ObligationHandlerBase",
    "PolicyCombinerBase",
    "PolicyRuleBase",
    "RuleEvaluatorBase",
    "ScopeMatcherBase",
]
