from tba_auth.cli.artifacts import build_openapi_contract, deployment_from_options


def test_rfc8615_well_known_endpoints_are_published_in_production_contract() -> None:
    deployment = deployment_from_options(profile="production")
    openapi = build_openapi_contract(deployment, version="0.0.0-test")
    for path in (
        "/.well-known/openid-configuration",
        "/.well-known/oauth-authorization-server",
        "/.well-known/oauth-protected-resource",
        "/.well-known/jwks.json",
    ):
        assert path in deployment.active_routes
        assert path in openapi["paths"]
