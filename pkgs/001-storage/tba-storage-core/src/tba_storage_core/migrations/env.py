"""Migration environment metadata exports."""

from tba_storage_core.tables import RestOltpTable

TARGET_METADATA = RestOltpTable.metadata

__all__ = ["TARGET_METADATA"]
