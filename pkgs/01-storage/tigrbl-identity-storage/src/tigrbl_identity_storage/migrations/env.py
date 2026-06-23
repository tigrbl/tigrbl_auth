"""Migration environment metadata exports."""

from tigrbl_identity_storage.tables import RestOltpTable

TARGET_METADATA = RestOltpTable.metadata

__all__ = ["TARGET_METADATA"]
