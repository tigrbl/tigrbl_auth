from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompatibilityDecision:
    compatible: bool
    reason: str


def require_exact_version(identifier: str) -> CompatibilityDecision:
    expected = "RFC7515"
    return CompatibilityDecision(
        identifier == expected,
        "exact revision" if identifier == expected else f"expected {expected}",
    )
