"""Use the Tigrbl Auth sender and construct deliberate negative proofs."""

import hashlib
from secrets import token_urlsafe
from time import time

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from tba_primitives_identity import base64url_encode
from tba_profile_workload_credential_wimse_wit import issue_wit
from tba_profile_workload_proof_wimse_wpt import present_wit
from tba_provider_jose_cryptography import JwsCryptographyProvider
from tba_provider_jose_cryptography.jws import sign_compact_jwt

TRUST_DOMAIN = "tba-interop.example"
WORKLOAD = f"wimse://{TRUST_DOMAIN}/acceptance/client"
ISSUER_KEY_ID = "tba-acceptance-issuer"
ALGORITHM = "EdDSA"


def _public_jwk(key: Ed25519PrivateKey) -> dict[str, str]:
    public_bytes = key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )
    return {
        "kty": "OKP",
        "crv": "Ed25519",
        "x": base64url_encode(public_bytes),
        "alg": ALGORITHM,
    }


class WorkloadTokens:
    def __init__(self) -> None:
        issuer = Ed25519PrivateKey.generate()
        workload = Ed25519PrivateKey.generate()
        self.trust_bundle = {
            "keys": [{**_public_jwk(issuer), "kid": ISSUER_KEY_ID, "use": "wit-svid"}]
        }
        self._confirmation_key = _public_jwk(workload)
        self._signer = JwsCryptographyProvider(
            {
                "issuer": issuer,
                "workload": workload,
                "untrusted": Ed25519PrivateKey.generate(),
            }
        )

    def _sign(self, kind: str, claims: dict, key: str, **headers: str) -> str:
        return sign_compact_jwt(
            self._signer,
            claims,
            headers={"typ": kind, "alg": ALGORITHM, **headers},
            key_reference=key,
        )

    def issue_wit(self, *, wrong_key: bool = False, expired: bool = False) -> str:
        now = int(time())
        return issue_wit(
            self._signer,
            subject=WORKLOAD,
            confirmation_jwk=self._confirmation_key,
            issuer_key_reference="untrusted" if wrong_key else "issuer",
            issuer_key_id=ISSUER_KEY_ID,
            issuer_algorithm=ALGORITHM,
            issued_at=now - 300 if expired else now,
            expires_at=now - 180 if expired else now + 120,
        )

    def request_headers(
        self,
        wit: str,
        audience: str,
        *,
        wrong_key: bool = False,
        expired: bool = False,
    ) -> dict[str, str]:
        now = int(time())
        if not wrong_key and not expired:
            return present_wit(
                self._signer,
                wit,
                workload_key_reference="workload",
                target_uri=audience,
                now=now,
            )
        proof = self._sign(
            "wpt+jwt",
            {
                "aud": audience,
                "exp": now - 180 if expired else now + 60,
                "jti": token_urlsafe(16),
                "wth": base64url_encode(hashlib.sha256(wit.encode("ascii")).digest()),
            },
            "untrusted" if wrong_key else "workload",
        )
        return {"Workload-Identity-Token": wit, "Authorization": f"WPT {proof}"}
