"""Permission decisions for user-authorized MCP connections."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Literal

PermissionStatus = Literal[
    "requested", "available_to_request", "unavailable_for_account",
    "unavailable_for_bot",
]


@dataclass(frozen=True, slots=True)
class Permission:
    id: str
    label: str
    status: PermissionStatus
    explicit: bool = False


def consent_permissions(
    labels: Mapping[str, str],
    requested: Iterable[str],
    account: Iterable[str],
    bot: Iterable[str] | None = None,
    *,
    explicit: Iterable[str] = (),
) -> tuple[Permission, ...]:
    requested, account, explicit = map(frozenset, (requested, account, explicit))
    bot = None if bot is None else frozenset(bot)

    def status(scope: str) -> PermissionStatus:
        if scope not in account:
            return "unavailable_for_account"
        if bot is not None and scope not in bot:
            return "unavailable_for_bot"
        if scope in requested:
            return "requested"
        return "available_to_request"

    return tuple(Permission(scope, label, status(scope), scope in explicit)
                 for scope, label in labels.items())


def effective_scopes(
    token: Iterable[str],
    grant: Iterable[str],
    account: Iterable[str],
    bot: Iterable[str] | None = None,
) -> frozenset[str]:
    allowed = frozenset(token).intersection(grant, account)
    return allowed if bot is None else allowed.intersection(bot)


def approve_scopes(
    selected: Iterable[str],
    requested: Iterable[str],
    account: Iterable[str],
    bot: Iterable[str] | None = None,
) -> frozenset[str]:
    approved = frozenset(selected)
    if not approved or not approved <= effective_scopes(requested, requested, account, bot):
        raise ValueError("Select requested permissions the acting identity holds.")
    return approved
