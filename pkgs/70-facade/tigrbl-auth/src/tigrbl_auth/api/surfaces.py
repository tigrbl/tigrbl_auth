"""Retired layer-70 HTTP-surface facade.

HTTP routers and assembled surfaces are owned by tigrbl-auth-backend-app-core.
The facade intentionally does not import layer 90.
"""


class BackendAppSurfaceMovedError(ImportError):
    pass


def __getattr__(name: str) -> object:
    raise BackendAppSurfaceMovedError(
        f"{name} moved to tigrbl_auth_backend_app_core.surfaces"
    )


__all__: list[str] = []
