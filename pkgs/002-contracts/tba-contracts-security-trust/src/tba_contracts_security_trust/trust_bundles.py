from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True, slots=True)
class TrustBundle:
    identifier: str
    version: str
    certificates_der: Sequence[bytes]


__all__ = ["TrustBundle"]
