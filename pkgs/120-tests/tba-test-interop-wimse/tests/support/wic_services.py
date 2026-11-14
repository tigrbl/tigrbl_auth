"""Stateful, local support roles for the WIC peer scenarios."""

from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import sha256
from threading import Lock
from time import perf_counter_ns
from secrets import token_urlsafe
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def b64(data):
    return urlsafe_b64encode(data).decode("ascii").rstrip("=")


def unb64(value):
    return urlsafe_b64decode(value + "=" * (-len(value) % 4))


class TokenIssuer:
    def __init__(self, issuer, audience):
        self.issuer, self.audience = issuer, audience
        self.key = Ed25519PrivateKey.generate()
        self.verification_key = self.key.public_key()

    def issue(self, subject, scope, *, nonce=None):
        claims = {"iss": self.issuer, "aud": self.audience, "sub": subject, "scope": scope}
        if nonce is not None:
            claims["nonce"] = nonce
        payload = b64(json.dumps(claims, sort_keys=True).encode())
        return payload + "." + b64(self.key.sign(payload.encode("ascii")))

    def verify(self, token):
        try:
            payload, signature = token.split(".")
            self.verification_key.verify(unb64(signature), payload.encode("ascii"))
        except (InvalidSignature, ValueError, AttributeError) as error:
            raise ValueError("issuer-signature-refused") from error
        claims = json.loads(unb64(payload))
        if (claims["iss"], claims["aud"]) != (self.issuer, self.audience):
            raise ValueError("issuer-audience-refused")
        return claims


class StatusAuthority:
    def __init__(self):
        self._revoked_at = None
        self.first_observed = None
        self.first_refused = None
        self._lock = Lock()

    def publish_revocation(self):
        with self._lock:
            self._revoked_at = perf_counter_ns()

    def permitted(self):
        with self._lock:
            if self._revoked_at is None:
                return True
            if self.first_observed is None:
                self.first_observed = perf_counter_ns()
            return False

    def refusal(self):
        self.first_refused = perf_counter_ns()
        return {
            "publication_to_observation_ns": self.first_observed - self._revoked_at,
            "publication_to_first_refusal_ns": self.first_refused - self._revoked_at,
        }


class AccountingAuthority:
    def __init__(self, limit):
        self._lock = Lock()
        self.limit = limit
        self.debits = []

    def authorize(self, identity, headers):
        if headers.get("X-Budget-Audience") != "shared-test-budget":
            raise ValueError("ambiguous-accounting-audience")
        with self._lock:
            if len(self.debits) >= self.limit:
                raise ValueError("budget-exhausted")
            self.debits.append(identity)


class BearerProvider:
    ttl = 60

    def __init__(self):
        self.tokens = {}
        self.effects = []
        self.time = 0

    def issue(self):
        token = token_urlsafe(24)
        self.tokens[token] = self.time + self.ttl
        return token

    def write(self, token):
        if self.time >= self.tokens.get(token, self.time):
            return False
        self.effects.append("synthetic-provider-write")
        return True
