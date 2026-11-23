"""Default policy rule and condition evaluators."""

from __future__ import annotations

from tba_bases_authorization_policy import ConditionEvaluatorBase, RuleEvaluatorBase
from tba_contracts_identity.policy import DynamicCondition, PolicyDecision, PolicyRequest, PolicyRule


class DefaultConditionEvaluator(ConditionEvaluatorBase):
    def evaluate_condition(self, condition: DynamicCondition, request: PolicyRequest, /) -> bool:
        return condition.evaluate(request.attributes)


class DefaultRuleEvaluator(RuleEvaluatorBase):
    def evaluate_rule(self, rule: PolicyRule, request: PolicyRequest, /) -> PolicyDecision:
        policy_id = rule.policy_id or rule.kind.value
        effect = str(getattr(rule.effect, "value", rule.effect))
        matched = (policy_id,)
        if effect == "deny":
            return PolicyDecision(False, f"denied by {rule.kind.value} policy", matched)
        return PolicyDecision(True, f"allowed by {rule.kind.value} policy", matched)


__all__ = ["DefaultConditionEvaluator", "DefaultRuleEvaluator"]
