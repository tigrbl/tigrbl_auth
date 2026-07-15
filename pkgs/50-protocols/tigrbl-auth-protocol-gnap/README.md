# tigrbl-auth-protocol-gnap

Layer-50 owner for RFC 9635, the Grant Negotiation and Authorization Protocol,
and the supported superseded draft migration paths.

The package owns RFC version/feature selection, compatibility, wire schemas,
subject-information claim composition, protocol errors, response envelopes,
and explicit mappings to grant negotiation, artifact verification, and replay
protection capabilities.

`sub_ids`, `assertions`, and RFC 3339 `updated_at` are imported from separate
layer-10 claim packages. The OIDC integer `updated_at` claim is intentionally
not reused because its value semantics differ.

## Non-goals

This package does not persist grants, generate continuation secrets, mint or
verify tokens, authenticate resource owners, choose keys, open sessions, or
mount the GNAP HTTP endpoints.
