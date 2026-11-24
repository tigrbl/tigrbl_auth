from tba_concrete_claim_cwt_expiration import CwtExpirationClaim

claim = CwtExpirationClaim(1700000000)
assert claim.name == "exp"
