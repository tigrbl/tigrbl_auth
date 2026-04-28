from pathlib import Path

import yaml

from tigrbl_auth.cli.main import build_parser


ROOT = Path(__file__).resolve().parents[2]


def _load_yaml(path: str):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_runtime_and_operator_manifests_exist_with_expected_labels():
    runtime = _load_yaml("compliance/targets/runtime-targets.yaml")
    operator = _load_yaml("compliance/targets/operator-targets.yaml")
    runtime_labels = {item["label"] for item in runtime["targets"]}
    operator_labels = {item["label"] for item in operator["targets"]}
    assert {
        "ASGI 3 application package",
        "Runner profile: Uvicorn",
        "Runner profile: Hypercorn",
        "Runner profile: Tigrcorn",
    } <= runtime_labels
    assert {
        "CLI operator surface",
        "Bootstrap and migration lifecycle",
        "Key lifecycle and JWKS publication",
        "Import/export portability",
        "Release bundle and signature verification",
    } <= operator_labels


def test_declared_claims_include_runtime_and_operator_targets():
    claims = _load_yaml("compliance/claims/declared-target-claims.yaml")
    labels = {item["target"] for item in claims["claim_set"]["claims"]}
    assert "ASGI 3 application package" in labels
    assert "CLI operator surface" in labels
    assert "Release bundle and signature verification" in labels


def test_cli_uses_keys_as_canonical_command():
    parser = build_parser()
    commands = parser._subparsers._group_actions[0].choices
    assert "keys" in commands
    assert "key" not in commands


def test_boundary_freeze_decision_is_recorded():
    scope = _load_yaml("compliance/targets/certification_scope.yaml")
    freeze = scope["boundary_freeze"]
    assert freeze["decision_id"] == "BND-012"
    assert freeze["retained_target_count"] == 48
    assert freeze["retained_rfc_target_count"] == 30
    assert freeze["retained_non_rfc_target_count"] == 18
