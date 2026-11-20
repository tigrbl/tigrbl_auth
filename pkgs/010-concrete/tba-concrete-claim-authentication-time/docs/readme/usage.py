from tba_concrete_claim_authentication_time import AuthenticationTimeClaim

claim = AuthenticationTimeClaim(1700000000)
assert claim.name == "auth_time"
