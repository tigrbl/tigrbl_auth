
from tigrbl_auth.cli.artifacts import build_openapi_contract, build_openrpc_contract, deployment_from_options

def test_live_contract_generation_has_paths_and_methods():
    deployment = deployment_from_options(profile='baseline')
    openapi = build_openapi_contract(deployment, version='0.0.0-test')
    openrpc = build_openrpc_contract(deployment, version='0.0.0-test')
    assert openapi['paths']
    assert openrpc['methods'] == []

    admin_deployment = deployment_from_options(profile='baseline', plugin_mode='mixed')
    admin_openrpc = build_openrpc_contract(admin_deployment, version='0.0.0-test')
    assert admin_openrpc['methods'] == []
    assert admin_openrpc['x-tigrbl-auth']['generation_mode'] == 'rest-only-no-rpc'
