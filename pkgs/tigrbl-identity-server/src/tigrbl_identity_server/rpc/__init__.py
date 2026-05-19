"""Implementation-backed admin/operator RPC registry.

This package intentionally keeps the method catalog, runtime handlers, and
schema definitions colocated so that OpenRPC generation is derived directly
from executable method registration instead of a detached static catalog.
"""

from .registry import (
    EmptyParams,
    RpcMethodDefinition,
    RpcRequestContext,
    RpcSchema,
    get_rpc_method,
    get_rpc_method_registry,
    invoke_rpc_method,
    invoke_rpc_method_async,
    iter_active_rpc_methods,
    list_rpc_methods,
)

__all__ = [
    "EmptyParams",
    "RpcMethodDefinition",
    "RpcRequestContext",
    "RpcSchema",
    "get_rpc_method",
    "get_rpc_method_registry",
    "invoke_rpc_method",
    "invoke_rpc_method_async",
    "iter_active_rpc_methods",
    "list_rpc_methods",
]
