from __future__ import annotations

from . import _table as _table
from ._table import *
from . import _account_route as _account_route

for _name in dir(_table):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_table, _name))
for _name in dir(_account_route):
    if not _name.startswith("__"):
        globals().setdefault(_name, getattr(_account_route, _name))

try:
    __all__ = list(_table.__all__)
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
try:
    __all__ += [name for name in _account_route.__all__ if name not in __all__]
except AttributeError:
    pass
