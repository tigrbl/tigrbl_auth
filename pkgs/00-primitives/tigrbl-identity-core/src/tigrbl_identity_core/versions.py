from __future__ import annotations

"""Version comparison primitives shared by identity packages."""


def semver_key(version: str) -> tuple[int, int, int]:
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


def version_in_range(version: str, compatible_runtime_range: tuple[str, str]) -> bool:
    lower, upper = compatible_runtime_range
    version_key = semver_key(version)
    return semver_key(lower) <= version_key <= semver_key(upper)


__all__ = ["semver_key", "version_in_range"]
