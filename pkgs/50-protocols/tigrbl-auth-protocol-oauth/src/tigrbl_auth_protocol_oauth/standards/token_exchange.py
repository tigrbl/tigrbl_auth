"""RFC 8693 token-exchange specification owner and compatibility exports."""

from __future__ import annotations
# ruff: noqa: F403,F405

from tigrbl_identity_core.standards import StandardOwner, describe_owner

from tigrbl_auth_protocol_oauth.standards._rfc8693.runtime import *
from tigrbl_auth_protocol_oauth.standards._rfc8693.endpoint import *


OWNER = StandardOwner(
    label="RFC 8693",
    title="OAuth 2.0 Token Exchange",
    runtime_status="lineage-audited-token-exchange-runtime",
    public_surface=("/token/exchange",),
    notes=(
        "RFC mapping for normalized token.exchange capability execution with "
        "subject-token validation, actor delegation, target selection, sender "
        "constraints, durable lineage, and audit observation."
    ),
)


def describe() -> dict[str, object]:
    return describe_owner(
        OWNER,
        requested_token_types_supported=(
            "urn:ietf:params:oauth:token-type:access_token",
            "access_token",
        ),
        delegation_supported=True,
        single_effective_target=True,
        spec_url=RFC8693_SPEC_URL,
    )

__all__ = [name for name in globals() if not name.startswith("_")]
