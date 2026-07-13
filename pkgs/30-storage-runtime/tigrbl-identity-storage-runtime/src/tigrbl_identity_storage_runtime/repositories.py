from collections.abc import Mapping, Sequence
from contextlib import AbstractAsyncContextManager
from typing import Any, Protocol


class AsyncRecordStore(Protocol):
    async def insert(self, table: type, values: Mapping[str, Any], /) -> Any: ...

    async def get(self, table: type, identifier: str, /) -> Any | None: ...

    async def update(
        self, table: type, identifier: str, values: Mapping[str, Any], /
    ) -> Any: ...

    async def list(
        self, table: type, filters: Mapping[str, Any], /
    ) -> Sequence[Any]: ...


class AsyncTransactionManager(Protocol):
    def transaction(self) -> AbstractAsyncContextManager[None]: ...


class DurableRepository:
    table: type
    retained_payload_fields: frozenset[str] = frozenset()

    def __init__(self, store: AsyncRecordStore):
        self._store = store

    async def create(self, **values: Any) -> Any:
        return await self._store.insert(self.table, self._sanitize(values))

    async def get(self, identifier: str) -> Any | None:
        return await self._store.get(self.table, identifier)

    async def update(self, identifier: str, **values: Any) -> Any:
        return await self._store.update(self.table, identifier, self._sanitize(values))

    async def find(self, **filters: Any) -> Sequence[Any]:
        return await self._store.list(self.table, filters)

    def _sanitize(self, values: Mapping[str, Any]) -> dict[str, Any]:
        forbidden = {
            name
            for name in values
            if name in {"raw_nonce", "pre_authorized_code", "presentation_disclosures"}
            and name not in self.retained_payload_fields
        }
        if forbidden:
            raise ValueError(
                f"repository refuses sensitive raw fields: {sorted(forbidden)}"
            )
        return dict(values)


class StorageTransactionCoordinator:
    def __init__(self, manager: AsyncTransactionManager):
        self._manager = manager

    def transaction(self) -> AbstractAsyncContextManager[None]:
        return self._manager.transaction()


__all__ = [
    "AsyncRecordStore",
    "AsyncTransactionManager",
    "DurableRepository",
    "StorageTransactionCoordinator",
]
