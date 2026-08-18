"""Server-side RP transaction runtime."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Callable, Protocol


@dataclass(frozen=True, slots=True)
class RPTransaction:
    state: str
    nonce: str
    code_verifier: str
    issuer: str
    client_id: str
    redirect_uri: str
    scope: tuple[str, ...]
    created_at: datetime
    expires_at: datetime


class RPTransactionRepository(Protocol):
    def save(self, transaction: RPTransaction) -> None: ...
    def consume(self, state: str) -> RPTransaction: ...


class InMemoryRPTransactionRepository:
    def __init__(self) -> None:
        self._items: dict[str, RPTransaction] = {}
        self._consumed: set[str] = set()

    def save(self, transaction: RPTransaction) -> None:
        self._items[transaction.state] = transaction

    def consume(self, state: str) -> RPTransaction:
        if state in self._consumed:
            raise ValueError("RP transaction state was already consumed")
        try:
            transaction = self._items.pop(state)
        except KeyError as exc:
            raise ValueError("RP transaction state is unknown") from exc
        self._consumed.add(state)
        return transaction


class RPTransactionRuntime:
    def __init__(self, repository: RPTransactionRepository, *, lifetime: timedelta = timedelta(minutes=10)) -> None:
        self._repository = repository
        self._lifetime = lifetime

    def begin(self, *, issuer: str, client_id: str, redirect_uri: str, scope: tuple[str, ...], now: datetime | None = None) -> RPTransaction:
        created_at = now or datetime.now(timezone.utc)
        transaction = RPTransaction(token_urlsafe(32), token_urlsafe(32), token_urlsafe(64), issuer, client_id, redirect_uri, tuple(scope), created_at, created_at + self._lifetime)
        self._repository.save(transaction)
        return transaction

    def consume(self, state: str, *, now: datetime | None = None) -> RPTransaction:
        transaction = self._repository.consume(state)
        if (now or datetime.now(timezone.utc)) >= transaction.expires_at:
            raise ValueError("RP transaction state expired")
        return transaction


@dataclass(frozen=True, slots=True)
class RPServerSession:
    session_id: str
    subject: str
    encrypted_refresh_token: str | None
    version: int
    expires_at: datetime


class InMemoryRPSessionRepository:
    def __init__(self) -> None:
        self._items: dict[str, RPServerSession] = {}

    def save(self, session: RPServerSession) -> None:
        self._items[session.session_id] = session

    def get(self, session_id: str) -> RPServerSession:
        return self._items[session_id]

    def compare_and_swap(self, session_id: str, expected_version: int, replacement: RPServerSession) -> bool:
        current = self._items.get(session_id)
        if current is None or current.version != expected_version:
            return False
        self._items[session_id] = replacement
        return True


class RPSessionRuntime:
    def __init__(self, repository: InMemoryRPSessionRepository, *, encrypt: Callable[[str], str]) -> None:
        self._repository = repository
        self._encrypt = encrypt

    def create(self, *, subject: str, refresh_token: str | None, expires_at: datetime) -> RPServerSession:
        session = RPServerSession(token_urlsafe(32), subject, self._encrypt(refresh_token) if refresh_token else None, 1, expires_at)
        self._repository.save(session)
        return session

    def rotate_refresh_token(self, session_id: str, *, expected_version: int, refresh_token: str, expires_at: datetime) -> RPServerSession:
        current = self._repository.get(session_id)
        replacement = RPServerSession(current.session_id, current.subject, self._encrypt(refresh_token), expected_version + 1, expires_at)
        if not self._repository.compare_and_swap(session_id, expected_version, replacement):
            raise ValueError("concurrent refresh rotation rejected")
        return replacement

__all__ = ["InMemoryRPSessionRepository", "InMemoryRPTransactionRepository", "RPServerSession", "RPSessionRuntime", "RPTransaction", "RPTransactionRepository", "RPTransactionRuntime"]
