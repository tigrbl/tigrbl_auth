from tigrbl_auth.cli.artifacts import build_openrpc_contract, deployment_from_options


def test_rpc_registry_surface_is_not_supported():
    try:
        import tigrbl_auth.api.rpc  # noqa: F401
    except ModuleNotFoundError:
        return
    raise AssertionError("tigrbl_auth.api.rpc must not be importable")


def test_openrpc_contract_is_empty_compatibility_artifact():
    deployment = deployment_from_options(profile="production", plugin_mode="mixed")
    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    assert contract["methods"] == []
    assert contract["x-tigrbl-auth"]["generation_mode"] == "rest-only-no-rpc"
