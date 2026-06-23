from __future__ import annotations

from . import _table as _table
from ._table import *
from ._lifecycle import *

for _name in dir(_table):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_table, _name))

try:
    __all__ = list(_table.__all__) + [
        "get_client_registration",
        "get_client_registration_async",
        "upsert_client_registration",
        "upsert_client_registration_async",
    ]
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
