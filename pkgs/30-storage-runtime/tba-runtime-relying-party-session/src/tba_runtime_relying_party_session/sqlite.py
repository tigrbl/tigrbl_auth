"""Durable, bounded RP transactions and browser sessions for a shared local volume."""

from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
import time
from collections.abc import Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from tba_contracts_identity.rp import LoginRequest
from tba_provider_security_proof_pkce import make_pkce_verifier


def _digest(value: str) -> bytes:
    return hashlib.sha256(value.encode()).digest()


class SQLiteRPStore:
    """Keep RP data isolated by client and issuer across workers and restarts."""

    def __init__(self, database: str | Path, *, realm: str) -> None:
        self.database = Path(database).resolve()
        self.realm = realm
        with self._connection() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS rp_transactions (
                    realm TEXT NOT NULL, digest BLOB NOT NULL, data TEXT NOT NULL,
                    expires INTEGER NOT NULL, PRIMARY KEY (realm, digest)
                );
                CREATE TABLE IF NOT EXISTS rp_sessions (
                    realm TEXT NOT NULL, digest BLOB NOT NULL, data TEXT NOT NULL,
                    expires INTEGER NOT NULL, PRIMARY KEY (realm, digest)
                );
                CREATE INDEX IF NOT EXISTS rp_transactions_expiry ON rp_transactions(expires);
                CREATE INDEX IF NOT EXISTS rp_sessions_expiry ON rp_sessions(expires);
                """
            )

    @contextmanager
    def _connection(self):
        db = sqlite3.connect(self.database, timeout=5)
        try:
            with db:
                yield db
        finally:
            db.close()

    def create(self, *, redirect_uri: str, scope: tuple[str, ...]) -> LoginRequest:
        state = secrets.token_urlsafe(32)
        login = LoginRequest(
            state, secrets.token_urlsafe(32), make_pkce_verifier(), redirect_uri, scope
        )
        now = int(time.time())
        payload = json.dumps([login.nonce, login.code_verifier, redirect_uri, scope])
        with self._connection() as db:
            db.execute("DELETE FROM rp_transactions WHERE expires <= ?", (now,))
            db.execute(
                "INSERT INTO rp_transactions VALUES (?, ?, ?, ?)",
                (self.realm, _digest(state), payload, now + 300),
            )
        return login

    def consume(self, state: str) -> LoginRequest:
        with self._connection() as db:
            row = db.execute(
                "DELETE FROM rp_transactions WHERE realm = ? AND digest = ? AND expires > ? "
                "RETURNING data",
                (self.realm, _digest(state), int(time.time())),
            ).fetchone()
        if row is None:
            raise ValueError("RP transaction is missing, expired, or already consumed")
        nonce, verifier, uri, scope = json.loads(row[0])
        return LoginRequest(state, nonce, verifier, uri, tuple(scope))

    def start_session(self, identity: Mapping[str, Any], *, expires: int) -> str:
        secret = secrets.token_urlsafe(32)
        with self._connection() as db:
            db.execute("DELETE FROM rp_sessions WHERE expires <= ?", (int(time.time()),))
            db.execute(
                "INSERT INTO rp_sessions VALUES (?, ?, ?, ?)",
                (self.realm, _digest(secret), json.dumps(dict(identity)), expires),
            )
        return secret

    def get_session(self, secret: str) -> dict[str, Any] | None:
        with self._connection() as db:
            row = db.execute(
                "SELECT data FROM rp_sessions WHERE realm = ? AND digest = ? AND expires > ?",
                (self.realm, _digest(secret), int(time.time())),
            ).fetchone()
        return json.loads(row[0]) if row else None

    def revoke_session(self, secret: str) -> None:
        with self._connection() as db:
            db.execute(
                "DELETE FROM rp_sessions WHERE realm = ? AND digest = ?",
                (self.realm, _digest(secret)),
            )
