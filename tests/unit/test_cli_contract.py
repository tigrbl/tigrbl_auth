from __future__ import annotations

import json
from pathlib import Path

from tigrbl_auth.cli.main import main
from tigrbl_auth.cli.metadata import build_cli_conformance_snapshot, build_cli_contract_manifest, build_parser
from tigrbl_auth.cli.reports import generate_state_reports
from tigrbl_auth.services._operator_store import resource_state_path, operator_state_root


ROOT = Path(__file__).resolve().parents[2]


def _nested_choices(parser, command: str) -> set[str]:
    command_parser = parser._subparsers._group_actions[0].choices[command]
    nested = next(action for action in command_parser._actions if action.__class__.__name__ == "_SubParsersAction")
    return set(nested.choices)


def test_cli_contract_exposes_required_lifecycle_verbs_and_no_catalog_only_resources():
    parser = build_parser()
    assert {"status", "manifest", "apply", "verify"} <= _nested_choices(parser, "bootstrap")
    assert {"status", "plan", "apply", "verify"} <= _nested_choices(parser, "migrate")
    assert {"create", "update", "delete", "get", "list", "enable", "disable"} <= _nested_choices(parser, "tenant")
    assert {"generate", "import", "export", "rotate", "retire", "publish-jwks", "get", "list", "delete"} <= _nested_choices(parser, "keys")
    assert {"show", "validate", "publish", "diff"} <= _nested_choices(parser, "discovery")

    snapshot = build_cli_conformance_snapshot()
    assert snapshot["summary"]["passed"] is True
    assert snapshot["summary"]["missing_required_verbs"] == {}
    assert snapshot["summary"]["catalog_only_resource_commands"] == []


def test_cli_contract_manifest_includes_outputs_exit_codes_and_help_snapshots():
    contract = build_cli_contract_manifest()
    summary = contract["summary"]

    assert summary["command_count"] >= 20
    assert summary["verb_count"] >= 82
    assert summary["global_flag_count"] >= 15

    tenant = next(item for item in contract["commands"] if item["name"] == "tenant")
    create = next(item for item in tenant["verbs"] if item["name"] == "create")
    assert create["output"]["name"] == "resource-record"
    assert any(code["code"] == 3 for code in create["exit_codes"])

    help_snapshots = build_cli_conformance_snapshot()["help_snapshots"]
    assert "tigrbl-auth tenant create" in help_snapshots
    assert "--set" in help_snapshots["tigrbl-auth tenant create"]
    assert "--if-exists" in help_snapshots["tigrbl-auth tenant create"]
    assert "--timeout" in help_snapshots["tigrbl-auth tenant create"]
    assert "tigrbl-auth keys generate" in help_snapshots
    assert "--publish" in help_snapshots["tigrbl-auth keys generate"]


def test_stateful_resource_handlers_are_durable_and_not_catalog_only(tmp_path: Path):
    repo_root = tmp_path
    create_rc = main([
        "tenant",
        "create",
        "--repo-root",
        str(repo_root),
        "--id",
        "tenant-capability",
        "--set",
        "name=Tenant browser-session checkpoint",
        "--yes",
    ])
    list_rc = main([
        "tenant",
        "list",
        "--repo-root",
        str(repo_root),
        "--format",
        "json",
    ])
    enable_rc = main([
        "tenant",
        "disable",
        "--repo-root",
        str(repo_root),
        "--id",
        "tenant-capability",
        "--yes",
    ])

    state_path = resource_state_path(repo_root, "tenant")
    store = json.loads(state_path.read_text(encoding="utf-8"))
    operator_root = operator_state_root(repo_root)

    assert create_rc == 0
    assert list_rc == 0
    assert enable_rc == 0
    assert "tenant-capability" in store
    assert store["tenant-capability"]["status"] == "disabled"
    assert store["tenant-capability"]["resource"] == "tenant"
    assert state_path.is_file()
    assert (operator_root / "operator_plane.sqlite3").exists()
    assert repo_root.resolve() not in operator_root.resolve().parents


def test_state_report_tracks_cli_contract_checkpoint():
    payload = generate_state_reports(ROOT)
    summary = payload["current_state"]
    gaps = payload["certification_state"]["open_gaps"]

    assert summary["cli_command_count"] >= 20
    assert summary["cli_verb_count"] >= 82
    assert summary["cli_catalog_only_resource_command_count"] == 0
    assert summary["cli_required_verbs_missing"] is False
    assert summary["cli_metadata_to_docs_sync_passed"] is True
    assert not any("Current generated public artifacts still drift from executable reality." in gap for gap in gaps)
