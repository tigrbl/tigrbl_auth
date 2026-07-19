from dataclasses import dataclass
import json
from typing import Mapping
from tigrbl_identity_core.base64url import base64url_decode

@dataclass(frozen=True, slots=True)
class JweRecipient:
    header: Mapping[str, object]
    encrypted_key: bytes

@dataclass(frozen=True, slots=True)
class JweJson:
    protected_headers: Mapping[str, object]
    unprotected_headers: Mapping[str, object]
    recipients: tuple[JweRecipient, ...]
    iv: bytes
    ciphertext: bytes
    tag: bytes
    aad: bytes | None


def parse_jwe_json(value: str | bytes | Mapping[str, object]) -> JweJson:
    obj = json.loads(value) if isinstance(value, (str, bytes)) else dict(value)
    protected_segment = obj.get("protected", "")
    protected = json.loads(base64url_decode(protected_segment)) if protected_segment else {}
    shared = obj.get("unprotected", {})
    raw_recipients = obj.get("recipients")
    if raw_recipients is None: raw_recipients = [{"header": obj.get("header", {}), "encrypted_key": obj.get("encrypted_key", "")}]
    recipients=[]
    for item in raw_recipients:
        header=item.get("header", {})
        if set(protected).intersection(shared) or set(protected).intersection(header) or set(shared).intersection(header): raise ValueError("JWE header parameters must be disjoint")
        recipients.append(JweRecipient(dict(header), base64url_decode(item.get("encrypted_key", ""))))
    return JweJson(dict(protected), dict(shared), tuple(recipients), base64url_decode(obj["iv"]), base64url_decode(obj["ciphertext"]), base64url_decode(obj["tag"]), base64url_decode(obj["aad"]) if "aad" in obj else None)