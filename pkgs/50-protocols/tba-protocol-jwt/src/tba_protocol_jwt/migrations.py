from typing import Any, Mapping


def migrate_claims(
    value: Mapping[str, Any], *, source: str, target: str = "RFC7519"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source != "draft-ietf-oauth-json-web-token-32" or target != "RFC7519":
        raise ValueError(f"unsupported JWT migration: {source} -> {target}")
    return dict(value)


__all__ = ["migrate_claims"]
