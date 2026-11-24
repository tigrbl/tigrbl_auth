from tba_router_oauth_device_authorization import build_device_authorization_router


async def handler(**kwargs):
    raise AssertionError("This example only registers routes")


def get_db():
    raise AssertionError("This example does not access storage")


router = build_device_authorization_router(
    device_authorization_request=handler,
    get_db=get_db,
)
paths = {
    getattr(route, "path", None) or getattr(route, "path_template", None)
    for route in router.routes
}
assert "/device_authorization" in paths
