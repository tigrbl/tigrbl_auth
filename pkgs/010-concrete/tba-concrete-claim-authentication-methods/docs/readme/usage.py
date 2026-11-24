from tba_concrete_claim_authentication_methods import AuthenticationMethodsClaim

claim = AuthenticationMethodsClaim(("pwd", "otp"))
assert claim.name == "amr"
