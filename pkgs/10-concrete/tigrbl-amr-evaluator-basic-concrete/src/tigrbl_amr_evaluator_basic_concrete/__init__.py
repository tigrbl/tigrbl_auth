from tigrbl_authentication_context_bases import AmrEvaluatorBase
from tigrbl_security_trust_contracts import (
    AmrEvaluationRequest,
    AmrEvaluationResult,
    CapabilityMap,
)


class BasicAmrEvaluator(AmrEvaluatorBase):
    """Report the required AMR values absent from achieved evidence."""

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"evaluate_amr": ("basic",)}, features=("amr",))

    def evaluate_amr(self, request: AmrEvaluationRequest) -> AmrEvaluationResult:
        required = {str(getattr(value, "value", value)) for value in request.required}
        achieved = {str(getattr(value, "value", value)) for value in request.achieved}
        missing = tuple(sorted(required - achieved))
        return AmrEvaluationResult(
            not missing,
            request.achieved,
            missing,
            None if not missing else "amr_not_satisfied",
        )


__all__ = ["BasicAmrEvaluator"]
