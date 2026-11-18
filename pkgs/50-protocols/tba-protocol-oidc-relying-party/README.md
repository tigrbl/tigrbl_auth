# tba-protocol-oidc-relying-party

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oidc-relying-party%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-oidc-relying-party/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oidc-relying-party%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-oidc-relying-party/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-oidc-relying-party/"><img alt="PyPI version for tba-protocol-oidc-relying-party" src="https://img.shields.io/pypi/v/tba-protocol-oidc-relying-party?label=tba-protocol-oidc-relying-party%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-oidc-relying-party"><img alt="Monthly PyPI downloads for tba-protocol-oidc-relying-party" src="https://static.pepy.tech/badge/tba-protocol-oidc-relying-party/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/README.md"><img alt="README hits for tba-protocol-oidc-relying-party" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-protocol-oidc-relying-party is the protocol-facing package name for OpenID Connect Relying Party and OAuth client behavior. It is introduced as the preferred name for new work while `tigrbl-identity-rp` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tba-protocol-oidc-relying-party`
- Import root: `tba_protocol_oidc_relying_party`
- Component kind: Auth protocol consumer package
- Use it for discovery consumption, login URL generation, PKCE, callback handling, token exchange, ID-token validation, UserInfo, logout, and RP session helpers.
- PKCE primitive generation and challenge verification are delegated to `tba-provider-security-proof-pkce`; this package keeps the RP/OAuth authorization-parameter wrapper.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical implementation lives in this package; `tigrbl-identity-rp` re-exports this package from `pkgs/deprecated` for compatibility.

## When to use it

Choose `tba-protocol-oidc-relying-party` for this responsibility: OpenID Connect relying-party and OAuth client protocol implementation package for the TBA package suite. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

```bash
pip install tba-protocol-oidc-relying-party
# or
uv add tba-protocol-oidc-relying-party
```

Install the current `tba-protocol-oidc-relying-party` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-oidc-relying-party
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_oidc_relying_party import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oidc-relying-party==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

## Usage

```python
from tba_protocol_oidc_relying_party import RPConfiguration, RelyingParty, make_pkce_verifier

config = RPConfiguration(issuer="https://id.example.com", client_id="app")
rp = RelyingParty(config)
verifier = make_pkce_verifier()
```

## Package Boundary

- Relying Party and OAuth client protocol behavior
- Discovery, authorization URL, PKCE, callback, token exchange, UserInfo, logout, and session helpers
- Discovery metadata semantics are consumed from the OIDC protocol package;
  runtime deployment resolution and provider-side publication are not owned by
  the RP package.
- App-side protocol integration consuming an issuer
- Browser/client storage and no-client-secret policy helpers
- The legacy `logout` module exports protocol validation semantics only;
  provider-side durable fanout planning is owned by the identity server runtime.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-oidc-relying-party`:

- `BrowserMemorySession` construction inputs: `policy`, `client_secret`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `DiscoveryClient` construction inputs: `fetch`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `UserInfoClient` construction inputs: `fetch`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `RelyingParty` construction inputs: `config`, `state_store`, `session_store`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `validate_id_token_claims` construction inputs: `issuer`, `audience`, `nonce`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `verify_id_token` construction inputs: `verifier`, `issuer`, `audience`, `nonce`, `now`, `userinfo`, `maximum_age`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `migrate_configuration` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-oidc-relying-party` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py).
- `compose_rp_id_token_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/claims.py).
- `BrowserMemorySession.set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `BrowserMemorySession.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `BrowserMemorySession.clear` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `assert_browser_no_client_secret` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `validate_browser_storage_policy` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `JwksCache.put` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `JwksCache.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `DiscoveryClient.discover` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `UserInfoClient.get` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).
- `RelyingParty.build_authorization_url` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/client.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-oidc-relying-party`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-router-relying-party-session](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/80-routers/tba-router-relying-party-session/README.md).

## Non-goals

`tba-protocol-oidc-relying-party` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tigrbl-identity-rp](https://pypi.org/project/tigrbl-identity-rp/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth provider protocol behavior.
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/) owns OIDC provider protocol behavior.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-oidc-relying-party)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oidc-relying-party/)

## Governance

This package is part of the SSOT-governed TBA package suite. New RP implementation work should prefer this package name over `tigrbl-identity-rp`.

`tba-protocol-oidc-relying-party` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py).
