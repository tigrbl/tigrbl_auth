from tba_concrete_claim_credential_status import CredentialStatusClaim

claim = CredentialStatusClaim({"type": "example"})
assert claim.name == "status"
