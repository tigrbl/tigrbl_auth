from __future__ import annotations

from dataclasses import dataclass

import pytest

from tigrbl_identity_contracts.tokens import (
    RefreshTokenRedemptionRequest,
    TokenPairIssueRequest,
)
from tigrbl_identity_core.digests import token_hash
from tigrbl_identity_core.errors import (
    InvalidRefreshTokenError,
    RefreshTokenReuseError,
)
from tigrbl_identity_server.security import token_issuance as runtime


@dataclass
class _Coder:
    issued: int = 0

    async def async_sign_pair(self, **kwargs):
        self.issued += 1
        return f"access-{self.issued}", f"refresh-{self.issued}"

    async def async_decode(self, token: str, **kwargs):
        if token == "presented-refresh":
            return {
                "typ": "refresh",
                "sub": "subject-1",
                "tid": "tenant-1",
                "iss": "https://issuer.example",
                "aud": ["https://resource-a.example", "https://resource-b.example"],
                "scope": "openid profile",
                "cnf": {"jkt": "key-1"},
            }
        kind = "refresh" if token.startswith("refresh-") else "access"
        return {
            "typ": kind,
            "sub": "subject-1",
            "tid": "tenant-1",
            "iss": "https://issuer.example",
            "aud": "https://resource-a.example",
            "scope": "openid profile",
        }


def _refresh_record(**changes):
    record = {
        "token_hash": token_hash("presented-refresh"),
        "token_kind": "refresh",
        "token_profile": "oauth-refresh-token",
        "client_id": "client-1",
        "tenant_id": "tenant-1",
        "subject": "subject-1",
        "active": True,
        "revoked_at": None,
        "used_at": None,
        "refresh_successor_hash": None,
        "refresh_family_id": "family-1",
        "claims": {
            "typ": "refresh",
            "sub": "subject-1",
            "tid": "tenant-1",
            "iss": "https://issuer.example",
            "aud": ["https://resource-a.example", "https://resource-b.example"],
            "scope": "openid profile",
        },
    }
    record.update(changes)
    return record


@pytest.mark.asyncio
async def test_issuance_uses_one_injected_session_and_explicit_profiles(
    monkeypatch,
) -> None:
    db = object()
    persisted: list[dict] = []
    audited: list[dict] = []

    async def persist(ctx):
        assert ctx["db"] is db
        persisted.append(dict(ctx["payload"]))
        return ctx["payload"]

    async def audit(ctx):
        assert ctx["db"] is db
        audited.append(dict(ctx["payload"]))

    monkeypatch.setattr(runtime, "persist_issued_token", persist)
    monkeypatch.setattr(runtime, "append_audit_event_record", audit)

    capability = runtime.build_token_issuance_capability(
        db=db,
        token_coder=_Coder(),
    )
    result = await capability.call(
        "issue_token_pair",
        TokenPairIssueRequest(
            subject="subject-1",
            tenant_id="tenant-1",
            client_id="client-1",
            issuer="https://issuer.example",
            scope="openid profile",
            audience="https://resource-a.example",
            confirmation={"jkt": "key-1"},
            token_type="DPoP",
        ),
    )

    assert result.value.token_type == "DPoP"
    assert [item["token_profile"] for item in persisted] == [
        "oauth-access-token",
        "oauth-refresh-token",
    ]
    assert persisted[0]["refresh_family_id"] == persisted[1]["refresh_family_id"]
    assert all(item["claims"]["client_id"] == "client-1" for item in persisted)
    assert audited[0]["event_type"] == "token.pair.issued"


