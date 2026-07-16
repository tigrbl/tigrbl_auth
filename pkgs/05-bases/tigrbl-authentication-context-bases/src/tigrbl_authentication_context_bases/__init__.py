from abc import ABC

from tigrbl_security_trust_contracts import (
    AcrEvaluationRequest,
    AcrEvaluationResult,
    AmrEvaluationRequest,
    AmrEvaluationResult,
    CapabilityMap,
    IAcrEvaluator,
    IAmrEvaluator,
    ICapabilityProvider,
)


class AcrEvaluatorBase(IAcrEvaluator, ICapabilityProvider, ABC):
    def supports(self) -> CapabilityMap:
        raise NotImplementedError

    def evaluate_acr(self, request: AcrEvaluationRequest) -> AcrEvaluationResult:
        raise NotImplementedError


class AmrEvaluatorBase(IAmrEvaluator, ICapabilityProvider, ABC):
    def supports(self) -> CapabilityMap:
        raise NotImplementedError

    def evaluate_amr(self, request: AmrEvaluationRequest) -> AmrEvaluationResult:
        raise NotImplementedError


class AuthenticationContextEvaluatorBase(AcrEvaluatorBase, AmrEvaluatorBase):
    """Aggregate base for implementations that evaluate both ACR and AMR."""


__all__ = ["AcrEvaluatorBase", "AmrEvaluatorBase", "AuthenticationContextEvaluatorBase"]
