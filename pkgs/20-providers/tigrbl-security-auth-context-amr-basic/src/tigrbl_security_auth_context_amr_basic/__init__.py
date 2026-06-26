from __future__ import annotations

from tigrbl_security_trust_contracts import AmrEvaluationRequest, AmrEvaluationResult, CapabilityMap
from tigrbl_security_trust_domain_bases import AmrEvaluatorBase


class BasicAmrEvaluator(AmrEvaluatorBase):
    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"evaluate_amr": ("basic",)}, features=("amr",))

    def evaluate_amr(self, request: AmrEvaluationRequest) -> AmrEvaluationResult:
        required = {str(getattr(value, "value", value)) for value in request.required}
        achieved = {str(getattr(value, "value", value)) for value in request.achieved}
        missing = tuple(sorted(required - achieved))
        return AmrEvaluationResult(not missing, request.achieved, missing, None if not missing else "amr_not_satisfied")


__all__ = ["BasicAmrEvaluator"]
