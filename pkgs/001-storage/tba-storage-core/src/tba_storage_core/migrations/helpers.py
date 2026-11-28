"""DDL helpers for executable repository-owned migrations."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol

from sqlalchemy import Column, ForeignKey, MetaData, Table, inspect, text
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError


class SupportsTable(Protocol):
    __table__: object


AUTHN_SCHEMA = "authn"
MIGRATION_TABLE = "schema_migrations"


def ensure_schema(conn) -> None:
    if conn.dialect.name != "sqlite":
        conn.exec_driver_sql(f"CREATE SCHEMA IF NOT EXISTS {AUTHN_SCHEMA}")


def ensure_migration_table(conn) -> None:
    ensure_schema(conn)
    if conn.dialect.name == "sqlite":
        conn.exec_driver_sql(
            f"CREATE TABLE IF NOT EXISTS {MIGRATION_TABLE} (revision VARCHAR(128) PRIMARY KEY, applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        return
    conn.exec_driver_sql(
        f"CREATE TABLE IF NOT EXISTS {AUTHN_SCHEMA}.{MIGRATION_TABLE} (revision VARCHAR(128) PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW())"
    )


def applied_revisions(conn) -> set[str]:
    ensure_migration_table(conn)
    if conn.dialect.name == "sqlite":
        rows = conn.exec_driver_sql(f"SELECT revision FROM {MIGRATION_TABLE}").fetchall()
    else:
        rows = conn.exec_driver_sql(f"SELECT revision FROM {AUTHN_SCHEMA}.{MIGRATION_TABLE}").fetchall()
    return {str(row[0]) for row in rows}


def mark_revision(conn, revision: str) -> None:
    ensure_migration_table(conn)
    table = MIGRATION_TABLE if conn.dialect.name == "sqlite" else f"{AUTHN_SCHEMA}.{MIGRATION_TABLE}"
    conn.execute(text(f"INSERT INTO {table} (revision) VALUES (:revision)"), {"revision": revision})


def unmark_revision(conn, revision: str) -> None:
    ensure_migration_table(conn)
    table = MIGRATION_TABLE if conn.dialect.name == "sqlite" else f"{AUTHN_SCHEMA}.{MIGRATION_TABLE}"
    conn.execute(text(f"DELETE FROM {table} WHERE revision = :revision"), {"revision": revision})


def _ddl_tables(conn, *models: SupportsTable) -> list[Table]:
    return [model.__table__ for model in models]


def create_tables(conn, *models: SupportsTable) -> None:
    ensure_schema(conn)
    for table in _ddl_tables(conn, *models):
        table.create(bind=conn, checkfirst=True)


def drop_tables(conn, *models: SupportsTable) -> None:
    for table in reversed(_ddl_tables(conn, *models)):
        table.drop(bind=conn, checkfirst=True)


def table_names(conn) -> set[str]:
    inspector = inspect(conn)
    if conn.dialect.name == "sqlite":
        return set(inspector.get_table_names(schema=AUTHN_SCHEMA))
    return set(inspector.get_table_names(schema=AUTHN_SCHEMA))


def column_names(conn, table: str) -> set[str]:
    inspector = inspect(conn)
    try:
        cols = inspector.get_columns(
            table,
            schema=AUTHN_SCHEMA if conn.dialect.name == "sqlite" else AUTHN_SCHEMA,
        )
    except NoSuchTableError:
        return set()
    return {str(col["name"]) for col in cols}


def _table_name(conn, table: str) -> str:
    return f'"{AUTHN_SCHEMA}"."{table}"'


def _index_name(conn, index: str) -> str:
    if conn.dialect.name == "sqlite":
        return f'"{AUTHN_SCHEMA}"."{index}"'
    return f'"{index}"'


def _copy_sqlalchemy_column(column, *, preserve_foreign_keys: bool = True) -> Column:
    args = [column.type]
    if preserve_foreign_keys:
        for fk in column.foreign_keys:
            target = fk.target_fullname
            if target.startswith(f"{AUTHN_SCHEMA}."):
                target = target[len(AUTHN_SCHEMA) + 1 :]
            args.append(
                ForeignKey(
                    target,
                    onupdate=fk.onupdate,
                    ondelete=fk.ondelete,
                    deferrable=fk.deferrable,
                    initially=fk.initially,
                    name=fk.constraint.name if fk.constraint is not None else None,
                )
            )
    server_default = None
    if column.server_default is not None and getattr(column.server_default, "arg", None) is not None:
        server_default = column.server_default.arg
    return Column(
        column.name,
        *args,
        primary_key=column.primary_key,
        nullable=column.nullable,
        unique=bool(column.unique),
        autoincrement=column.autoincrement,
        server_default=server_default,
        comment=column.comment,
    )


def _sqlite_rebuild_without_columns(conn, table: str, columns_to_drop: Iterable[str]) -> None:
    drop_set = {name for name in columns_to_drop if name in column_names(conn, table)}
    if not drop_set:
        return

    old_meta = MetaData()
    old_table = Table(table, old_meta, schema=AUTHN_SCHEMA, autoload_with=conn)
    keep_columns = [column for column in old_table.columns if column.name not in drop_set]
    if not keep_columns:
        raise ValueError(f"cannot rebuild SQLite table '{table}' without any remaining columns")

    old_indexes = inspect(conn).get_indexes(table, schema=AUTHN_SCHEMA)
    tmp_table_name = f"__tmp__{table}"

    conn.exec_driver_sql("PRAGMA foreign_keys=OFF")
    try:
        new_meta = MetaData()
        new_table = Table(
            tmp_table_name,
            new_meta,
            schema=AUTHN_SCHEMA,
            *(_copy_sqlalchemy_column(column, preserve_foreign_keys=False) for column in keep_columns),
        )
        new_table.create(bind=conn, checkfirst=False)

        keep_names = [column.name for column in keep_columns]
        select_columns = ", ".join(f'"{name}"' for name in keep_names)
        conn.exec_driver_sql(
            f'INSERT INTO {_table_name(conn, tmp_table_name)} ({select_columns}) '
            f'SELECT {select_columns} FROM {_table_name(conn, table)}'
        )
        conn.exec_driver_sql(f'DROP TABLE {_table_name(conn, table)}')
        conn.exec_driver_sql(
            f'ALTER TABLE {_table_name(conn, tmp_table_name)} RENAME TO "{table}"'
        )

        for index in old_indexes:
            index_columns = list(index.get("column_names") or [])
            if not index_columns or any(name in drop_set for name in index_columns):
                continue
            unique_sql = "UNIQUE " if bool(index.get("unique", False)) else ""
            rendered = ", ".join(f'"{name}"' for name in index_columns)
            conn.exec_driver_sql(
                f"CREATE {unique_sql}INDEX IF NOT EXISTS {_index_name(conn, index['name'])} "
                f'ON "{table}" ({rendered})'
            )
    finally:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON")


def drop_columns(conn, table: str, columns_to_drop: Iterable[str]) -> None:
    drop_list = [name for name in columns_to_drop if name in column_names(conn, table)]
    if not drop_list:
        return

    if conn.dialect.name == "sqlite":
        remaining = list(drop_list)
        for name in drop_list:
            try:
                conn.exec_driver_sql(f'ALTER TABLE {_table_name(conn, table)} DROP COLUMN "{name}"')
                remaining.remove(name)
            except SQLAlchemyError:
                continue
        if remaining:
            _sqlite_rebuild_without_columns(conn, table, remaining)
        return

    rendered_table = _table_name(conn, table)
    for name in drop_list:
        conn.exec_driver_sql(f'ALTER TABLE {rendered_table} DROP COLUMN IF EXISTS "{name}"')


__all__ = [
    "AUTHN_SCHEMA",
    "MIGRATION_TABLE",
    "applied_revisions",
    "column_names",
    "create_tables",
    "drop_columns",
    "drop_tables",
    "ensure_migration_table",
    "ensure_schema",
    "mark_revision",
    "table_names",
    "unmark_revision",
]
