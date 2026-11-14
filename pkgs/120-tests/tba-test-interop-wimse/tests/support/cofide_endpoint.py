"""Cofide request signing and verification over the shared HTTPS resource."""

import base64
from hashlib import sha256
import json
from pathlib import Path
from secrets import token_urlsafe
import subprocess
from time import time

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from tba_profile_workload_credential_wimse_wit import verify_wit
from tba_test_interop_wimse.httpsig import SignatureCaller, SignatureReceiver
from tba_test_interop_wimse.signatures import authenticate_signature, covered, normalize, sign_request
from tba_test_interop_wimse.wpt import audience

from support.signature_cases import verify_spiffe_wit
from support.wpt_fixture import WptFixture, public_jwk, sign_es256_jwt

PROFILE = "wit-http-signature"
SLOT = "cofide"
REVISION = "7984a60105002dc65b31e9cd08572cd5d10ed9d6"


def binary_digest(binary):
    return sha256(Path(binary).read_bytes()).hexdigest()


def call_bridge(binary, **payload):
    result = subprocess.run([str(binary)], input=json.dumps(payload), capture_output=True,
                            text=True, check=True, timeout=10)
    response = json.loads(result.stdout)
    if "denied" in response:
        raise ValueError(f"Cofide HTTP signature refused: {response['denied']}")
    return response


def cofide_hop(directory, case, direction, binary, issuer, names):
    hop = case["hops"][case["target_hop"]]
    use_spire = hop["wit_issuer"] == "spire-wit-svid"
    scheme = "spiffe" if use_spire else "wimse"
    caller_name = names.get("caller_name", "workload")
    expected = f"{scheme}://example.org/{caller_name}"
    credential_verifier = verify_spiffe_wit if use_spire else verify_wit

    def verify_with_cofide(headers, method, authority, path, fields, jwk):
        call_bridge(binary, command="verify", method=method, authority=authority,
                    target=path, headers=headers, fields=fields, publicKey=jwk)

    class Caller(SignatureCaller):
        cofide = True

        def present(self, dns_name, port, *, readback=False, extra_headers=None, signed_path=None,
                    signed_authority=None):
            path = "/effects" if readback else "/writes"
            target = signed_path or path
            authority = signed_authority or f"{dns_name}:{port}"
            method = "GET" if readback else "POST"
            now = int(time())
            if direction == "forward":
                return sign_request(self.signer, self.wit, method, target, audience(dns_name, port, path),
                                    now, extra_headers=extra_headers, authority=authority, cofide=True)
            headers = {**(extra_headers or {}), "workload-identity-token": self.wit}
            key = self.signer.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8,
                                            serialization.NoEncryption())
            proof = call_bridge(binary, command="sign", privateKey=base64.b64encode(key).decode("ascii"),
                                headers=headers, method=method, authority=authority, target=target,
                                nonce=token_urlsafe(16), expires=now + 60,
                                fields=covered(normalize(headers.items()), cofide=True))
            return {**headers, **proof}

    class Receiver(SignatureReceiver):
        def authenticate_proof(self, request, path):
            if request.headers.get("Transfer-Encoding") or request.headers.get("Content-Length", "0") != "0":
                raise ValueError("signature fixture accepts bodyless requests only")
            return authenticate_signature(
                request.headers.items(), method=request.command, path=request.path,
                audience=audience(self.dns_name, self.server_port, path), now=int(time()),
                trust_by_domain=self.trust_by_domain, replay_store=self.replay_store,
                verify_credential=credential_verifier, authority=f"{self.dns_name}:{self.server_port}",
                cofide=True, proof_verifier=verify_with_cofide if direction == "forward" else None,
            )

    authority = ec.generate_private_key(ec.SECP256R1())
    alternate = ec.generate_private_key(ec.SECP256R1())
    workload = ec.generate_private_key(ec.SECP256R1())

    def issue(subject, *, alternate=False):
        if use_spire:
            selected = issuer.foreign if "://other.example/" in subject else issuer
            return selected.mint_wit(subject, alternate=alternate)
        return issue_local(subject, alternate)

    def issue_local(subject, wrong_anchor):
        selected = alternate if wrong_anchor else authority
        now = int(time())
        headers = {"typ": "wit+jwt", "alg": "ES256", "kid": "cofide-lab"}
        claims = {"sub": subject, "iss": "https://example.org", "iat": now, "exp": now + 180,
                  "jti": token_urlsafe(16), "cnf": {"jwk": public_jwk(workload)}}
        wit = sign_es256_jwt(selected, claims, headers)
        return wit, workload, {**public_jwk(selected), "kid": "cofide-lab"}

    fixture = WptFixture(directory, case, signature_caller=Caller, signature_receiver=Receiver,
                         identity=expected, issued_wit=issue)
    fixture.server_identity = f"{scheme}://example.org/{names.get('receiver_name', 'resource')}"
    return fixture
