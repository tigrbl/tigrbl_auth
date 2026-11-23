"""Policy decision providers with a standalone canonical platform PDP."""

from .platform import PlatformPolicyDecisionEngine

try:
    from .legacy_engine import *
except ImportError:
    # The canonical platform PDP deliberately has no legacy engine dependency.
    # Legacy symbols remain available whenever that optional dependency graph is installed.
    pass

__all__ = [name for name in globals() if not name.startswith("_")]
