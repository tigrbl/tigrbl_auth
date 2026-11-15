"""Use the pinned go-spiffe identity verifier on either side of lab mTLS."""

from base64 import b64encode
from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from tba_contracts_security_trust import CertificateStatus
from tba_test_interop_wimse.qualification import pair_has_baseline

from support.wic_fixture import WicFixture
from support.wic_policy import POLICY_INPUTS
from support.wic_support_cases import SUPPORT_FAMILIES
from support.wimsey_signature_endpoint import WimseySignatureAdapter


PEER = "go-spiffe"
REVISION = "8c6e059350b69c072aaebb41f70592faf20202c8"


class SpiffePeerVerifier:
    workload_name_only = True

    def __init__(self, command, anchor, identity, status):
        self.command = command
        self.anchor = anchor
        self.expected_identity = identity
        self.status = status

    def verify(self, certificate, *, dns_name=None):
        request = {"certificate": b64encode(certificate).decode("ascii"),
                   "anchor": str(self.anchor), "expected": self.expected_identity}
        result = subprocess.run(self.command, input=json.dumps(request),
                                capture_output=True, text=True, timeout=5)
        if result.returncode == 1 and result.stderr:
            raise ValueError(result.stderr.strip())
        result.check_returncode()
        identity = json.loads(result.stdout)
        assert identity == self.expected_identity
        if self.status.status(certificate).status != CertificateStatus.GOOD:
            raise ValueError("SPIFFE lab certificate status was not confirmed")
        return identity


@contextmanager
def spiffe_peer_hop(directory, command, issuer, case, direction, hop, names):
    with TemporaryDirectory(dir=directory) as work:
        issue_pair = issuer.issue_pair if hop["wic_issuer"] in {"spire-x509-svid", "teleport-x509-svid"} else None
        yield WicFixture(
            Path(work), case, scheme="spiffe", direction=direction, issue_pair=issue_pair,
            external_verifier=lambda anchor, identity, status: SpiffePeerVerifier(command, anchor, identity, status),
            **names,
        )


def go_spiffe_hop(directory, binary, issuer, case, direction, hop, names):
    return spiffe_peer_hop(directory, [str(binary), "verify"], issuer, case, direction, hop, names)


class SpiffePeerAdapter(WimseySignatureAdapter):
    families = WimseySignatureAdapter.families | POLICY_INPUTS.keys() | SUPPORT_FAMILIES.keys()

    def __init__(self, fallback, commands, peers, *, directory=None, issuer=None):
        self.fallback = fallback
        self.directory = directory if fallback is None else fallback.directory
        self.issuer = issuer if fallback is None else fallback.issuer
        self.commands = commands
        self.peers = peers

    def supports(self, case):
        return case["scenario_id"] in self.families

    def supports_execution(self, case, execution):
        return all(pair_has_baseline(self.peers, pair) for pair in execution["pairs"].values()) and any(
            endpoint["implementation"] in self.commands
            for pair in execution["pairs"].values() for endpoint in pair.values()
        )

    def setup_key(self, case, execution):
        pins = tuple(tuple(endpoint["implementation"] for endpoint in pair.values())
                     for pair in execution["pairs"].values())
        return super().setup_key(case, execution), pins

    def hops(self, case, execution):
        enriched = {}
        for name, hop in case["hops"].items():
            pair = execution["pairs"][name]
            enriched[name] = {**hop, **{f"{role}_pin": (endpoint["implementation"],)
                                       for role, endpoint in pair.items()}}
        return super().hops({**case, "hops": enriched}, execution)

    @contextmanager
    def hop(self, case, direction, hop, names):
        peer = next((hop[f"{role}_pin"][0] for role in ("caller", "receiver")
                    if hop.get(f"{role}_pin", (None,))[0] in self.commands), None)
        if peer:
            direction = "forward" if hop["receiver_pin"][0] == peer else "reverse"
            with spiffe_peer_hop(self.directory, self.commands[peer], self.issuer, case, direction, hop, names) as fixture:
                yield fixture
        elif self.fallback is not None:
            with self.fallback.hop(case, direction, hop, names) as fixture:
                yield fixture
        else:
            raise ValueError("SPIFFE hop has no registered caller or receiver verifier")
