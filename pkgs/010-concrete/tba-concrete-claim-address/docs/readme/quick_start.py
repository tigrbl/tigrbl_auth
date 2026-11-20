from tba_concrete_claim_address import AddressClaim

claim = AddressClaim(
    {"country": "US", "postal_code": "20001", "locality": "Washington"}
)
assert claim.name == "address"
