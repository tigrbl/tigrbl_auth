"""TbA issuer and verifier bindings for native WIT-SVID workloads."""

from time import time
from uuid import uuid4

from cryptography.hazmat.primitives.asymmetric import ec
from tba_concrete_jwt import decode_jwt_unverified
from tba_profile_workload_credential_spiffe_wit_svid.validation import validate_wit_svid_claims
from tba_test_interop_wimse.httpsig import SignatureReceiver

from support.signature_cases import verify_spiffe_wit
from support.wpt_fixture import public_jwk, sign_es256_jwt


class NativeWitSvidIssuer:
    def __init__(self):
        self.authority = ec.generate_private_key(ec.SECP256R1())
        self.alternate = ec.generate_private_key(ec.SECP256R1())
        self.workload = ec.generate_private_key(ec.SECP256R1())

    def mint(self, subject, *, alternate=False):
        key = self.alternate if alternate else self.authority
        now = int(time())
        headers = {"typ": "wit+jwt", "alg": "ES256", "kid": "tba-native-wit-svid"}
        claims = {"sub": subject, "iat": now, "exp": now + 120, "jti": uuid4().hex,
                  "cnf": {"jwk": public_jwk(self.workload)}}
        validate_wit_svid_claims(headers, claims, now=now)
        token = sign_es256_jwt(key, claims, headers)
        return token, self.workload, {**public_jwk(key), "kid": headers["kid"], "use": "wit-svid"}


class NativeWitSvidSignatureReceiver(SignatureReceiver):
    @staticmethod
    def verify_credential(serialized, *, trust_by_domain, now):
        token = decode_jwt_unverified(serialized)
        validate_wit_svid_claims(token.jws.protected_headers, token.claims, now=now)
        return verify_spiffe_wit(serialized, trust_by_domain=trust_by_domain, now=now)
