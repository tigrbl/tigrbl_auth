import base64
from hashlib import new


def _digest(value: bytes, algorithm: str) -> str:
    try:
        digest = new(algorithm, value).digest()
    except ValueError as exc:
        raise ValueError(f"unsupported digest algorithm: {algorithm}") from exc
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def disclosure_digest(encoded_disclosure: str, algorithm: str = "sha256") -> str:
    return _digest(encoded_disclosure.encode("ascii"), algorithm)


def sd_hash(
    serialized_presentation_without_kb_jwt: str, algorithm: str = "sha256"
) -> str:
    return _digest(serialized_presentation_without_kb_jwt.encode("ascii"), algorithm)


__all__ = ["disclosure_digest", "sd_hash"]
