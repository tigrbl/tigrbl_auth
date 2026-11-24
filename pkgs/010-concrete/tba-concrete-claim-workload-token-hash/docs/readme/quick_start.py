from tba_concrete_claim_workload_token_hash import WorkloadTokenHashClaim

claim = WorkloadTokenHashClaim("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
assert claim.name == "wth"
