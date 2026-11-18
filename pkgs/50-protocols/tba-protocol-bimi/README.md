# tba-protocol-bimi

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-bimi%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-bimi/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-bimi%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-bimi/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-bimi/"><img alt="PyPI version for tba-protocol-bimi" src="https://img.shields.io/pypi/v/tba-protocol-bimi?label=tba-protocol-bimi%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-bimi"><img alt="Monthly PyPI downloads for tba-protocol-bimi" src="https://static.pepy.tech/badge/tba-protocol-bimi/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/README.md"><img alt="README hits for tba-protocol-bimi" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-bimi/README.md.svg?label=hits"></a>
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

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/50-protocols/tba-protocol-bimi
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
