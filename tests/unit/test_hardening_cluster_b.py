from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options
from tigrbl_auth.config.settings import settings
from tigrbl_identity_storage_runtime.par import _normalized_par_params
from tigrbl_auth_protocol_oauth.standards.issuer_identification import (
    IssuerIdentificationError,
    authorization_response_issuer,
    extract_issuer_from_redirect_uri,
)
from tigrbl_auth_protocol_oauth.standards.jwt_secured_authorization_requests import (
    RequestObjectValidationError,
    make_request_object,
    merge_request_object_params,
    parse_request_object,
)
from tigrbl_auth_protocol_oauth.standards.pushed_authorization_requests import PushedAuthorizationRequestError, validate_pushed_authorization_request_row
from tigrbl_auth_protocol_oauth.standards.rich_authorization_requests import normalize_authorization_details
from tigrbl_auth_protocol_oidc.standards.discovery_metadata import build_openid_config



def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')



def _raw_request_object(payload: dict[str, object], *, secret: str, algorithm: str = 'HS256') -> str:
    header = {'alg': algorithm, 'typ': 'JWT'}
    signing_input = '.'.join(
        (
            _b64url(json.dumps(header, separators=(',', ':'), sort_keys=True).encode('utf-8')),
            _b64url(json.dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8')),
        )
    )
    if algorithm.lower() == 'none':
        return f'{signing_input}.'
    digest_name = {'HS256': 'sha256', 'HS384': 'sha384', 'HS512': 'sha512'}[algorithm]
    signature = hmac.new(secret.encode('utf-8'), signing_input.encode('ascii'), getattr(hashlib, digest_name)).digest()
    return f'{signing_input}.{_b64url(signature)}'


@pytest.mark.asyncio
async def test_request_object_round_trip_and_validation(monkeypatch):
    monkeypatch.setattr(settings, 'enable_rfc9101', True)
    token = await make_request_object(
        {
            'client_id': 'client-1',
            'response_type': 'code',
            'redirect_uri': 'https://client.example/cb',
            'scope': 'openid',
        },
        secret='capability-secret',
        issuer='client-1',
        audience='https://issuer.example',
    )
    parsed = await parse_request_object(
        token,
        secret='capability-secret',
        expected_client_id='client-1',
        expected_audience='https://issuer.example',
    )
    assert parsed['client_id'] == 'client-1'
    assert parsed['iss'] == 'client-1'
    assert parsed['aud'] == 'https://issuer.example'
    assert int(parsed['exp']) > int(parsed['iat'])


@pytest.mark.asyncio
async def test_request_object_rejects_unsigned_stale_and_mismatched_inputs(monkeypatch):
    monkeypatch.setattr(settings, 'enable_rfc9101', True)
    now = datetime(2026, 3, 24, tzinfo=timezone.utc)
    unsigned = _raw_request_object({'client_id': 'client-1', 'aud': 'https://issuer.example'}, secret='x', algorithm='none')
    with pytest.raises(RequestObjectValidationError):
        await parse_request_object(unsigned, secret='x', expected_client_id='client-1', expected_audience='https://issuer.example')

    expired = _raw_request_object(
        {
            'client_id': 'client-1',
            'iss': 'client-1',
            'sub': 'client-1',
            'aud': 'https://issuer.example',
            'exp': int((now - timedelta(minutes=5)).timestamp()),
            'iat': int((now - timedelta(minutes=10)).timestamp()),
        },
        secret='capability-secret',
    )
    with pytest.raises(RequestObjectValidationError):
        await parse_request_object(
            expired,
            secret='capability-secret',
            expected_client_id='client-1',
            expected_audience='https://issuer.example',
            now=now,
        )

    mismatched = _raw_request_object(
        {
            'client_id': 'other-client',
            'iss': 'other-client',
            'sub': 'other-client',
            'aud': 'https://issuer.example',
            'exp': int((now + timedelta(minutes=5)).timestamp()),
        },
        secret='capability-secret',
    )
    with pytest.raises(RequestObjectValidationError):
        await parse_request_object(
            mismatched,
            secret='capability-secret',
            expected_client_id='client-1',
            expected_audience='https://issuer.example',
            now=now,
        )



def test_merge_request_object_params_rejects_conflicts():
    with pytest.raises(RequestObjectValidationError):
        merge_request_object_params(
            {'client_id': 'client-1', 'redirect_uri': 'https://client.example/cb'},
            {'client_id': 'client-1', 'redirect_uri': 'https://evil.example/cb'},
        )



def test_validate_pushed_authorization_request_row_enforces_expiry_binding_and_consumption():
    future = datetime.now(timezone.utc) + timedelta(minutes=5)
    row = SimpleNamespace(
        request_uri='urn:ietf:params:oauth:request_uri:capability',
        client_id='client-1',
        expires_at=future,
        consumed_at=None,
        params={'client_id': 'client-1', 'scope': 'openid'},
    )
    result = validate_pushed_authorization_request_row(row, client_id='client-1')
    assert result.request_uri == row.request_uri
    assert result.params['scope'] == 'openid'

    with pytest.raises(PushedAuthorizationRequestError):
        validate_pushed_authorization_request_row(row, client_id='other-client')
    with pytest.raises(PushedAuthorizationRequestError):
        validate_pushed_authorization_request_row(SimpleNamespace(**{**row.__dict__, 'expires_at': datetime.now(timezone.utc) - timedelta(seconds=1)}), client_id='client-1')
    with pytest.raises(PushedAuthorizationRequestError):
        validate_pushed_authorization_request_row(SimpleNamespace(**{**row.__dict__, 'consumed_at': datetime.now(timezone.utc)}), client_id='client-1')


@pytest.mark.asyncio
async def test_normalized_par_params_integrates_jar_rar_and_resource_binding(monkeypatch):
    monkeypatch.setattr(settings, 'enable_rfc9101', True)
    monkeypatch.setattr(settings, 'enable_rfc9126', True)
    monkeypatch.setattr(settings, 'enable_rfc9396', True)
    monkeypatch.setattr(settings, 'enable_rfc8707', True)
    deployment = deployment_from_options(profile='hardening', issuer='https://issuer.example')
    request_object = await make_request_object(
        {
            'client_id': 'client-1',
            'response_type': 'code',
            'redirect_uri': 'https://client.example/cb',
            'scope': 'openid',
            'authorization_details': [
                {'type': 'payment_initiation', 'locations': ['https://rs.example/payments']}
            ],
        },
        secret=settings.jwt_secret,
        issuer='client-1',
        audience='https://issuer.example',
    )
    normalized = await _normalized_par_params({'client_id': 'client-1', 'request': request_object}, deployment)
    assert normalized['audience'] == 'https://rs.example/payments'
    assert normalized['resource'] == ['https://rs.example/payments']
    assert normalized['authorization_details'][0]['_resource'] == 'https://rs.example/payments'



def test_rfc9207_hardening_profile_activates_target_and_contract_requires_iss(monkeypatch):
    monkeypatch.setattr(settings, 'enable_rfc9207', True)
    deployment = deployment_from_options(profile='hardening', issuer='https://issuer.example')
    assert 'RFC 9207' in set(deployment.active_targets)
    metadata = build_openid_config(deployment)
    assert metadata['authorization_response_iss_parameter_supported'] is True
    openapi = build_openapi_contract(deployment, version='0.0.0-test')
    auth_schema = openapi['paths']['/authorize']['get']['responses']['200']['content']['application/json']['schema']
    assert auth_schema['allOf'][1]['required'] == ['iss']
    assert authorization_response_issuer('https://issuer.example') == ('iss', 'https://issuer.example')



def test_extract_issuer_from_redirect_uri_supports_query_and_fragment(monkeypatch):
    monkeypatch.setattr(settings, 'enable_rfc9207', True)
    assert extract_issuer_from_redirect_uri(
        'https://client.example/cb?code=abc&iss=https%3A%2F%2Fissuer.example',
        'https://issuer.example',
    ) == 'https://issuer.example'
    assert extract_issuer_from_redirect_uri(
        'com.example.app:/cb#code=abc&iss=https%3A%2F%2Fissuer.example',
        'https://issuer.example',
    ) == 'https://issuer.example'
    with pytest.raises(IssuerIdentificationError):
        extract_issuer_from_redirect_uri('https://client.example/cb?iss=https%3A%2F%2Fevil.example', 'https://issuer.example')



def test_normalize_authorization_details_rejects_conflicting_resource_binding(monkeypatch):
    monkeypatch.setattr(settings, 'enable_rfc9396', True)
    with pytest.raises(ValueError):
        normalize_authorization_details(
            {'type': 'payment_initiation', 'locations': ['https://rs.example/payments']},
            resource='https://other.example/resource',
        )
