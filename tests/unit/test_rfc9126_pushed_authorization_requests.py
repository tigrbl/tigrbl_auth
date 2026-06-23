import pytest
from http import HTTPStatus as status
from types import SimpleNamespace

from tigrbl_auth.tables.pushed_authorization_request import (
    PushedAuthorizationRequest,
    DEFAULT_PAR_EXPIRY,
)
from tigrbl_identity_storage_runtime import par as par_runtime


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
async def test_par_runtime_disabled_returns_404(monkeypatch):
    monkeypatch.setattr(par_runtime.settings, "enable_rfc9126", False)
    request = SimpleNamespace(body=b"", app=None)
    with pytest.raises(par_runtime.HTTPException) as exc:
        await par_runtime.pushed_authorization_request(request=request, db=None)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
