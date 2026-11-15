# tba-profile-workload-proof-wimse-http-signature

The [WIMSE HTTP Signature draft-08](https://www.ietf.org/archive/id/draft-ietf-wimse-http-signature-08.html#section-3)
request profile uses a Workload Identity Token (WIT) and an RFC 9421 signature.
Import `sign_request` and `authenticate_signature` from
`tba_profile_workload_proof_wimse_http_signature`.

`sign_request` signs the method, path, query and applicable headers, including
`Txn-Token` when supplied in `extra_headers`. Use the workload private key
corresponding to the WIT's `cnf.jwk`. `authenticate_signature` validates the
WIT against configured trust-domain anchors, verifies the message signature
and checks nonce reuse using the supplied replay store. It returns the
authenticated workload subject. Transaction authorization and HTTPS are
provided by the caller and receiver.

This implementation supports a single tagged signature on bodyless GET and
POST requests with Ed25519 or P-256 keys. Requests with bodies, CONNECT,
signed responses, and general RFC 9421 parsing are outside its scope.
