"""Reusable Tigrbl ORM authoring surface for identity storage packages.

This optional module centralizes stable imports without creating a storage-layer
package dependency. Importing the rest of :mod:`tigrbl_identity_core` remains
dependency-light and does not import Tigrbl or SQLAlchemy.
"""

from __future__ import annotations

from tigrbl import ForeignKeySpec, RestOltpTable
from tigrbl.orm.mixins import (
    ActiveToggle,
    Bootstrappable,
    Created,
    GUIDPk,
    KeyDigest,
    LastUsed,
    Principal,
    TenantBound,
    TenantColumn,
    Timestamped,
    UserColumn,
    ValidityWindow,
)
from tigrbl.orm.tables import Client as ClientBase
from tigrbl.orm.tables import Tenant as TenantBase
from tigrbl.orm.tables import User as UserBase
from tigrbl.shortcuts.column import ColumnSpec, F, IO, S, acol
from tigrbl.types import (
    Boolean,
    Integer,
    JSON,
    LargeBinary,
    Mapped,
    PgUUID,
    String,
    TZDateTime,
    UUID,
    relationship,
)

AUTHN_SCHEMA = "authn"

__all__ = [
    "AUTHN_SCHEMA",
    "ActiveToggle",
    "Boolean",
    "Bootstrappable",
    "ClientBase",
    "ColumnSpec",
    "Created",
    "F",
    "ForeignKeySpec",
    "GUIDPk",
    "IO",
    "Integer",
    "JSON",
    "KeyDigest",
    "LargeBinary",
    "LastUsed",
    "Mapped",
    "PgUUID",
    "Principal",
    "RestOltpTable",
    "S",
    "String",
    "TZDateTime",
    "TenantBase",
    "TenantBound",
    "TenantColumn",
    "Timestamped",
    "UUID",
    "UserBase",
    "UserColumn",
    "ValidityWindow",
    "acol",
    "relationship",
]
