from tba_concrete_claim_access_token_digest import AccessTokenDigestClaim

claim = AccessTokenDigestClaim("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
assert claim.name == "ath"
