# tigrbl-client-registration-capability

This layer-40 package composes the protocol-neutral lifecycle of a registered
client. Its required delegated operations create, read, update, and disable a
canonical client-registration aggregate. An optional delegated operation
records lifecycle audit events. The capability reports the effective binding
state of every operation.

It does not parse HTTP, generate or hash secrets, validate OAuth metadata,
select RFC 7591/7592 errors, or open storage sessions. Layer 50 maps the
capability to protocol revisions; layer 60 injects durable operations and
security policy; layer 80 owns HTTP.
