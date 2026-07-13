"""Deprecated CoRIM store compatibility surface."""

from warnings import warn

from tigrbl_corim_reference_memory_provider import CorimReferenceMemoryProvider

warn(
    "tigrbl-corim-store-provider is deprecated; use "
    "tigrbl-corim-reference-memory-provider or a durable reference repository",
    DeprecationWarning,
    stacklevel=2,
)

InMemoryCorimStore = CorimReferenceMemoryProvider

__all__ = ["InMemoryCorimStore"]
