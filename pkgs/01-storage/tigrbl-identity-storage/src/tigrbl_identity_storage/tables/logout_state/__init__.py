from __future__ import annotations

from . import _table as _table
from ._table import *
from ._lifecycle import *

for _name in dir(_table):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_table, _name))

try:
    __all__ = list(_table.__all__) + [
        "get_latest_logout_for_session",
        "get_latest_logout_for_session_async",
        "mark_logout_channel",
        "mark_logout_channel_async",
        "terminate_session",
        "terminate_session_async",
        "update_logout_metadata",
        "update_logout_metadata_async",
    ]
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
