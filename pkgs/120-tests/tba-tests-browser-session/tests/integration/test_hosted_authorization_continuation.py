"""Synthetic provider and relying-party continuation with durable storage."""

from __future__ import annotations

import os
import pickle
import sqlite3
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlencode, urlsplit

import pytest

from tba_runtime_hosted_authorization_continuation import (
    AuthenticationEvidence,
    ContinuationReason,
    ContinuationRequirements,
    ContinuationStatus,
    ContinuationUnavailable,
    HostedAuthorizationContinuation,
    ValidatedAuthorizationRequest,
)


class _SqliteContinuations:
    def __init__(self, path):
        self.path = path
        with sqlite3.connect(path) as db:
            db.execute(
                "CREATE TABLE flow (id TEXT PRIMARY KEY, payload BLOB NOT NULL, "
                "expires REAL NOT NULL, consumed INTEGER NOT NULL DEFAULT 0)"
            )

    def create(self, record):
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT INTO flow (id, payload, expires) VALUES (?, ?, ?)",
                (record.flow_id, pickle.dumps(record), record.expires_at.timestamp()),
            )

    def get(self, flow_id):
        with sqlite3.connect(self.path) as db:
            result = db.execute(
                "SELECT payload FROM flow WHERE id = ? AND consumed = 0", (flow_id,)
            ).fetchone()
        return pickle.loads(result[0]) if result else None

    def consume(self, record, *, now):
        with sqlite3.connect(self.path) as db:
            return (
                db.execute(
                    "UPDATE flow SET consumed = 1 "
                    "WHERE id = ? AND payload = ? AND consumed = 0 AND expires > ?",
                    (record.flow_id, pickle.dumps(record), now.timestamp()),
                ).rowcount
                == 1
            )


@dataclass
class _Clock:
    now: datetime = datetime(2026, 1, 2, tzinfo=timezone.utc)

    def __call__(self):
        return self.now


class _SyntheticProvider:
    issuer = "https://issuer.test"
    client = "synthetic-client"
    callback = "https://relying.test/callback?profile=original"
    restart = "https://relying.test/fresh-sign-in"
    browser = "secret-browser-transaction"

    def __init__(self, tmp_path):
        self.clock = _Clock()
        self.store = _SqliteContinuations(tmp_path / "continuation.db")
        self.runtime = HostedAuthorizationContinuation(self.store, clock=self.clock)
        self.parameters = {
            "client_id": self.client,
            "redirect_uri": self.callback,
            "response_type": "code",
            "scope": "openid",
            "state": "original-state",
            "nonce": "original-nonce",
            "code_challenge_method": "S256",
            "code_challenge": "original-pkce",
        }
        self.request = ValidatedAuthorizationRequest.from_parameters(
            self.issuer, self.parameters
        )
        self.active_registration = self.callback

    def start(self):
        return self.runtime.begin(
            self.request,
            browser_transaction_id=self.browser,
            requirements=ContinuationRequirements(
                subject="account-1",
                required_methods=frozenset({"email_verified", "otp"}),
                not_before=self.clock.now,
            ),
            ttl=timedelta(minutes=5),
        )

    def resume(self, flow_id, *, evidence=None, **override):
        arguments = {
            "issuer": self.issuer,
            "client_id": self.client,
            "browser_transaction_id": self.browser,
            "registration_is_current": (
                lambda request: request.redirect_uri == self.active_registration
            ),
            "evidence": evidence,
        }
        return self.runtime.resume(flow_id, **(arguments | override))

    def evidence(self, *methods, subject="account-1"):
        return AuthenticationEvidence(subject, self.clock.now, frozenset(methods))


