from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from urllib.parse import urlencode
from unittest.mock import AsyncMock

import pytest

from tigrbl_auth_protocol_oauth.standards.client_registration_management import describe as describe_rfc7592
from tigrbl_auth_protocol_oauth.standards.device_authorization import (
    DEVICE_CODE_INTERVAL,
    DEVICE_CODE_SLOW_DOWN_INCREMENT,
    describe as describe_rfc8628,
    next_device_poll_interval,
    poll_too_frequently,
)
from tigrbl_auth_protocol_oauth.standards.resource_indicators import (
    describe as describe_rfc8707,
    resource_binding_summary,
    select_resource_indicator,
)
import tigrbl_identity_storage_runtime.token_exchange as token_exchange_mod
import tigrbl_identity_server.token_request as token_ops
import tigrbl_identity_server.token_device_grant as device_ops

from tigrbl_identity_storage_runtime.token_exchange import (
    HTTPException,
    _actor_claim,
    _normalize_requested_token_type,
    describe as describe_rfc8693,
)


@pytest.mark.unit
def test_resource_indicator_selection_accepts_same_effective_target() -> None:
    selection = select_resource_indicator(
        ["https://rs.example", "https://rs.example"],
        audience="https://rs.example",
    )
    assert selection.resource == "https://rs.example"
    assert selection.audience == "https://rs.example"
    assert selection.resources == ("https://rs.example",)
    assert resource_binding_summary(["https://rs.example"], audience="https://rs.example")["single_effective_target"] is True


@pytest.mark.unit
def test_resource_indicator_selection_rejects_ambiguous_targets() -> None:
    with pytest.raises(ValueError):
        select_resource_indicator(["https://rs-a.example", "https://rs-b.example"])


@pytest.mark.unit
def test_resource_indicator_selection_rejects_audience_conflict() -> None:
    with pytest.raises(ValueError):
        select_resource_indicator(["https://rs.example"], audience="https://aud.example")


@pytest.mark.unit
def test_device_poll_helpers_enforce_slow_down_profile() -> None:
    now = datetime.now(timezone.utc)
    assert next_device_poll_interval(DEVICE_CODE_INTERVAL, slow_down_count=2) == (
        DEVICE_CODE_INTERVAL + (DEVICE_CODE_SLOW_DOWN_INCREMENT * 2)
    )
    assert poll_too_frequently(
        last_polled_at=now - timedelta(seconds=DEVICE_CODE_INTERVAL - 1),
        now=now,
        interval=DEVICE_CODE_INTERVAL,
    ) is True
    assert poll_too_frequently(
        last_polled_at=now - timedelta(seconds=DEVICE_CODE_INTERVAL),
        now=now,
        interval=DEVICE_CODE_INTERVAL,
    ) is False


@pytest.mark.unit
def test_token_exchange_helpers_are_bounded_and_actor_aware() -> None:
    assert _normalize_requested_token_type(None) == "urn:ietf:params:oauth:token-type:access_token"
    assert _normalize_requested_token_type("access_token") == "access_token"
    assert _actor_claim({"sub": "actor-123"}) == {"sub": "actor-123"}
    assert _actor_claim({}) is None
    with pytest.raises(HTTPException):
        _normalize_requested_token_type("urn:ietf:params:oauth:token-type:refresh_token")


@pytest.mark.unit
def test_describe_metadata_is_truthful() -> None:
    rfc7592 = describe_rfc7592()
    rfc8628 = describe_rfc8628()
    rfc8693 = describe_rfc8693()
    rfc8707 = describe_rfc8707()
    assert rfc7592["runtime_status"] == "persistence-backed-client-management-runtime"
    assert "/register/{client_id}" in rfc7592["public_surface"]
    assert rfc8628["approval_denial_supported"] is True
    assert "slow_down" in rfc8628["notes"]
    assert "/token/exchange" in rfc8693["public_surface"]
    assert "lineage" in rfc8693["notes"]
    assert rfc8707["single_effective_target"] is True
    assert rfc8707["conflicting_inputs_fail_closed"] is True


