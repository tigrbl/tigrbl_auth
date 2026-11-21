# TBA DNS domain ownership proof

Verify an exact TXT record containing a caller-generated challenge and the exact
CNAME record for the requested host. The caller supplies a trusted HTTPS DNS
resolver implementing the DNS JSON response format, the expected canonical
target, and the requested DNS owner names. DNS failures and malformed responses
fail closed. This provider does not grant access, provision TLS, or manage DNS.

Persist the challenge and its expiration in the calling service. Use a new
challenge whenever a domain is claimed again.
