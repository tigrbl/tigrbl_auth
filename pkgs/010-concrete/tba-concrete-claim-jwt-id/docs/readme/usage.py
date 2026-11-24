from tba_concrete_claim_jwt_id import JwtIdClaim

claim = JwtIdClaim("token-1")
assert claim.name == "jti"
