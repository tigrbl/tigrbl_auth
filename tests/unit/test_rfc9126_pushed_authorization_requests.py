import pytest
from tigrbl_auth.tables.pushed_authorization_request import (
    PushedAuthorizationRequest,
    DEFAULT_PAR_EXPIRY,
)
from tigrbl_auth_protocol_oauth.standards.pushed_authorization_requests import (
    PushedAuthorizationDisabledError,
)
from tigrbl_identity_server.security.pushed_authorization import (
    build_rfc9126_pushed_authorization_service,
)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_par_returns_request_uri_and_expires(enable_rfc9126, db_session):
    obj = await PushedAuthorizationRequest.handlers.create.core(
        {"payload": {"params": {"client_id": "abc"}}, "db": db_session}
    )
    assert obj.request_uri.startswith("urn:ietf:params:oauth:request_uri:")
    assert obj.expires_in == DEFAULT_PAR_EXPIRY


@pytest.mark.unit
@pytest.mark.asyncio
async def test_par_runtime_composition_disables_rfc9126_before_persistence():
    service = build_rfc9126_pushed_authorization_service(
        object(),
        type("Settings", (), {"enable_rfc9126": False})(),
    )
    with pytest.raises(PushedAuthorizationDisabledError):
        await service.push(client_id="client-1", tenant_id=None, params={})
