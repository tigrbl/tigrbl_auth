"""RFC 7516 - JSON Web Encryption (JWE).

The package currently claims a bounded JWE profile for encrypted ID tokens and
other compact encrypted artifacts. The supported release-path profile is:

- Compact serialization
- ``alg=dir``
- ``enc=A256GCM``
- symmetric ``oct`` content-encryption keys

The implementation intentionally stays dependency-light so it can run in
minimal checkpoint environments without importing the full Tigrbl runtime.
"""

from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Final, Mapping

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from tigrbl_auth.config.settings import settings

RFC7516_SPEC_URL: Final[str] = "https://www.rfc-editor.org/rfc/rfc7516"
SUPPORTED_JWE_ALG_VALUES: Final[tuple[str, ...]] = ("dir",)
SUPPORTED_JWE_ENC_VALUES: Final[tuple[str, ...]] = ("A256GCM",)
_DEFAULT_KEY_SIZE_BYTES: Final[int] = 32


class JWEPolicyError(ValueError):
    """Raised when a JWE request or token violates the active JWE profile."""


@dataclass(frozen=True, slots=True)
class JWEPolicy:
    alg: str = "dir"
    enc: str = "A256GCM"
    key_type: str = "oct"
    key_size_bytes: int = _DEFAULT_KEY_SIZE_BYTES

    def as_header(self, *, typ: str | None = None, cty: str | None = None) -> dict[str, str]:
        header = {"alg": self.alg, "enc": self.enc}
        if typ:
            header["typ"] = typ
        if cty:
            header["cty"] = cty
        return header


ACTIVE_JWE_POLICY: Final[JWEPolicy] = JWEPolicy()



def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")



def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)



def _normalize_oct_key_material(key: Mapping[str, Any] | bytes | bytearray | str) -> bytes:
    if isinstance(key, (bytes, bytearray)):
        return bytes(key)
    if isinstance(key, str):
        try:
            decoded = _b64url_decode(key)
            if decoded:
                return decoded
        except Exception:
            return key.encode("utf-8")
        return key.encode("utf-8")
    key_type = str(key.get("kty") or ACTIVE_JWE_POLICY.key_type)
    if key_type != ACTIVE_JWE_POLICY.key_type:
        raise JWEPolicyError(
            f"unsupported JWE key type {key_type!r}; supported kty values: {ACTIVE_JWE_POLICY.key_type}"
        )
    material = key.get("k")
    if material is None:
        raise JWEPolicyError("missing symmetric key material 'k' for direct encryption")
    if isinstance(material, (bytes, bytearray)):
        return bytes(material)
    if isinstance(material, str):
        try:
            decoded = _b64url_decode(material)
            if decoded:
                return decoded
        except Exception:
            return material.encode("utf-8")
        return material.encode("utf-8")
    raise JWEPolicyError("unsupported symmetric key material type")



def validate_oct_key(key: Mapping[str, Any] | bytes | bytearray | str, *, policy: JWEPolicy = ACTIVE_JWE_POLICY) -> bytes:
    material = _normalize_oct_key_material(key)
    if len(material) != policy.key_size_bytes:
        raise JWEPolicyError(
            f"invalid JWE direct-encryption key length {len(material)}; expected {policy.key_size_bytes} bytes"
        )
    return material



def validate_jwe_header(header: Mapping[str, Any], *, policy: JWEPolicy = ACTIVE_JWE_POLICY) -> dict[str, Any]:
    alg = str(header.get("alg") or "")
    enc = str(header.get("enc") or "")
    if alg != policy.alg:
        raise JWEPolicyError(
            f"unsupported JWE alg {alg!r}; supported values: {', '.join(SUPPORTED_JWE_ALG_VALUES)}"
        )
    if enc != policy.enc:
        raise JWEPolicyError(
            f"unsupported JWE enc {enc!r}; supported values: {', '.join(SUPPORTED_JWE_ENC_VALUES)}"
        )
    return dict(header)



def jwe_policy_metadata(*, policy: JWEPolicy = ACTIVE_JWE_POLICY) -> dict[str, list[str]]:
    return {
        "id_token_encryption_alg_values_supported": [policy.alg],
        "id_token_encryption_enc_values_supported": [policy.enc],
    }


