from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetadataProfile:
    service_identifier: str = "fido-mds"
    signed_blob_required: bool = True
    reject_compromised_authenticators: bool = True
    cache_until_next_update: bool = True


DEFAULT_METADATA_PROFILE = MetadataProfile()

__all__ = ["DEFAULT_METADATA_PROFILE", "MetadataProfile"]
