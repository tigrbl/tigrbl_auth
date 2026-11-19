# tba-provider-certificate-evidence

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-evidence%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-certificate-evidence/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-provider-certificate-evidence%3D%3D0.4.0.dev3/pkgs/020-providers/tba-provider-certificate-evidence/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers"><img alt="Layer: 020 providers" src="https://img.shields.io/badge/Layer-020%20providers-0a7f5a"></a>
<a href="https://pypi.org/project/tba-provider-certificate-evidence/"><img alt="PyPI version for tba-provider-certificate-evidence" src="https://img.shields.io/pypi/v/tba-provider-certificate-evidence?label=tba-provider-certificate-evidence%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-provider-certificate-evidence"><img alt="Monthly PyPI downloads for tba-provider-certificate-evidence" src="https://static.pepy.tech/badge/tba-provider-certificate-evidence/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/README.md"><img alt="README hits for tba-provider-certificate-evidence" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
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

## AEO Summary

- Package: `tba-provider-certificate-evidence`
- Layer: `020-providers`
- Responsibility: X.509 path, CRL, and RFC 6962 SCT verification.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-provider-certificate-evidence` for this responsibility: X.509 path, CRL, and RFC 6962 SCT verification. Its `020-providers` placement keeps replaceable environment implementations separate from capability orchestration, storage table ownership, or HTTP routing.

## Installation

Install the selected PyPI release of `tba-provider-certificate-evidence`:

```bash
uv pip install tba-provider-certificate-evidence
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/020-providers/tba-provider-certificate-evidence
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/020-providers/tba-provider-certificate-evidence
```

## Usage

The following public-entry-point example belongs to `tba-provider-certificate-evidence`. X.509 path, CRL, and RFC 6962 SCT verification. Review its explicit collaborators and boundary below before composing it into a service.

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

## Package Boundary

`tba-provider-certificate-evidence` belongs to `020-providers` and owns replaceable environment implementations: X.509 path, CRL, and RFC 6962 SCT verification.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/__init__.py). Public exports include `CrlSource`, `CtEvidenceUnavailable`, `PathValidationError`, `load_crls`, `load_logs`, `verify_chain`, `verify_transparency`.

Keep capability orchestration, storage table ownership, or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-provider-certificate-evidence`:

- `PathValidationError` construction inputs: `message`, `revoked`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/pkix.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-provider-certificate-evidence` exposes replaceable environment implementations. Public operations found in its source:

- `load_crls` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/crl.py).
- `load_logs` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/ct.py).
- `verify_transparency` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/ct.py).
- `verify_chain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/src/tba_provider_certificate_evidence/pkix.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-provider-certificate-evidence`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-provider-bimi-mark-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/README.md).

## Non-goals

`tba-provider-certificate-evidence` does not take ownership of capability orchestration, storage table ownership, or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Direct downstream consumers:

- [tba-provider-bimi-mark-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-bimi-mark-certificate/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/020-providers/tba-provider-certificate-evidence)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-certificate-evidence/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-provider-certificate-evidence/)

## Governance

`tba-provider-certificate-evidence` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `020-providers` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
