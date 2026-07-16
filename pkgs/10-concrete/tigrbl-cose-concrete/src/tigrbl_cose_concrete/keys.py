"""Provider-free COSE key decoding."""

from collections.abc import Mapping

import cbor2

MAX_COSE_KEY_BYTES = 8192


def decode_cose_key(encoded: bytes) -> Mapping[int, object]:
    if not isinstance(encoded, bytes) or not encoded:
        raise ValueError("encoded COSE key is required")
    if len(encoded) > MAX_COSE_KEY_BYTES:
        raise ValueError("encoded COSE key exceeds the supported size")
    value = cbor2.loads(encoded)
    if not isinstance(value, Mapping) or not all(isinstance(key, int) for key in value):
        raise ValueError("COSE key must be an integer-keyed CBOR map")
    if cbor2.dumps(dict(value), canonical=True) != encoded:
        raise ValueError("COSE key must use canonical CBOR encoding")
    if 1 not in value:
        raise ValueError("COSE key type label is required")
    return dict(value)
