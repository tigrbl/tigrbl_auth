from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.integration


ROOT = Path(__file__).resolve().parents[2]


def _openapi(profile: str) -> dict:
    return json.loads((ROOT / 'specs' / 'openapi' / 'profiles' / profile / 'tigrbl_auth.public.openapi.json').read_text(encoding='utf-8'))


def _discovery(profile: str) -> dict:
    return json.loads((ROOT / 'specs' / 'discovery' / 'profiles' / profile / 'openid-configuration.json').read_text(encoding='utf-8'))


def test_profile_openapi_snapshots_publish_capability_and_capability_routes():
    baseline_paths = set(_openapi('baseline').get('paths', {}))
    production_paths = set(_openapi('production').get('paths', {}))
    hardening_paths = set(_openapi('hardening').get('paths', {}))

    assert '/register' in production_paths and '/register' in hardening_paths
    assert '/revoke' in production_paths and '/revoke' in hardening_paths
    assert '/logout' in production_paths and '/logout' in hardening_paths
    assert '/device_authorization' not in baseline_paths and '/device_authorization' not in production_paths
    assert '/device_authorization' in hardening_paths
    assert '/par' not in baseline_paths and '/par' not in production_paths
    assert '/par' in hardening_paths
    assert '/token/exchange' not in baseline_paths and '/token/exchange' not in production_paths
    assert '/token/exchange' in hardening_paths


def test_hardening_discovery_snapshot_matches_runtime_allow_deny_policy():
    hardening = _discovery('hardening')
    production = _discovery('production')

    assert 'password' not in set(hardening.get('grant_types_supported', []))
    assert 'password' in set(production.get('grant_types_supported', []))

    hardening_response_types = set(hardening.get('response_types_supported', []))
    assert 'token' not in hardening_response_types
    assert 'id_token' not in hardening_response_types
    assert 'id_token token' not in hardening_response_types
    assert 'code' in hardening_response_types

    assert hardening.get('pushed_authorization_request_endpoint')
    assert hardening.get('dpop_signing_alg_values_supported')
