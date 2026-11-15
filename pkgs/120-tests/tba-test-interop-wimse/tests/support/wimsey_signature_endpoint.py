"""Compose the independent wimsey signature component with the WIC lab."""

from contextlib import contextmanager
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from time import time
from urllib.parse import urlsplit
from cryptography.hazmat.primitives.asymmetric import ec

from tba_primitives_identity import base64url_encode
from tba_test_interop_wimse.adapters.wimsey_wic import WIMSEY_REVISION, WimseyVerifier
from tba_test_interop_wimse.httpsig import SignatureCaller, SignatureReceiver
from tba_test_interop_wimse.signatures import ATTRIBUTE, PARAMS
from tba_test_interop_wimse.wpt import audience

from support.wic_fixture import WicFixture
from support.wimsey_endpoint import CONFIGURATION
from support.wpt_fixture import WptFixture, public_jwk
from support.wimsey_wpt import PROFILE as WPT_PROFILE, SLOT as WPT_SLOT, wpt_endpoints
from support.cofide_endpoint import PROFILE as COFIDE_PROFILE, REVISION as COFIDE_REVISION, cofide_hop
from support.cred_endpoint import PROFILE as CRED_PROFILE, REVISION as CRED_REVISION, cred_hop

SLOT = "combined-signature-candidate"
PROFILE = "wic-mtls-http-signature"
PEER_SLOTS = {"wic-mtls": "wimsey", PROFILE: SLOT, WPT_PROFILE: WPT_SLOT, COFIDE_PROFILE: "cofide", CRED_PROFILE: "cred"}
STANDALONE_PROFILES = {COFIDE_PROFILE, CRED_PROFILE}
PEER_REVISIONS = {COFIDE_PROFILE: COFIDE_REVISION, CRED_PROFILE: CRED_REVISION}
VARIANTS = {
    "01": {"valid-peer"},
    "02": {"untrusted-domain", "wrong-anchor"},
    "03": {"missing-workload-uri", "multiple-workload-uris", "wrong-server-identity"},
    "04": {"validated-origin-proof", "trusted-origin-handoff", "missing-origin-identity"},
    "05": {"missing-proof", "wrong-proof-key", "wrong-audience"},
    "06": {"first-presentation", "duplicate-presentation"},
    "07": {"local-token", "token-binding-mismatch"},
    "08": {"destination-access-token", "foreign-transaction-token"},
    "09": {"autonomous-delegated-only", "delegated-outside-scope", "delegated-in-scope"},
    "12": {"no-revocation", "revocation-before-effect"},
    "15": {"unchanged", "signed-authority-changed", "signed-path-changed", "trusted-proxy-verification"},
    "19": {"identity-equality-policy", "trusted-gateway-mapping"},
}
from support.wic_support_cases import SUPPORT_FAMILIES, WicSupportFixture
from support.wic_policy import POLICY_INPUTS, WicPolicyFixture
from support.signature_cases import SignatureHop, SignatureBoundaryCase, verify_spiffe_wit


def run_signature(binary, command, args):
    result = subprocess.run([str(binary), "httpsig", command, *args],
                            capture_output=True, text=True, timeout=10)
    if result.returncode:
        message = result.stderr.strip()
        if result.returncode != 1 or not message.startswith("error:"):
            raise RuntimeError(f"wimsey signature command failed: {message}")
        raise ValueError(message)
    return result.stdout


