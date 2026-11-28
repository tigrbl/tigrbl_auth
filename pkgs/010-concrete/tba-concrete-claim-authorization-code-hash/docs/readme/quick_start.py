from tba_concrete_claim_authorization_code_hash import AuthorizationCodeHashClaim

claim = AuthorizationCodeHashClaim("AAAAAAAAAAAAAAAAAAAAAA")
assert claim.name == "c_hash"
