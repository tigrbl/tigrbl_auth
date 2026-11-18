# tba-protocol-bimi

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-bimi%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-bimi/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-bimi%3D%3D0.4.0.dev4/pkgs/50-protocols/tba-protocol-bimi/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-bimi/"><img alt="PyPI version for tba-protocol-bimi" src="https://img.shields.io/pypi/v/tba-protocol-bimi?label=tba-protocol-bimi%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-bimi"><img alt="Monthly PyPI downloads for tba-protocol-bimi" src="https://static.pepy.tech/badge/tba-protocol-bimi/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/README.md"><img alt="README hits for tba-protocol-bimi" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

BIMI TXT record parsing and selector discovery.

Use `parse_assertion` to inspect a known record or `discover_assertion` to
look up a selector at the author domain and, if the record is absent, its
organizational domain. Discovery returns the actual assertion owner.

```python
from tba_protocol_bimi import discover_assertion
from tba_protocol_dmarc import discover_policy

policy = discover_policy(dns, "mail.example.com")
result = discover_assertion(
    dns, "mail.example.com", organizational_domain=policy.organizational_domain
)
```

These functions perform domain-level discovery. The layer-55 BIMI profile
evaluates DMARC eligibility and Mark Certificate evidence.

## AEO Summary

- Package: `tba-protocol-bimi`
- Layer: `50-protocols`
- Responsibility: BIMI TXT record parsing and selector discovery.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/src/tba_protocol_bimi/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-protocol-bimi` for this responsibility: BIMI TXT record parsing and selector discovery. Its `50-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

Install the selected PyPI release of `tba-protocol-bimi`:

```bash
uv pip install tba-protocol-bimi
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/50-protocols/tba-protocol-bimi
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/50-protocols/tba-protocol-bimi
```

## Usage

The following public-entry-point example belongs to `tba-protocol-bimi`. BIMI TXT record parsing and selector discovery. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_protocol_bimi import discover_assertion
from tba_protocol_dmarc import discover_policy

policy = discover_policy(dns, "mail.example.com")
result = discover_assertion(
    dns, "mail.example.com", organizational_domain=policy.organizational_domain
)
```

## Package Boundary

`tba-protocol-bimi` belongs to `50-protocols` and owns protocol semantics and projections: BIMI TXT record parsing and selector discovery.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/src/tba_protocol_bimi/__init__.py). Public exports include `AssertionDiscovery`, `AssertionStatus`, `BimiAssertion`, `assertion_owner`, `discover_assertion`, `normalize_selector`, `parse_assertion`.

Keep deployment hosting or ownership of persistence implementations in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-bimi`:

- `parse_assertion` construction inputs: `name`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/src/tba_protocol_bimi/record.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-bimi` exposes protocol semantics and projections. Public operations found in its source:

- `discover_assertion` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/src/tba_protocol_bimi/discovery.py).
- `normalize_selector` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/src/tba_protocol_bimi/record.py).
- `assertion_owner` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/src/tba_protocol_bimi/record.py).
- `parse_assertion` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/src/tba_protocol_bimi/record.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-bimi`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-profile-communications-identity-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/README.md).

## Non-goals

`tba-protocol-bimi` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-codec-x509-logotype](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/03-codecs/tba-codec-x509-logotype/README.md)
- [tba-contracts-dns](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/README.md)

Direct downstream consumers:

- [tba-profile-communications-identity-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols/tba-protocol-bimi)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-bimi/)

## Governance

`tba-protocol-bimi` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `50-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
