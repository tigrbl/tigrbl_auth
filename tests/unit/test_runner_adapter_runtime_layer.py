from __future__ import annotations

from tigrbl_auth_backend_app_core import app as api_app, build_application_runtime_plan
from tigrbl_auth_backend_app_public import app as package_app
from tigrbl_auth.config.deployment import resolve_deployment
from tigrbl_auth.gateway import build_gateway_runtime_plan
from tigrbl_auth.runtime import build_runtime_hash_matrix, get_runner_adapter, registered_runner_names
from tigrbl_auth.cli.main import build_parser


EXPECTED_RUNNERS = {"uvicorn", "hypercorn", "tigrcorn"}


def test_runner_registry_and_layer_90_apps_are_present():
    assert EXPECTED_RUNNERS == set(registered_runner_names())
    assert callable(api_app)
    assert callable(package_app)


def test_runtime_plan_hashing_is_application_invariant_across_runners():
    deployment = resolve_deployment(profile="baseline", runtime_style="standalone")
    matrix = build_runtime_hash_matrix(deployment=deployment, environment="test")

    assert EXPECTED_RUNNERS == set(matrix)
    assert len({payload["application_hash"] for payload in matrix.values()}) == 1
    assert len({payload["runtime_hash"] for payload in matrix.values()}) == len(EXPECTED_RUNNERS)


def test_runtime_plans_separate_carrier_neutral_and_composed_factories():
    plan = build_application_runtime_plan(runner="uvicorn", environment="test")
    gateway_plan = build_gateway_runtime_plan(runner="hypercorn", environment="test")

    assert plan.runner == "uvicorn"
    assert gateway_plan.runner == "hypercorn"
    assert plan.app_factory == "tigrbl_auth_backend_app_core.app.build_app"
    assert gateway_plan.app_factory == "unbound"
    assert len(plan.runner_capabilities) > 0
    assert len(gateway_plan.runner_flag_metadata) > 0


def test_cli_serve_accepts_runner_profile_selection():
    parser = build_parser()
    args = parser.parse_args(["serve", "--server", "hypercorn", "--format", "json"])

    assert args.server == "hypercorn"
    assert args.command == "serve"


def test_tigrcorn_adapter_contract_is_declared_even_when_not_installed():
    adapter = get_runner_adapter("tigrcorn")
    plan = build_gateway_runtime_plan(runner="tigrcorn", environment="test")
    diagnostics = adapter.validate(plan)

    assert adapter.name == "tigrcorn"
    assert len(adapter.capabilities) > 0
    assert any(item.code == "runner-not-installed" for item in diagnostics) or adapter.is_available()
