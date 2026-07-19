import cbor2


def sig_structure(
    context: str,
    protected: bytes,
    external_aad: bytes,
    payload: bytes,
    *,
    signer_protected: bytes | None = None,
) -> bytes:
    values = [context, protected]
    if signer_protected is not None:
        values.append(signer_protected)
    values.extend([external_aad, payload])
    return cbor2.dumps(values, canonical=True)


def enc_structure(context: str, protected: bytes, external_aad: bytes) -> bytes:
    return cbor2.dumps([context, protected, external_aad], canonical=True)


def mac_structure(
    context: str, protected: bytes, external_aad: bytes, payload: bytes
) -> bytes:
    return cbor2.dumps([context, protected, external_aad, payload], canonical=True)
