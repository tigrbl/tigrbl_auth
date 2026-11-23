from tba_concrete_claim_confirmation import ConfirmationClaim

claim = ConfirmationClaim({"jkt": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"})
assert claim.name == "cnf"