class _Form(dict):
    def getlist(self, key: str):
        value = self.get(key)
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]


class _FakeRequest:
    def __init__(self, form_data: dict[str, object] | None = None, *, headers: dict[str, str] | None = None, body: bytes | None = None):
        self._form_data = _Form(form_data or {})
        self.headers = headers or {}
        self.body = body or b''

    async def form(self):
        return self._form_data


class _FakeDB:
    def __init__(self, *scalars):
        self._scalars = list(scalars)
        self.commits = 0

    async def scalar(self, stmt):
        if not self._scalars:
            return None
        return self._scalars.pop(0)

    async def commit(self):
        self.commits += 1


def _patch_token_handler_records(monkeypatch, *, client, registration=None, device_code=None):
    updates = {}
    monkeypatch.setattr(
        token_ops.client_secret_authentication,
        'verify_client_record',
        lambda record, secret: SimpleNamespace(authenticated=True),
    )

    async def _read_handler_record(model, db, ident):
        if model is token_ops._runtime.Client:
            return client
        return None

    async def _first_handler_record(model, db, filters):
        if model is token_ops._runtime.ClientRegistration:
            return registration
        if model is device_ops.DeviceCode:
            return device_code
        return None

    async def _update_handler_record(model, db, ident, payload):
        updates.update(payload)
        if device_code is not None:
            for key, value in payload.items():
                setattr(device_code, key, value)
        return device_code

    monkeypatch.setattr(token_ops, 'read_handler_record', _read_handler_record)
    monkeypatch.setattr(token_ops._runtime, 'read_handler_record', _read_handler_record)
    monkeypatch.setattr(token_ops._runtime, 'first_handler_record', _first_handler_record)
    monkeypatch.setattr(device_ops, 'first_handler_record', _first_handler_record)
    monkeypatch.setattr(device_ops, 'update_handler_record', _update_handler_record)
    return updates


class _FakeDeployment:
    issuer = 'https://issuer.example/tenants/test'
    protected_resource_identifier = 'https://rs.example'

    def flag_enabled(self, flag: str) -> bool:
        return True


class _FakeSenderConstraint:
    confirmation_claim = None
    cert_thumbprint = None
    token_type = 'bearer'
    mechanism = 'none'


