import re
from dataclasses import dataclass
from urllib.parse import urlsplit

_UNRESERVED = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)
_AUTHORITY = re.compile(r"(?:[A-Za-z0-9._~-]|%[0-9A-Fa-f]{2})+")
_PATH = re.compile(r"/(?:[A-Za-z0-9._~!$&'()*+,;=:@/-]|%[0-9A-Fa-f]{2})*")


def _normalize_percent(value: str) -> str:
    def replace(match):
        character = chr(int(match[0][1:], 16))
        return character if character in _UNRESERVED else match[0].upper()

    return re.sub(r"%[0-9A-Fa-f]{2}", replace, value)


@dataclass(frozen=True, slots=True)
class WorkloadIdentifier:
    trust_domain: str
    path: str

    def __str__(self) -> str:
        return f"wimse://{self.trust_domain}{self.path}"

    @classmethod
    def parse(cls, value: str) -> "WorkloadIdentifier":
        if (
            not isinstance(value, str)
            or not value.isascii()
            or any(ord(character) <= 32 or ord(character) == 127 for character in value)
            or "?" in value
            or "#" in value
        ):
            raise ValueError("invalid WIMSE workload URI")
        uri = urlsplit(value)
        if (
            uri.scheme != "wimse"
            or not _AUTHORITY.fullmatch(uri.netloc)
            or not _PATH.fullmatch(uri.path)
        ):
            raise ValueError("expected wimse://trust-domain/path")
        domain = _normalize_percent(uri.netloc)
        if "%" in domain:
            raise ValueError("WIMSE trust domain requires an ASCII name")
        path = _normalize_percent(uri.path)
        if {".", ".."}.intersection(path.split("/")):
            raise ValueError("WIMSE identifier cannot contain dot segments")
        return cls(domain.lower(), path)
