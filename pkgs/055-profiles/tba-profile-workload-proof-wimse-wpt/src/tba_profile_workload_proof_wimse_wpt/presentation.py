from tba_provider_jose_cryptography.jws import ProtectedEnvelopeIssuerPort

from .issuance import issue_wpt
from .verification import _hash_token


def present_wit(
    signer: ProtectedEnvelopeIssuerPort,
    wit: str,
    *,
    workload_key_reference: str,
    target_uri: str,
    now: int,
    lifetime_seconds: int = 60,
    transaction_token: str | None = None,
) -> dict[str, str]:
    """Sign and present a proof for an already provisioned WIT."""
    digests = {}
    request_headers = {"Workload-Identity-Token": wit}
    if transaction_token is not None:
        if (
            not isinstance(transaction_token, str)
            or not transaction_token
            or not transaction_token.isascii()
            or any(
                not 33 <= ord(char) <= 126 or char == "," for char in transaction_token
            )
        ):
            raise ValueError("expected a single ASCII transaction token")
        digests["txn-token"] = _hash_token(transaction_token)
        request_headers["Txn-Token"] = transaction_token
    proof = issue_wpt(
        signer,
        wit,
        workload_key_reference=workload_key_reference,
        audience=target_uri,
        now=now,
        lifetime_seconds=lifetime_seconds,
        accompanying_token_digests=digests,
    )
    return {**request_headers, "Authorization": f"WPT {proof}"}
