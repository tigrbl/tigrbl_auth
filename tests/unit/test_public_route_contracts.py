from tigrbl_auth.cli.artifacts import build_openapi_contract, deployment_from_options


def test_production_contract_exposes_capability_public_routes():
    deployment = deployment_from_options(profile="production")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    for path in ("/register", "/register/{client_id}", "/revoke", "/logout", "/introspect"):
        assert path in deployment.active_routes
        assert path in openapi["paths"]


def test_hardening_contract_exposes_capability_public_routes():
    deployment = deployment_from_options(profile="hardening")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    for path in ("/register", "/register/{client_id}", "/revoke", "/logout", "/introspect", "/device_authorization", "/par", "/token/exchange"):
        assert path in deployment.active_routes
        assert path in openapi["paths"]
