"""HTTP route composition for the My Account API product."""

from __future__ import annotations

from tigrbl import TigrblRouter

from .consents import api as consent_api
from .profiles import api as profile_api
from .sessions import api as session_api


api = router = TigrblRouter()
api.include_router(profile_api)
api.include_router(session_api)
api.include_router(consent_api)


__all__ = ["api", "router"]
