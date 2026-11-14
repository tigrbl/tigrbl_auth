import json

from tba_testkit_workload_credential_conformance.fixtures import (
    exercise_wimse_mtls_round_trip,
)
from tba_testkit_workload_credential_conformance.profiles import (
    exercise_wic,
    exercise_wimse,
)
from tba_testkit_workload_credential_conformance.wheels import run_installed

WIMSE = (
    "tba-profile-workload-credential-wimse-wit",
    "tba-profile-workload-proof-wimse-wpt",
)


def exercise_wimse_sender_contract():
    from tba_concrete_jwt import decode_jwt_unverified
    from tba_profile_workload_proof_wimse_wpt import present_wit

    signer, wit, _ = wimse_credentials()
    headers = present_wit(
        signer,
        wit,
        workload_key_reference="workload",
        target_uri="https://service.example.org/work?limit=1#fragment",
        now=100,
    )
    assert headers["Workload-Identity-Token"] == wit
    scheme, proof = headers["Authorization"].split(" ", 1)
    assert scheme == "WPT"
    token = decode_jwt_unverified(proof)
    assert token.jws.protected_headers["typ"] == "wpt+jwt"
    assert token.claims["aud"] == "https://service.example.org/work"
    assert token.claims["exp"] == 160
    assert len(token.claims["jti"]) >= 22
    credential = decode_jwt_unverified(wit)
    assert credential.jws.protected_headers["typ"] == "wit+jwt"
    assert credential.claims["sub"] == "wimse://example.org/workload"


def wimse_credentials():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from tba_primitives_identity import base64url_encode
    from tba_profile_workload_credential_wimse_wit import issue_wit
    from tba_provider_jose_cryptography import JwsCryptographyProvider

    def jwk(key):
        return {
            "kty": "OKP",
            "crv": "Ed25519",
            "alg": "EdDSA",
            "x": base64url_encode(
                key.public_key().public_bytes(
                    serialization.Encoding.Raw,
                    serialization.PublicFormat.Raw,
                )
            ),
        }

    issuer, workload, wrong = (Ed25519PrivateKey.generate() for _ in range(3))
    signer = JwsCryptographyProvider(
        {"issuer": issuer, "workload": workload, "wrong": wrong}
    )
    wit = issue_wit(
        signer,
        subject="wimse://EXAMPLE.ORG/workload",
        confirmation_jwk=jwk(workload),
        issuer_key_reference="issuer",
        issuer_key_id="issuer",
        issuer_algorithm="EdDSA",
        issued_at=100,
        expires_at=200,
    )
    return signer, wit, {"example.org": [{**jwk(issuer), "kid": "issuer"}]}


def exercise_wimse_sender_signatures():
    import hashlib

    from tba_concrete_jwt import decode_jwt_unverified
    from tba_primitives_identity import base64url_encode
    from tba_profile_workload_credential_wimse_wit import verify_wit
    from tba_profile_workload_proof_wimse_wpt import present_wit
    from tba_provider_jose_cryptography.public_jws import verify_public_jws

    signer, wit, trust = wimse_credentials()
    verified = verify_wit(wit, trust_by_domain=trust, now=100)
    assert verified.jwt.integrity_verified
    options = {"target_uri": "https://service.example.org/work", "now": 100}
    first = present_wit(signer, wit, workload_key_reference="workload", **options)
    second = present_wit(signer, wit, workload_key_reference="workload", **options)
    proof = first["Authorization"].split(" ", 1)[1]
    verify_public_jws(proof, verified.claims["cnf"]["jwk"])
    assert decode_jwt_unverified(proof).claims["wth"] == base64url_encode(
        hashlib.sha256(wit.encode("ascii")).digest()
    )
    assert first["Authorization"] != second["Authorization"]
    try:
        present_wit(signer, wit, workload_key_reference="wrong", **options)
    except ValueError as error:
        assert "signature" in str(error)
    else:
        raise AssertionError("sender signed with an unrelated workload key")


def exercise_wimse_http_round_trip():
    from http.client import HTTPConnection
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from threading import Thread

    from tba_concrete_jwt import decode_jwt_unverified
    from tba_profile_workload_credential_wimse_wit import issue_wit
    from tba_profile_workload_proof_wimse_wpt import (
        authenticate_wpt_request,
        present_wit,
    )
    from tba_provider_jose_cryptography.jws import sign_compact_jwt
    from tba_provider_replay_memory import MemoryReplayCheckProvider

    signer, wit, trust = wimse_credentials()
    replay = MemoryReplayCheckProvider()

    class Receiver(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                credential = authenticate_wpt_request(
                    self.headers.items(),
                    audience=base + self.path,
                    trust_by_domain=trust,
                    now=100,
                    replay_store=replay,
                )
            except ValueError as error:
                self.send_response(401)
                body = str(error)
            else:
                self.send_response(200)
                body = credential.claims["sub"]
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))

    with HTTPServer(("127.0.0.1", 0), Receiver) as server:
        port = server.server_port
        base = f"http://127.0.0.1:{port}"
        route = "/work?limit=1"
        worker = Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05})
        worker.start()

        def send(headers):
            connection = HTTPConnection("127.0.0.1", port, timeout=5)
            try:
                connection.request("GET", route, headers=headers)
                response = connection.getresponse()
                return response.status, response.read().decode("utf-8")
            finally:
                connection.close()

        def present(credential=wit, path=route):
            return present_wit(
                signer,
                credential,
                workload_key_reference="workload",
                target_uri=base + path,
                now=100,
            )

        def refused(headers, reason):
            status, body = send(headers)
            assert status == 401 and reason in body, (status, body)

        def reissue(
            subject="wimse://example.org/workload", key="issuer", expires_at=199
        ):
            return issue_wit(
                signer,
                subject=subject,
                confirmation_jwk=confirmation,
                issuer_key_reference=key,
                issuer_key_id="issuer",
                issuer_algorithm="EdDSA",
                issued_at=10,
                expires_at=expires_at,
            )

        try:
            valid = present()
            expected = (200, "wimse://example.org/workload")
            assert send(valid) == expected
            refused(valid, "replay")
            assert send(present()) == expected
            refused(present(path="/other"), "audience")
            confirmation = decode_jwt_unverified(wit).claims["cnf"]["jwk"]
            refused(present(reissue(key="wrong")), "signature")
            refused(
                present(reissue(subject="wimse://unknown.example/workload")),
                "trust domain",
            )
            refused(present(reissue(expires_at=99)), "validity period")
            fresh = present()
            refused({**fresh, "Workload-Identity-Token": reissue()}, "WIT binding")
            proof = decode_jwt_unverified(fresh["Authorization"].split(" ", 1)[1])
            for changes, key, reason in (
                ({}, "wrong", "signature"),
                ({"exp": 99}, "workload", "expiry"),
            ):
                invalid = sign_compact_jwt(
                    signer,
                    {**proof.claims, **changes},
                    headers={"typ": "wpt+jwt", "alg": "EdDSA"},
                    key_reference=key,
                )
                refused({**fresh, "Authorization": f"WPT {invalid}"}, reason)
            assert send(fresh) == expected
        finally:
            server.shutdown()
            worker.join(timeout=5)


