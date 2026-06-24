from __future__ import annotations

from . import _table as _table
from . import _hooks as _hooks
from ._hooks import *
from ._table import *
from . import _ops as _ops

for _name in dir(_table):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_table, _name))

try:
    __all__ = list(_table.__all__) + list(_hooks.__all__)
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
