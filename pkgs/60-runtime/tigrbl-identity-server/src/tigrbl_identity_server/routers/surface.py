"""
tigrbl_identity_server.routers.surface
======================================

Table-backed API surface for the authentication service.

Exports
-------
Base        : Declarative base for all models in **tigrbl_authn**.
metadata    : Shared SQLAlchemy ``MetaData`` with a sane naming-convention.
surface_api : ``TigrblRouter`` combining Tigrbl resources and REST flows.

The resulting ``surface_api`` exposes a REST surface under
namespaces like ``surface_api.core.User.create`` and
``surface_api.core_raw.User.create``.

Notes
-----
*   Importing this module has the side-effect of importing
    ``tigrbl_identity_storage.tables``, so every model class is registered with the
    declarative base **before** Tigrbl introspects the metadata.
"""

from __future__ import annotations

from tigrbl_identity_server.framework import TigrblRouter
from tigrbl_identity_storage.tables import (
    Realm,
    Tenant,
    User,
    Client,
    ApiKey,
    Service,
    ServiceKey,
    AuthSession,
    PushedAuthorizationRequest,
    AuthCode,
)
from tigrbl_identity_storage.tables.engine import dsn
from tigrbl_identity_storage.tables.auth_code._auth_flows import api as flows_api

# ----------------------------------------------------------------------
# 3.  Build Tigrbl instance & router
# ----------------------------------------------------------------------
surface_api = TigrblRouter(engine=dsn)

surface_api.include_tables(
    [
        Realm,
        Tenant,
        User,
        Client,
        ApiKey,
        Service,
        ServiceKey,
        AuthSession,
        AuthCode,
        PushedAuthorizationRequest,
    ]
)

surface_api.include_router(flows_api)

__all__ = ["surface_api"]
