from tba_runtime_oidc_provider_logout import LogoutRequest

request = LogoutRequest(
    issuer="https://authority.example",
    client_id="my-app",
    post_logout_redirect_uri="https://app.example/signed-out",
    state="browser-transaction",
)
assert request.client_id == "my-app"
