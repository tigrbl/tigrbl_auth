from collections.abc import Callable, Mapping
from .rpcs import RPC_NAMES
class WorkloadApiService:
    def __init__(self, handlers: Mapping[str, Callable[..., object]]) -> None:
        unknown = set(handlers).difference(RPC_NAMES)
        if unknown: raise ValueError(f"Workload API must not be extended: {sorted(unknown)}")
        missing = RPC_NAMES.difference(handlers)
        if missing: raise ValueError(f"missing Workload API handlers: {sorted(missing)}")
        self._handlers = dict(handlers)
    def dispatch(self, rpc: str, request: object) -> object:
        if rpc not in RPC_NAMES: raise ValueError(f"unknown Workload API RPC: {rpc}")
        return self._handlers[rpc](request)