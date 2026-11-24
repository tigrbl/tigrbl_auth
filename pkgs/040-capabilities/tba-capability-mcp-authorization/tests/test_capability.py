"""Exercise the common grant boundary using journal and forum scope fixtures."""

import asyncio
from dataclasses import replace

import pytest

from tba_capability_mcp_authorization import (
    MCPAuthorizationCapability,
    MCPGrant,
    MCPGrantBinding,
    MCPSubject,
    resolve_mcp_grant,
)


class Grants:
    def __init__(self, grant):
        self.grant = grant

    async def load(self, binding):
        # The capability must also check the binding returned by the adapter.
        return self.grant

    async def revoke(self, binding, owner_id):
        if (self.grant.binding, self.grant.owner_id) != (binding, owner_id):
            return False
        self.grant = replace(self.grant, active=False)
        return True


@pytest.fixture(params=[("journal:read", "journal:publish"), ("forum:read", "topics:create")])
def connection(request):
    read, write = request.param
    binding = MCPGrantBinding("grant-1", "tenant-1", "client-1", "https://example.com/mcp")
    subjects = {
        "owner": MCPSubject(binding.tenant_id, "owner", frozenset({read, write}), True),
        "bot": MCPSubject(binding.tenant_id, "bot", frozenset({read}), True, "owner"),
    }
    grant = MCPGrant(binding, "owner", "bot", frozenset({read, write}), True, 200)
    grants = Grants(grant)

    async def load_subject(tenant_id, subject_id):
        return subjects.get(subject_id)

    capability = MCPAuthorizationCapability(grants, load_subject, clock=lambda: 100)
    return capability, grants, subjects, read, write


def test_consent_checks_live_account_and_selected_bot(connection):
    capability, _, subjects, read, write = connection
    request = dict(
        tenant_id="tenant-1", owner_id="owner", bot_id="bot", requested={read, write}
    )
    assert asyncio.run(capability.approve(selected={read}, **request)) == {read}
    with pytest.raises(ValueError, match="Select requested permissions"):
        asyncio.run(capability.approve(selected={write}, **request))
    subjects["bot"] = replace(subjects["bot"], owner_id="different-owner")
    with pytest.raises(PermissionError, match="selected bot"):
        asyncio.run(capability.approve(selected={read}, **request))


def test_direct_connection_and_tool_policy_use_current_owner_scopes(connection):
    capability, grants, subjects, read, write = connection
    grants.grant = replace(grants.grant, bot_id=None)
    binding = grants.grant.binding

    async def owned_resource(principal):
        return principal.actor.subject_id == "owner"

    async def forbidden_resource(principal):
        return False

    allowed = asyncio.run(
        capability.authorize_tool(
            binding, {read, write, "ungranted"}, required_scopes={write},
            check_resource=owned_resource,
        )
    )
    assert allowed is not None
    assert allowed.actor == allowed.owner
    assert allowed.scopes == {read, write}
    assert asyncio.run(
        capability.authorize_tool(
            binding, {read, write}, required_scopes={read}, check_resource=forbidden_resource
        )
    ) is None
    subjects["owner"] = replace(subjects["owner"], scopes=frozenset({read}))
    assert asyncio.run(
        capability.authorize_tool(
            binding, {read, write}, required_scopes={write}, check_resource=owned_resource
        )
    ) is None


def test_bot_changes_and_owner_revocation_are_applied_on_the_next_use(connection):
    capability, grants, subjects, read, write = connection
    binding = grants.grant.binding
    principal = asyncio.run(capability.resolve(binding, {read, write}))
    assert principal is not None
    assert principal.actor.subject_id == "bot"
    assert principal.scopes == {read}
    assert asyncio.run(capability.resolve(binding, {write})) is None
    subjects["bot"] = replace(subjects["bot"], active=False)
    assert asyncio.run(capability.resolve(binding, {read})) is None
    subjects["bot"] = replace(subjects["bot"], active=True)
    subjects["owner"] = replace(subjects["owner"], active=False)
    assert asyncio.run(capability.resolve(binding, {read})) is None
    subjects["owner"] = replace(subjects["owner"], active=True)
    assert not asyncio.run(capability.revoke(binding, owner_id="other-account"))
    assert asyncio.run(capability.revoke(binding, owner_id="owner"))
    assert asyncio.run(capability.resolve(binding, {read})) is None


@pytest.mark.parametrize("field", ["grant_id", "tenant_id", "client_id", "resource"])
def test_a_differently_bound_grant_is_rejected(connection, field):
    capability, grants, _, read, _ = connection
    wrong_binding = replace(grants.grant.binding, **{field: "different"})
    assert asyncio.run(capability.resolve(wrong_binding, {read})) is None
    assert not asyncio.run(capability.revoke(wrong_binding, owner_id="owner"))


def test_expired_grant_cannot_be_resolved(connection):
    capability, grants, _, read, _ = connection
    grants.grant = replace(grants.grant, expires_at=100)
    assert asyncio.run(capability.resolve(grants.grant.binding, {read})) is None


def test_existing_store_snapshot_retains_current_binding_and_subject_checks(connection):
    _, grants, subjects, read, write = connection
    stored = grants.grant

    async def load_subject(tenant_id, subject_id):
        assert tenant_id == stored.binding.tenant_id
        return subjects[subject_id]

    principal = asyncio.run(
        resolve_mcp_grant(
            stored, stored.binding, {read, write}, load_subject=load_subject, clock=lambda: 100
        )
    )
    assert principal is not None
    assert principal.scopes == {read}
    subjects["owner"] = replace(subjects["owner"], scopes=frozenset())
    assert asyncio.run(
        resolve_mcp_grant(
            stored, stored.binding, {read, write}, load_subject=load_subject, clock=lambda: 100
        )
    ) is None
