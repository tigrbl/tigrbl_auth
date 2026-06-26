"""Concrete policy combining algorithms."""

from __future__ import annotations

from tigrbl_identity_contracts.policy import CombiningAlgorithmKind, PolicyCombineRequest, PolicyDecision


class DefaultPolicyCombiner:
    def combine(self, request: PolicyCombineRequest, /) -> PolicyDecision:
        if not request.decisions:
            return PolicyDecision(False, "no policy decision", ())
        if request.algorithm is CombiningAlgorithmKind.FIRST_APPLICABLE:
            return request.decisions[0]
        if request.algorithm is CombiningAlgorithmKind.PERMIT_OVERRIDES:
            for decision in request.decisions:
                if decision.allowed:
                    return decision
            return request.decisions[0]
        if request.algorithm is CombiningAlgorithmKind.ONLY_ONE_APPLICABLE:
            applicable = [decision for decision in request.decisions if decision.matched]
            if len(applicable) == 1:
                return applicable[0]
            return PolicyDecision(False, "only-one-applicable policy count mismatch", ())
        for decision in request.decisions:
            if not decision.allowed:
                return decision
        return request.decisions[0]


__all__ = ["DefaultPolicyCombiner"]
