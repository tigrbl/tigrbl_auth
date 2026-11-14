"""Pin and run Cred's independent WIT/WPT components in the HTTPS lab."""

from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess

from tba_primitives_identity import base64url_encode
from cryptography.hazmat.primitives.asymmetric import ec

from support.wimsey_wpt import CONTEXT_HEADER, wpt_endpoints
from support.wpt_fixture import WptFixture, public_jwk

PROFILE = "wit-wpt"
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


def cred_hop(directory, case, direction, bridge, issuer, names):
    use_spire = case["hops"][case["target_hop"]]["wit_issuer"] == "spire-wit-svid"
    scheme = "spiffe" if use_spire else "wimse"
    expected = f"{scheme}://example.org/{names.get('caller_name', 'workload')}"

    def issue(subject, *, alternate=False):
        selected = issuer.foreign if "://other.example/" in subject else issuer
        return selected.mint_wit(subject, alternate=alternate)

    def sign(key, **options):
        raw = (key.private_numbers().private_value.to_bytes(32, "big")
               if isinstance(key, ec.EllipticCurvePrivateKey) else key.private_bytes_raw())
        jwk = {**public_jwk(key), "d": base64url_encode(raw)}
        return call_bridge(bridge, command="sign", key=jwk, context_header=CONTEXT_HEADER, **options)["proof"]

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
