# tba-router-wpt-verification

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-wpt-verification%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-wpt-verification/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-router-wpt-verification%3D%3D0.4.0.dev3/pkgs/80-routers/tba-router-wpt-verification/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers"><img alt="Layer: 80 routers" src="https://img.shields.io/badge/Layer-80%20routers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-router-wpt-verification/"><img alt="PyPI version for tba-router-wpt-verification" src="https://img.shields.io/pypi/v/tba-router-wpt-verification?label=tba-router-wpt-verification%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-router-wpt-verification"><img alt="Monthly PyPI downloads for tba-router-wpt-verification" src="https://static.pepy.tech/badge/tba-router-wpt-verification/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/README.md"><img alt="README hits for tba-router-wpt-verification" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Authenticated remote WIT/WPT verification for a configured recipient.

## Quick start

Mount `build_wpt_verification_router(verifier=..., audience=...,
authenticate=..., authorize_verification=...)` on a `TigrblApp`.
`authenticate` identifies the calling recipient service; the separate
`authorize_verification` callback must explicitly allow that service to delegate
verification for the configured audience. These checks precede proof validation.

`POST /wpt/verify` accepts:

```json
{
  "workload_identity_token": "<original WIT>",
  "workload_proof_token": "<original WPT, without the WPT scheme prefix>",
  "token_headers": [{"name": "Txn-Token", "value": "<original token>"}]
}
```

`token_headers` is a list so duplicate original headers remain observable and
are rejected when used as bindings. Do not collapse duplicates before forwarding.
Caller authentication belongs in this API request's headers, separately from
the submitted workload proof. Submitted audiences and trust configuration are rejected.
The audience and `required_token_headers` are selected when mounting. Required
headers must be present and cryptographically bound; clients cannot disable this
policy by omitting a header. This strict presence policy is separate from the
profile's optional `bound_token_headers` binding selector.

A successful response contains `valid`, `subject`, `audience`, `proof_id`, and
`expires_at`. Missing/denied caller credentials return 401/403, malformed requests
return 400, and invalid or replayed workload proofs return 401. Responses disable
caching and do not echo tokens. An infrastructure exception fails the request;
it never returns a successful verification decision.

Verification **consumes replay state**. Use the result once for the original
request; do not preflight it and then verify the same proof again. The result
authenticates the workload; the recipient still applies resource authorization.
Transport this delegation over the deployment's authenticated confidential channel.

Build from the repository root:

```bash
uv build --wheel pkgs/80-routers/tba-router-wpt-verification
```

## Verification

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_wit_wpt_services.py
```
