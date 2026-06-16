"""Dynamic client registration public operation surface.

RFC 7591/7592 endpoint callables live here; validation, access checks, and
presentation helpers live in named runtime modules.
"""
from __future__ import annotations

from . import registration_endpoint as _endpoint
from . import registration_runtime as _runtime

globals().update(
    {
        name: value
        for name, value in _runtime.__dict__.items()
        if not name.startswith("__")
    }
)

_SYNC_NAMES = tuple(
    name
    for name in _runtime.__dict__
    if not name.startswith("__")
)
_RUNTIME_HELPER_NAMES = {
    "_load_client_and_registration",
    "_registration_response",
    "_require_registration_access",
    "_resolve_registration_tenant",
    "_tenant_from_operator_record",
    "_validated_registration_payload",
    "_validated_token_endpoint_auth_method",
}
_runtime_registration_response = _runtime._registration_response
_runtime_require_registration_access = _runtime._require_registration_access
_runtime_validated_registration_payload = _runtime._validated_registration_payload


def _sync_endpoint_runtime() -> None:
    for name in _SYNC_NAMES:
        if name in globals():
            if name not in _RUNTIME_HELPER_NAMES:
                setattr(_runtime, name, globals()[name])
            setattr(_endpoint, name, globals()[name])


async def _validated_registration_payload(*args, **kwargs):
    _sync_endpoint_runtime()
    return await _runtime_validated_registration_payload(*args, **kwargs)


async def _require_registration_access(*args, **kwargs):
    _sync_endpoint_runtime()
    return await _runtime_require_registration_access(*args, **kwargs)


async def _registration_response(*args, **kwargs):
    _sync_endpoint_runtime()
    return await _runtime_registration_response(*args, **kwargs)


async def register_client(*, request, db, payload: DynamicClientRegistrationIn | None = None):
    _sync_endpoint_runtime()
    return await _endpoint.register_client(request=request, db=db, payload=payload)


async def get_registered_client(*, request, db, client_id: str):
    _sync_endpoint_runtime()
    return await _endpoint.get_registered_client(request=request, db=db, client_id=client_id)


async def update_registered_client(
    *,
    request,
    db,
    client_id: str,
    payload: DynamicClientRegistrationManagementIn | None = None,
):
    _sync_endpoint_runtime()
    return await _endpoint.update_registered_client(
        request=request,
        db=db,
        client_id=client_id,
        payload=payload,
    )


async def delete_registered_client(*, request, db, client_id: str):
    _sync_endpoint_runtime()
    return await _endpoint.delete_registered_client(request=request, db=db, client_id=client_id)


__all__ = [name for name in globals() if not name.startswith("__")]
