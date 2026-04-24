r"""Minimal Tigrbl JSON-RPC validation/error-leak repro.

Run in a scratch directory with:

    python -m venv .venv
    .venv\\Scripts\\python -m pip install "tigrbl==0.3.15" "sqlalchemy[asyncio]" aiosqlite httpx
    .venv\\Scripts\\python tigrbl_jsonrpc_minimal_repro.py

On POSIX shells, use `.venv/bin/python` instead of `.venv\Scripts\python`.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import httpx
from tigrbl import Base, TigrblApi, TigrblApp
from tigrbl.column.shortcuts import S, acol
from tigrbl.engine import engine
from tigrbl.orm.mixins import GUIDPk
from tigrbl.types import Mapped, String


DB_PATH = Path("tigrbl-jsonrpc-repro.sqlite").resolve()


class Thing(Base, GUIDPk):
    __tablename__ = "things"

    label: Mapped[str] = acol(storage=S(String, nullable=False))


async def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    db_url = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
    db_engine = engine(db_url)
    raw_engine, _sessionmaker = db_engine.raw()
    async with raw_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    api = TigrblApi(engine=db_engine, models=[Thing], jsonrpc_prefix="/rpc")
    app = TigrblApp(engine=db_engine, apis=[api])

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "method": "Thing.create", "params": {}, "id": 1},
        )

    print("HTTP status:", response.status_code)
    print(json.dumps(response.json(), indent=2))

    body = response.text
    print("\nLeak checks:")
    for marker in ("sqlalchemy", "sqlite3", "INSERT INTO", "[parameters:"):
        print(f"- contains {marker!r}: {marker in body}")


if __name__ == "__main__":
    asyncio.run(main())
