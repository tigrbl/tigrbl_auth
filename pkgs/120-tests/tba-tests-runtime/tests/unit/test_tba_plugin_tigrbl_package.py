from __future__ import annotations

import inspect


def test_tba_plugin_tigrbl_package_owns_plugin_surface() -> None:
    from tba_plugin_tigrbl import TbaPlugin, install

    assert inspect.isclass(TbaPlugin)
    assert callable(install)
    assert TbaPlugin.__module__ == "tba_plugin_tigrbl.plugin"
    assert install.__module__ == "tba_plugin_tigrbl.plugin"


def test_identity_server_plugin_is_compatibility_export() -> None:
    from tba_plugin_tigrbl import TbaPlugin, install
    from tba_server_identity.plugin import TbaPlugin as server_plugin
    from tba_server_identity.plugin import install as server_install

    assert server_plugin is TbaPlugin
    assert server_install is install