@pytest.mark.asyncio
async def test_refresh_rotation_preserves_lineage_and_uses_same_session(
    monkeypatch,
) -> None:
    db = object()
    persisted: list[dict] = []
    rotations: list[dict] = []
    audits: list[dict] = []

    async def read(ctx):
        assert ctx["db"] is db
        return _refresh_record()

    async def persist(ctx):
        assert ctx["db"] is db
        persisted.append(dict(ctx["payload"]))
        return ctx["payload"]

    async def rotate(ctx):
        assert ctx["db"] is db
        rotations.append(dict(ctx["payload"]))
        return ctx["payload"]

    async def audit(ctx):
        assert ctx["db"] is db
        audits.append(dict(ctx["payload"]))

    monkeypatch.setattr(runtime, "read_token_record", read)
    monkeypatch.setattr(runtime, "persist_issued_token", persist)
    monkeypatch.setattr(runtime, "mark_refresh_token_rotated", rotate)
    monkeypatch.setattr(runtime, "append_audit_event_record", audit)

    service = runtime.build_rfc6749_token_endpoint_service(
        db=db,
        token_coder=_Coder(),
    )
    result = await service.refresh(
        RefreshTokenRedemptionRequest(
            refresh_token="presented-refresh",
            tenant_id="tenant-1",
            client_id="client-1",
            certificate_thumbprint="certificate-1",
            requested_audience="https://resource-a.example",
            token_type="DPoP",
        )
    )

    assert result.refresh_token == "refresh-1"
    assert result.token_type == "DPoP"
    assert all(item["refresh_family_id"] == "family-1" for item in persisted)
    assert all(
        item["refresh_parent_hash"] == token_hash("presented-refresh")
        for item in persisted
    )
    assert rotations == [
        {
            "token_hash": token_hash("presented-refresh"),
            "successor_hash": token_hash("refresh-1"),
            "reason": "refresh_rotated",
        }
    ]
    assert audits[0]["event_type"] == "token.refresh.rotated"


@pytest.mark.asyncio
async def test_refresh_replay_revokes_family_and_records_every_digest(
    monkeypatch,
) -> None:
    db = object()
    revoked: list[dict] = []

    async def read(ctx):
        return _refresh_record(used_at="already-used")

    async def revoke(ctx):
        assert ctx["db"] is db
        return [
            {
                "token_hash": "digest-1",
                "token_type_hint": "refresh_token",
                "subject": "subject-1",
                "tenant_id": "tenant-1",
                "client_id": "client-1",
            },
            {
                "token_hash": "digest-2",
                "token_type_hint": "access_token",
                "subject": "subject-1",
                "tenant_id": "tenant-1",
                "client_id": "client-1",
            },
        ]

    async def record(ctx):
        assert ctx["db"] is db
        revoked.append(dict(ctx["payload"]))

    monkeypatch.setattr(runtime, "read_token_record", read)
    monkeypatch.setattr(runtime, "revoke_refresh_token_family", revoke)
    monkeypatch.setattr(runtime, "record_revoked_token_hash", record)

    capability = runtime.build_token_issuance_capability(
        db=db,
        token_coder=_Coder(),
    )
    with pytest.raises(RefreshTokenReuseError, match="replay"):
        await capability.call(
            "redeem_refresh_token",
            RefreshTokenRedemptionRequest(
                refresh_token="presented-refresh",
                tenant_id="tenant-1",
                client_id="client-1",
            ),
        )

    assert [item["token_hash"] for item in revoked] == ["digest-1", "digest-2"]
    assert all(item["refresh_family_id"] == "family-1" for item in revoked)


@pytest.mark.asyncio
async def test_refresh_rejects_audience_widening(monkeypatch) -> None:
    async def read(ctx):
        return _refresh_record()

    monkeypatch.setattr(runtime, "read_token_record", read)
    capability = runtime.build_token_issuance_capability(
        db=object(),
        token_coder=_Coder(),
    )
    with pytest.raises(InvalidRefreshTokenError, match="audience"):
        await capability.call(
            "redeem_refresh_token",
            RefreshTokenRedemptionRequest(
                refresh_token="presented-refresh",
                tenant_id="tenant-1",
                client_id="client-1",
                requested_audience="https://unrelated.example",
            ),
        )
