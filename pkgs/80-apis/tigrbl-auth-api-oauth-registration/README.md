# tigrbl-auth-api-oauth-registration

This layer-80 package owns the RFC 7591 and RFC 7592 HTTP carrier at
`/register` and `/register/{client_id}`. It parses protocol schemas and
delegates every lifecycle operation to injected runtime collaborators.

It does not own registration state, generate secrets, validate client policy,
authorize registration access tokens, or compose capabilities.
