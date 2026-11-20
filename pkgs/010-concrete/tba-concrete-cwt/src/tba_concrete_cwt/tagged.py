from collections.abc import Mapping

import cbor2
from .claims import CwtClaimsSet

CWT_TAG = 61


def encode_tagged_cwt(claims: CwtClaimsSet) -> bytes:
    return cbor2.dumps(cbor2.CBORTag(CWT_TAG, dict(claims.claims)), canonical=True)


def decode_tagged_cwt(encoded: bytes, *, require_tag: bool = True) -> CwtClaimsSet:
    value = cbor2.loads(encoded)
    if isinstance(value, cbor2.CBORTag):
        if value.tag != CWT_TAG:
            raise ValueError(f"unexpected CBOR tag: {value.tag}")
        value = value.value
    elif require_tag:
        raise ValueError("CWT tag 61 is required")
    if not isinstance(value, Mapping):
        raise ValueError("CWT payload must be a map")
    return CwtClaimsSet(dict(value))
