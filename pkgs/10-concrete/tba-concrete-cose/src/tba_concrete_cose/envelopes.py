"""Concrete COSE envelope values."""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CoseSign1Envelope:
    encoded: bytes
    payload: bytes
    protected_headers: Mapping[int | str, object]

    def __post_init__(self) -> None:
        if not self.encoded or not self.payload:
            raise ValueError("COSE_Sign1 envelope requires encoded bytes and payload")
        if 1 not in self.protected_headers and "alg" not in self.protected_headers:
            raise ValueError("COSE_Sign1 protected algorithm header is required")
