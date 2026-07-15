"""RFC 9449 feature metadata."""

from __future__ import annotations

from tigrbl_identity_core.standards import describe_owner

from .primitives import OWNER, RFC9449_SPEC_URL, _ALG_VALUE


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        spec_url=RFC9449_SPEC_URL,
        signing_alg_values_supported=[_ALG_VALUE],
        ath_supported=True,
        nonce_supported=True,
        replay_detection_supported=True,
    )
