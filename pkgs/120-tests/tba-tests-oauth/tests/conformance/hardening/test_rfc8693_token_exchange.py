from tba_auth.cli.artifacts import build_openapi_contract, deployment_from_options


def test_rfc8693_token_exchange_route_is_active_in_hardening():
    deployment = deployment_from_options(profile="hardening")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    assert "/token/exchange" in deployment.active_routes
    assert "/token/exchange" in openapi["paths"]
