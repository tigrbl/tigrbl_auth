"""Tigrbl-native engine and DB dependency wiring."""

from tigrbl import bootstrap_dbschema
from tigrbl.ddl import sqlite_default_attach_map

from tigrbl_identity_storage.framework import build_engine
from tigrbl_identity_runtime.settings import settings

if settings.pg_dsn_env or (settings.pg_host and settings.pg_db and settings.pg_user):
    dsn = settings.apg_dsn
else:
    dsn = "sqlite+aiosqlite:///./authn.db"

ENGINE = build_engine(dsn)


def _bootstrap_runtime_engine() -> None:
    provider = getattr(ENGINE, "provider", None)
    if provider is None:
        return
    try:
        raw_engine, _ = provider.ensure()
    except Exception:
        return
    dialect = getattr(getattr(raw_engine, "dialect", None), "name", "")
    if dialect != "sqlite":
        return
    attachments = sqlite_default_attach_map(raw_engine, ("authn",))
    bootstrap_dbschema(
        raw_engine,
        schemas=("authn",),
        sqlite_attachments=attachments,
        immediate=False,
    )


_bootstrap_runtime_engine()
get_db = ENGINE.get_db

__all__ = ["ENGINE", "dsn", "get_db"]
