# tba-concrete-claim-confirmation

Owns the JOSE `cnf` claim value and its supported `jwk`, `jkt`, and
`x5t#S256` methods. CWT integer-labelled confirmation is owned separately by
`tba-concrete-claim-cwt-confirmation`.

## Non-goals

Protocol claim-set composition, version selection, proof verification, key
resolution, and private-key custody are not owned here.