from tigrbl_auth.uix import RESOURCE_VIEW_METHODS, build_resource_views


def test_resource_views_handle_empty_loading_error_filtered_and_detail_states():
    views = build_resource_views(
        method for required in RESOURCE_VIEW_METHODS.values() for method in required
    )

    for view in views.values():
        assert view.states == ("empty", "loading", "error", "filtered", "detail")


def test_resource_views_cover_tenants_clients_identities_sessions_tokens_consents_audits_keys_and_profiles():
    views = build_resource_views(
        method for required in RESOURCE_VIEW_METHODS.values() for method in required
    )

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
