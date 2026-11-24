from tba_concrete_claim_authorization_context import AuthorizationContextClaim

claim = AuthorizationContextClaim({"type": "moqt", "action": "SUBSCRIBE"})
assert claim.name == "actx"
