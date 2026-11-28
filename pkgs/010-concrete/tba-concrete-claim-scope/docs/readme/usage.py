from tba_concrete_claim_scope import ScopeClaim

claim = ScopeClaim("openid profile")
assert claim.name == "scope"
