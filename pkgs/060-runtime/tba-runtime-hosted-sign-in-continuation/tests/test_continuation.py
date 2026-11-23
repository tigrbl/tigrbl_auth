from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from hmac import compare_digest
from threading import Barrier, Lock

import pytest

from tba_runtime_hosted_sign_in_continuation import (
    HostedSignInContinuationRuntime,
    Restart,
    Resume,
    StayLocal,
    ValidatedAuthorizationRequest,
)


class PendingRepository:
    def __init__(self):
        self.pending = {}
        self.lock = Lock()

    def insert(self, pending):
        with self.lock:
            assert pending.flow_id not in self.pending
            self.pending[pending.flow_id] = pending

    def get_pending(self, flow_id):
        with self.lock:
            return self.pending.get(flow_id)

    def consume_pending(self, pending, *, now):
        with self.lock:
            if self.pending.get(pending.flow_id) != pending or now >= pending.expires_at:
                return False
            del self.pending[pending.flow_id]
            return True


class ProviderFixture:
    def __init__(self, *, check_assurance=None):
        self.now = datetime(2026, 11, 23, tzinfo=timezone.utc)
        self.active_redirect = "https://app.example.test/callback"
        self.repo = PendingRepository()
        self.params = [("state", "client-state"), ("nonce", "client-nonce"), ("code_challenge", "client-s256")]
        self.request = ValidatedAuthorizationRequest(
            "https://issuer.example.test", "tenant-a", "app-a", self.active_redirect, self.params,
        )
        self.runtime = HostedSignInContinuationRuntime(
            self.repo,
            clock=lambda: self.now,
            client_is_active=lambda request: request.redirect_uri == self.active_redirect,
            browser_matches=compare_digest,
            assurance_is_sufficient=check_assurance or self.check_assurance,
            lifetime=timedelta(minutes=10),
            recovery_window=timedelta(minutes=2),
        )
        self.flow = self.runtime.begin(self.request, browser_binding="browser-a", required_assurance="fresh-otp")

    def check_assurance(self, pending, evidence):
        assert pending.required_assurance == "fresh-otp"
        methods = evidence["methods"]
        return (
            {"pwd", "otp"} <= methods
            and "remembered_device" not in methods
            and evidence["authenticated_at"] >= pending.started_at
        )

    def resolve(self, **changes):
        context = {
            "issuer": "https://issuer.example.test",
            "tenant_id": "tenant-a",
            "browser_binding": "browser-a",
            "assurance": {"methods": {"pwd", "otp"}, "authenticated_at": self.now},
        }
        return self.runtime.resolve(self.flow, **(context | changes))


def test_first_enrollment_resumes_original_request_once():
    provider = ProviderFixture()
    provider.params[0] = ("state", "changed")
    assert provider.resolve(assurance={"methods": {"pwd"}, "authenticated_at": provider.now}) == StayLocal()
    assert provider.resolve(assurance={
        "methods": {"pwd", "otp", "remembered_device"}, "authenticated_at": provider.now,
    }) == StayLocal()
    assert provider.resolve(assurance={
        "methods": {"pwd", "otp"}, "authenticated_at": provider.now - timedelta(seconds=1),
    }) == StayLocal()
    result = provider.resolve()
    assert isinstance(result, Resume)
    assert result.request.redirect_uri == "https://app.example.test/callback"
    assert result.request.parameters == (
        ("state", "client-state"), ("nonce", "client-nonce"), ("code_challenge", "client-s256"),
    )
    with pytest.raises(FrozenInstanceError):
        result.request.redirect_uri = "https://changed.example.test/callback"
    assert provider.resolve() == StayLocal()


@pytest.mark.parametrize("scope", [
    {"issuer": "https://other.example.test"},
    {"tenant_id": "tenant-b"},
    {"browser_binding": "browser-b"},
    {"browser_binding": ""},
])
def test_another_browser_or_scope_cannot_resume_or_see_restart(scope):
    provider = ProviderFixture()
    assert provider.resolve(**scope) == StayLocal()
    assert provider.repo.get_pending(provider.flow) is not None
    provider.now += timedelta(minutes=10)
    assert provider.resolve(**scope) == StayLocal()
    assert provider.resolve() == Restart("app-a")


def test_expiry_returns_only_a_bounded_registered_restart_hint():
    provider = ProviderFixture()
    provider.now += timedelta(minutes=10)
    assert provider.resolve() == Restart("app-a")
    provider.now += timedelta(minutes=2)
    assert provider.resolve() == StayLocal()


@pytest.mark.parametrize("redirect", [None, "https://app.example.test/new-callback"])
def test_disabled_client_or_changed_redirect_cannot_resume_or_restart(redirect):
    provider = ProviderFixture()
    provider.active_redirect = redirect
    assert provider.resolve() == StayLocal()
    provider.now += timedelta(minutes=10)
    assert provider.resolve() == StayLocal()


def test_request_expiring_during_assurance_check_cannot_resume():
    def slow_check(_, __):
        provider.now += timedelta(minutes=10)
        return True

    provider = ProviderFixture(check_assurance=slow_check)
    assert provider.resolve() == Restart("app-a")


def test_concurrent_resolution_exposes_request_once():
    barrier = Barrier(2, timeout=5)

    def check_assurance(_, __):
        barrier.wait()
        return True

    provider = ProviderFixture(check_assurance=check_assurance)
    with ThreadPoolExecutor(max_workers=2) as workers:
        results = list(workers.map(lambda _: provider.resolve(), range(2)))
    assert results.count(Resume(provider.request)) == 1
    assert results.count(StayLocal()) == 1


def test_unknown_flow_stays_local():
    provider = ProviderFixture()
    provider.flow = "not-a-started-flow"
    assert provider.resolve() == StayLocal()


def test_request_parameters_cannot_override_registered_redirect():
    with pytest.raises(ValueError, match="bound fields"):
        ValidatedAuthorizationRequest(
            "https://issuer.example.test", "tenant-a", "app-a", "https://app.example.test/callback",
            (("redirect_uri", "https://changed.example.test/callback"),),
        )
