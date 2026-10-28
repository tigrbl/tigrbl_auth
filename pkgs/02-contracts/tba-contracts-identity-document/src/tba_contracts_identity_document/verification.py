from dataclasses import dataclass, field
from typing import Mapping
from .documents import IdentityDocument

@dataclass(frozen=True, slots=True)
class IdentityDocumentVerificationRequest:
    document: IdentityDocument
    expected_subject: str | None = None
    expected_controller: str | None = None

@dataclass(frozen=True, slots=True)
class IdentityDocumentVerificationResult:
    valid: bool
    structural_valid: bool = False
    controller_authorized: bool = False
    key_material_valid: bool = False
    representation_valid: bool = False
    subject: str | None = None
    controller: str | None = None
    reason: str | None = None
    evidence: Mapping[str, object] = field(default_factory=dict)