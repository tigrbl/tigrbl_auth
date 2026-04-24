import pytest


pytestmark = pytest.mark.skip(reason="Admin UIX implementation pending; SSOT declares the expected behavior.")


def test_resource_views_are_backed_by_required_openrpc_methods():
    pass


def test_resource_views_do_not_require_unbacked_backend_methods():
    pass
