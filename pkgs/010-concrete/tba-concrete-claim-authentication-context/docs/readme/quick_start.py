from tba_concrete_claim_authentication_context import AuthenticationContextClaim

claim = AuthenticationContextClaim("urn:example:assurance:2")
assert claim.name == "acr"
