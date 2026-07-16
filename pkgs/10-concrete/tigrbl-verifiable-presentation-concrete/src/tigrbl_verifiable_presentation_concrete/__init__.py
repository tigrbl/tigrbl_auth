from dataclasses import dataclass
from typing import Mapping

from tigrbl_digital_credential_bases import PresentationFormatBase


@dataclass(frozen=True, slots=True)
class VerifiablePresentation(PresentationFormatBase):
    format_identifier = "w3c-vp"
    contexts: tuple[object, ...]
    types: tuple[str, ...]
    credentials: tuple[object, ...] = ()
    holder: str | Mapping[str, object] | None = None
    identifier: str | None = None
    proof: object | None = None


__all__ = ["VerifiablePresentation"]
