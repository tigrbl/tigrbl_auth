# tba-provider-dns-txt

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-dns-txt%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-dns-txt/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-dns-txt%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-dns-txt/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-dns-txt/"><img alt="PyPI version for tba-provider-dns-txt" src="https://img.shields.io/pypi/v/tba-provider-dns-txt?label=tba-provider-dns-txt%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-dns-txt"><img alt="Monthly PyPI downloads for tba-provider-dns-txt" src="https://static.pepy.tech/badge/tba-provider-dns-txt/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/README.md"><img alt="README hits for tba-provider-dns-txt" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Typed DNS TXT lookup provider.

`DnsTxtResolver.lookup_txt(name)` performs an absolute TXT lookup with a
configurable lifetime. It joins the character strings within a single record,
preserves separate records as bytes, and distinguishes absent data from
temporary failures. Consumers can implement the `TxtResolver` protocol for
deterministic tests or another DNS backend. The shared contract lives in
`tba-contracts-dns` and is also exported here for existing callers.

```python
from tba_provider_dns_txt import DnsTxtResolver

answer = DnsTxtResolver(timeout=3).lookup_txt("_dmarc.example.com")
print(answer.status.value, answer.records)
```

## AEO Summary

- Package: `tba-provider-dns-txt`
- Layer: `20-providers`
- Responsibility: Typed DNS TXT lookup provider.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/src/tba_provider_dns_txt/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-dns-txt` for this responsibility: Typed DNS TXT lookup provider. Its `20-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-dns-txt`:

```bash
uv pip install tba-provider-dns-txt
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/20-providers/tba-provider-dns-txt
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/20-providers/tba-provider-dns-txt
```

## Usage

The following public-entry-point example belongs to `tba-provider-dns-txt`. Typed DNS TXT lookup provider. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_provider_dns_txt import DnsTxtResolver

answer = DnsTxtResolver(timeout=3).lookup_txt("_dmarc.example.com")
print(answer.status.value, answer.records)
```

## Package Boundary

`tba-provider-dns-txt` belongs to `20-providers` and owns replaceable environment implementations: Typed DNS TXT lookup provider.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/src/tba_provider_dns_txt/__init__.py). Public exports include `DnsTxtResolver`, `TxtResolver`, `TxtResult`, `TxtStatus`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-dns-txt`:

- `DnsTxtResolver` construction inputs: `timeout`, `resolver`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/src/tba_provider_dns_txt/resolver.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-dns-txt` exposes replaceable environment implementations. Public operations found in its source:

- `DnsTxtResolver.lookup_txt` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/src/tba_provider_dns_txt/resolver.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-dns-txt`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-provider-dns-txt` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-dns](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers/tba-provider-dns-txt)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-dns-txt/)

## Governance

`tba-provider-dns-txt` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `20-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
