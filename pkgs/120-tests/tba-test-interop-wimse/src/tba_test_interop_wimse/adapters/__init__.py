"""In-process reference fixtures for the ordering and effect contracts."""
from contextlib import contextmanager

from ..observations import Observation


class LocalPolicyFixture:
    """Exercise a local ledger and a recording provider with synthetic authority."""

    def __init__(self, case):
        self.case = case
        self.revoked = False
        self.ledger = []
        self.tokens = []
        self.events = []

    def authorize(self):
        return not self.revoked

    def commit(self):
        if not self.authorize():
            return False
        self.ledger.append("operation")
        return True

    def release(self, scope):
        if scope != "write" or not self.authorize():
            return None
        self.tokens.append("fixture-token")
        return self.tokens[-1]

    def revoke(self):
        self.revoked = True
        self.events.append("revocation-observed")

    def observe(self):
        variant = self.case["variant"]
        family = self.case["scenario_id"]
        if variant in {"missing-delegation", "readonly-grant-write"}:
            token = self.release(None if variant == "missing-delegation" else "read")
            assert token is None
            self.events.extend(("broker-refused", "no-bearer-release"))
            return self.result("deny")
        assert self.authorize()
        self.events.append("initial-allow")
        if family == "12":
            if variant == "revocation-before-effect":
                self.revoke()
            committed = self.commit()
            self.events.append("commit" if committed else "commit-refused")
            return self.result("allow" if committed else "deny")
        if variant == "revocation-before-release":
            self.revoke()
        token = self.release("write")
        if token is None:
            self.events.append("release-refused")
            return self.result("deny")
        self.events.append("bearer-released")
        if variant == "revocation-after-release":
            self.revoke()
        assert token in self.tokens
        self.ledger.append("provider-operation")
        if variant == "revocation-after-release":
            self.events.append("provider-decision")
            return self.result("provider-policy")
        self.events.append("provider-effect")
        return self.result("allow")

    def result(self, decision):
        return Observation(decision, self.case["target_hop"], tuple(self.events),
                           len(self.ledger), len(self.tokens), reason="reference fixture policy")


class LocalPolicyAdapter:
    """Reference behavior only. This adapter supplies no wire or release evidence."""

    def supports(self, case):
        return case["scenario_id"] in {"12", "18"}

    def setup_key(self, case, execution):
        return "in-process-policy"

    def check_setup(self, case, execution):
        control = LocalPolicyFixture(case)
        assert control.authorize() and control.commit()
        assert control.release("write") is not None

    @contextmanager
    def isolated(self, case, execution):
        yield LocalPolicyFixture(case)


REFERENCE_ADAPTERS = {family: LocalPolicyAdapter() for family in ("12", "18")}
