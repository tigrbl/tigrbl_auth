"""Configured WPT authentication and carrier-neutral proof verification."""

from collections.abc import Callable, Mapping, Sequence
from inspect import iscoroutinefunction
from time import time

from tba_contracts_proof_of_possession import (
    PossessionProofVerificationRequest,
    PossessionProofVerificationResult,
)
from tba_contracts_replay import ReplayCheckPort

from .verification import _verify_wpt, authenticate_wpt_request


class WptProofVerifier:
    """Reuse the same signature, context, and replay checks on both entry points."""

    def __init__(
        self,
        *,
        trust_by_domain: Mapping[str, Sequence[Mapping[str, object]]],
        replay_store: ReplayCheckPort,
        clock: Callable[[], float] = time,
    ) -> None:
        if not trust_by_domain or any(not keys for keys in trust_by_domain.values()):
            raise ValueError("WPT requires configured trust-domain keys")
        check_and_store = getattr(replay_store, "check_and_store", None)
        if not callable(check_and_store) or iscoroutinefunction(check_and_store):
            raise ValueError("WPT requires a synchronous atomic replay store")
        self._trust_by_domain = {
            domain: tuple(dict(key) for key in keys)
            for domain, keys in trust_by_domain.items()
        }
        self._replay_store = replay_store
        self._clock = clock

    def authenticate_request(
        self,
        headers,
        *,
        audience: str,
        bound_token_headers=(),
        required_token_headers=(),
    ):
        """Verify the WIT and WPT from HTTP using a trusted recipient audience."""
        return authenticate_wpt_request(
            headers,
            audience=audience,
            trust_by_domain=self._trust_by_domain,
            now=self._clock(),
            replay_store=self._replay_store,
            bound_token_headers=bound_token_headers,
            required_token_headers=required_token_headers,
        )

    def verify(
        self, request: PossessionProofVerificationRequest, /
    ) -> PossessionProofVerificationResult:
        """Verify a WPT against an already authenticated WIT and trusted context."""
        context = request.context
        confirmation = request.confirmation
        if confirmation.method != "jwk" or not context.credential_digest:
            return PossessionProofVerificationResult(
                False, reason="invalid WIT binding context"
            )
        target = context.audience or context.target_uri
        if not target:
            return PossessionProofVerificationResult(
                False, reason="WPT audience is required"
            )
        try:
            proof = request.proof.artifact
            if isinstance(proof, bytes):
                proof = proof.decode("ascii")
            token = _verify_wpt(
                proof,
                wit_digest=context.credential_digest,
                confirmation_key=confirmation.confirmation,
                audience=target,
                now=self._clock(),
                replay_store=self._replay_store,
                token_digests=context.accompanying_token_digests,
                required=context.accompanying_token_digests.keys() - {"txn-token"},
                expected_proof_id=request.proof.proof_id,
            )
        except (KeyError, TypeError, ValueError):
            return PossessionProofVerificationResult(
                False, reason="WPT verification failed"
            )
        return PossessionProofVerificationResult(
            True, proof_id=token.claims["jti"], replay_accepted=True
        )
