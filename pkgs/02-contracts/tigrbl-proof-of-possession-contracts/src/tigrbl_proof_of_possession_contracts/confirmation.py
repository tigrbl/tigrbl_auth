"""Credential-to-key confirmation bindings."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ConfirmationKeyBinding:
    method: str
    confirmation: Mapping[object, object]
    credential_id: str | None = None
    key_reference: str | None = None

    def __post_init__(self) -> None:
        if not self.method.strip() or not self.confirmation:
            raise ValueError("confirmation method and value are required")
        object.__setattr__(self, "method", self.method.strip().lower())
        object.__setattr__(self, "confirmation", deepcopy(dict(self.confirmation)))


__all__ = ["ConfirmationKeyBinding"]