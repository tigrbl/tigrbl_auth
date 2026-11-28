"""HTTP route composition for the My Account API product."""

from __future__ import annotations

from tigrbl import TigrblRouter

from .consents import router as consent_router
from .profiles import router as profile_router
from .sessions import router as session_router


router = TigrblRouter()
router.include_router(profile_router)
router.include_router(session_router)
router.include_router(consent_router)


__all__ = ["router"]
