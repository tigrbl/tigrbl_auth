# tba-provider-certificate-evidence

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-evidence/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-evidence/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-evidence%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-certificate-evidence/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-evidence%3D%3D0.4.0.dev3/pkgs/20-providers/tba-provider-certificate-evidence/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-certificate-evidence/"><img alt="PyPI version for tba-provider-certificate-evidence" src="https://img.shields.io/pypi/v/tba-provider-certificate-evidence?label=tba-provider-certificate-evidence%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-certificate-evidence"><img alt="Monthly PyPI downloads for tba-provider-certificate-evidence" src="https://static.pepy.tech/badge/tba-provider-certificate-evidence/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-evidence/README.md"><img alt="README hits for tba-provider-certificate-evidence" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-evidence/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-certificate-evidence/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

X.509 path, CRL, and RFC 6962 SCT verification.

Supply parsed certificates, explicit trust anchors, a timezone-aware
verification time, and evidence from your deployment. `verify_chain` returns
the selected chain in leaf-first order. Passing CRLs enables chain-wide
revocation checking. `load_crls` checks signed CRL freshness and
`verify_transparency` verifies embedded SCTs against configured log keys.

```python
from tba_provider_certificate_evidence import (
    load_crls,
    load_logs,
    verify_chain,
    verify_transparency,
)

chain = verify_chain(leaf, intermediates, roots, at)
crls = load_crls(chain, local_crls_by_url.get, at)
verify_chain(leaf, chain[1:-1], chain[-1:], at, crls)
verify_transparency(chain[0], chain[1], load_logs(ct_public_keys_pem), at)
```

The caller supplies the CRL source. The provider does not fetch distribution
point URLs or decide which anchors and logs are appropriate for a profile.

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/20-providers/tba-provider-certificate-evidence
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
