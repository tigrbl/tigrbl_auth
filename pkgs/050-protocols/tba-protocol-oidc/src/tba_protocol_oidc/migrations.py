from typing import Any, Mapping


def migrate_client_metadata(
    value: Mapping[str, Any], *, source: str, target: str = "1.0-errata2"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if source != "1.0" or target != "1.0-errata2":
        raise ValueError(f"unsupported OIDC migration: {source} -> {target}")
    return dict(value)


__all__ = ["migrate_client_metadata"]
