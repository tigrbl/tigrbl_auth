"""Test resource policies for direct WIC runs with authenticated workload identities."""

from dataclasses import dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class PolicyInput:
    payload: dict
    denial: str = ""


def digest(content):
    return sha256(content.encode("utf-8")).hexdigest()


TOOL_PIN = digest("fixture tool, revision 1")
BUILD_PIN = digest("fixture build, revision 1")
PARENT = {"host": "resource.example.org", "methods": ["GET", "POST"], "expiry": 120}
CHILD = {**PARENT, "methods": ["POST"], "expiry": 110}
NOW = 100
STATUS_MAX_AGE = 5
STATUS_GRACE = 10
PROTECTED_VALUE = "synthetic-protected-value"
CREDENTIAL_VALUE = "synthetic-test-credential"


def authority(payload):
    # These grants and their scopes are receiver-side fixtures bound to the
    # authenticated identity. The request can select an authority, never grant one.
    if payload["authority"] != "delegated":
        raise ValueError("delegated-authority-required")
    if payload["operation"] != "write":
        raise ValueError("delegated-scope-mismatch")


def status_evidence(evidence, *, grace):
    if evidence is None:
        raise ValueError("delegated-status-unavailable")
    state, observed_at = evidence
    if state == "revoked":
        raise ValueError("delegated-status-revoked")
    age = NOW - observed_at
    if state != "good" or age < 0:
        raise ValueError("delegated-status-unavailable")
    if age > STATUS_MAX_AGE + grace:
        raise ValueError("delegated-status-grace-expired" if grace else "delegated-status-stale")


def validate_child(child):
    if child["host"] != PARENT["host"]:
        raise ValueError("child-host-outside-parent")
    if not child["methods"] or set(child["methods"]) - set(PARENT["methods"]):
        raise ValueError("child-method-outside-parent")
    if child["expiry"] > PARENT["expiry"]:
        raise ValueError("child-expiry-outside-parent")
    if child["expiry"] <= NOW:
        raise ValueError("child-expired")


def validate_pins(payload):
    if payload["tool"] != TOOL_PIN:
        raise ValueError("tool-digest-mismatch")
    if payload["build"] != BUILD_PIN:
        raise ValueError("build-claim-mismatch")


class ProtectedOperations:
    def __init__(self, *, allowed_operations, allowed_destinations):
        self.allowed_operations = allowed_operations
        self.allowed_destinations = allowed_destinations
        self.reads = []
        self.output_sink = []

    def perform(self, payload):
        # This endpoint represents the untrusted model channel. Its origin
        # comes from fixture configuration, independently of the request.
        operation = payload["operation"]
        if operation == "protected-read":
            if operation not in self.allowed_operations:
                raise ValueError("protected-read-outside-scope")
            self.reads.append(PROTECTED_VALUE)
        elif operation == "credential-disclosure":
            if payload["destination"] not in self.allowed_destinations:
                raise ValueError("credential-disclosure-forbidden")
            self.output_sink.append(CREDENTIAL_VALUE)
        else:
            raise ValueError("unknown-protected-operation")


STATUS_INPUTS = {
    "current-status": (("good", 98), 0, ""),
    "confirmed-revoked": (("revoked", 98), STATUS_GRACE, "delegated-status-revoked"),
    "stale-cache": (("good", 94), 0, "delegated-status-stale"),
    "unavailable-status": (None, 0, "delegated-status-unavailable"),
    "grace-period-expired": (("good", 84), STATUS_GRACE, "delegated-status-grace-expired"),
    "within-bounded-grace": (("good", 85), STATUS_GRACE, ""),
}

DELEGATED_WRITE = {"authority": "delegated", "operation": "write"}
MATCHING_PINS = {"tool": TOOL_PIN, "build": BUILD_PIN}
POLICY_INPUTS = {
    "09": {
        "autonomous-delegated-only": PolicyInput(
            {**DELEGATED_WRITE, "authority": "autonomous"}, "delegated-authority-required",
        ),
        "delegated-outside-scope": PolicyInput(
            {**DELEGATED_WRITE, "operation": "admin-write"}, "delegated-scope-mismatch",
        ),
        "delegated-in-scope": PolicyInput(DELEGATED_WRITE),
    },
    "10": {
        "protected-read-refused": PolicyInput(
            {"operation": "protected-read"}, "protected-read-outside-scope",
        ),
        "credential-disclosure-refused": PolicyInput(
            {"operation": "credential-disclosure", "destination": "model-output"},
            "credential-disclosure-forbidden",
        ),
    },
    "11": {variant: PolicyInput(DELEGATED_WRITE, denial)
           for variant, (_, _, denial) in STATUS_INPUTS.items()},
    "13": {
        "narrower-child-grant": PolicyInput(CHILD),
        "wider-host": PolicyInput({**CHILD, "host": "*.example.org"}, "child-host-outside-parent"),
        "extra-method": PolicyInput({**CHILD, "methods": ["POST", "DELETE"]}, "child-method-outside-parent"),
        "longer-expiry": PolicyInput({**CHILD, "expiry": 121}, "child-expiry-outside-parent"),
    },
    "16": {
        "matching-digests": PolicyInput(MATCHING_PINS),
        "tool-digest-mismatch": PolicyInput(
            {**MATCHING_PINS, "tool": digest("fixture tool, revision 2")}, "tool-digest-mismatch",
        ),
        "build-claim-mismatch": PolicyInput(
            {**MATCHING_PINS, "build": digest("fixture build, revision 2")}, "build-claim-mismatch",
        ),
    },
}


class WicPolicyFixture:
    def __init__(self, transport, family, variant):
        self.transport = transport
        self.family = family
        self.variant = variant
        self.input = POLICY_INPUTS[family][variant]
        self.protected = ProtectedOperations(
            allowed_operations={"public-read"},
            allowed_destinations={"private-credential-consumer"},
        )

    def authorize(self, identity, headers):
        if identity != self.transport.identity:
            raise ValueError("unexpected-policy-subject")
        payload = json.loads(headers.get("X-Fixture-Operation", "null"))
        if not isinstance(payload, dict):
            raise ValueError("missing-fixture-operation")
        if self.family == "11":
            authority(payload)
            evidence, grace, _ = STATUS_INPUTS[self.variant]
            status_evidence(evidence, grace=grace)
        else:
            checks = {"09": authority, "10": self.protected.perform,
                      "13": validate_child, "16": validate_pins}
            checks[self.family](payload)

    def check_response(self, result):
        if self.family == "10":
            assert not self.protected.reads
            assert not self.protected.output_sink
            response = json.dumps(result["response"])
            assert PROTECTED_VALUE not in response and CREDENTIAL_VALUE not in response

    def observe(self):
        observed = self.transport.observe(
            authorize_write=self.authorize,
            headers={"X-Fixture-Operation": json.dumps(self.input.payload)},
            check_response=self.check_response,
        )
        assert observed.reason == (self.input.denial or self.transport.identity), observed
        return observed
