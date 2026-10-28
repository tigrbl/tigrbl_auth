from tba_bases_authentication_context import AcrEvaluatorBase
from tba_contracts_security_trust import (
    AcrEvaluationRequest,
    AcrEvaluationResult,
    CapabilityMap,
)


class BasicAcrEvaluator(AcrEvaluatorBase):
    """Evaluate an achieved ACR by exact requested-value membership."""

    def supports(self) -> CapabilityMap:
        return CapabilityMap(ops={"evaluate_acr": ("basic",)}, features=("acr",))

    def evaluate_acr(self, request: AcrEvaluationRequest) -> AcrEvaluationResult:
        achieved = request.achieved
        requested = tuple(
            str(getattr(value, "value", value)) for value in request.requested
        )
        if not requested:
            return AcrEvaluationResult(True, achieved)
        value = (
            str(getattr(achieved, "value", achieved)) if achieved is not None else ""
        )
        return AcrEvaluationResult(
            value in requested,
            achieved,
            None if value in requested else "acr_not_satisfied",
        )


__all__ = ["BasicAcrEvaluator"]
