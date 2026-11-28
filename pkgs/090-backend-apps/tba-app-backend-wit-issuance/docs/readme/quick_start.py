from tba_app_backend_wit_issuance import WitIssuerConfig, build_app


def create_app(signer, authenticate, resolve_identity, authorize_confirmation_key):
    return build_app(
        WitIssuerConfig(
            trust_domain="example.org",
            issuer="https://issuer.example.org",
            key_reference="workload-issuer",
            key_id="issuer-2026",
            algorithm="EdDSA",
        ),
        signer=signer,
        authenticate=authenticate,
        resolve_identity=resolve_identity,
        authorize_confirmation_key=authorize_confirmation_key,
    )
