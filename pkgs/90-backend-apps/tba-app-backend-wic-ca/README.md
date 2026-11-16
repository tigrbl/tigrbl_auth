# tba-app-backend-wic-ca

In your deployment module, construct the ASGI application with
`build_app(WicCaSettings(...), authenticate=..., resolve_identity=...)`.
Settings point to the CA certificate and private key PEM files and set the
WIMSE trust domain and leaf lifetime. The authentication callback checks the
request's deployment-provided credential and returns an enrollment principal.
The identity resolver receives that principal and returns its authorized
`wimse://` URI or `None`. Serve the app over an authenticated transport.
Mount the WIT router separately if the deployment also issues workload tokens.
