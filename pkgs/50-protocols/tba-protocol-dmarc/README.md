# tba-protocol-dmarc

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-dmarc/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-dmarc/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-dmarc%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-dmarc/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-dmarc%3D%3D0.4.0.dev3/pkgs/50-protocols/tba-protocol-dmarc/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/50-protocols"><img alt="Layer: 50 protocols" src="https://img.shields.io/badge/Layer-50%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-dmarc/"><img alt="PyPI version for tba-protocol-dmarc" src="https://img.shields.io/pypi/v/tba-protocol-dmarc?label=tba-protocol-dmarc%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-dmarc"><img alt="Monthly PyPI downloads for tba-protocol-dmarc" src="https://static.pepy.tech/badge/tba-protocol-dmarc/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-dmarc/README.md"><img alt="README hits for tba-protocol-dmarc" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-dmarc/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-dmarc/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

DMARC TXT record parsing, DNS discovery and policy selection.

`parse_policy_record` returns the policy, subdomain policy, testing flag, and
other fields used in policy selection. `discover_policy` walks the DNS tree
using an injected resolver and reports the effective policy and its source.
Supply `author_exists=False` when the caller has established that the author
domain is nonexistent and needs `np` handling.

```python
from tba_protocol_dmarc import discover_policy

result = discover_policy(dns, "mail.example.com")
print(result.status.value, result.policy_source, result.effective_policy)
```

This package selects published policy. It does not perform per-message SPF
or DKIM authentication.

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/50-protocols/tba-protocol-dmarc
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