async def encrypt_jwe(
    plaintext: str | bytes,
    key: Mapping[str, Any] | bytes | bytearray | str,
    *,
    alg: str | None = None,
    enc: str | None = None,
    typ: str | None = None,
    cty: str | None = None,
) -> str:
    """Encrypt *plaintext* and return a compact JWE string.

    Only the active direct-encryption profile is supported. Callers may provide
    ``alg`` or ``enc`` for explicit policy assertions; unsupported values fail
    closed with :class:`JWEPolicyError`.
    """

    if not settings.enable_rfc7516:
        raise RuntimeError(f"RFC 7516 support disabled: {RFC7516_SPEC_URL}")
    policy = ACTIVE_JWE_POLICY
    requested_header = policy.as_header(typ=typ, cty=cty)
    if alg is not None:
        requested_header["alg"] = alg
    if enc is not None:
        requested_header["enc"] = enc
    header = validate_jwe_header(requested_header, policy=policy)
    key_bytes = validate_oct_key(key, policy=policy)
    aad_segment = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    iv = os.urandom(12)
    aesgcm = AESGCM(key_bytes)
    raw_ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8") if isinstance(plaintext, str) else plaintext, aad_segment.encode("ascii"))
    ciphertext, tag = raw_ciphertext[:-16], raw_ciphertext[-16:]
    return ".".join(
        (
            aad_segment,
            "",  # direct encryption has an empty encrypted-key component
            _b64url_encode(iv),
            _b64url_encode(ciphertext),
            _b64url_encode(tag),
        )
    )


async def decrypt_jwe(
    token: str,
    key: Mapping[str, Any] | bytes | bytearray | str,
    *,
    expected_alg: str | None = None,
    expected_enc: str | None = None,
) -> str:
    """Decrypt *token* and return its plaintext string."""

    if not settings.enable_rfc7516:
        raise RuntimeError(f"RFC 7516 support disabled: {RFC7516_SPEC_URL}")
    try:
        header_segment, encrypted_key_segment, iv_segment, ciphertext_segment, tag_segment = token.split(".")
    except ValueError as exc:
        raise JWEPolicyError("invalid compact JWE serialization") from exc
    if encrypted_key_segment not in {"", None}:
        raise JWEPolicyError("direct-encryption JWE must not contain an encrypted key segment")
    try:
        header = json.loads(_b64url_decode(header_segment).decode("utf-8"))
    except Exception as exc:
        raise JWEPolicyError("invalid compact JWE header") from exc
    if expected_alg is not None:
        header = dict(header)
        header.setdefault("alg", expected_alg)
    if expected_enc is not None:
        header = dict(header)
        header.setdefault("enc", expected_enc)
    validate_jwe_header(header, policy=ACTIVE_JWE_POLICY)
    key_bytes = validate_oct_key(key, policy=ACTIVE_JWE_POLICY)
    try:
        iv = _b64url_decode(iv_segment)
        ciphertext = _b64url_decode(ciphertext_segment)
        tag = _b64url_decode(tag_segment)
    except Exception as exc:
        raise JWEPolicyError("invalid compact JWE body encoding") from exc
    if len(iv) != 12:
        raise JWEPolicyError("invalid compact JWE IV length")
    aesgcm = AESGCM(key_bytes)
    try:
        plaintext = aesgcm.decrypt(iv, ciphertext + tag, header_segment.encode("ascii"))
    except Exception as exc:
        raise JWEPolicyError("unable to decrypt compact JWE") from exc
    return plaintext.decode("utf-8")


__all__ = [
    "ACTIVE_JWE_POLICY",
    "JWEPolicy",
    "JWEPolicyError",
    "RFC7516_SPEC_URL",
    "SUPPORTED_JWE_ALG_VALUES",
    "SUPPORTED_JWE_ENC_VALUES",
    "decrypt_jwe",
    "encrypt_jwe",
    "jwe_policy_metadata",
    "validate_jwe_header",
    "validate_oct_key",
]
