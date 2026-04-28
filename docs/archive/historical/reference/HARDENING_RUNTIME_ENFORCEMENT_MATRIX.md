> [!WARNING]
> Archived historical reference. This document is retained for audit history only and is **not** an authoritative current-state artifact.
> Use `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md` for the current source of truth.

# Hardening Runtime Enforcement Matrix

This matrix captures the executable runtime-hardening checkpoint runtime policy derived from `tigrbl_auth/standards/oauth2/rfc9700.py`.

| Profile | PKCE required for all clients | Implicit/hybrid allowed | Password grant allowed | PAR required | Sender constraint required | DPoP supported | mTLS supported | Allowed response types | Allowed grant types |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| baseline | False | True | True | False | False | False | False | code, token, id_token, code token, code id_token, token id_token, code token id_token | authorization_code, client_credentials, password |
| production | False | True | True | False | False | False | False | code, token, id_token, code token, code id_token, token id_token, code token id_token | authorization_code, client_credentials, password |
| hardening | True | False | False | True | True | True | False | code | authorization_code, client_credentials, urn:ietf:params:oauth:grant-type:device_code |
| peer-claim | True | False | False | True | True | True | False | code | authorization_code, client_credentials, urn:ietf:params:oauth:grant-type:device_code |

## Interpretation

- baseline and production retain broader compatibility posture
- hardening and peer-claim collapse authorization to `code` only
- hardening and peer-claim reject the password grant
- when RFC 9126 is active, hardening and peer-claim require `request_uri`/PAR
- when DPoP or mTLS support is active in hardening and peer-claim, sender-constrained issuance becomes mandatory at the token boundary
