"""Synthetic lifecycle tests with actual TOTP verification and SQLite transitions."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import pickle
import sqlite3

import pytest

from tba_concrete_totp import hotp, time_step
from tba_provider_authenticator_totp_local import TotpLocalAuthenticator, new_secret
from tba_provider_authenticator_totp_local.provisioning import decode_secret
from tba_runtime_mfa_lifecycle import (
    AssuranceRequirement,
    CeremonyKind,
    EnrollmentRuntime,
    FactorAssurance,
    FactorBinding,
    LifecycleStatus,
    StepUpRuntime,
    satisfies_assurance,
)
from tba_runtime_mfa_lifecycle.totp import TotpCredential, totp_verifier


class _SqliteFactors:
    def __init__(self, path):
        self.path = path
        with sqlite3.connect(path) as db:
            db.executescript(
                "CREATE TABLE attempt (id TEXT PRIMARY KEY, snapshot BLOB NOT NULL);"
                "CREATE TABLE factor (scope TEXT, subject TEXT, factor TEXT, "
                "reference TEXT, last_step INTEGER, PRIMARY KEY (scope, subject, factor));"
            )

    def create(self, attempt):
        with sqlite3.connect(self.path) as db:
            db.execute(
                "INSERT INTO attempt VALUES (?, ?)",
                (attempt.attempt_id, pickle.dumps(attempt)),
            )

    def get(self, attempt_id):
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                "SELECT snapshot FROM attempt WHERE id = ?", (attempt_id,)
            ).fetchone()
        return pickle.loads(row[0]) if row else None

    @staticmethod
    def _key(binding):
        return binding.scope, binding.subject, binding.factor

    def active(self, binding):
        with sqlite3.connect(self.path) as db:
            return db.execute(
                "SELECT reference, last_step FROM factor WHERE scope = ? AND subject = ? AND factor = ?",
                self._key(binding),
            ).fetchone()

    def commit(self, attempt, proof, *, now):
        with sqlite3.connect(self.path) as db:
            db.execute("BEGIN IMMEDIATE")
            pending = db.execute(
                "SELECT snapshot FROM attempt WHERE id = ?", (attempt.attempt_id,)
            ).fetchone()
            if pending != (pickle.dumps(attempt),) or now >= attempt.expires_at:
                return False
            key = self._key(attempt.binding)
            active = db.execute(
                "SELECT reference, last_step FROM factor WHERE scope = ? AND subject = ? AND factor = ?",
                key,
            ).fetchone()
            update = proof.credential
            if attempt.kind == CeremonyKind.ENROLLMENT:
                if (active[0] if active else None) != attempt.replace_reference:
                    return False
                db.execute(
                    "INSERT INTO factor VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT (scope, subject, factor) DO UPDATE "
                    "SET reference = excluded.reference, last_step = excluded.last_step",
                    (*key, update.reference, update.verified_step),
                )
            else:
                if active != (update.reference, update.previous_step):
                    return False
                db.execute(
                    "UPDATE factor SET last_step = ? WHERE scope = ? AND subject = ? AND factor = ?",
                    (update.verified_step, *key),
                )
            db.execute("DELETE FROM attempt WHERE id = ?", (attempt.attempt_id,))
            return True

    def cancel(self, attempt):
        with sqlite3.connect(self.path) as db:
            return (
                db.execute(
                    "DELETE FROM attempt WHERE id = ? AND snapshot = ?",
                    (attempt.attempt_id, pickle.dumps(attempt)),
                ).rowcount
                == 1
            )


@pytest.fixture
def host(tmp_path):
    store = _SqliteFactors(tmp_path / "factors.db")
    binding = FactorBinding("tenant-1", "account-1", "totp", "account-change")
    now = [datetime(2026, 1, 2, tzinfo=timezone.utc)]
    secrets = {"old": new_secret(), "new": new_secret()}

    def resolve(attempt):
        reference = attempt.credential_reference
        if attempt.kind == CeremonyKind.ENROLLMENT:
            return TotpCredential(reference, secrets[reference])
        active = store.active(attempt.binding)
        return (
            TotpCredential(active[0], secrets[active[0]], active[1]) if active else None
        )

    verifiers = {"totp": totp_verifier(TotpLocalAuthenticator(), resolve)}
    return (
        EnrollmentRuntime(store, verifiers, clock=lambda: now[0]),
        StepUpRuntime(store, verifiers, clock=lambda: now[0]),
        store,
        binding,
        now,
        lambda reference: hotp(
            decode_secret(secrets[reference]), time_step(int(now[0].timestamp()))
        ),
    )


def test_invalid_replacement_and_cancellation_keep_old_factor(host):
    enrollment, _, store, binding, _, code = host
    started = enrollment.begin(binding, credential_reference="old")
    assert started.status is LifecycleStatus.CHALLENGE_REQUIRED
    assert store.active(binding) is None
    assert enrollment.complete(
        started.attempt.attempt_id, binding, code("old")
    ).status is (LifecycleStatus.COMPLETED)
    replacement = enrollment.begin(
        binding, credential_reference="new", replace_reference="old"
    ).attempt
    original = store.active(binding)
    assert (
        enrollment.complete(replacement.attempt_id, binding, "invalid").status
        is LifecycleStatus.REJECTED
    )
    assert store.active(binding) == original
    assert enrollment.cancel(replacement.attempt_id, binding)
    assert (
        enrollment.complete(replacement.attempt_id, binding, code("new")).status
        is LifecycleStatus.REJECTED
    )
    assert store.active(binding) == original


def test_scope_purpose_and_enrollment_expiry(host):
    enrollment, step_up, store, binding, now, code = host
    started = enrollment.begin(
        binding, credential_reference="old", ttl=timedelta(seconds=1)
    ).attempt
    for other in (
        replace(binding, scope="tenant-2"),
        replace(binding, subject="account-2"),
        replace(binding, purpose="sign-in"),
    ):
        assert (
            enrollment.complete(started.attempt_id, other, code("old")).status
            is LifecycleStatus.REJECTED
        )
    assert (
        step_up.complete(started.attempt_id, binding, code("old")).status
        is LifecycleStatus.REJECTED
    )
    now[0] = started.expires_at
    assert (
        enrollment.complete(started.attempt_id, binding, code("old")).status
        is LifecycleStatus.EXPIRED
    )
    assert store.active(binding) is None


def test_concurrent_completion_commits_factor_once(host):
    enrollment, _, store, binding, _, code = host
    started = enrollment.begin(binding, credential_reference="new").attempt
    proof = code("new")

    def complete(_):
        return enrollment.complete(started.attempt_id, binding, proof).status

    with ThreadPoolExecutor(max_workers=8) as pool:
        statuses = list(pool.map(complete, range(8)))
    assert statuses.count(LifecycleStatus.COMPLETED) == 1
    assert statuses.count(LifecycleStatus.REJECTED) == 7
    assert store.active(binding)[0] == "new"


def test_totp_step_up_is_fresh_subject_bound_and_not_replayable(host):
    enrollment, step_up, _, binding, now, code = host
    started = enrollment.begin(binding, credential_reference="old").attempt
    assert (
        enrollment.complete(started.attempt_id, binding, code("old")).status
        is LifecycleStatus.COMPLETED
    )
    attempt = step_up.begin(binding, credential_reference="old").attempt
    assert (
        step_up.complete(attempt.attempt_id, binding, code("old")).status
        is LifecycleStatus.REJECTED
    )
    now[0] += timedelta(seconds=30)
    accepted = step_up.complete(attempt.attempt_id, binding, code("old"))
    assert accepted.status is LifecycleStatus.COMPLETED
    next_attempt = step_up.begin(binding, credential_reference="old").attempt
    assert (
        step_up.complete(next_attempt.attempt_id, binding, code("old")).status
        is LifecycleStatus.REJECTED
    )

    otp = AssuranceRequirement(frozenset({"otp"}), timedelta(seconds=30))
    both = AssuranceRequirement(frozenset({"pwd", "otp"}), timedelta(seconds=30))
    query = {
        "scope": binding.scope,
        "subject": binding.subject,
        "purpose": binding.purpose,
        "now": now[0],
    }
    proofs = (accepted.assurance,)
    assert satisfies_assurance(proofs, otp, **query)
    assert not satisfies_assurance(proofs, both, **query)
    assert satisfies_assurance(
        (*proofs, FactorAssurance(binding, "pwd", now[0])), both, **query
    )
    assert not satisfies_assurance(
        proofs, otp, **(query | {"subject": "different-subject"})
    )
    assert not satisfies_assurance(
        proofs, otp, **(query | {"now": now[0] + timedelta(seconds=31)})
    )
