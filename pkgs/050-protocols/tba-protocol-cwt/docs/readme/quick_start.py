from tba_concrete_claim_issuer import IssuerClaim
from tba_protocol_cwt import build_cwt_claims, cwt_label_for

issuer = IssuerClaim("https://issuer.example")
assert cwt_label_for(issuer) == 1
encoded = build_cwt_claims(issuer).encode()
assert encoded.startswith(b"\xa1\x01")
