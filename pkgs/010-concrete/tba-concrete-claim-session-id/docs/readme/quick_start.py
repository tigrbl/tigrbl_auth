from tba_concrete_claim_session_id import SessionIdClaim

claim = SessionIdClaim("session-1")
assert claim.name == "sid"
