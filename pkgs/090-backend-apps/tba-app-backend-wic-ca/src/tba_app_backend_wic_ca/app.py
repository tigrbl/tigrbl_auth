"""ASGI application factory for the TBA WIC CA."""

from collections.abc import Awaitable, Callable

from tigrbl import Request, TigrblApp
from tba_router_wic_ca import build_wic_ca_router
from tba_runtime_identity.workload.enrollment import ResolveWorkloadIdentity

from .dependencies import build_wic_service
from .settings import WicCaSettings


def build_app(
    settings: WicCaSettings,
    *,
    authenticate: Callable[[Request], Awaitable[str | None]],
    resolve_identity: ResolveWorkloadIdentity,
    ca_key_password: bytes | None = None,
) -> TigrblApp:
    """Build a CA with a deployment-supplied workload authenticator."""
    service = build_wic_service(
        settings, resolve_identity=resolve_identity, ca_key_password=ca_key_password
    )
    app = TigrblApp()
    app.include_router(build_wic_ca_router(service=service, authenticate=authenticate))
    return app
