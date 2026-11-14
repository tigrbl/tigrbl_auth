"""WPT caller and receiver for the pinned wimsey lab composition."""

from hashlib import sha256
import json
import os
from pathlib import Path
from secrets import token_urlsafe
import shutil
import subprocess
from time import time
from urllib.parse import urlsplit

from cryptography.hazmat.primitives.asymmetric import ec
from tba_concrete_jwt import decode_jwt_unverified
from tba_primitives_identity import base64url_encode
from tba_profile_workload_credential_wimse_wit import verify_wit
from tba_profile_workload_proof_wimse_wpt import verify_wpt
from tba_test_interop_wimse.wpt import WptCaller, WptReceiver, audience

from support.signature_cases import verify_spiffe_wit
from support.wpt_fixture import public_jwk, sign_wpt_claims

PROFILE = "wic-mtls-wpt"
SLOT = "combined-wpt-candidate"
CONTEXT_HEADER = "x-destination-access-token"


def build_bridge(checkout, directory):
    checkout, directory = Path(checkout).resolve(), Path(directory).resolve()
    crates = checkout / "crates"
    key_module = json.dumps((crates / "cli/src/key.rs").as_posix())
    source = Path(__file__).with_name("wimsey_wpt_bridge.rs")
    (directory / "main.rs").write_text(f"#[allow(dead_code)]\n#[path = {key_module}]\nmod key;\n" +
                                      source.read_text(encoding="utf-8"), encoding="utf-8")
    dependencies = "\n".join(f'wimsey-{name} = {{ path = "{(crates / name).as_posix()}" }}'
                             for name in ("jose", "wit", "wpt"))
    manifest = directory / "Cargo.toml"
    manifest.write_text(
        '[package]\nname = "tba-wimsey-wpt-bridge"\nversion = "0.0.0"\nedition = "2021"\n'
        '[[bin]]\nname = "tba-wimsey-wpt-bridge"\npath = "main.rs"\n'
        '[dependencies]\nserde = { version = "1", features = ["derive"] }\nserde_json = "1"\n'
        + dependencies + "\n", encoding="utf-8",
    )
    shutil.copyfile(checkout / "Cargo.lock", directory / "Cargo.lock")
    subprocess.run(["cargo", "build", "--offline", "--quiet", "--manifest-path", str(manifest),
                    "--target-dir", str(checkout / "target")], check=True, timeout=120)
    binary = checkout / "target/debug/tba-wimsey-wpt-bridge"
    return binary.with_suffix(".exe") if os.name == "nt" else binary


def bridge(binary, **request):
    result = subprocess.run([str(binary)], input=json.dumps(request), capture_output=True,
                            text=True, check=True, timeout=10)
    response = json.loads(result.stdout)
    if "denied" in response:
        raise ValueError(response["denied"])
    return response


def token_hash(token):
    return base64url_encode(sha256(token.strip().encode("ascii")).digest())


def wpt_endpoints(binary, signing_key, issuer_key, *, spire, peer_sign=None, peer_verify=None):
    class Caller(WptCaller):
        def present(self, dns_name, port, *, readback=False, extra_headers=None):
            headers = {name.lower(): value for name, value in (extra_headers or {}).items()}
            if {"authorization", "workload-identity-token"} & headers.keys():
                raise ValueError("WPT proof headers are reserved")
            path = "/effects" if readback else "/writes"
            target = audience(dns_name, port, path)
            now = int(time())
            transaction, context = headers.get("txn-token"), headers.get(CONTEXT_HEADER)
            jti = token_urlsafe(16)
            if peer_sign:
                proof = peer_sign(self.signer, wit=self.wit, audience=target, now=now, jti=jti,
                                  transaction=transaction, context=context)
            elif binary:
                raw = (self.signer.private_numbers().private_value.to_bytes(32, "big")
                       if isinstance(self.signer, ec.EllipticCurvePrivateKey) else self.signer.private_bytes_raw())
                signing_key.write_text(json.dumps({**public_jwk(self.signer), "d": base64url_encode(raw)}),
                                       encoding="ascii")
                proof = bridge(binary, command="sign", key=str(signing_key), wit=self.wit, audience=target,
                               now=now, jti=jti, transaction=transaction, context=context)["proof"]
            else:
                claims = {"aud": target, "exp": now + 60, "jti": jti, "wth": token_hash(self.wit)}
                if transaction is not None:
                    claims["tth"] = token_hash(transaction)
                if context is not None:
                    claims["oth"] = {CONTEXT_HEADER: token_hash(context)}
                algorithm = decode_jwt_unverified(self.wit).claims["cnf"]["jwk"]["alg"]
                proof = sign_wpt_claims(self.signer, claims, algorithm)
            return {**headers, "Workload-Identity-Token": self.wit, "Authorization": f"WPT {proof}"}

    class Receiver(WptReceiver):
        context_token_header = CONTEXT_HEADER

        def authenticate_proof(self, request, path):
            headers = request.headers
            if any(len(headers.get_all(name, ())) != 1 for name in ("Workload-Identity-Token", "Authorization")):
                raise ValueError("expected one WIT and WPT")
            if any(len(headers.get_all(name, ())) > 1 for name in ("txn-token", CONTEXT_HEADER)):
                raise ValueError("duplicate token binding header")
            scheme, _, proof = headers["Authorization"].partition(" ")
            if scheme.lower() != "wpt" or not proof:
                raise ValueError("expected WPT authorization")
            wit = headers["Workload-Identity-Token"]
            target = audience(self.dns_name, self.server_port, path)
            now = int(time())
            if not binary and not peer_verify:
                verifier = verify_spiffe_wit if spire else verify_wit
                credential = verifier(wit, trust_by_domain=self.trust_by_domain, now=now)
                claims = credential.claims
                verify_wpt(proof, wit_serialized=wit, confirmation_key=claims["cnf"]["jwk"],
                           subject=claims["sub"], audience=target, now=now, replay_store=self.replay_store,
                           presented_headers=headers.items(), bound_token_headers=(CONTEXT_HEADER,))
                return claims["sub"]

            if peer_verify:
                result = peer_verify(headers, self.trust_by_domain, wit=wit, audience=target, now=now, proof=proof)
            else:
                result = bridge(binary, command="verify", key=str(issuer_key), wit=wit, audience=target,
                                now=now, proof=proof, transaction=headers.get("txn-token"),
                                context=headers.get(CONTEXT_HEADER))
            subject = urlsplit(result["sub"])
            if subject.scheme != ("spiffe" if spire else "wimse") or subject.netloc != "example.org":
                raise ValueError("untrusted WIT subject domain")
            if not self.replay_store.check_and_store(f"peer-wpt:{result['sub']}:{result['jti']}",
                                                    now=now, ttl_s=result["exp"] - now):
                raise ValueError("WPT replay rejected")
            return result["sub"]

    return Caller, Receiver
