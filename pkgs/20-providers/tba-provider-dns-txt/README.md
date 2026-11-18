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

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/20-providers/tba-provider-dns-txt
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
