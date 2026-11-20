from tba_storage_core.tables import Federation as CanonicalFederation
from tba_auth.services.advanced_identity_plane import (
    Federation,
)


def test_federation_surface_exports_storage_table_registry() -> None:
    assert Federation is CanonicalFederation
