"""Shared primitives for independently installable identity table packages."""

from .framework import *  # noqa: F401,F403
from .metadata import table_names_for_models, tables_for_models
from .relationships import bind_relationship
from .schema import AUTHN_SCHEMA

__all__ = ["AUTHN_SCHEMA", "bind_relationship", "table_names_for_models", "tables_for_models"]
