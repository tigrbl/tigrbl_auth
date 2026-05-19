"""
tigrbl_auth.adapters.local_adapter
──────────────────
Concrete implementation of the ``AuthNProvider`` ABC declared by
``tigrbl.authn_abc``.  It merely **adapts** the public helpers that already
exist in *tigrbl_auth* so that Tigrbl can consume them automatically.

Usage
-----
>>> from tigrbl_auth.framework import TigrblRouter
>>> from tigrbl_auth.adapters import LocalAuthNAdapter
>>> api = TigrblRouter(engine=ENGINE, authn=LocalAuthNAdapter())
"""

from __future__ import annotations

from tigrbl_auth.framework import AuthNProvider, Request
from tigrbl_auth.security.auth import get_principal
from tigrbl_auth.security.context import principal_var  # noqa: F401  # ensure ContextVar is initialised
from .auth_context import set_auth_context


class LocalAuthNAdapter(AuthNProvider):
    """
    Thin wrapper that plugs existing *tigrbl_auth* functions into
    the abstract interface expected by Tigrbl.
    """

    # ------------------------------------------------------------------ #
    # Tigrbl dependency (mandatory)                                     #
    # ------------------------------------------------------------------ #
    async def get_principal(self, request: Request) -> dict:  # noqa: D401
        """
        Delegate to ``tigrbl_auth.security.deps.get_principal`` and forward
        whatever dict it returns.

        Raises
        ------
        tigrbl.types.HTTPException(401)
            If the API‑key / bearer token is invalid or expired.
        """
        principal = await get_principal(request)  # type: ignore[arg-type]
        set_auth_context(request, principal)
        return principal


__all__ = ["LocalAuthNAdapter"]
