from tba_concrete_claim_cwt_subject import CwtSubjectClaim

claim = CwtSubjectClaim("alice")
assert claim.name == "sub"
