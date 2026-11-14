from tba_auth.cli.artifacts import build_openapi_contract, deployment_from_options


def test_rfc7592_management_route_is_published_in_hardening_contract():
    deployment = deployment_from_options(profile="hardening")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert "/register/{client_id}" in deployment.active_routes
    assert "/register/{client_id}" in openapi["paths"]
    assert set(openapi["paths"]["/register/{client_id}"]) == {"get", "put", "delete"}
