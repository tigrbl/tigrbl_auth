from tba_concrete_claim_audience import AudienceClaim

claim = AudienceClaim("https://api.example")
assert claim.name == "aud"
