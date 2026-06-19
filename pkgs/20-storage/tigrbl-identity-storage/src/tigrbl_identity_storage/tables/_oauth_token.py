"""OAuth 2.0 token endpoint public operation surface.

The endpoint implementation is split into named modules, but this module remains
the stable import and monkeypatch surface for protocol tests and legacy facades.
"""
from __future__ import annotations

from . import _oauth_token_endpoint as _endpoint
from . import _oauth_token_runtime as _runtime

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


def _sync_endpoint_runtime() -> None:
    for name in _SYNC_NAMES:
        if name in globals():
            setattr(_runtime, name, globals()[name])
            setattr(_endpoint, name, globals()[name])


async def token_request(*, request, db):
    _sync_endpoint_runtime()
    return await _endpoint.token_request(request=request, db=db)


__all__ = [name for name in globals() if not name.startswith("__")]
