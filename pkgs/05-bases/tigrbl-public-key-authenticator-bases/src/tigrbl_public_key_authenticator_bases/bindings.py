from abc import ABC


class VerifierBindingEvaluatorBase(ABC):
    def allows(self, *, verifier_id: str, origin: str) -> bool:
        raise NotImplementedError


__all__ = ["VerifierBindingEvaluatorBase"]
