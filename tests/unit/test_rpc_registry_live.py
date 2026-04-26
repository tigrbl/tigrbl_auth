from tigrbl_auth.api.rpc import get_rpc_method_registry, iter_active_rpc_methods
from tigrbl_auth.cli.artifacts import build_openrpc_contract, deployment_from_options


REQUIRED_METHODS = {
    "rpc.discover",
    "client.registration.list",
    "client.registration.show",
    "client.registration.upsert",
    "session.list",
    "session.show",
    "session.terminate",
    "token.list",
    "token.inspect",
    "consent.list",
    "consent.show",
    "consent.revoke",
    "audit.list",
    "audit.export",
    "keys.list",
    "jwks.show",
    "keys.rotate",
    "profile.show",
    "target.list",
    "target.show",
}


def test_rpc_registry_contains_required_operator_methods():
    registry = get_rpc_method_registry()
    assert REQUIRED_METHODS <= set(registry)
    for name in REQUIRED_METHODS:
        meta = registry[name]
        assert meta["owner_module"].startswith("tigrbl_auth/api/rpc/methods/")
        assert meta["surface_set"] == "admin-rpc"


def test_openrpc_contract_is_derived_from_live_registry():
    deployment = deployment_from_options(profile="production", plugin_mode="mixed")
    contract = build_openrpc_contract(deployment, version="0.0.0-test")
    method_names = {item["name"] for item in contract["methods"]}
    expected = {item.name for item in iter_active_rpc_methods(deployment)}
    assert method_names == expected
    assert REQUIRED_METHODS <= method_names
    assert contract["x-tigrbl-auth"]["generation_mode"] == "implementation-backed-rpc-registry"
    assert contract["components"]["schemas"]
    for item in contract["methods"]:
        assert item["x-tigrbl-auth"]["owner_module"].startswith("tigrbl_auth/api/rpc/methods/")
        assert item["params"] is not None
        assert item["result"]["schema"]["$ref"].startswith("#/components/schemas/")
