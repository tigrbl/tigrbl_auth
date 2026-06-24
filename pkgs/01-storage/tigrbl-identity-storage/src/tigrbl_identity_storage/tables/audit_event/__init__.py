from __future__ import annotations

from . import _table as _table
from ._table import *
from . import _ops as _ops

append_audit_event_async = AuditEvent.append_event
def append_audit_event(**kwargs):
    return _table.run_async(AuditEvent.append_event(**kwargs))

try:
    __all__ = list(_table.__all__)
except AttributeError:
    __all__ = [name for name in globals() if not name.startswith("_")]
__all__ += ["append_audit_event", "append_audit_event_async"]
