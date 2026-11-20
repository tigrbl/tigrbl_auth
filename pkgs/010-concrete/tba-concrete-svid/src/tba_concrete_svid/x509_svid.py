from dataclasses import dataclass

from .spiffe_ids import normalize_spiffe_id


@dataclass(frozen=True, slots=True)
class X509SvidStructure:
    uri_sans: tuple[str, ...]
    dns_sans: tuple[str, ...] = ()
    key_usage_digital_signature: bool = True
    is_ca: bool = False


def validate_x509_svid_structure(value: X509SvidStructure):
    if len(value.uri_sans) != 1:
        raise ValueError("X.509-SVID requires exactly one SPIFFE ID URI SAN")
    spiffe_id = normalize_spiffe_id(value.uri_sans[0])
    if value.is_ca or not value.key_usage_digital_signature:
        raise ValueError("X.509-SVID leaf must be non-CA and permit digital signatures")
    return spiffe_id


__all__ = ["X509SvidStructure", "validate_x509_svid_structure"]
