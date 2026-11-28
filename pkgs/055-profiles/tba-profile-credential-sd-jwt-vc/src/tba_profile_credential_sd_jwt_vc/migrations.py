from typing import Any, Mapping


def migrate_claims(
    value: Mapping[str, Any], *, source: str, target: str = "draft-17"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source not in {"draft-10", "draft-13"} or target != "draft-17":
        raise ValueError(f"unsupported SD-JWT VC migration: {source} -> {target}")
    if not isinstance(value.get("vct"), str):
        raise ValueError("SD-JWT VC migration requires vct")
    return dict(value)


__all__ = ["migrate_claims"]
