import json

from tigrbl_auth.uix import RESOURCE_VIEW_METHODS, build_resource_views


def test_resource_views_are_backed_by_required_openrpc_methods():
    contract = json.loads(
        open("specs/openrpc/profiles/production/tigrbl_auth.admin.openrpc.json", encoding="utf-8").read()
    )
    available_methods = {method["name"] for method in contract["methods"]}
    views = build_resource_views(available_methods)

    assert set(views) == set(RESOURCE_VIEW_METHODS)
    assert all(view.backed for view in views.values())


def test_resource_views_do_not_require_unbacked_backend_methods():
    views = build_resource_views({"tenant.list", "tenant.show", "client.list"})

    assert views["tenants"].backed
    assert not views["clients"].backed
    assert views["clients"].missing_methods == ("client.show",)
