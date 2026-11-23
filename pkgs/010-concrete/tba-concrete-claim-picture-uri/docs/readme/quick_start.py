from tba_concrete_claim_picture_uri import PictureUriClaim

claim = PictureUriClaim("https://alice.example/avatar.png")
assert claim.name == "picture"
