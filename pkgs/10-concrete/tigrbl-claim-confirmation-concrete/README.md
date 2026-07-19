# tigrbl-claim-confirmation-concrete

Owns the JOSE `cnf` claim value and its supported `jwk`, `jkt`, and
`x5t#S256` methods. CWT integer-labelled confirmation is owned separately by
`tigrbl-claim-cwt-confirmation-concrete`.

## Non-goals

Protocol claim-set composition, version selection, proof verification, key
resolution, and private-key custody are not owned here.