from typing import Any, Mapping


def migrate_claims(
    value: Mapping[str | int, Any], *, source: str, target: str = "RFC9711"
) -> dict[str | int, Any]:
    if source == target:
        return dict(value)
    if source != "draft-ietf-rats-eat-30" or target != "RFC9711":
        raise ValueError(f"unsupported EAT migration: {source} -> {target}")
    if "eat_profile" not in value and 265 not in value:
        raise ValueError("EAT migration requires an explicit eat_profile")
    return dict(value)


__all__ = ["migrate_claims"]
