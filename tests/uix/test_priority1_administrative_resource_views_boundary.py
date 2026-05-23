from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPERATOR_SRC = ROOT / "pkgs" / "tigrbl-identity-operator" / "src"
if str(OPERATOR_SRC) not in sys.path:
    sys.path.append(str(OPERATOR_SRC))

import tigrbl_identity_operator.uix as operator_uix  # noqa: E402

from tigrbl_auth.uix import (  # noqa: E402
    ADMINISTRATIVE_RESOURCE_VIEW_FEATURES,
    RESOURCE_VIEW_METHODS,
    administrative_resource_views_boundary_integrity,
    administrative_resource_views_boundary_manifest,
    build_resource_views,
)


BOUNDARY_FEATURE_IDS = {
    "feat:uix-tenant-admin-view",
    "feat:uix-client-admin-view",
    "feat:uix-identity-admin-view",
    "feat:uix-session-admin-view",
    "feat:uix-token-admin-view",
    "feat:uix-consent-admin-view",
    "feat:uix-audit-admin-view",
    "feat:uix-keys-jwks-admin-view",
    "feat:uix-profile-certification-view",
}


def _admin_openrpc_methods() -> set[str]:
    contract = json.loads(
        (ROOT / "specs/openrpc/profiles/baseline-development/tigrbl_auth.admin.openrpc.json").read_text(
            encoding="utf-8"
        )
    )
    return {method["name"] for method in contract["methods"]}


def test_priority1_administrative_resource_views_boundary_t0_inventory_tracks_all_features():
    manifest = administrative_resource_views_boundary_manifest()
    integrity = administrative_resource_views_boundary_integrity()
    operator_manifest = operator_uix.administrative_resource_views_boundary_manifest()
    operator_integrity = operator_uix.administrative_resource_views_boundary_integrity()

    assert set(manifest) == BOUNDARY_FEATURE_IDS
    assert set(ADMINISTRATIVE_RESOURCE_VIEW_FEATURES) == BOUNDARY_FEATURE_IDS
    assert manifest == operator_manifest
    assert integrity["passed"] is True
    assert operator_integrity["passed"] is True
    assert integrity["feature_count"] == 9
    assert set(integrity["views"]) == set(RESOURCE_VIEW_METHODS)


def test_priority1_administrative_resource_views_boundary_t1_backs_all_views_from_openrpc_contract():
    views = build_resource_views(_admin_openrpc_methods())

    assert tuple(views) == (
        "tenants",
        "clients",
        "identities",
        "sessions",
        "tokens",
        "consents",
        "audit",
        "keys-jwks",
        "profile-certification",
    )
    assert all(view.backed for view in views.values())
    for view_name, view in views.items():
        assert view.required_methods == RESOURCE_VIEW_METHODS[view_name]
        assert view.states == ("empty", "loading", "error", "filtered", "detail")


def test_priority1_administrative_resource_views_boundary_t2_reports_missing_methods_fail_closed():
    available = _admin_openrpc_methods()
    available.remove("client.show")
    available.remove("keys.list")
    available.remove("evidence.status")

    views = build_resource_views(available)

    assert views["tenants"].backed
    assert views["clients"].missing_methods == ("client.show",)
    assert views["keys-jwks"].missing_methods == ("keys.list",)
    assert views["profile-certification"].missing_methods == ("evidence.status",)
    assert not views["clients"].backed
    assert not views["keys-jwks"].backed
    assert not views["profile-certification"].backed