def test_email_verification_and_first_factor_preserve_original_callback(tmp_path):
    provider = _SyntheticProvider(tmp_path)
    record = provider.start()
    provider.parameters["state"] = "changed-by-host"
    email_only = provider.evidence("email_verified")
    assert provider.resume(record.flow_id, evidence=email_only).reason is (
        ContinuationReason.AUTHENTICATION_REQUIRED
    )
    wrong_subject = provider.evidence(
        "email_verified", "otp", subject="another-account"
    )
    assert provider.resume(record.flow_id, evidence=wrong_subject).reason is (
        ContinuationReason.AUTHENTICATION_REQUIRED
    )
    finished = provider.evidence("email_verified", "otp")
    result = provider.resume(record.flow_id, evidence=finished)
    assert result.status is ContinuationStatus.RESUME
    assert result.request.redirect_uri == provider.callback
    assert (
        dict(result.request.parameters) | {"state": "changed-by-host"}
        == provider.parameters
    )
    assert dict(result.request.parameters)["state"] == "original-state"
    assert provider.resume(record.flow_id, evidence=finished).status is (
        ContinuationStatus.RESTART_REQUIRED
    )


@pytest.mark.parametrize(
    "override",
    [
        {"issuer": "https://another-issuer.test"},
        {"client_id": "another-app"},
        {"browser_transaction_id": "another-browser"},
    ],
)
def test_mismatched_flow_cannot_be_consumed(tmp_path, override):
    provider = _SyntheticProvider(tmp_path)
    record = provider.start()
    proof = provider.evidence("email_verified", "otp")
    assert provider.resume(record.flow_id, evidence=proof, **override).status is (
        ContinuationStatus.RESTART_REQUIRED
    )
    assert (
        provider.resume(record.flow_id, evidence=proof).status
        is ContinuationStatus.RESUME
    )


def test_expired_or_changed_registration_restarts_at_host_owned_destination(tmp_path):
    provider = _SyntheticProvider(tmp_path)
    expired = provider.start()
    provider.clock.now = expired.expires_at
    proof = provider.evidence("email_verified", "otp")
    result = provider.resume(expired.flow_id, evidence=proof)
    assert result.status is ContinuationStatus.RESTART_REQUIRED
    assert result.request is None
    assert provider.restart != provider.callback
    changed = provider.start()
    provider.active_registration = "https://relying.test/new-callback"
    assert provider.resume(changed.flow_id, evidence=proof).reason is (
        ContinuationReason.REGISTRATION_CHANGED
    )


def test_storage_unavailability_does_not_emit_or_consume_request(tmp_path, monkeypatch):
    provider = _SyntheticProvider(tmp_path)
    record = provider.start()
    proof = provider.evidence("email_verified", "otp")

    def unavailable(*args, **kwargs):
        raise ContinuationUnavailable

    with monkeypatch.context() as context:
        context.setattr(provider.store, "consume", unavailable)
        result = provider.resume(record.flow_id, evidence=proof)
        assert (
            result.status is ContinuationStatus.UNAVAILABLE and result.request is None
        )
    assert (
        provider.resume(record.flow_id, evidence=proof).status
        is ContinuationStatus.RESUME
    )


def test_concurrent_resumes_consume_one_durable_flow(tmp_path):
    provider = _SyntheticProvider(tmp_path)
    record = provider.start()
    proof = provider.evidence("email_verified", "otp")

    def resume(_):
        return provider.resume(record.flow_id, evidence=proof).status

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(resume, range(8)))
    assert results.count(ContinuationStatus.RESUME) == 1
    assert results.count(ContinuationStatus.RESTART_REQUIRED) == 7


