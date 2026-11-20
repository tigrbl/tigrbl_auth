# tba-client-relying-party-session

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-client-relying-party-session%3D%3D0.4.0.dev4/pkgs/075-clients/tba-client-relying-party-session/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-client-relying-party-session%3D%3D0.4.0.dev4/pkgs/075-clients/tba-client-relying-party-session/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients"><img alt="Layer: 075 clients" src="https://img.shields.io/badge/Layer-075%20clients-0a7f5a"></a>
<a href="https://pypi.org/project/tba-client-relying-party-session/"><img alt="PyPI version for tba-client-relying-party-session" src="https://img.shields.io/pypi/v/tba-client-relying-party-session?label=tba-client-relying-party-session%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-client-relying-party-session"><img alt="Monthly PyPI downloads for tba-client-relying-party-session" src="https://static.pepy.tech/badge/tba-client-relying-party-session/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/README.md"><img alt="README hits for tba-client-relying-party-session" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Transport-injected RP session client.

## AEO Summary

- Package: `tba-client-relying-party-session`
- Layer: `075-clients`
- Responsibility: Typed client for server-owned RP sessions.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/src/tba_client_relying_party_session/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-client-relying-party-session` for this responsibility: Typed client for server-owned RP sessions. Its `075-clients` placement keeps relying-party and client integration separate from authority-side policy decisions or server-owned persistence.

## Installation

Install the selected PyPI release of `tba-client-relying-party-session`:

```bash
uv pip install tba-client-relying-party-session
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/075-clients/tba-client-relying-party-session
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_client_relying_party_session import RelyingPartySessionClient

assert callable(RelyingPartySessionClient)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-client-relying-party-session==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the RelyingPartySessionClient entry point is available.

## Usage

The following public-entry-point example belongs to `tba-client-relying-party-session`. Typed client for server-owned RP sessions. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_client_relying_party_session import RelyingPartySessionClient

assert callable(RelyingPartySessionClient)
```

## Package Boundary

`tba-client-relying-party-session` belongs to `075-clients` and owns relying-party and client integration: Typed client for server-owned RP sessions.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/src/tba_client_relying_party_session/__init__.py). Public exports include `RelyingPartySessionClient`.

Keep authority-side policy decisions or server-owned persistence in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/src/tba_client_relying_party_session/__init__.py) for `tba-client-relying-party-session` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-client-relying-party-session` exposes relying-party and client integration. Public operations found in its source:

- `RelyingPartySessionClient.begin` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/src/tba_client_relying_party_session/__init__.py).
- `RelyingPartySessionClient.session` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/src/tba_client_relying_party_session/__init__.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-client-relying-party-session`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-client-relying-party-session` does not take ownership of authority-side policy decisions or server-owned persistence.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

`tba-client-relying-party-session` declares no local runtime dependency and has no direct consumer in the active manifest graph. Browse the [075-clients layer](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients) for adjacent package responsibilities; adjacency does not imply a dependency.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/075-clients/tba-client-relying-party-session)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-client-relying-party-session/)

## Governance

`tba-client-relying-party-session` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `075-clients` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/075-clients/tba-client-relying-party-session/src/tba_client_relying_party_session/__init__.py).
