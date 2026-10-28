from __future__ import annotations

from . import _table as _table
from ._table import *

for _name in dir(_table):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_table, _name))

__all__ = list(_table.__all__)
