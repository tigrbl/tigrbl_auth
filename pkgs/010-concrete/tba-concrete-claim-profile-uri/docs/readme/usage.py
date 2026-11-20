from tba_concrete_claim_profile_uri import ProfileUriClaim

claim = ProfileUriClaim("https://alice.example/profile")
assert claim.name == "profile"
