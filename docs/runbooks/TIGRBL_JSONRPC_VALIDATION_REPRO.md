# Tigrbl JSON-RPC Validation Repro

This note captures a framework-level issue observed through a minimal Tigrbl
table-backed JSON-RPC surface. The behavior should be fixed in `tigrbl`, not by
adding per-application guards in downstream packages.

## Issue

Tigrbl JSON-RPC table CRUD dispatch can invoke persistence with missing required
create parameters. When the database rejects the write, the JSON-RPC response
leaks the raw SQLAlchemy/driver exception, including SQL text and bound
parameters.

This makes the database the first effective validator and exposes internals to
clients.

## Repro

The smallest standalone repro is
`docs/runbooks/tigrbl_jsonrpc_minimal_repro.py`. It can be copied into an empty
scratch directory and run with only published dependencies:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install "tigrbl==0.3.15" "sqlalchemy[asyncio]" aiosqlite httpx
.venv\Scripts\python tigrbl_jsonrpc_minimal_repro.py
```

On POSIX shells:

```bash
python -m venv .venv
.venv/bin/python -m pip install "tigrbl==0.3.15" "sqlalchemy[asyncio]" aiosqlite httpx
.venv/bin/python tigrbl_jsonrpc_minimal_repro.py
```

The script defines one model:

```python
class Thing(Base, GUIDPk):
    __tablename__ = "things"

    label: Mapped[str] = acol(storage=S(String, nullable=False))
```

It mounts the model through `TigrblApi(..., jsonrpc_prefix="/rpc")` and sends:

```json
{"jsonrpc": "2.0", "method": "Thing.create", "params": {}, "id": 1}
```

## Actual Behavior

The request reaches the database with `label = NULL`. SQLite rejects the write
and the JSON-RPC response includes a raw
`sqlalchemy.exc.IntegrityError` message. The message includes database driver
details, table/column names, generated SQL, and parameter values.

Observed response shape:

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "<class 'sqlalchemy.exc.IntegrityError'>: (sqlite3.IntegrityError) NOT NULL constraint failed: things.label\n[SQL: INSERT INTO things ...]\n[parameters: (None, ...)]"
  },
  "id": 1
}
```

## Expected Behavior

Tigrbl should validate generated JSON-RPC input schemas before calling the table
operation or persistence layer.

For this request, the response should be a clean JSON-RPC invalid-params error:

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params: Thing.create requires label."
  },
  "id": 1
}
```

The exact wording can differ, but the response should not include SQLAlchemy
types, DBAPI driver messages, SQL text, table names, or bound parameter values.

## Suggested Tigrbl Fix

- Validate JSON-RPC `params` against the generated operation input model before
  dispatching table CRUD handlers.
- Convert Pydantic/schema validation failures to JSON-RPC `-32602 Invalid
  params`.
- Sanitize persistence exceptions at the framework JSON-RPC boundary as a final
  fail-safe.
- Keep raw persistence exceptions in server logs only when debug logging is
  explicitly enabled.
- Add regression coverage for table-backed `*.create` with missing required
  fields, including a check that responses do not contain `sqlalchemy`,
  `sqlite3`, `INSERT INTO`, or bind parameter values.
