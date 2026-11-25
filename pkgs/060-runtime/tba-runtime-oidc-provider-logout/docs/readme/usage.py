from tba_runtime_oidc_provider_logout import append_logout_state

redirect = append_logout_state(
    "https://app.example/signed-out?lang=en", "browser/transaction"
)
assert redirect == (
    "https://app.example/signed-out?lang=en&state=browser%2Ftransaction"
)
