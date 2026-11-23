from tba_concrete_claim_cwt_issuer import CwtIssuerClaim

claim = CwtIssuerClaim("https://issuer.example")
assert claim.name == "iss"
