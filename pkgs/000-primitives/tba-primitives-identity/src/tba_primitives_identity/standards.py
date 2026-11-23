"""Shared metadata helpers for standards-owned modules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StandardOwner:
    label: str
    title: str
    runtime_status: str
    public_surface: tuple[str, ...]
    notes: str
    organization: str | None = None
    version: str | None = None
    status: str | None = None
    specification_uri: str | None = None
    protocol_tags: tuple[str, ...] = ()
    claimable: bool = False


def describe_owner(owner: StandardOwner, **extra: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "label": owner.label,
        "title": owner.title,
        "runtime_status": owner.runtime_status,
        "public_surface": list(owner.public_surface),
        "notes": owner.notes,
        "organization": owner.organization,
        "version": owner.version,
        "status": owner.status,
        "specification_uri": owner.specification_uri,
        "protocol_tags": list(owner.protocol_tags),
        "claimable": owner.claimable,
    }
    payload.update(extra)
    return payload


__all__ = ["StandardOwner", "describe_owner"]
