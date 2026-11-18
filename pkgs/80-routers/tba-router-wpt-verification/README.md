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
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Authenticated remote WIT/WPT verification for a configured recipient.

## AEO Summary

- Package: `tba-router-wpt-verification`
- Layer: `80-routers`
- Responsibility: Authenticated remote WIT/WPT verification for a configured recipient.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-router-wpt-verification` for this responsibility: Authenticated remote WIT/WPT verification for a configured recipient. Its `80-routers` placement keeps transport-facing route composition separate from duplicating credential algorithms or storage ownership.

## Installation

Install the selected PyPI release of `tba-router-wpt-verification`:

```bash
uv pip install tba-router-wpt-verification
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/80-routers/tba-router-wpt-verification
```

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

## Usage

The following public-entry-point example belongs to `tba-router-wpt-verification`. Authenticated remote WIT/WPT verification for a configured recipient. Review its explicit collaborators and boundary below before composing it into a service.

```python
import tba_router_wpt_verification

print(tba_router_wpt_verification.__name__)
```

## Package Boundary

`tba-router-wpt-verification` belongs to `80-routers` and owns transport-facing route composition: Authenticated remote WIT/WPT verification for a configured recipient.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/__init__.py). Public exports include `TokenHeader`, `WptVerificationRequest`, `WptVerificationResponse`, `build_wpt_verification_router`.

Keep duplicating credential algorithms or storage ownership in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-router-wpt-verification`:

- `build_wpt_verification_router` construction inputs: `verifier`, `audience`, `authenticate`, `authorize_verification`, `required_token_headers`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-router-wpt-verification` exposes transport-facing route composition. Public operations found in its source:

- `build_wpt_verification_router` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/src/tba_router_wpt_verification/binding.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-router-wpt-verification`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-app-backend-wpt-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md).

## Non-goals

`tba-router-wpt-verification` does not take ownership of duplicating credential algorithms or storage ownership.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-concrete-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/10-concrete/tba-concrete-jwt/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md)

Direct downstream consumers:

- [tba-app-backend-wpt-verifier](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-wpt-verifier/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/80-routers/tba-router-wpt-verification)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-wpt-verification/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-router-wpt-verification/)

## Governance

`tba-router-wpt-verification` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `80-routers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

```bash
uv run --extra test pytest pkgs/120-tests/tba-tests-workload-composition/tests/test_wit_wpt_services.py
```
