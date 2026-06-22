from __future__ import annotations

import inspect


def test_tigrbl_auth_plugin_package_owns_plugin_surface() -> None:
    from tigrbl_auth_plugin import TigrblAuthPlugin, install

    assert inspect.isclass(TigrblAuthPlugin)
    assert callable(install)
    assert TigrblAuthPlugin.__module__ == "tigrbl_auth_plugin.plugin"
    assert install.__module__ == "tigrbl_auth_plugin.plugin"


def test_identity_server_plugin_is_compatibility_export() -> None:
    from tigrbl_auth_plugin import TigrblAuthPlugin, install
    from tigrbl_identity_server.plugin import TigrblAuthPlugin as server_plugin
    from tigrbl_identity_server.plugin import install as server_install

    assert server_plugin is TigrblAuthPlugin
    assert server_install is install
