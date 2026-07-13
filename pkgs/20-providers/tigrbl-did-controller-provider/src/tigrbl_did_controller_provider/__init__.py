from collections.abc import Callable
from dataclasses import dataclass

from tigrbl_did_concrete import validate_did_document
from tigrbl_identity_contracts.did import Did, DidDocument

ControlProofVerifier = Callable[[DidDocument | None, DidDocument, bytes | str], bool]
DocumentPublisher = Callable[[DidDocument, str], object]


@dataclass(frozen=True, slots=True)
class DidControllerResult:
    identifier: Did
    version_id: str
    created: bool


class DidControllerProvider:
    def __init__(
        self, proof_verifier: ControlProofVerifier, publisher: DocumentPublisher
    ):
        self._proof_verifier = proof_verifier
        self._publisher = publisher
        self._current: dict[Did, DidDocument] = {}

    def apply(
        self, document: DidDocument, version_id: str, proof: bytes | str
    ) -> DidControllerResult:
        validate_did_document(document)
        if not version_id or not proof:
            raise ValueError("DID update requires version ID and control proof")
        current = self._current.get(document.identifier)
        if current is not None and current.identifier != document.identifier:
            raise ValueError("DID update cannot change the identifier")
        if not self._proof_verifier(current, document, proof):
            raise PermissionError("DID control proof was not authorized")
        self._publisher(document, version_id)
        self._current[document.identifier] = document
        return DidControllerResult(document.identifier, version_id, current is None)

    def current(self, identifier: Did) -> DidDocument:
        try:
            return self._current[identifier]
        except KeyError as exc:
            raise LookupError(str(identifier)) from exc


__all__ = [
    "ControlProofVerifier",
    "DidControllerProvider",
    "DidControllerResult",
    "DocumentPublisher",
]
