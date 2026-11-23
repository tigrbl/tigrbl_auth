"""Revalidate approved grants and their subjects at each MCP authorization boundary."""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from typing import Protocol

from tba_concrete_capability import Capability
from tba_concrete_mcp_delegation import approve_scopes, effective_scopes
from tba_contracts_identity.capabilities import CapabilityDefinition, CapabilityOperation


@dataclass(frozen=True, slots=True)
class MCPGrantBinding:
    """Grant identity taken from validated OAuth state and the expected resource."""

    grant_id: str
    tenant_id: str
    client_id: str
    resource: str


@dataclass(frozen=True, slots=True)
class MCPGrant:
    binding: MCPGrantBinding
    owner_id: str
    bot_id: str | None
    scopes: frozenset[str]
    active: bool
    expires_at: float | None = None


@dataclass(frozen=True, slots=True)
class MCPSubject:
    """Current account or bot returned by the application's authoritative store."""

    tenant_id: str
    subject_id: str
    scopes: frozenset[str]
    active: bool
    owner_id: str | None = None


@dataclass(frozen=True, slots=True)
class MCPPrincipal:
    grant: MCPGrant
    owner: MCPSubject
    actor: MCPSubject
    scopes: frozenset[str]


class MCPGrantStore(Protocol):
    """Adapter over the app's durable grant store or TBA delegation operations."""

    async def load(self, binding: MCPGrantBinding) -> MCPGrant | None: ...

    async def revoke(self, binding: MCPGrantBinding, owner_id: str) -> bool:
        """Revoke the grant with the binding and owner checked in the write."""
        ...


MCPSubjectLookup = Callable[[str, str], Awaitable[MCPSubject | None]]
MCPResourceCheck = Callable[[MCPPrincipal], Awaitable[bool]]


class MCPAuthorizationCapability(Capability):
    """Combine validated OAuth state, consent and current app authorization."""

    def __init__(
        self,
        grants: MCPGrantStore,
        load_subject: MCPSubjectLookup,
        *,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._grants = grants
        self._load_subject = load_subject
        self._clock = clock
        super().__init__(
            CapabilityDefinition("mcp.authorization", "1.0"),
            operations={
                "approve": CapabilityOperation(target=self.approve),
                "resolve": CapabilityOperation(target=self.resolve),
                "authorize_tool": CapabilityOperation(target=self.authorize_tool),
                "revoke": CapabilityOperation(target=self.revoke),
            },
        )

    async def _current_subject(
        self, tenant_id: str, subject_id: str, owner_id: str | None
    ) -> MCPSubject | None:
        subject = await self._load_subject(tenant_id, subject_id)
        if (
            subject is None
            or not subject.active
            or subject.tenant_id != tenant_id
            or subject.subject_id != subject_id
            or subject.owner_id != owner_id
        ):
            return None
        return subject

    async def approve(
        self,
        *,
        tenant_id: str,
        owner_id: str,
        bot_id: str | None,
        selected: Iterable[str],
        requested: Iterable[str],
    ) -> frozenset[str]:
        """Validate browser consent after OAuth and browser identity validation."""
        owner = await self._current_subject(tenant_id, owner_id, None)
        if owner is None:
            raise PermissionError("The authorizing account is unavailable.")
        bot = None
        if bot_id is not None:
            bot = await self._current_subject(tenant_id, bot_id, owner_id)
            if bot is None:
                raise PermissionError("The selected bot is unavailable.")
        return approve_scopes(
            selected,
            requested,
            owner.scopes,
            bot.scopes if bot is not None else None,
        )

    async def resolve(
        self, binding: MCPGrantBinding, token_scopes: Iterable[str]
    ) -> MCPPrincipal | None:
        """Resolve the acting identity after the token or grant is authenticated."""
        grant = await self._grants.load(binding)
        if grant is None or grant.binding != binding or not grant.active:
            return None
        if grant.expires_at is not None and not grant.expires_at > self._clock():
            return None
        owner = await self._current_subject(binding.tenant_id, grant.owner_id, None)
        if owner is None:
            return None
        actor = owner
        bot_scopes = None
        if grant.bot_id is not None:
            bot = await self._current_subject(
                binding.tenant_id, grant.bot_id, grant.owner_id
            )
            if bot is None:
                return None
            actor = bot
            bot_scopes = bot.scopes
        scopes = effective_scopes(token_scopes, grant.scopes, owner.scopes, bot_scopes)
        return MCPPrincipal(grant, owner, actor, scopes) if scopes else None

    async def authorize_tool(
        self,
        binding: MCPGrantBinding,
        token_scopes: Iterable[str],
        *,
        required_scopes: Iterable[str],
        check_resource: MCPResourceCheck,
    ) -> MCPPrincipal | None:
        """Recheck the grant and the app's own resource policy before a tool call."""
        principal = await self.resolve(binding, token_scopes)
        if principal is None or not frozenset(required_scopes) <= principal.scopes:
            return None
        return principal if await check_resource(principal) else None

    async def revoke(self, binding: MCPGrantBinding, *, owner_id: str) -> bool:
        """Revoke from an authenticated account's browser connection list."""
        return await self._grants.revoke(binding, owner_id)
