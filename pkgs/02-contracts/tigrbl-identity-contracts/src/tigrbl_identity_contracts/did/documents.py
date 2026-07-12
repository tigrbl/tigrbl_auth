from dataclasses import dataclass
from typing import Mapping, Sequence

from .identifiers import Did
from .services import DidService
from .verification_methods import DidVerificationMethod, VerificationRelationship


@dataclass(frozen=True, slots=True)
class DidDocument:
    identifier: Did
    verification_methods: Sequence[DidVerificationMethod] = ()
    relationships: Mapping[VerificationRelationship, Sequence[str]] | None = None
    services: Sequence[DidService] = ()
    also_known_as: Sequence[str] = ()
    controller: Sequence[Did] = ()


__all__ = ["DidDocument"]
