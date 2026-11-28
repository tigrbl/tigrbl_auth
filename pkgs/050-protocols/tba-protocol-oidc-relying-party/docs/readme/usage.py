from tba_protocol_oidc_relying_party import (
    RPConfiguration,
    RelyingParty,
    make_pkce_verifier,
)

config = RPConfiguration(issuer="https://id.example.com", client_id="app")
rp = RelyingParty(config)
verifier = make_pkce_verifier()
