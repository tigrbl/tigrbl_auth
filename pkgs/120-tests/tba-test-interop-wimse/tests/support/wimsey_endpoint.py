"""Pinned wimsey verifier plus the shared TLS endpoint and test resource."""

from contextlib import contextmanager
from hashlib import sha256
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from tba_test_interop_wimse.adapters.wimsey_wic import WIMSEY_REVISION, WimseyVerifier

from support.wic_fixture import WicFixture
from support.wic_policy import POLICY_INPUTS, WicPolicyFixture
from support.wic_support_cases import SUPPORT_FAMILIES, WicSupportFixture

CONFIGURATION = "shared-python-tls-direct-ca-ledger-v1"
IDENTITY_FAMILIES = frozenset({"01", "02", "03"})


class WimseyWicAdapter:
    families = IDENTITY_FAMILIES | POLICY_INPUTS.keys() | SUPPORT_FAMILIES.keys()

    def __init__(self, directory, checkout, issuer=None):
        self.directory = directory
        self.issuer = issuer
        checkout = Path(checkout).resolve()
        revision = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True, timeout=10,
        ).strip()
        if revision != WIMSEY_REVISION:
            raise ValueError(f"Expected wimsey {WIMSEY_REVISION}, found {revision}")
        self.binary = checkout / "target/debug" / ("wimsey.exe" if os.name == "nt" else "wimsey")
        self.binary_sha256 = sha256(self.binary.read_bytes()).hexdigest()

    def supports(self, case):
        family = case["scenario_id"]
        if family not in self.families:
            return False
        if family in POLICY_INPUTS and case["variant"] not in POLICY_INPUTS[family]:
            return False
        return all(hop["profile"] == "wic-mtls" and (
            hop["wic_issuer"] == "baseline"
            or hop["wic_issuer"] == "spire-x509-svid" and self.issuer is not None
        ) for hop in case["hops"].values())

    def supports_execution(self, case, execution):
        return all(
            {row["implementation"] for row in pair.values()} == {"tba", "wimsey"}
            and all(row.get("configuration") == CONFIGURATION for row in pair.values())
            and any(row["implementation"] == "wimsey" and row.get("version") == WIMSEY_REVISION
                    for row in pair.values())
            for pair in execution["pairs"].values()
        )

    def setup_key(self, case, execution):
        return execution["direction"], tuple((hop["identifier_scheme"], hop["wic_issuer"])
                                             for hop in case["hops"].values())

    def check_setup(self, case, execution):
        with self.isolated(dict(case, scenario_id="01", variant="valid-peer", checker="receiver"),
                           execution) as fixture:
            observed = fixture.observe()
            assert observed.decision == "allow" and observed.effects == 1, observed
            return observed

    def check_issuers(self, case, execution):
        control = dict(case, scenario_id="01", variant="valid-peer")
        observations = {}
        with self.materialize(control, execution) as hops:
            for name, fixture in hops.items():
                observed = fixture.observe()
                assert observed.decision == "allow" and observed.effects == 1, observed
                observations[name] = observed
        return observations

    @contextmanager
    def materialize(self, case, execution):
        def verifier(anchor, identity, status):
            return WimseyVerifier(self.binary, anchor, identity, status_provider=status)

        with TemporaryDirectory(dir=self.directory) as directory:
            family = case["scenario_id"]
            hops = {}
            for name, hop in case["hops"].items():
                location = Path(directory) / name
                location.mkdir()
                direction = execution["direction"]
                if name == "enforcing" and "ingress" in case["hops"]:
                    direction = {"forward": "reverse", "reverse": "forward"}[direction]
                local_case = case
                if name == "enforcing" and family == "20" and case["variant"] == "trust-refused":
                    local_case = dict(case, variant="wrong-server-identity")
                issue_pair = self.issuer.issue_pair if hop["wic_issuer"] == "spire-x509-svid" else None
                names = {}
                if len(case["hops"]) == 2:
                    names = ({"caller_name": "origin", "receiver_name": "gateway"} if name == "ingress"
                             else {"caller_name": "gateway", "receiver_name": "resource"})
                hops[name] = WicFixture(
                    location, local_case, scheme=hop["identifier_scheme"], external_verifier=verifier,
                    direction=direction, issue_pair=issue_pair, **names,
                )
            yield hops

    @contextmanager
    def isolated(self, case, execution):
        with self.materialize(case, execution) as hops:
            family = case["scenario_id"]
            fixture = hops[case["target_hop"]]
            if family in SUPPORT_FAMILIES:
                yield WicSupportFixture(case, hops)
            elif family in POLICY_INPUTS:
                yield WicPolicyFixture(fixture, family, case["variant"])
            else:
                yield fixture
