import pytest


pytestmark = pytest.mark.skip(reason="Admin UIX implementation pending; SSOT declares the expected behavior.")


def test_admin_uix_golden_path_from_login_to_dashboard_to_mutation_audit():
    pass
