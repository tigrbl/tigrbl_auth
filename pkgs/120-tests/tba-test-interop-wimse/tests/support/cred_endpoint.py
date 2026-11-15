"""Pin and run Cred's independent WIMSE components in the HTTPS lab."""

from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from time import time
from uuid import uuid4

from tba_primitives_identity import base64url_encode
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from tba_concrete_jwt import decode_jwt_unverified
from tba_provider_jose_cryptography import JwsCryptographyProvider
from tba_provider_jose_cryptography.jws import sign_compact_jwt
from tba_provider_jose_cryptography.public_jws import verify_public_jws
from tba_test_interop_wimse.httpsig import SignatureCaller, SignatureReceiver
from tba_test_interop_wimse.signatures import normalize
from tba_test_interop_wimse.wpt import audience

from support.signature_cases import SignatureBoundaryCase, SignatureHop
from support.wimsey_endpoint import CONFIGURATION
from support.wimsey_wpt import CONTEXT_HEADER, wpt_endpoints
from support.wpt_fixture import WptFixture, public_jwk

PROFILE = "wit-wpt"
HTTP_PROFILE = "wit-http-signature"
SLOT = "cred"
REVISION = "586e1a76f487c2376e0ba0a4687bb2de8d3eb588"


def build_cred_bridge(checkout, directory):
    checkout, directory = Path(checkout).resolve(), Path(directory).resolve()
    revision = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
    status = subprocess.check_output(["git", "-C", str(checkout), "status", "--porcelain",
                                      "--untracked-files=no"], text=True)
    if revision != REVISION or status:
        raise ValueError("Cred requires a clean checkout at the pinned revision")
    directory.mkdir(parents=True, exist_ok=True)
    bridge = directory / "cred_bridge.mjs"
    shutil.copyfile(Path(__file__).with_name(bridge.name), bridge)
    subprocess.run(["node", str(bridge), "build", str(checkout), str(directory)], check=True, timeout=30)
    return bridge


def bridge_digest(bridge):
    names = ("cred_bridge.mjs", "client.mjs", "issuers.mjs", "package.json", "wimse.js",
             "types.js", "http-signature.js", "structured-fields.js")
    digest = sha256()
    for name in names:
        digest.update(name.encode("ascii") + b"\0" + bridge.with_name(name).read_bytes())
    return digest.hexdigest()


def call_bridge(bridge, **request):
    result = subprocess.run(["node", str(bridge)], input=json.dumps(request), capture_output=True,
                            text=True, check=True, timeout=10)
    response = json.loads(result.stdout)
    if "denied" in response:
        raise ValueError(response["denied"])
    return response


def private_jwk(key):
    raw = (key.private_numbers().private_value.to_bytes(32, "big")
           if isinstance(key, ec.EllipticCurvePrivateKey) else key.private_bytes_raw())
    return {**public_jwk(key), "d": base64url_encode(raw)}


def cred_hop(directory, case, direction, bridge, issuer, names):
    use_spire = case["hops"][case["target_hop"]]["wit_issuer"] == "spire-wit-svid"
    scheme = "spiffe" if use_spire else "wimse"
    expected = f"{scheme}://example.org/{names.get('caller_name', 'workload')}"

    def issue(subject, *, alternate=False):
        selected = issuer.foreign if "://other.example/" in subject else issuer
        return selected.mint_wit(subject, alternate=alternate)

    def sign(key, **options):
        return call_bridge(bridge, command="sign", key=private_jwk(key),
                           context_header=CONTEXT_HEADER, **options)["proof"]

    def verify(headers, trust, **options):
        return call_bridge(bridge, command="verify", headers={name.lower(): value for name, value in headers.items()},
                           trust=trust, context_header=CONTEXT_HEADER, **options)

    caller, receiver = wpt_endpoints(None, None, None, spire=use_spire,
                                    peer_sign=sign if direction == "reverse" else None,
                                    peer_verify=verify if direction == "forward" else None)
    fixture = WptFixture(directory, case, proof_caller=caller, proof_receiver=receiver,
                         identity=expected, issued_wit=issue if use_spire else None)
    fixture.server_identity = f"{scheme}://example.org/{names.get('receiver_name', 'resource')}"
    return fixture