@pytest.mark.parametrize(
    ("entry", "destination"), [("start", "callback"), ("expired", "restart")]
)
def test_browser_first_enrollment_and_expired_restart(tmp_path, entry, destination):
    """Run the synthetic provider and RP through an opted-in Chromium executable."""
    executable = os.environ.get("TBA_TEST_CHROMIUM")
    if not executable:
        pytest.skip(
            "set TBA_TEST_CHROMIUM to run the standalone browser acceptance test"
        )
    assert Path(executable).is_file(), (
        "TBA_TEST_CHROMIUM must name a Chromium executable"
    )

    provider = _SyntheticProvider(tmp_path)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, _format, *_args):
            pass

        def _reply(self, body, *, status=200, location=None, cookie=None):
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            if location:
                self.send_header("Location", location)
            if cookie:
                self.send_header("Set-Cookie", cookie)
            self.end_headers()
            self.wfile.write(body.encode())

        def do_GET(self):
            url = urlsplit(self.path)
            if url.path in {"/start", "/expired"}:
                record = provider.start()
                if url.path == "/expired":
                    provider.clock.now = record.expires_at
                self._reply(
                    "",
                    status=303,
                    location=f"/verify?flow={record.flow_id}",
                    cookie=f"browser={provider.browser}; HttpOnly; SameSite=Lax; Path=/",
                )
            elif url.path == "/verify":
                self._form("/verify", parse_qs(url.query)["flow"][0], "Verify email")
            elif url.path == "/callback" and parse_qs(url.query) == {
                "profile": ["original"],
                "code": ["synthetic-code"],
                "state": ["original-state"],
            }:
                self._reply("<h1>accepted original callback</h1>")
            elif url.path == "/restart" and not url.query:
                self._reply("<h1>accepted registered restart</h1>")
            else:
                self._reply("<h1>unexpected destination</h1>", status=400)

        def _form(self, action, flow, button):
            self._reply(
                f'<form method="post" action="{action}">'
                f'<input type="hidden" name="flow" value="{flow}">'
                f'<button type="submit">{button}</button></form>'
                "<script>document.querySelector('button').click()</script>"
            )

        def do_POST(self):
            cookie = SimpleCookie(self.headers.get("Cookie", ""))
            browser = cookie["browser"].value if "browser" in cookie else ""
            flow_id = parse_qs(
                self.rfile.read(int(self.headers["Content-Length"])).decode()
            )["flow"][0]
            verified = "verified" in cookie and cookie["verified"].value == flow_id
            evidence = (
                provider.evidence("email_verified", "otp")
                if self.path == "/enroll" and verified
                else provider.evidence("email_verified")
            )
            result = provider.resume(
                flow_id, evidence=evidence, browser_transaction_id=browser
            )
            if result.status is ContinuationStatus.RESTART_REQUIRED:
                self._reply("", status=303, location=provider.restart)
            elif (
                result.reason is ContinuationReason.AUTHENTICATION_REQUIRED
                and self.path == "/verify"
            ):
                self._reply(
                    '<form method="post" action="/enroll">'
                    f'<input type="hidden" name="flow" value="{flow_id}">'
                    '<button type="submit">Complete first enrollment</button></form>'
                    "<script>document.querySelector('button').click()</script>",
                    cookie=f"verified={flow_id}; HttpOnly; SameSite=Lax; Path=/",
                )
            elif (
                result.status is ContinuationStatus.RESUME
                and dict(result.request.parameters) == provider.parameters
            ):
                params = urlencode(
                    {
                        "code": "synthetic-code",
                        "state": dict(result.request.parameters)["state"],
                    }
                )
                self._reply(
                    "", status=303, location=f"{result.request.redirect_uri}&{params}"
                )
            else:
                self._reply("<h1>unexpected continuation</h1>", status=400)

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        base = f"http://127.0.0.1:{server.server_port}"
        provider.callback = f"{base}/callback?profile=original"
        provider.restart = f"{base}/restart"
        provider.active_registration = provider.callback
        provider.parameters["redirect_uri"] = provider.callback
        provider.request = ValidatedAuthorizationRequest.from_parameters(
            provider.issuer, provider.parameters
        )
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            result = subprocess.run(
                [
                    executable,
                    "--headless",
                    "--disable-gpu",
                    "--no-first-run",
                    "--disable-background-networking",
                    f"--user-data-dir={tmp_path / 'chromium'}",
                    "--virtual-time-budget=5000",
                    "--dump-dom",
                    f"{base}/{entry}",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )
        finally:
            server.shutdown()
            worker.join()
    expected = (
        "original callback" if destination == "callback" else "registered restart"
    )
    assert f"<h1>accepted {expected}</h1>" in result.stdout
