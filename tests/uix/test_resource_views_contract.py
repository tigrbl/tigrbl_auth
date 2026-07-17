from tigrbl_auth.uix import RESOURCE_VIEW_OPERATIONS, build_resource_views
from tigrbl_operator_administration_capability import OPERATOR_ADMINISTRATION_OPERATIONS


def test_resource_views_are_backed_by_required_capability_operations():
    views = build_resource_views(set(OPERATOR_ADMINISTRATION_OPERATIONS))

    assert set(views) == set(RESOURCE_VIEW_OPERATIONS)
    assert all(view.backed for view in views.values())


def test_resource_views_do_not_require_unbacked_capability_operations():
    views = build_resource_views({"list_resources", "get_resource", "key_list"})

    assert views["tenants"].backed
    assert not views["keys-jwks"].backed
    assert views["keys-jwks"].missing_operations == ("key_get", "key_publish_jwks")
