"""Owned mapped-table inventory."""

from .scim_group import ScimGroupRecord
from .scim_patch_event import ScimPatchEvent
from .scim_schema import ScimSchemaRecord
from .scim_user import ScimUserRecord

TABLE_MODELS = (
    ScimSchemaRecord,
    ScimUserRecord,
    ScimGroupRecord,
    ScimPatchEvent,
)
TABLE_MODEL_BY_NAME = {model.__name__: model for model in TABLE_MODELS}
TABLE_MODEL_BY_TABLENAME = {model.__tablename__: model for model in TABLE_MODELS}
__all__ = [model.__name__ for model in TABLE_MODELS] + [
    "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME",
]
