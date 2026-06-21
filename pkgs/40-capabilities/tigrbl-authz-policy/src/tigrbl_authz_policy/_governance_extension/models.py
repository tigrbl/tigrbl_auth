from __future__ import annotations

from datetime import datetime, timezone
from tigrbl_identity_contracts.governance import *


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def _utc_now_iso() -> str:
    return _utc_now().isoformat()


def _semver_key(version: str) -> tuple[int, int, int]:
    text = version.strip().lstrip("v")
    head = text.split("-", 1)[0]
    parts = [part for part in head.split(".") if part]
    numbers: list[int] = []
    for part in parts[:3]:
        digits = "".join(ch for ch in part if ch.isdigit())
        numbers.append(int(digits or "0"))
    while len(numbers) < 3:
        numbers.append(0)
    return numbers[0], numbers[1], numbers[2]


def _version_in_range(version: str, compatible_runtime_range: tuple[str, str]) -> bool:
    lower, upper = compatible_runtime_range
    version_key = _semver_key(version)
    return _semver_key(lower) <= version_key <= _semver_key(upper)