class WimseySignatureAdapter:
    families = VARIANTS.keys()

    def __init__(self, directory, binary, issuer, *, wpt_bridge=None, signature=True,
                 wimse_signatures=False, wimse_wpt=False, cofide_bridge=None, cred_bridge=None):
        self.directory, self.binary, self.issuer = directory, binary, issuer
        self.wpt_bridge = wpt_bridge
        self.cofide_bridge = cofide_bridge
        self.cred_bridge = cred_bridge
        self.profiles = {PROFILE} if signature else set()
        self.signature_schemes = {"spiffe", "wimse"} if wimse_signatures else {"spiffe"}
        self.wpt_schemes = {"spiffe", "wimse"} if wimse_wpt else {"spiffe"}
        if wpt_bridge is not None:
            self.profiles.add(WPT_PROFILE)
        if cofide_bridge is not None:
            self.profiles.add(COFIDE_PROFILE)
        if cred_bridge is not None:
            self.profiles.add(CRED_PROFILE)
        if self.profiles & STANDALONE_PROFILES:
            self.families = self.families | POLICY_INPUTS.keys() | SUPPORT_FAMILIES.keys()

    def supports(self, case):
        family = case["scenario_id"]
        has_standalone = any(hop["profile"] in STANDALONE_PROFILES for hop in case["hops"].values())
        if (case["variant"] not in VARIANTS.get(family, ())
                and not (has_standalone and family in POLICY_INPUTS.keys() | SUPPORT_FAMILIES.keys())):
            return False
        return any(hop["profile"] in self.profiles for hop in case["hops"].values()) and all(
            (hop["profile"] == "wic-mtls" or
             hop["profile"] in self.profiles
             and hop["identifier_scheme"] in (
                 self.signature_schemes if hop["profile"] == PROFILE else
                 {"none"} if hop["profile"] in STANDALONE_PROFILES else self.wpt_schemes
             )
             and (hop["wit_issuer"] == "baseline" or self.issuer is not None and self.issuer.alternate))
            and (hop["wic_issuer"] in {"baseline", "none"} or self.issuer is not None)
            for hop in case["hops"].values()
        )

    def supports_execution(self, case, execution):
        return all(({row["implementation"] for row in pair.values()} ==
                    {"tba", PEER_SLOTS[hop["profile"]]}
                and all(row.get("configuration") == CONFIGURATION for row in pair.values())
                and any(row["implementation"] != "tba" and row.get("version") ==
                        PEER_REVISIONS.get(hop["profile"], WIMSEY_REVISION)
                        for row in pair.values()))
            for name, hop in case["hops"].items() for pair in (execution["pairs"][name],))

    def setup_key(self, case, execution):
        return CONFIGURATION, execution["direction"], tuple(
            (hop["profile"], hop["identifier_scheme"], hop["wic_issuer"], hop["wit_issuer"])
            for hop in case["hops"].values()
        )

    def check_setup(self, case, execution):
        with self.hops(dict(case, scenario_id="01", variant="valid-peer", layer="operation"), execution) as hops:
            for fixture in hops.values():
                observed = fixture.observe()
                assert observed.decision == "allow" and observed.effects == 1, observed
            assert observed.decision == "allow" and observed.effects == 1, observed
            return observed

    @contextmanager
    def hop(self, case, direction, hop, names):
        with TemporaryDirectory(dir=self.directory) as work:
            location = Path(work)
            if hop["profile"] == COFIDE_PROFILE:
                yield cofide_hop(location, case, direction, self.cofide_bridge, self.issuer, names)
                return
            if hop["profile"] == CRED_PROFILE:
                yield cred_hop(location, case, direction, self.cred_bridge, self.issuer, names)
                return
            wic_case = case if case["layer"] == "tls" else dict(case, variant="valid-peer")
            wic = WicFixture(
                location, wic_case, scheme=hop["identifier_scheme"], direction=direction,
                external_verifier=lambda anchor, identity, status:
                    WimseyVerifier(self.binary, anchor, identity, status_provider=status),
                issue_pair=self.issuer.issue_pair if hop["wic_issuer"] != "baseline" else None,
                **names,
            )
            if hop["profile"] == "wic-mtls":
                yield wic
                return
            binary = self.binary
            use_spire = hop["wit_issuer"] == "spire-wit-svid"

            class PeerCaller(SignatureCaller):
                def present(self, dns_name, port, *, readback=False, extra_headers=None, signed_path=None,
                            signed_authority=None):
                    key = location / "peer-signing-key.json"
                    raw = (self.signer.private_numbers().private_value.to_bytes(32,"big")
                           if isinstance(self.signer, ec.EllipticCurvePrivateKey)
                           else self.signer.private_bytes_raw())
                    key.write_text(json.dumps({**public_jwk(self.signer),
                                              "d": base64url_encode(raw)}),
                                   encoding="ascii")
                    path = "/effects" if readback else "/writes"
                    args = ["--pop-key", str(key), "--method", "GET" if readback else "POST",
                            "--authority", signed_authority or f"{dns_name}:{port}", "--path", signed_path or path,
                            "--aud", audience(dns_name, port, path), "--wit", self.wit,
                            "--expires-in", "60"]
                    extra = {name.lower(): value for name, value in (extra_headers or {}).items()}
                    if signed_authority:
                        args.extend(("--cover", "@method,@path,@query,workload-identity-token,@authority"))
                    for name, value in extra.items():
                        if name.lower() in {"txn-token", "authorization"}:
                            args.extend(("--header", f"{name}: {value}"))
                    output = run_signature(binary, "sign", args)
                    return {"workload-identity-token": self.wit, **{
                        name.lower(): value
                        for name, value in (line.split(": ", 1) for line in output.splitlines())
                    }, **extra}

            class PeerReceiver(SignatureReceiver):
                def authenticate_proof(self, request, path):
                    headers = request.headers
                    if any(len(headers.get_all(name, ())) != 1
                           for name in ("workload-identity-token", "signature-input", "signature")):
                        raise ValueError("expected one WIT and signature")
                    if headers.get("Transfer-Encoding") or headers.get("Content-Length", "0") != "0":
                        raise ValueError("signature fixture accepts bodyless requests only")
                    now = int(time())
                    issuer = location / "trusted-wit-issuer.json"
                    authority = f"{self.dns_name}:{self.server_port}"
                    args = ["--issuer-jwk", str(issuer), "--wit", headers["workload-identity-token"],
                            "--authority", authority, "--path", path, "--method", request.command,
                            "--signature-input", headers["signature-input"], "--signature", headers["signature"],
                            "--aud", audience(self.dns_name, self.server_port, path), "--now", str(now)]
                    for name in ("txn-token", "authorization"):
                        if headers.get(name):
                            args.extend(("--header", f"{name}: {headers[name]}"))
                    result = json.loads(run_signature(binary, "verify", args))
                    subject = urlsplit(result["sub"])
                    if subject.scheme != ("spiffe" if use_spire else "wimse") or subject.netloc != "example.org":
                        raise ValueError("untrusted WIT subject domain")
                    parsed = PARAMS.fullmatch(headers["signature-input"])
                    if parsed is None:
                        raise ValueError("unsupported signature nonce encoding")
                    params = dict(ATTRIBUTE.findall(parsed["attributes"]))
                    key = "wimsey-signature:" + result["sub"] + ":" + params["nonce"]
                    if not self.replay_store.check_and_store(key, now=now, ttl_s=max(1, int(params["expires"]) - now + 5)):
                        raise ValueError("HTTP signature replay rejected")
                    return result["sub"]

            class SpireReceiver(SignatureReceiver):
                verify_credential = staticmethod(verify_spiffe_wit)

            # Keep the application proof valid when testing a transport refusal.
            proof_case = dict(case, variant="valid-peer") if case["layer"] == "tls" else case
            subject_scheme = "spiffe" if use_spire else "wimse"
            identity = f"{subject_scheme}://{wic.identity.split('://', 1)[1]}"

            def issue(subject, *, alternate=False):
                issuer = self.issuer.foreign if urlsplit(subject).netloc == "other.example" else self.issuer
                return issuer.mint_wit(subject, alternate=alternate)

            proof_options = {}
            if hop["profile"] == WPT_PROFILE:
                paths = (location / "peer-signing-key.json", location / "trusted-wit-issuer.json")
                peer_caller, peer_receiver = wpt_endpoints(self.wpt_bridge, *paths, spire=use_spire)
                native_caller, native_receiver = wpt_endpoints(None, *paths, spire=use_spire)
                proof_options = {
                    "proof_caller": peer_caller if direction == "reverse" else native_caller,
                    "proof_receiver": peer_receiver if direction == "forward" else native_receiver,
                }
            fixture = WptFixture(
                location, proof_case, wic=wic,
                identity=identity, issued_wit=issue if use_spire else None,
                signature_caller=PeerCaller if direction == "reverse" else SignatureCaller,
                signature_receiver=PeerReceiver if direction == "forward" else SpireReceiver if use_spire else SignatureReceiver,
                **proof_options,
            )
            # A SPIFFE peer has a separate transport principal and WIMSE WIT.
            # The shared receiver fixture enforces the configured pair.
            (location / "trusted-wit-issuer.json").write_text(
                json.dumps(fixture.trust["example.org"][0]), encoding="ascii",
            )
            yield fixture

    @contextmanager
    def hops(self, case, execution):
        from contextlib import ExitStack

        with ExitStack() as stack:
            hops = {}
            for name, row in case["hops"].items():
                local = dict(case, hops={name: row}, target_hop=name)
                direction = execution["direction"]
                names = {}
                if len(case["hops"]) == 2:
                    local.update(variant="valid-peer", layer="operation")
                    names = (dict(caller_name="origin", receiver_name="gateway") if name == "ingress"
                             else dict(caller_name="gateway", receiver_name="resource"))
                    if name == "enforcing":
                        direction = "reverse" if direction == "forward" else "forward"
                        if case["variant"] == "trust-refused" and case["layer"] == "tls":
                            local.update(variant="wrong-server-identity", layer="tls")
                hops[name] = stack.enter_context(self.hop(local, direction, row, names))
            yield hops

    @contextmanager
    def isolated(self, case, execution):
        with self.hops(case, execution) as hops:
            family = case["scenario_id"]
            enforcing = hops[case["target_hop"]]
            if family in SUPPORT_FAMILIES or family == "19" and len(hops) == 2:
                endpoints = {
                    name: SignatureHop(hop, operation_variant=(
                        "wrong-anchor" if name == case["target_hop"] and case["variant"] == "trust-refused"
                        and case["layer"] == "application" else "valid-peer"))
                    if isinstance(hop, WptFixture) else hop for name, hop in hops.items()
                }
                fixture = WicSupportFixture(case, endpoints)
                yield SignatureBoundaryCase(case, endpoints["enforcing"], gateway=fixture) if family == "19" else fixture
            elif family in POLICY_INPUTS:
                yield WicPolicyFixture(SignatureHop(enforcing), family, case["variant"])
            elif family in {"07", "15"}:
                yield SignatureBoundaryCase(case, SignatureHop(enforcing))
            else:
                yield enforcing


class PeerLabAdapter:
    """Dispatch each profile to its independently pinned implementation."""

    def __init__(self, wic, signature=None):
        self.wic, self.signature = wic, signature
        self.families = wic.families | (signature.families if signature else set())

    def adapter(self, case):
        return self.signature if any(hop["profile"] in (PROFILE, WPT_PROFILE, COFIDE_PROFILE, CRED_PROFILE)
                                     for hop in case["hops"].values()) else self.wic

    def supports(self, case):
        adapter = self.adapter(case)
        return adapter is not None and adapter.supports(case)

    def supports_execution(self, case, execution):
        return self.adapter(case).supports_execution(case, execution)

    def setup_key(self, case, execution):
        return self.adapter(case).setup_key(case, execution)

    def check_setup(self, case, execution):
        return self.adapter(case).check_setup(case, execution)

    def isolated(self, case, execution):
        return self.adapter(case).isolated(case, execution)
