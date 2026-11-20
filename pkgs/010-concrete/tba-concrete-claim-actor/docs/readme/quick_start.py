from tba_concrete_claim_actor import ActorClaim

claim = ActorClaim({"sub": "service-operator"})
assert claim.name == "act"
