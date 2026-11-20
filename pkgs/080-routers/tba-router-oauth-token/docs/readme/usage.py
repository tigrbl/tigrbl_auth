from tba_router_oauth_token import build_token_router


async def handler(**kwargs):
    raise AssertionError("This example only registers routes")


def get_db():
    raise AssertionError("This example does not access storage")


router = build_token_router(
    token_request=handler,
    get_db=get_db,
)
paths = {
    getattr(route, "path", None) or getattr(route, "path_template", None)
    for route in router.routes
}
assert "/token" in paths