@pytest.mark.asyncio
@pytest.mark.unit
async def test_device_code_poll_slow_down(monkeypatch) -> None:
    client = SimpleNamespace(id='client-1', tenant_id='tenant-1', verify_secret=lambda secret: True)
    row = SimpleNamespace(
        client_id='client-1',
        device_code='device-code-1',
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        consumed_at=None,
        interval=DEVICE_CODE_INTERVAL,
        last_polled_at=datetime.now(timezone.utc) - timedelta(seconds=1),
        poll_count=0,
        slow_down_count=0,
        denied_at=None,
        denial_reason=None,
        authorized=False,
        user_id=None,
        tenant_id='tenant-1',
        id='row-1',
        resource='https://rs.example',
        audience='https://rs.example',
        scope='openid',
    )
    db = _FakeDB(client, None, row)
    updates = _patch_token_handler_records(monkeypatch, client=client, device_code=row)
    monkeypatch.setattr(token_ops, '_enforce_tls', lambda request, deployment: None)
    monkeypatch.setattr(token_ops, '_resolve_request_deployment', lambda request: _FakeDeployment())
    monkeypatch.setattr(token_ops, 'assert_token_request_allowed', lambda data, deployment: None)
    monkeypatch.setattr(token_ops, 'validate_sender_constraint_async', AsyncMock(return_value=_FakeSenderConstraint()))
    captured = {}

    async def _audit(db, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(device_ops, 'append_audit_event_record', _audit)
    request = _FakeRequest({'grant_type': token_ops.DEVICE_CODE_GRANT_TYPE, 'client_id': 'client-1', 'client_secret': 'secret', 'device_code': 'device-code-1'})
    response = await token_ops.token_request(request=request, db=db)
    assert response.status_code == 400
    assert response.content['error'] == 'slow_down'
    assert row.poll_count == 1
    assert row.slow_down_count == 1
    assert row.interval == next_device_poll_interval(DEVICE_CODE_INTERVAL, slow_down_count=1)
    assert updates['poll_count'] == 1
    assert updates['slow_down_count'] == 1
    assert updates['interval'] == row.interval
    assert captured['event_type'] == 'device.authorization.poll.slow_down'


@pytest.mark.asyncio
@pytest.mark.unit
async def test_device_code_poll_denied_and_expired(monkeypatch) -> None:
    monkeypatch.setattr(token_ops, '_enforce_tls', lambda request, deployment: None)
    monkeypatch.setattr(token_ops, '_resolve_request_deployment', lambda request: _FakeDeployment())
    monkeypatch.setattr(token_ops, 'assert_token_request_allowed', lambda data, deployment: None)
    monkeypatch.setattr(token_ops, 'validate_sender_constraint_async', AsyncMock(return_value=_FakeSenderConstraint()))

    client = SimpleNamespace(id='client-1', tenant_id='tenant-1', verify_secret=lambda secret: True)
    denied_row = SimpleNamespace(
        client_id='client-1',
        device_code='device-code-2',
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        consumed_at=None,
        interval=DEVICE_CODE_INTERVAL,
        last_polled_at=None,
        poll_count=0,
        slow_down_count=0,
        denied_at=datetime.now(timezone.utc),
        denial_reason='access_denied',
        authorized=False,
        user_id=None,
        tenant_id='tenant-1',
        id='row-2',
        resource='https://rs.example',
        audience='https://rs.example',
        scope='openid',
    )
    expired_row = SimpleNamespace(
        client_id='client-1',
        device_code='device-code-3',
        expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
        consumed_at=None,
        interval=DEVICE_CODE_INTERVAL,
        last_polled_at=None,
        poll_count=0,
        slow_down_count=0,
        denied_at=None,
        denial_reason=None,
        authorized=False,
        user_id=None,
        tenant_id='tenant-1',
        id='row-3',
        resource='https://rs.example',
        audience='https://rs.example',
        scope='openid',
    )
    denied_db = _FakeDB(client, None, denied_row)
    expired_db = _FakeDB(client, None, expired_row)
    rows_by_code = {denied_row.device_code: denied_row, expired_row.device_code: expired_row}

    async def _read_handler_record(model, db, ident):
        if model is token_ops._runtime.Client:
            return client
        return None

    async def _first_handler_record(model, db, filters):
        if model is token_ops._runtime.ClientRegistration:
            return None
        if model is device_ops.DeviceCode:
            return rows_by_code.get(filters.get('device_code'))
        return None

    async def _update_handler_record(model, db, ident, payload):
        for row in rows_by_code.values():
            if str(getattr(row, 'id', '')) == str(ident):
                for key, value in payload.items():
                    setattr(row, key, value)
                return row
        return None

    monkeypatch.setattr(token_ops, 'read_handler_record', _read_handler_record)
    monkeypatch.setattr(token_ops._runtime, 'read_handler_record', _read_handler_record)
    monkeypatch.setattr(token_ops._runtime, 'first_handler_record', _first_handler_record)
    monkeypatch.setattr(device_ops, 'first_handler_record', _first_handler_record)
    monkeypatch.setattr(device_ops, 'update_handler_record', _update_handler_record)
    monkeypatch.setattr(
        token_ops.client_secret_authentication,
        'verify_client_record',
        lambda record, secret: SimpleNamespace(authenticated=True),
    )
    denied_request = _FakeRequest({'grant_type': token_ops.DEVICE_CODE_GRANT_TYPE, 'client_id': 'client-1', 'client_secret': 'secret', 'device_code': 'device-code-2'})
    expired_request = _FakeRequest({'grant_type': token_ops.DEVICE_CODE_GRANT_TYPE, 'client_id': 'client-1', 'client_secret': 'secret', 'device_code': 'device-code-3'})
    denied_response = await token_ops.token_request(request=denied_request, db=denied_db)
    expired_response = await token_ops.token_request(request=expired_request, db=expired_db)
    assert denied_response.content['error'] == 'access_denied'
    assert expired_response.content['error'] == 'expired_token'


@pytest.mark.asyncio
@pytest.mark.unit
async def test_token_exchange_runtime_rejects_conflicting_target(monkeypatch) -> None:
    monkeypatch.setattr(token_exchange_mod, 'deployment_from_request', lambda request, settings: _FakeDeployment())
    monkeypatch.setattr(token_exchange_mod, 'validate_sender_constraint', lambda *args, **kwargs: _FakeSenderConstraint())

    class _JWT:
        async def async_decode(self, token, verify_exp=True):
            return {'sub': 'user-1', 'tid': 'tenant-1', 'iss': 'https://issuer.example', 'aud': 'https://rs.example'}

        async def async_sign(self, **kwargs):
            return 'access-token'

    monkeypatch.setattr(token_exchange_mod, '_jwt_coder', lambda: _JWT())
    request = _FakeRequest(
        body=urlencode(
            {
                'grant_type': token_exchange_mod.TOKEN_EXCHANGE_GRANT_TYPE,
                'subject_token': 'subject-token',
                'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
                'audience': 'https://aud.example',
                'resource': 'https://rs.example',
            }
        ).encode('utf-8')
    )
    with pytest.raises(token_exchange_mod.HTTPException) as excinfo:
        await token_exchange_mod.token_exchange(request)
    assert excinfo.value.detail['error'] == 'invalid_target'


@pytest.mark.asyncio
@pytest.mark.unit
async def test_token_exchange_runtime_emits_lineage_audit(monkeypatch) -> None:
    monkeypatch.setattr(token_exchange_mod, 'deployment_from_request', lambda request, settings: _FakeDeployment())
    monkeypatch.setattr(token_exchange_mod, 'validate_sender_constraint', lambda *args, **kwargs: _FakeSenderConstraint())
    monkeypatch.setattr(
        token_exchange_mod,
        'build_protected_resource_verifier_contract',
        lambda deployment: SimpleNamespace(verifier_logic_id='protected-resource-verifier', required_claims=('sub', 'iss', 'aud')),
    )
    captured = {}

    async def _audit(**kwargs):
        captured.update(kwargs)

    async def _persist_token(*args, **kwargs):
        return "token-digest"

    class _JWT:
        async def async_decode(self, token, verify_exp=True):
            if token == 'actor-token':
                return {'sub': 'actor-1'}
            return {'sub': 'user-1', 'tid': 'tenant-1', 'iss': 'https://issuer.example', 'aud': 'https://rs.example', 'scope': 'read'}

        async def async_sign(self, **kwargs):
            return 'access-token'

    monkeypatch.setattr(token_exchange_mod, '_jwt_coder', lambda: _JWT())
    monkeypatch.setattr(token_exchange_mod, 'append_audit_event_async', _audit)
    monkeypatch.setattr(token_exchange_mod, 'upsert_token_record_async', _persist_token)
    request = _FakeRequest(
        body=urlencode(
            {
                'grant_type': token_exchange_mod.TOKEN_EXCHANGE_GRANT_TYPE,
                'subject_token': 'subject-token',
                'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
                'actor_token': 'actor-token',
                'actor_token_type': 'urn:ietf:params:oauth:token-type:access_token',
                'requested_token_type': 'access_token',
                'audience': 'https://rs.example',
                'resource': 'https://rs.example',
            }
        ).encode('utf-8')
    )
    response = await token_exchange_mod.token_exchange(request)
    assert response['access_token'] == 'access-token'
    assert response['exchange_mode'] == 'delegation'
    assert captured['event_type'] == 'oauth2.token_exchange.issued'
    assert captured['details']['exchange_mode'] == 'delegation'
    assert captured['details']['resource'] == 'https://rs.example'
    assert captured['details']['audience'] == 'https://rs.example'
    assert captured['details']['authorization_trace_decision_key']
    assert captured['details']['delegation_lineage_id']
