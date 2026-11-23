from tba_concrete_claim_transaction_token_hash import TransactionTokenHashClaim

claim = TransactionTokenHashClaim("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
assert claim.name == "tth"
