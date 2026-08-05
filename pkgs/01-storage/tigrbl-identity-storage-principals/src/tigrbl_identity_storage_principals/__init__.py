"""Standalone identity storage component."""

from .manifest import MANIFEST, load_manifest
from .tables import *  # noqa: F401,F403
from .tables import TABLE_MODEL_BY_NAME, TABLE_MODEL_BY_TABLENAME, TABLE_MODELS

__all__ = ["MANIFEST", "load_manifest", "TABLE_MODELS", "TABLE_MODEL_BY_NAME", "TABLE_MODEL_BY_TABLENAME"] + [model.__name__ for model in TABLE_MODELS]
