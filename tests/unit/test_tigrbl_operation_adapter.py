"""Run real credential verification and PDP decisions through mounted operations."""

from dataclasses import replace
from datetime import datetime, timezone

import pytest
from httpx import ASGITransport, AsyncClient
from tba_capability_api_key_authentication import ApiKeyAuthenticationCapability
from tba_contracts_authorization import (
    ActionDefinition,
    AuthenticationContext,
    PrincipalRef,
    ResourceRef,
    RoleDefinition,
    RoleGrant,
)
from tba_plugin_tigrbl import (
    OperationAuthorizationAdapter,
    OperationPolicy,
    OperationPrincipal,
    operation_catalog_digest,
)
from tba_provider_authenticator_api_key_local import ApiKeyLocalAuthenticator
from tba_provider_authorization_policy_decision_engine import PlatformPolicyDecisionEngine
from tigrbl import (
    Column,
    HttpJsonRpcBindingSpec,
    HttpRestBindingSpec,
    OperationSecurity,
    Table,
    TableProfileSpec,
    TigrblApp,
    op_ctx,
)
from tigrbl.factories.engine import mem


@pytest.mark.asyncio
async def test_policy_is_enforced_through_bound_rest_and_rpc():
    notes = {"alice-note": ("alice", "A"), "bob-note": ("bob", "B")}
    action = "proof.note.update"

    class Note(Table):
        __tablename__ = "authorization_proof_notes"
        TABLE_PROFILE = TableProfileSpec(kind="authorization-proof", custom=True, namespace="proof")
        id = Column.make(
            storage=Column.S(primary_key=True),
            field=Column.F(py_type=str),
            io=Column.IO(),
        )

        @op_ctx(
            alias="health",
            target="custom",
            bindings=(HttpRestBindingSpec("http.rest", ("GET",), "/proof/health"),),
            security=OperationSecurity("proof.note.health", "note", access="public"),
        )
        async def health(cls, ctx):
            return {"ready": True}

        @op_ctx(
            alias="edit",
            target="custom",
            bindings=(
                HttpRestBindingSpec("http.rest", ("POST",), "/proof/edit"),
                HttpJsonRpcBindingSpec("http.jsonrpc", "Note.edit"),
            ),
            security=OperationSecurity(action, "note"),
        )
        async def edit(cls, ctx):
            payload = ctx["payload"]
            owner, _ = notes[payload["id"]]
            notes[payload["id"]] = (owner, payload["text"])
            return {"saved": payload["id"]}

        @op_ctx(
            alias="owned",
            target="custom",
            bindings=(HttpRestBindingSpec("http.rest", ("GET",), "/proof/owned"),),
            security=OperationSecurity("proof.note.list", "note"),
        )
        async def owned(cls, ctx):
            owner = ctx["operation_principal"].principal.principal_id
            return sorted(key for key, row in notes.items() if row[0] == owner)

        @op_ctx(
            alias="publish",
            target="custom",
            bindings=(HttpRestBindingSpec("http.rest", ("POST",), "/proof/publish"),),
            security=OperationSecurity("proof.note.publish", "note"),
        )
        async def publish(cls, ctx):
            return {"published": True}

    app = TigrblApp(engine=mem(async_=False), mount_system=False)
    app.include_table(Note)
    app.mount_jsonrpc()

    alice = PrincipalRef("alice", "user", "team")
    digest_key = ApiKeyLocalAuthenticator.digest_key
    keys = {
        digest_key("editor-key"): {"audience": "proof"},
        digest_key("list-key"): {"audience": "proof", "actions": frozenset({"proof.note.list"})},
        digest_key("wrong-audience"): {"audience": "different"},
        digest_key("step-up-key"): {"audience": "proof", "acr": "mfa"},
    }
    credentials = ApiKeyAuthenticationCapability(
        find_api_keys=lambda db, digest: [keys[digest]] if digest in keys else [],
        resolve_user=lambda db, key: {"id": alice.principal_id},
        mark_used=lambda db, key: None,
    )

    async def authenticate(ctx):
        authorization = ctx["request"].headers.get("authorization", "")
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return None
        result = await credentials.authenticate_api_key(api_key=token, db=None)
        if not result.authenticated:
            return None
        key = result.credential_record
        return OperationPrincipal(
            alice, key["audience"], AuthenticationContext(acr=key.get("acr")),
            actions=key.get("actions"),
        )

    def resource(operation, ctx, principal):
        if operation.action_id == action:
            note_id = ctx["payload"].get("id")
            if not isinstance(note_id, str) or note_id not in notes:
                return None
            return ResourceRef("note", note_id, "team")
        return ResourceRef("note", principal.principal_id, "team")

    catalog = app.operation_security_catalog()
    assert {item["action_id"] for item in catalog} == {
        "proof.note.health", action, "proof.note.list", "proof.note.publish",
    }
    edit = next(item for item in catalog if item["action_id"] == action)
    assert {binding["protocol"] for binding in edit["bindings"]} == {"http.rest", "http.jsonrpc"}
    digest = operation_catalog_digest(app)
    grants = [
        RoleGrant("owner", "team", alice, "editor", ResourceRef("note", "alice-note", "team")),
        RoleGrant("personal", "team", alice, "editor", ResourceRef("note", "alice", "team")),
    ]
    published_digest = digest

    def load_policy(operation, ctx, principal):
        engine = PlatformPolicyDecisionEngine(
            actions=(
                ActionDefinition(action, "note"),
                ActionDefinition("proof.note.list", "note"),
                ActionDefinition("proof.note.publish", "note", required_acr="mfa"),
            ),
            roles=(RoleDefinition("editor", "Editor", "team", (action, "proof.note.list", "proof.note.publish")),),
            grants=grants,
        )
        return OperationPolicy(published_digest, engine.evaluate)

    await app.initialize()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        def bearer(token):
            return {"authorization": f"Bearer {token}"}

        mine = {"id": "alice-note", "text": "saved"}
        other = {"id": "bob-note", "text": "denied"}
        editor = bearer("editor-key")
        assert (await client.get("/proof/health")).json() == {"ready": True}
        assert (await client.post("/proof/edit", json=mine, headers=editor)).status_code == 503
        OperationAuthorizationAdapter("proof", authenticate, resource, load_policy).install(app)
        assert (await client.post("/proof/edit", json=mine)).status_code == 401
        assert (await client.post("/proof/edit", json=mine, headers=bearer("wrong-audience"))).status_code == 401
        assert (await client.post("/proof/edit", json=mine, headers=bearer("list-key"))).status_code == 403
        assert (await client.post("/proof/edit", json=other, headers=editor)).status_code == 403
        assert notes == {"alice-note": ("alice", "A"), "bob-note": ("bob", "B")}
        assert (await client.post("/proof/edit", json=mine, headers=editor)).is_success
        assert notes["alice-note"] == ("alice", "saved")
        assert (await client.get("/proof/owned?owner=bob", headers=editor)).json() == ["alice-note"]
        assert (await client.post("/proof/publish", headers=editor)).status_code == 403
        assert (await client.post("/proof/publish", headers=bearer("step-up-key"))).json() == {"published": True}

        async def rpc(payload):
            return (await client.post("/rpc", headers=editor, json={
                "jsonrpc": "2.0", "id": 1, "method": "Note.edit", "params": payload,
            })).json()

        assert "error" in await rpc(other)
        assert (await rpc(mine))["result"] == {"saved": "alice-note"}
        grants[0] = replace(grants[0], revoked_at=datetime.now(timezone.utc))
        assert (await client.post("/proof/edit", json=mine, headers=editor)).status_code == 403
        assert "error" in await rpc(mine)
        assert notes["bob-note"] == ("bob", "B")
        published_digest = "old-catalog"
        assert (await client.get("/proof/owned", headers=editor)).status_code == 503
