"""CoRIM family map-field ownership.

CoRIM does not register JWT/CWT claims. Its concise map fields describe
reference values, endorsements, trust lists, and trust stores.
"""

CORIM_CLAIM_CLASSES: tuple[type, ...] = ()
CORIM_MAP_FIELDS = (
    "tag-identity",
    "profile",
    "tags",
    "validity",
    "entities",
)

__all__ = ["CORIM_CLAIM_CLASSES", "CORIM_MAP_FIELDS"]
