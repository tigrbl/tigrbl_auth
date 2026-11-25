from __future__ import annotations

import asyncio
import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from tba_runtime_oidc_provider_logout import (
    LogoutAttempt,
    LogoutRejected,
    LogoutRequest,
    LogoutRuntime,
    LogoutSession,
    LogoutStatus,
    ValidatedLogout,
)


ISSUER = "https://authority.example"
OTHER_ISSUER = "https://another.example"
RETURN = "https://rp.example/signed-out?lang=en"
BROWSER = "synthetic-browser"
SESSION = LogoutSession(ISSUER, "session-a", "alice")
OTHER = LogoutSession(OTHER_ISSUER, "session-b", "bob")


class SQLiteAttempts:
    def __init__(self, path: Path) -> None:
        self.path = path
        with sqlite3.connect(path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS attempts (token text PRIMARY KEY, "
                "issuer text, browser text, expires real, data text)"
            )

    async def save(self, token, attempt):
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT INTO attempts VALUES (?, ?, ?, ?, ?)",
                (
                    token,
                    attempt.request.issuer,
                    attempt.browser_binding,
                    attempt.expires_at,
                    json.dumps(asdict(attempt)),
                ),
            )

    async def consume(self, token, *, issuer, browser_binding, now):
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                "DELETE FROM attempts WHERE token = ? AND issuer = ? AND browser = ? "
                "AND expires > ? RETURNING data",
                (token, issuer, browser_binding, now),
            ).fetchone()
        if row is None:
            return None
        data = json.loads(row[0])
        data["request"] = LogoutRequest(**data["request"])
        if data["session"] is not None:
            data["session"] = LogoutSession(**data["session"])
        return LogoutAttempt(**data)


class IssuerFixture:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.now = 100
        self.active = {SESSION, OTHER}
        self.redirect = RETURN
        self.fail_revocation = False

    async def validate(self, request, session):
        if (
            request.client_id != "public-app"
            or request.post_logout_redirect_uri != self.redirect
        ):
            raise LogoutRejected("unregistered client or redirect")
        hint = request.id_token_hint == "verified-a" and session == SESSION
        return ValidatedLogout(request.client_id, self.redirect, hint)

    async def revoke(self, session, validated):
        if self.fail_revocation:
            raise OSError("unavailable test store")
        self.active.discard(session)
        return True

    def runtime(self):
        return LogoutRuntime(
            self.validate,
            self.revoke,
            SQLiteAttempts(self.path),
            now=lambda: self.now,
        )

    def request(self, *, hint=None):
        return LogoutRequest(
            ISSUER, "public-app", hint, RETURN, "browser&return=opaque"
        )


def test_cross_site_handoff_resumes_after_restart_and_preserves_unrelated_session(
    tmp_path,
):
    fixture = IssuerFixture(tmp_path / "attempts.db")

    async def scenario():
        result = await fixture.runtime().handoff(
            fixture.request(hint="verified-a"), browser_binding=BROWSER
        )
        assert result.status is LogoutStatus.HANDOFF_REQUIRED
        assert fixture.active == {SESSION, OTHER}
        assert result.token is not None

        restarted = fixture.runtime()
        wrong_scope = await restarted.resume(
            result.token, OTHER_ISSUER, OTHER, browser_binding=BROWSER
        )
        assert wrong_scope.status is LogoutStatus.REJECTED
        wrong_browser = await restarted.resume(
            result.token, ISSUER, SESSION, browser_binding="other"
        )
        assert wrong_browser.status is LogoutStatus.REJECTED

        outcome, replay = await asyncio.gather(
            restarted.resume(result.token, ISSUER, SESSION, browser_binding=BROWSER),
            restarted.resume(result.token, ISSUER, SESSION, browser_binding=BROWSER),
        )
        assert {outcome.status, replay.status} == {
            LogoutStatus.COMPLETED,
            LogoutStatus.REJECTED,
        }
        completed = outcome if outcome.status is LogoutStatus.COMPLETED else replay
        assert completed.redirect_uri == RETURN + "&state=browser%26return%3Dopaque"
        assert fixture.active == {OTHER}

    asyncio.run(scenario())


def test_confirmation_cancellation_expiry_and_registration_change(tmp_path):
    fixture = IssuerFixture(tmp_path / "attempts.db")
    runtime = fixture.runtime()

    async def begin():
        attempt = await runtime.begin(
            fixture.request(), SESSION, browser_binding=BROWSER
        )
        assert attempt.status is LogoutStatus.CONFIRMATION_REQUIRED
        assert attempt.token is not None
        return attempt.token

    async def scenario():
        cancelled = await runtime.resume(
            await begin(),
            ISSUER,
            SESSION,
            browser_binding=BROWSER,
            confirmed=False,
        )
        assert cancelled.status is LogoutStatus.CANCELLED
        assert cancelled.redirect_uri is None

        token = await begin()
        fixture.now += 301
        expired = await runtime.resume(
            token, ISSUER, SESSION, browser_binding=BROWSER, confirmed=True
        )
        assert expired.status is LogoutStatus.REJECTED

        token = await begin()
        fixture.redirect = "https://rp.example/new-return"
        changed = await runtime.resume(
            token, ISSUER, SESSION, browser_binding=BROWSER, confirmed=True
        )
        assert changed.status is LogoutStatus.REJECTED
        assert fixture.active == {SESSION, OTHER}

    asyncio.run(scenario())


def test_failed_revocation_provides_no_success_redirect(tmp_path):
    fixture = IssuerFixture(tmp_path / "attempts.db")
    fixture.fail_revocation = True
    result = asyncio.run(
        fixture.runtime().begin(
            fixture.request(hint="verified-a"),
            SESSION,
            browser_binding=BROWSER,
        )
    )
    assert result.status is LogoutStatus.UNAVAILABLE
    assert result.redirect_uri is None
    assert fixture.active == {SESSION, OTHER}
