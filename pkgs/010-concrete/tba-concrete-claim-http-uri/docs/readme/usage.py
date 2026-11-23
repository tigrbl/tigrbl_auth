from tba_concrete_claim_http_uri import HttpUriClaim

claim = HttpUriClaim("https://issuer.example")
assert claim.name == "htu"
