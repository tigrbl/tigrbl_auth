from collections.abc import Callable, Mapping
from .rpcs import RPC_NAMES
class BrokerApiService:
    def __init__(self, *, authorize: Callable[[object], bool], handlers: Mapping[str, Callable[..., object]]) -> None:
        unknown = set(handlers).difference(RPC_NAMES)
        missing = RPC_NAMES.difference(handlers)
        if unknown or missing: raise ValueError(f"Broker API handler mismatch; unknown={sorted(unknown)}, missing={sorted(missing)}")
        self._authorize, self._handlers = authorize, dict(handlers)
    def dispatch(self, actor: object, rpc: str, request: object) -> object:
        if not self._authorize(actor): raise PermissionError("broker caller is not authorized")
        if rpc not in RPC_NAMES: raise ValueError(f"unknown Broker API RPC: {rpc}")
        return self._handlers[rpc](request)