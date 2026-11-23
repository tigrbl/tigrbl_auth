from tba_concrete_claim_email_verified import EmailVerifiedClaim

claim = EmailVerifiedClaim(True)
assert claim.name == "email_verified"
