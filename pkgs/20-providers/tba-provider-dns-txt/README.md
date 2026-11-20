# tba-provider-dns-txt

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/20-providers"><img alt="Layer: 20 providers" src="https://img.shields.io/badge/Layer-20%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-dns-txt/"><img alt="PyPI version for tba-provider-dns-txt" src="https://img.shields.io/pypi/v/tba-provider-dns-txt?label=tba-provider-dns-txt%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-dns-txt"><img alt="Monthly PyPI downloads for tba-provider-dns-txt" src="https://static.pepy.tech/badge/tba-provider-dns-txt/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/20-providers/tba-provider-dns-txt/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Typed TXT lookups backed by the in-house TBA DNS resolver.

```python
from tba_provider_dns_txt import DnsTxtResolver

answer = DnsTxtResolver(timeout=3).lookup_txt("_dmarc.example.com")
print(answer.status.value, answer.records)
```

The adapter joins byte strings within each TXT record and distinguishes absent
data from temporary failures. Consumers can implement the `TxtResolver`
protocol from [tba-contracts-dns](../../02-contracts/tba-contracts-dns).

The standalone [DNS resolver](../tba-provider-dns-resolver) and
[DNS codec](../../03-codecs/tba-codec-dns) provide the general-purpose APIs.
The TXT resolver and its codec and resolver imports retain their existing paths. Zone and protocol operations live in [tba-concrete-dns-zone](../../10-concrete/tba-concrete-dns-zone) and [tba-protocol-dns](../../50-protocols/tba-protocol-dns). Install `tba-protocol-dns[dnssec]` for DNSSEC.

## Verification

Run the [DNS suite](../../120-tests/tba-tests-dns) from the repository root.

```bash
uv run --locked --extra test pytest pkgs/120-tests/tba-tests-dns/tests
```

The [peer suite](../../120-tests/tba-tests-interop-dns) runs the built DNS
packages against BIND and MIT Kerberos.
