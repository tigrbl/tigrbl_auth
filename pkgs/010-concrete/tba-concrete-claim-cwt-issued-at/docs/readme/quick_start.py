from tba_concrete_claim_cwt_issued_at import CwtIssuedAtClaim

claim = CwtIssuedAtClaim(1700000000)
assert claim.name == "iat"
