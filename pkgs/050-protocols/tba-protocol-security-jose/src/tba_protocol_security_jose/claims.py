"""Claim ownership boundary for the JOSE container family.

JOSE defines protected and unprotected header parameters. It does not define
an application claim set; JWT, SET, EAT-JWT, and other profiles do that.
"""

JOSE_CLAIM_CLASSES: tuple[type[object], ...] = ()
CLAIMS_ARE_PROFILE_OWNED = True

__all__ = ["CLAIMS_ARE_PROFILE_OWNED", "JOSE_CLAIM_CLASSES"]
