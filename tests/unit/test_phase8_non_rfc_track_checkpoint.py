from __future__ import annotations

import json
from http import HTTPStatus
from pathlib import Path

from tigrbl_auth.app import _package_default_profile
from tigrbl_auth.cli.artifacts import build_effective_claims_manifest, deployment_from_options

ROOT = Path(__file__).resolve().parents[2]


def test_http_status_compat_aliases_are_installed() -> None:
    assert HTTPStatus.HTTP_200_OK == 200
    assert HTTPStatus.HTTP_401_UNAUTHORIZED == 401
    assert HTTPStatus.HTTP_404_NOT_FOUND == 404


def test_package_default_profile_uses_production_when_global_profile_is_baseline() -> None:
    assert _package_default_profile() == 'production'


def test_step8_effective_claims_include_baseline_openrpc_contract() -> None:
    deployment = deployment_from_options(profile='production')
    manifest = build_effective_claims_manifest(ROOT, deployment, profile_label='production-test')
    claims = manifest['claim_set']['claims']
    assert any(item['target'] == 'OpenRPC 1.4.x admin/control-plane contract' for item in claims)


def test_non_rfc_status_report_tracks_zero_scope_discrepancies() -> None:
    payload = json.loads((ROOT / 'docs' / 'compliance' / 'non_rfc_status_report.json').read_text(encoding='utf-8'))
    assert payload['summary']['non_rfc_target_count'] == 18
    assert payload['summary']['non_rfc_targets_with_scope_discrepancies'] == 0
    assert payload['summary']['non_rfc_targets_internally_backed_now'] == 18
