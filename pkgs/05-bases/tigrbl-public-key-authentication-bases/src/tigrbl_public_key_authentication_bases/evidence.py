from abc import ABC

from tigrbl_public_key_authentication_contracts import (
    PublicKeyAuthenticationEvidence,
)


class PublicKeyEvidenceEvaluatorBase(ABC):
    def evaluate(self, evidence: PublicKeyAuthenticationEvidence, /) -> tuple[str, ...]:
        raise NotImplementedError


__all__ = ["PublicKeyEvidenceEvaluatorBase"]
