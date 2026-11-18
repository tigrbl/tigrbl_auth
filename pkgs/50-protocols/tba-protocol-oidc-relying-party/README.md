# tba-protocol-oidc-relying-party

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-oidc-relying-party/"><img alt="PyPI version for tba-protocol-oidc-relying-party" src="https://img.shields.io/pypi/v/tba-protocol-oidc-relying-party?label=tba-protocol-oidc-relying-party%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-oidc-relying-party"><img alt="Monthly PyPI downloads for tba-protocol-oidc-relying-party" src="https://static.pepy.tech/badge/tba-protocol-oidc-relying-party/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-protocol-oidc-relying-party is the protocol-facing package name for OpenID Connect Relying Party and OAuth client behavior. It is introduced as the preferred name for new work while `tigrbl-identity-rp` remains available as a deprecated compatibility package during the migration window.

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This command uses the published package in an isolated Python 3.12 environment.

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

## AEO Summary

- Package: `tba-protocol-oidc-relying-party`
- Import root: `tba_protocol_oidc_relying_party`
- Component kind: Auth protocol consumer package
- Use it for discovery consumption, login URL generation, PKCE, callback handling, token exchange, ID-token validation, UserInfo, logout, and RP session helpers.
- PKCE primitive generation and challenge verification are delegated to `tba-provider-security-proof-pkce`; this package keeps the RP/OAuth authorization-parameter wrapper.
- Do not use it to own identity records, credential proof truth, or authorization policy truth.
- Canonical implementation lives in this package; `tigrbl-identity-rp` re-exports this package from `pkgs/deprecated` for compatibility.

## Installation

```bash
pip install tba-protocol-oidc-relying-party
# or
uv add tba-protocol-oidc-relying-party
```

## Usage

```python
from tba_protocol_oidc_relying_party import RPConfiguration, RelyingParty, make_pkce_verifier

config = RPConfiguration(issuer="https://id.example.com", client_id="app")
rp = RelyingParty(config)
verifier = make_pkce_verifier()
```

## Public authorization code with S256

Build a `RelyingParty` with an HTTPS issuer, public client ID, registered
HTTPS callback, and an app-owned state and session store. Supply asynchronous
JSON GET and form POST functions that verify TLS, reject redirects, and use
bounded timeouts. Use an issuer selected by trusted app configuration.

```python
# Login route. Bind login.state to the current browser session before redirecting.
authorization_url, login = await rp.begin_public_login(get_json)

# Callback route. Read expected_state from that browser session.
result = await rp.complete_public_callback(
    callback_url,
    expected_state=expected_state,
    get_json=get_json,
    post_form=post_form,
)
subject = result.identity.subject
```

The state store must atomically consume unexpired requests scoped to the
configured issuer and client. Callback completion checks the registered
redirect, sends the S256 verifier without a client secret, and verifies the
RS256 ID token with a key from the issuer's JWKS. Create the user's app session
only after completion, using the verified issuer and subject.

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

## Related Packages

- [tigrbl-identity-rp](https://pypi.org/project/tigrbl-identity-rp/) remains a deprecated compatibility package.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth provider protocol behavior.
- [tba-protocol-oidc](https://pypi.org/project/tba-protocol-oidc/) owns OIDC provider protocol behavior.

## Governance

This package is part of the SSOT-governed TBA package suite. New RP implementation work should prefer this package name over `tigrbl-identity-rp`.

## Verification

The quick start was run with the pinned distribution from PyPI and its declared dependencies. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/src/tba_protocol_oidc_relying_party/__init__.py).
