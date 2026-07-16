from typing import Mapping

from tigrbl_verifiable_credential_concrete import VerifiableCredential
from tigrbl_verifiable_presentation_concrete import VerifiablePresentation

from .schemas import parse_verifiable_credential, parse_verifiable_presentation


def _validate_proof_container(proof: object) -> None:
    if proof is None:
        return
    proofs = proof if isinstance(proof, list) else [proof]
    if not proofs or not all(
        isinstance(item, Mapping) and isinstance(item.get("type"), str)
        for item in proofs
    ):
        raise ValueError("proof must be an object or array of objects with type")


def validate_verifiable_credential(
    value: Mapping[str, object] | VerifiableCredential,
) -> None:
    credential = (
        parse_verifiable_credential(value) if isinstance(value, Mapping) else value
    )
    _validate_proof_container(credential.proof)
    if (
        credential.valid_from
        and credential.valid_until
        and credential.valid_from > credential.valid_until
    ):
        raise ValueError("validFrom must not follow validUntil")


def validate_verifiable_presentation(
    value: Mapping[str, object] | VerifiablePresentation,
) -> None:
    presentation = (
        parse_verifiable_presentation(value) if isinstance(value, Mapping) else value
    )
    _validate_proof_container(presentation.proof)


__all__ = ["validate_verifiable_credential", "validate_verifiable_presentation"]