def test_t2_shared_wimse_consumers(wheelhouse, tmp_path, record_property):
    inventory = run_installed(
        wheelhouse,
        tmp_path,
        (*WIMSE, "tba-profile-workload-authentication-wimse-mtls"),
        (exercise_wimse, exercise_wic),
        ("spiffe", "spire"),
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))


def exercise_wit_rotation():
    import base64

    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec, utils
    from tba_profile_workload_credential_wimse_wit import verify_wit

    def encode(value):
        return base64.urlsafe_b64encode(value).rstrip(b"=").decode()

    def create_key(kid):
        private = ec.generate_private_key(ec.SECP256R1())
        numbers = private.public_key().public_numbers()
        return private, {
            "kid": kid,
            "alg": "ES256",
            "kty": "EC",
            "crv": "P-256",
            "x": encode(numbers.x.to_bytes(32, "big")),
            "y": encode(numbers.y.to_bytes(32, "big")),
        }

    def token(key, jwk):
        header = {"alg": "ES256", "kid": jwk["kid"], "typ": "wit+jwt"}
        claims = {
            "sub": "wimse://example.org/workload",
            "exp": 200,
            "cnf": {"jwk": confirmation},
        }
        message = ".".join(
            encode(json.dumps(value).encode()) for value in (header, claims)
        )
        r, s = utils.decode_dss_signature(
            key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))
        )
        return message + "." + encode(r.to_bytes(32, "big") + s.to_bytes(32, "big"))

    _, confirmation = create_key("workload")
    old, old_jwk = create_key("old")
    new, new_jwk = create_key("new")
    old_wit, new_wit = token(old, old_jwk), token(new, new_jwk)
    trust = {"example.org": [old_jwk, new_jwk]}
    assert verify_wit(old_wit, trust_by_domain=trust, now=100).jwt.integrity_verified
    assert verify_wit(new_wit, trust_by_domain=trust, now=100).jwt.integrity_verified
    trust["example.org"] = [new_jwk]
    assert verify_wit(new_wit, trust_by_domain=trust, now=100).jwt.integrity_verified
    try:
        verify_wit(old_wit, trust_by_domain=trust, now=100)
    except ValueError as error:
        assert "signing key" in str(error)
    else:
        raise AssertionError("retired WIT issuer remained trusted")


def test_t2_wit_issuer_rotation(wheelhouse, tmp_path, record_property):
    inventory = run_installed(
        wheelhouse, tmp_path, WIMSE, (exercise_wit_rotation,), ("spiffe", "spire")
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))


def test_t0_wimse_sender_contract():
    exercise_wimse_sender_contract()


def test_t1_wimse_sender_signatures():
    exercise_wimse_sender_signatures()


def test_t2_wimse_sender_install(wheelhouse, tmp_path, record_property):
    inventory = run_installed(
        wheelhouse,
        tmp_path,
        WIMSE,
        (exercise_wimse_sender_contract, exercise_wimse_sender_signatures),
        ("spiffe", "spire", "cred"),
        helpers=(wimse_credentials,),
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))


def test_t3_wimse_http_round_trip(wheelhouse, tmp_path, record_property):
    inventory = run_installed(
        wheelhouse,
        tmp_path,
        (*WIMSE, "tba-provider-replay-memory"),
        (exercise_wimse_http_round_trip,),
        ("spiffe", "spire", "cred"),
        helpers=(wimse_credentials,),
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))


def test_t3_wimse_mtls_round_trip(wheelhouse, tmp_path, record_property):
    from tba_testkit_workload_credential_conformance.fixtures import (
        _certificate,
        _mutual_tls_peers,
        _tls_context,
    )

    inventory = run_installed(
        wheelhouse,
        tmp_path,
        (
            "tba-profile-workload-authentication-wimse-mtls",
            "tba-provider-certificate-status",
        ),
        (exercise_wimse_mtls_round_trip,),
        ("spiffe", "spire", "cred"),
        helpers=(_certificate, _tls_context, _mutual_tls_peers),
    )
    record_property("wheel_inventory", json.dumps(inventory, sort_keys=True))
