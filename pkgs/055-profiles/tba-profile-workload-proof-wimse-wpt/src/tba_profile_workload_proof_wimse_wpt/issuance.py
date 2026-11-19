"""Create WPTs without selecting a transport or exposing the workload key."""

from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from math import isfinite
import re
from secrets import token_urlsafe
from time import time

from tba_concrete_jwt import decode_jwt_unverified
from tba_contracts_proof_of_possession import PossessionProof, PossessionProofContext
from tba_provider_jose_cryptography.jws import (
    ProtectedEnvelopeIssuerPort,
    sign_compact_jwt,
)
from tba_provider_jose_cryptography.public_jws import verify_public_jws

from .verification import _hash_token, _target_audience


def _lifetime(value: int) -> None:
    if type(value) is not int or not 0 < value <= 300:
        raise ValueError("WPT lifetime must be between 1 and 300 seconds")


def issue_wpt(
    signer: ProtectedEnvelopeIssuerPort,
    wit: str,
    *,
    workload_key_reference: str,
    audience: str,
    now: int,
    lifetime_seconds: int = 60,
    accompanying_token_digests: Mapping[str, str] | None = None,
) -> str:
    """Sign a fresh proof with the WIT confirmation key; return its compact JWT.

    The caller supplies a provisioned WIT. Its issuer is authenticated by the
    recipient, not by this presentation helper. Additional token values stay
    with the caller; this function accepts their SHA-256 base64url digests.
    """
    _lifetime(lifetime_seconds)
    if type(now) is not int or not workload_key_reference:
        raise ValueError("WPT requires an integer time and workload key reference")
    token = decode_jwt_unverified(wit)
    if token.jws.protected_headers.get("typ") not in ("wit+jwt", "application/wit+jwt"):
        raise ValueError("expected a WIT")
    expiry = token.claims.get("exp")
    if type(expiry) not in (int, float) or not isfinite(expiry) or expiry <= now:
        raise ValueError("WIT is expired or has an invalid expiry")
    confirmation = token.claims.get("cnf")
    jwk = confirmation.get("jwk") if isinstance(confirmation, Mapping) else None
    algorithm = jwk.get("alg") if isinstance(jwk, Mapping) else None
    if not isinstance(algorithm, str):
        raise ValueError("WIT confirmation JWK requires a signing algorithm")
    digests = dict(accompanying_token_digests or {})
    for name, digest in digests.items():
        if (
            not isinstance(name, str)
            or not re.fullmatch(r"[a-z][a-z0-9-]*", name)
            or name in {"authorization", "workload-identity-token"}
            or not isinstance(digest, str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{43}", digest)
        ):
            raise ValueError("invalid accompanying token name or SHA-256 digest")
    claims = {
        "aud": _target_audience(audience),
        "exp": min(now + lifetime_seconds, expiry),
        "jti": token_urlsafe(16),
        "wth": _hash_token(wit),
    }
    if "txn-token" in digests:
        claims["tth"] = digests.pop("txn-token")
    if digests:
        claims["oth"] = digests
    proof = sign_compact_jwt(
        signer,
        claims,
        headers={"typ": "wpt+jwt", "alg": algorithm},
        key_reference=workload_key_reference,
    )
    verify_public_jws(proof, jwk)
    return proof


class WptProofIssuer:
    """Configured implementation of PossessionProofIssuerPort."""

    def __init__(
        self,
        signer: ProtectedEnvelopeIssuerPort,
        wit: str,
        *,
        workload_key_reference: str,
        lifetime_seconds: int = 60,
        clock: Callable[[], float] = time,
    ) -> None:
        _lifetime(lifetime_seconds)
        self._signer = signer
        self._wit = wit
        self._key_reference = workload_key_reference
        self._lifetime = lifetime_seconds
        self._clock = clock

    def issue(self, context: PossessionProofContext, /) -> PossessionProof:
        audience = context.audience or context.target_uri
        if not audience:
            raise ValueError("WPT audience is required")
        audience = _target_audience(audience)
        if context.target_uri and _target_audience(context.target_uri) != audience:
            raise ValueError("WPT audience and target URI disagree")
        if context.method is not None:
            raise ValueError("WPT does not bind HTTP methods")
        digest = _hash_token(self._wit)
        if (
            context.credential_digest is not None
            and context.credential_digest != digest
        ):
            raise ValueError("WPT context does not match the configured WIT")
        proof = issue_wpt(
            self._signer,
            self._wit,
            workload_key_reference=self._key_reference,
            audience=audience,
            now=int(self._clock()),
            lifetime_seconds=self._lifetime,
            accompanying_token_digests=context.accompanying_token_digests,
        )
        claims = decode_jwt_unverified(proof).claims
        bound_context = PossessionProofContext(
            audience=audience,
            target_uri=context.target_uri,
            credential_digest=digest,
            accompanying_token_digests=context.accompanying_token_digests,
        )
        return PossessionProof(
            claims["jti"],
            proof,
            datetime.fromtimestamp(claims["exp"], timezone.utc),
            bound_context,
            profile="wimse-wpt",
        )
