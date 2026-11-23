from tba_concrete_claim_cwt_not_before import CwtNotBeforeClaim

claim = CwtNotBeforeClaim(1700000000)
assert claim.name == "nbf"
