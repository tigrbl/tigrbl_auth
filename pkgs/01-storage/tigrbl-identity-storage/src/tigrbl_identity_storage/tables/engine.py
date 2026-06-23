"""Tigrbl-native engine and DB dependency wiring."""

from contextlib import asynccontextmanager
import os
from typing import Any, AsyncIterator

from tigrbl import bootstrap_dbschema
from tigrbl.ddl import sqlite_default_attach_map

from tigrbl_identity_storage.framework import build_engine


def _async_postgres_dsn() -> str:
    dsn = os.environ.get("POSTGRES_URL") or os.environ.get("PG_DSN") or ""
    if not dsn:
        host = os.environ.get("PG_HOST")
        database = os.environ.get("PG_DB")
        user = os.environ.get("PG_USER")
        if host and database and user:
            password = os.environ.get("PG_PASS") or ""
            port = os.environ.get("PG_PORT") or "5432"
            dsn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    if dsn.startswith("postgresql://"):
        return dsn.replace("postgresql://", "postgresql+asyncpg://", 1)
    return dsn or os.environ.get("ASYNC_FALLBACK_DB", "")


_configured_dsn = _async_postgres_dsn()
if _configured_dsn:
    dsn = _configured_dsn
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


def resolve_storage_provider() -> Any:
    try:
        from tigrbl.engine import resolver as engine_resolver

        provider = engine_resolver.resolve_provider()
        if provider is not None:
            return provider
    except Exception:
        pass
    return ENGINE.provider


@asynccontextmanager
async def storage_session() -> AsyncIterator[Any]:
    provider = resolve_storage_provider()
    _, maker = provider.ensure()
    async with maker() as session:
        try:
            yield session
            commit = getattr(session, "commit", None)
            if callable(commit):
                result = commit()
                if hasattr(result, "__await__"):
                    await result
        except Exception:
            rollback = getattr(session, "rollback", None)
            if callable(rollback):
                result = rollback()
                if hasattr(result, "__await__"):
                    await result
            raise


__all__ = ["ENGINE", "dsn", "get_db", "resolve_storage_provider", "storage_session"]
