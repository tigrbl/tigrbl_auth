"""Base32 secrets and authenticator enrollment URLs."""

import base64
import binascii
import secrets
from urllib.parse import quote, urlencode


def new_secret() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii")


def decode_secret(secret: str) -> bytes:
    if not isinstance(secret, str) or not secret:
        raise ValueError("A Base32 secret is required.")
    try:
        return base64.b32decode(secret + "=" * (-len(secret) % 8), casefold=True)
    except (ValueError, binascii.Error):
        raise ValueError("Invalid Base32 secret.") from None


def provisioning_uri(secret: str, account: str, issuer: str) -> str:
    """Encode the interoperable SHA-1, six-digit, 30-second TOTP profile."""
    if not account or not issuer:
        raise ValueError("Account and issuer labels are required.")
    key = base64.b32encode(decode_secret(secret)).decode("ascii").rstrip("=")
    label = f"{quote(issuer, safe='')}:{quote(account, safe='')}"
    return "otpauth://totp/" + label + "?" + urlencode(
        {"secret": key, "issuer": issuer}, quote_via=quote
    )
