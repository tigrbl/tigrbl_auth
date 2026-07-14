# tigrbl-pushed-authorization-capability

This layer-40 package accepts an already normalized and authenticated pushed
authorization request. Its required `push_authorization_request` operation
delegates durable request-URI creation; its optional `record_audit_event`
operation records the resulting event.

It does not parse HTTP, validate request objects, authenticate OAuth clients,
verify DPoP, select FAPI policy, open storage sessions, or implement RFC 9126
errors. Those collaborators are composed by protocol/runtime/API owners.
