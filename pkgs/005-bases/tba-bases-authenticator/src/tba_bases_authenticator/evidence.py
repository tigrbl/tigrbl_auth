from abc import ABC


class AuthenticatorEvidenceEvaluatorBase(ABC):
    def evaluate_evidence(self, evidence: object, /) -> object:
        raise NotImplementedError


class PhishingResistanceEvaluatorBase(ABC):
    def is_phishing_resistant(self, evidence: object, /) -> bool:
        raise NotImplementedError


class HardwareKeyProtectionEvaluatorBase(ABC):
    def is_hardware_protected(self, evidence: object, /) -> bool:
        raise NotImplementedError


__all__ = [
    "AuthenticatorEvidenceEvaluatorBase",
    "HardwareKeyProtectionEvaluatorBase",
    "PhishingResistanceEvaluatorBase",
]
