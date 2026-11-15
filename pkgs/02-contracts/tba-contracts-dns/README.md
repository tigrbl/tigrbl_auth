# tba-contracts-dns

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-dns/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-dns/"><img alt="PyPI version for tba-contracts-dns" src="https://img.shields.io/pypi/v/tba-contracts-dns?label=tba-contracts-dns%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-dns"><img alt="Monthly PyPI downloads for tba-contracts-dns" src="https://static.pepy.tech/badge/tba-contracts-dns/month"></a>
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

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/02-contracts/tba-contracts-dns
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
