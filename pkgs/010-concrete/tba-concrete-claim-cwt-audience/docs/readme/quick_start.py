from tba_concrete_claim_cwt_audience import CwtAudienceClaim

claim = CwtAudienceClaim("https://api.example")
assert claim.name == "aud"
