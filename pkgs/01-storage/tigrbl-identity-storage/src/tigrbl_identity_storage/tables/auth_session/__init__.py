from __future__ import annotations

from . import _table as _table
from ._table import *
from ._lifecycle import *

for _name in dir(_table):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_table, _name))

try:
    __all__ = list(_table.__all__) + [
        "bind_session_client",
        "bind_session_client_async",
        "create_session",
        "create_session_async",
        "get_active_session",
        "get_active_session_async",
        "get_session",
        "get_session_async",
        "rotate_session_cookie_secret",
        "rotate_session_cookie_secret_async",
        "touch_session",
        "touch_session_async",
    ]
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
