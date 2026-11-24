from tba_concrete_claim_cwt_id import CwtIdClaim

claim = CwtIdClaim("token-1")
assert claim.name == "jti"
