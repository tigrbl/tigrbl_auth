from __future__ import annotations

from . import _table as _table
from ._table import *
from ._lifecycle import *

for _name in dir(_table):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_table, _name))

try:
    __all__ = list(_table.__all__) + [
        "get_token_record_async",
        "mark_token_used_async",
        "remove_token_record_async",
        "revoke_refresh_family_async",
        "token_hash",
        "upsert_token_record_async",
    ]
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
