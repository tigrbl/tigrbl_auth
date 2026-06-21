from __future__ import annotations

import hashlib
from typing import Any, Mapping, Sequence

from .base import CertificationError
from tigrbl_release_contracts import RuntimeQualification


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
