from __future__ import annotations

__all__: list[str] = []

# BEGIN classmethod-to-op_ctx migration
from tigrbl import op_ctx as _table_op_ctx
from . import _table as _table_module

for _table_name in dir(_table_module):
    if not _table_name.startswith("__"):
        globals().setdefault(_table_name, getattr(_table_module, _table_name))

@_table_op_ctx(bind=Client, alias="new", target="custom", rest=False)
def new(
    cls,
    tenant_id: uuid.UUID,
    client_id: str,
    client_secret: str,
    redirects: list[str],
):
    if not _CLIENT_ID_RE.fullmatch(client_id):
        raise ValueError("invalid client_id format")
    if settings.enforce_rfc8252:
        for uri in redirects:
            parsed = urlparse(uri)
            if is_native_redirect_uri(uri):
                validate_native_redirect_uri(uri)
            elif parsed.scheme == "http":
                raise ValueError(
                    f"redirect URI not permitted for native apps per RFC 8252: {RFC8252_SPEC_URL}"
                )
    secret_hash = hash_pw(client_secret)
    try:
        obj_id: uuid.UUID | str = uuid.UUID(client_id)
    except ValueError:
        obj_id = client_id
    return cls(
        tenant_id=tenant_id,
        id=obj_id,
        client_secret_hash=secret_hash,
        redirect_uris=" ".join(redirects),
    )

@_table_op_ctx(bind=Client, alias="authenticate", target="custom", rest=False)
async def authenticate(cls, db: Any, *, client_secret: str, client_id: str | uuid.UUID | None = None):
    from .._ops import field, first_record, list_records

    rows = [await first_record(cls, db, {"id": client_id})] if client_id is not None else await list_records(cls, db, {"is_active": True})
    for row in rows:
        if row is not None and bool(field(row, "is_active", True)) and row.verify_secret(client_secret):
            return row
    return None

# END classmethod-to-op_ctx migration
