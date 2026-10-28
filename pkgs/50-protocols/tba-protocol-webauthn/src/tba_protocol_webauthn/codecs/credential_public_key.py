"""WebAuthn credential public-key codec."""

from tba_concrete_cose import decode_cose_key


def decode_credential_public_key(encoded: bytes):
    return decode_cose_key(encoded)


__all__ = ["decode_credential_public_key"]
