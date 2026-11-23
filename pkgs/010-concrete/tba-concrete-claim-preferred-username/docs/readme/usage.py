from tba_concrete_claim_preferred_username import PreferredUsernameClaim

claim = PreferredUsernameClaim("alice")
assert claim.name == "preferred_username"
