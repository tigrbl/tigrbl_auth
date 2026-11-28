"""AuthZEN claim-set ownership declaration.

Authorization API 1.0 exchanges policy entities and decisions, not a JWT-style
registered claim set. Signed PDP metadata is a JWT carrier whose generic claims
remain owned by the JWT protocol package.
"""

AUTHZEN_CLAIM_CLASSES: tuple[type[object], ...] = ()

__all__ = ["AUTHZEN_CLAIM_CLASSES"]
