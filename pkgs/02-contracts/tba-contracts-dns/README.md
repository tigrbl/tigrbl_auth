# tba-contracts-dns

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-dns%3D%3D0.4.0.dev4/pkgs/02-contracts/tba-contracts-dns/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-dns%3D%3D0.4.0.dev4/pkgs/02-contracts/tba-contracts-dns/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-dns/"><img alt="PyPI version for tba-contracts-dns" src="https://img.shields.io/pypi/v/tba-contracts-dns?label=tba-contracts-dns%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-dns"><img alt="Monthly PyPI downloads for tba-contracts-dns" src="https://static.pepy.tech/badge/tba-contracts-dns/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/README.md"><img alt="README hits for tba-contracts-dns" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

DNS TXT lookup contracts and shared TXT record handling.

`TxtResolver`, `TxtResult`, and `TxtStatus` let protocol consumers accept a
resolver without a DNS transport dependency. `normalize_domain` canonicalizes
domain names for lookup. `versioned_records` and `parse_tags` handle the shared
TXT tag-list shape used by BIMI and DMARC.

```python
from tba_contracts_dns import TxtResult, TxtStatus


class StaticDns:
    def lookup_txt(self, name: str) -> TxtResult:
        if name == "_dmarc.example.com":
            return TxtResult(TxtStatus.FOUND, (b"v=DMARC1; p=reject",))
        return TxtResult(TxtStatus.ABSENT)
```

## AEO Summary

- Package: `tba-contracts-dns`
- Layer: `02-contracts`
- Responsibility: DNS TXT lookup contracts and shared TXT record handling.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/src/tba_contracts_dns/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-dns` for this responsibility: DNS TXT lookup contracts and shared TXT record handling. Its `02-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-dns`:

```bash
uv pip install tba-contracts-dns
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/02-contracts/tba-contracts-dns
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/02-contracts/tba-contracts-dns
```

## Usage

The following public-entry-point example belongs to `tba-contracts-dns`. DNS TXT lookup contracts and shared TXT record handling. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_dns import TxtResult, TxtStatus


class StaticDns:
    def lookup_txt(self, name: str) -> TxtResult:
        if name == "_dmarc.example.com":
            return TxtResult(TxtStatus.FOUND, (b"v=DMARC1; p=reject",))
        return TxtResult(TxtStatus.ABSENT)
```

## Package Boundary

`tba-contracts-dns` belongs to `02-contracts` and owns shared types and structural ports: DNS TXT lookup contracts and shared TXT record handling.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/src/tba_contracts_dns/__init__.py). Public exports include `TxtResolver`, `TxtResult`, `TxtStatus`, `normalize_domain`, `parse_tags`, `versioned_records`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/src/tba_contracts_dns/__init__.py) for `tba-contracts-dns` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-dns` exposes shared types and structural ports. Public operations found in its source:

- `normalize_domain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/src/tba_contracts_dns/names.py).
- `versioned_records` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/src/tba_contracts_dns/tags.py).
- `parse_tags` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/src/tba_contracts_dns/tags.py).
- `TxtResolver.lookup_txt` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/src/tba_contracts_dns/txt.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-contracts-dns`:

- [tba-protocol-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/README.md)
- [tba-protocol-dmarc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-dmarc/README.md)

Other direct consumers include [tba-profile-communications-identity-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/README.md), [tba-provider-dns-txt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/README.md).

## Non-goals

`tba-contracts-dns` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-profile-communications-identity-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/README.md)
- [tba-protocol-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/README.md)
- [tba-protocol-dmarc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-dmarc/README.md)
- [tba-provider-dns-txt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-dns)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-dns/)

## Governance

`tba-contracts-dns` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `02-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
