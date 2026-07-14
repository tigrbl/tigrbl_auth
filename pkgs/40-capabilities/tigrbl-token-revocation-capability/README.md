# tigrbl-token-revocation-capability

This layer-40 package exposes the required `token.revocation:revoke_token`
operation and the optional delegated `record_audit_event` operation. It
coordinates an injected durable revocation target with an optional audit
target and reports effective readiness from those bindings.

It does not parse HTTP, select RFC 7009 responses, open storage sessions,
authenticate callers, or own token/revocation state. OAuth RFC 7009 maps the
capability at layer 50; runtime composition injects layer-30 operations; a
layer-80 carrier owns HTTP.
