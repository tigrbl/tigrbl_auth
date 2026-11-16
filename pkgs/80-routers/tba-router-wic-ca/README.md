# tba-router-wic-ca

Mount `build_wic_ca_router(service=..., authenticate=...)` on a Tigrbl app.
`POST /wic/issue` accepts JSON with `csr_pem` and returns `certificate_pem`.
The async authenticator must return a trusted enrollment principal or `None`.
