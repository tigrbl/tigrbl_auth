# tigrbl-digital-credential-issuance

Layer-40 orchestration for credential configuration, offers, wallet trust, and
credential issuance.

## Injected dependencies

Required collaborators are a `CredentialIssuerPort`, configuration read/write
operations, an offer recorder, and an issuance-result recorder. A
`WalletAttestationVerifierPort` is optional. All operations are async-safe and
durable state remains behind the injected callables.

## Operations and readiness

Required operations are `register_configuration`, `create_offer`, `issue`, and
`record_issuance`. `verify_wallet_attestation` is optional and is reported as
unavailable when unbound. Construction rejects a missing required operation.

## Protocol consumers

Layer-50 OID4VCI maps issuance messages to this capability. HAIP selects and
constrains the OID4VCI composition when its profile is enabled.

## Non-goals

This package does not own credential formats, protocol schemas, HTTP, wallet
attestation policy, signing keys, trust resolution, or persistence.
