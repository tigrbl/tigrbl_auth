from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .base import CertificationError


@dataclass(frozen=True)
class RuntimeQualification:
    artifact_sha256: str
    dependency_lock_sha256: str
    config_sha256: str
    product_surface: str
    capabilities: frozenset[str]


def stable_sha256(value: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(value, str):
        payload = value.encode("utf-8")
    else:
        payload = repr(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def assert_runtime_qualified(
    qualified: RuntimeQualification,
    running: RuntimeQualification,
) -> None:
    if qualified != running:
        raise CertificationError("running runtime does not match qualified deployment truth")
