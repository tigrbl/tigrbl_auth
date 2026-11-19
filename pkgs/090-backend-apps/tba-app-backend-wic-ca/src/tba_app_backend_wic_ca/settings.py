"""Deployment settings for the native WIC CA."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class WicCaSettings:
    trust_domain: str
    ca_certificate_path: Path
    ca_private_key_path: Path
    lifetime_seconds: int = 3600
