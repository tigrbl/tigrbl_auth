from .spiffe_id import validate_spiffe_id

def validate_x509_svid(*, uri_sans: tuple[str, ...], dns_sans: tuple[str, ...], key_usage_digital_signature: bool, basic_constraints_ca: bool) -> str:
    spiffe_ids = tuple(value for value in uri_sans if value.startswith("spiffe://"))
    if len(spiffe_ids) != 1: raise ValueError("X.509-SVID requires exactly one SPIFFE URI SAN")
    validate_spiffe_id(spiffe_ids[0])
    if dns_sans: raise ValueError("X.509-SVID must not contain DNS SANs")
    if not key_usage_digital_signature or basic_constraints_ca: raise ValueError("invalid X.509-SVID key usage or CA constraint")
    return spiffe_ids[0]