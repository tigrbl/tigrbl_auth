from tba_concrete_claim_issuer import IssuerClaim

claim = IssuerClaim("https://issuer.example")
assert claim.name == "iss"
