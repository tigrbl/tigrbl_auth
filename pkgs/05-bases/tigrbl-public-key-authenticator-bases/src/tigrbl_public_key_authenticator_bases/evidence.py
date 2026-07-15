from abc import ABC

from tigrbl_identity_contracts.public_key_authentication import (
    PublicKeyAuthenticationEvidence,
)


class PublicKeyEvidenceEvaluatorBase(ABC):
    def evaluate(self, evidence: PublicKeyAuthenticationEvidence, /) -> tuple[str, ...]:
        raise NotImplementedError


__all__ = ["PublicKeyEvidenceEvaluatorBase"]
