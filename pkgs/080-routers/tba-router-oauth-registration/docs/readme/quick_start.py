from tba_router_oauth_registration import build_client_registration_router


async def handler(**kwargs):
    raise AssertionError("This example only registers routes")


def get_db():
    raise AssertionError("This example does not access storage")


router = build_client_registration_router(
    register_client=handler,
    get_registration=handler,
    update_registration=handler,
    delete_registration=handler,
    get_db=get_db,
)
paths = {
    getattr(route, "path", None) or getattr(route, "path_template", None)
    for route in router.routes
}
assert "/register" in paths
