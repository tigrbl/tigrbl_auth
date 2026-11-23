from tba_runtime_hosted_sign_in_continuation import ValidatedAuthorizationRequest


request = ValidatedAuthorizationRequest(
    issuer="https://tenant.example.test",
    tenant_id="tenant",
    client_id="application",
    redirect_uri="https://app.example.test/callback",
    parameters=(("state", "client-state"), ("nonce", "client-nonce")),
)
assert request.redirect_uri == "https://app.example.test/callback"
