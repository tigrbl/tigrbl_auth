"""Protocol-neutral reusable claim-set composition behavior."""

from abc import ABC
from collections.abc import Sequence

from tigrbl_identity_contracts.claims import Claim, ClaimSet, ClaimSetComposerPort


class ClaimSetComposerBase(ClaimSetComposerPort, ABC):
    """Compose a set while enforcing carrier-neutral structural invariants."""

    def compose(
        self, claims: Sequence[Claim], /, *, protocol: str, version: str
    ) -> ClaimSet:
        if not protocol or not version:
            raise ValueError("claim sets require explicit protocol and version")
        materialized = tuple(claims)
        identifiers = [claim.identifier for claim in materialized]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("claim sets must not contain duplicate identifiers")
        return ClaimSet(materialized, protocol, version)


__all__ = ["ClaimSetComposerBase"]
