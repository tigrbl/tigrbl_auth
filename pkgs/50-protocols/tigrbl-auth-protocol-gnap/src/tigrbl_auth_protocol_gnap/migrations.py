from typing import Any, Mapping


def migrate_request(
    value: Mapping[str, Any], *, source: str, target: str = "RFC9635"
) -> dict[str, Any]:
    if source == target:
        return dict(value)
    if (
        source not in {"draft-13", "draft-ietf-gnap-core-protocol-20"}
        or target != "RFC9635"
    ):
        raise ValueError(f"unsupported GNAP migration: {source} -> {target}")
    # The supported draft request members retained their RFC 9635 wire names.
    # Migration metadata is deliberately not injected into protocol payloads.
    return dict(value)


__all__ = ["migrate_request"]
