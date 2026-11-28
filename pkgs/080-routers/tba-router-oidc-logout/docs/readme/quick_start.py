from tba_router_oidc_logout import build_logout_router


async def handler(**kwargs):
    raise AssertionError("This example only registers routes")


def get_db():
    raise AssertionError("This example does not access storage")


router = build_logout_router(
    logout_request=handler,
    get_db=get_db,
)
paths = {
    getattr(route, "path", None) or getattr(route, "path_template", None)
    for route in router.routes
}
assert "/logout" in paths
