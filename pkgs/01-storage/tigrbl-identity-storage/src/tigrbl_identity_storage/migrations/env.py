"""Migration environment metadata and schema verification exports."""

from tigrbl_identity_storage.tables import RestOltpTable
from tigrbl_identity_storage.migrations.runtime import expected_table_names, verify_schema_async, verify_schema_sync

TARGET_METADATA = RestOltpTable.metadata

__all__ = ["TARGET_METADATA", "expected_table_names", "verify_schema_async", "verify_schema_sync"]
