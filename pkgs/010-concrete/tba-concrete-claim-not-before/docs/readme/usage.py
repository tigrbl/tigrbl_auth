from tba_concrete_claim_not_before import NotBeforeClaim

claim = NotBeforeClaim(1700000000)
assert claim.name == "nbf"
