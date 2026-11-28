from tba_app_backend_wpt_verifier import WptVerifierSettings, build_app


def create_app(trusted_keys, replay_store, authenticate, authorize_verification):
    return build_app(
        WptVerifierSettings(
            audience="https://resource.example.org/work",
            trust_by_domain=trusted_keys,
            required_token_headers=("txn-token",),
        ),
        replay_store=replay_store,
        authenticate=authenticate,
        authorize_verification=authorize_verification,
    )
