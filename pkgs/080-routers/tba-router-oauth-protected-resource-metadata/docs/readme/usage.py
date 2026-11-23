from tigrbl import TigrblApp
from tba_router_oauth_protected_resource_metadata import (
    build_protected_resource_metadata_router,
    include_protected_resource_metadata,
)


async def metadata(request):
    return {
        "resource": "https://api.example",
        "authorization_servers": ["https://issuer.example"],
    }


app = TigrblApp()
router = build_protected_resource_metadata_router(protected_resource_metadata=metadata)
include_protected_resource_metadata(app, router, enabled=True)
assert any(
    (getattr(route, "path", None) or getattr(route, "path_template", None))
    == "/.well-known/oauth-protected-resource"
    for route in app.router.routes
)