class LabTransactionIssuer:
    """Mint and validate short-lived OAuth transaction JWTs for this fixture."""

    def __init__(self, domain):
        key = Ed25519PrivateKey.generate()
        self.signer = JwsCryptographyProvider({"txn": key})
        self.anchor = {**public_jwk(key), "kid": "txn"}
        self.domain = domain

    def issue(self, subject, scope, *, nonce=None):
        now = int(time())
        return sign_compact_jwt(
            self.signer, {"aud": self.domain, "iat": now, "exp": now + 60, "txn": str(uuid4()),
                          "sub": subject, "req_wl": subject, "scope": scope,
                          "rctx": {}, "tctx": {"action": scope}},
            headers={"typ": "txntoken+jwt", "alg": "EdDSA", "kid": "txn"}, key_reference="txn",
        )

    def verify(self, serialized):
        verify_public_jws(serialized, self.anchor)
        token = decode_jwt_unverified(serialized)
        claims = token.claims
        if (token.jws.protected_headers.get("typ") != "txntoken+jwt" or claims["aud"] != self.domain
                or not claims["iat"] <= int(time()) < claims["exp"]):
            raise ValueError("invalid transaction token")
        return claims


class CredHttpSignatureAdapter:
    families = {"01", "07"}

    def __init__(self, directory, bridge):
        self.directory, self.bridge = directory, bridge

    def supports(self, case):
        hop = case["hops"][case["target_hop"]]
        return (case["scenario_id"] in self.families and len(case["hops"]) == 1
                and hop["profile"] == HTTP_PROFILE and hop["wit_issuer"] == "baseline")

    def supports_execution(self, case, execution):
        pair = execution["pairs"][case["target_hop"]]
        return ({row["implementation"] for row in pair.values()} == {"tba", SLOT}
                and all(row["configuration"] == CONFIGURATION for row in pair.values())
                and any(row["implementation"] == SLOT and row["version"] == REVISION
                        for row in pair.values()))

    def setup_key(self, case, execution):
        return SLOT, HTTP_PROFILE, execution["direction"]

    def check_setup(self, case, execution):
        with self.isolated(dict(case, scenario_id="01", variant="valid-peer"), execution) as fixture:
            observation = fixture.observe()
            assert observation.decision == "allow" and observation.effects == 1, observation
            return observation

    @contextmanager
    def isolated(self, case, execution):
        bridge = self.bridge

        class CredCaller(SignatureCaller):
            def present(self, dns_name, port, *, readback=False, extra_headers=None,
                        signed_path=None, signed_authority=None):
                path = "/effects" if readback else "/writes"
                return call_bridge(
                    bridge, command="sign-http", key=private_jwk(self.signer), wit=self.wit,
                    method="GET" if readback else "POST", path=signed_path or path,
                    headers=extra_headers or {}, audience=audience(dns_name, port, path), now=int(time()),
                )["headers"]

        class CredReceiver(SignatureReceiver):
            def authenticate_proof(self, request, path):
                if request.headers.get("Transfer-Encoding") or request.headers.get("Content-Length", "0") != "0":
                    raise ValueError("signature fixture accepts bodyless requests only")
                now = int(time())
                result = call_bridge(
                    bridge, command="verify-http", trust=self.trust_by_domain,
                    method=request.command, path=path, headers=normalize(request.headers.items()),
                    audience=audience(self.dns_name, self.server_port, path), now=now,
                )
                key = f"cred-httpsig:{result['sub']}:{result['nonce']}"
                if not self.replay_store.check_and_store(key, now=now, ttl_s=max(1, result["exp"] - now)):
                    raise ValueError("HTTP signature replay rejected")
                return result["sub"]

        reverse = execution["direction"] == "reverse"
        with TemporaryDirectory(dir=self.directory) as directory:
            fixture = WptFixture(
                Path(directory), case, signature_caller=CredCaller if reverse else SignatureCaller,
                signature_receiver=SignatureReceiver if reverse else CredReceiver,
            )
            if case["scenario_id"] == "07":
                yield SignatureBoundaryCase(
                    case, SignatureHop(fixture), transaction_issuer=LabTransactionIssuer("example.org"),
                )
            else:
                yield fixture
