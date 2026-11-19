# tba-profile-communications-identity-bimi

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-communications-identity-bimi%3D%3D0.4.0.dev3/pkgs/055-profiles/tba-profile-communications-identity-bimi/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-communications-identity-bimi%3D%3D0.4.0.dev3/pkgs/055-profiles/tba-profile-communications-identity-bimi/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles"><img alt="Layer: 055 profiles" src="https://img.shields.io/badge/Layer-055%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-communications-identity-bimi/"><img alt="PyPI version for tba-profile-communications-identity-bimi" src="https://img.shields.io/pypi/v/tba-profile-communications-identity-bimi?label=tba-profile-communications-identity-bimi%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-communications-identity-bimi"><img alt="Monthly PyPI downloads for tba-profile-communications-identity-bimi" src="https://static.pepy.tech/badge/tba-profile-communications-identity-bimi/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/README.md"><img alt="README hits for tba-profile-communications-identity-bimi" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Optional BIMI Mark Certificate and DNS readiness profile.

Install from the TBA workspace with `uv sync --extra bimi`.

- `check_readiness` inspects the selected BIMI TXT record and the sender and
  organizational domains' DMARC enforcement. It returns separate DNS and DMARC
  findings, the assertion owner after any fallback, and the published asset
  URLs. `ready` describes DNS/DMARC preflight for a mark-backed deployment.
- `verify_certificate` takes a leaf-first PEM bundle and the assertion owner.
  It checks the certificate policy, classifies CMC/VMC from the signed mark
  type, matches the assertion domain or selector-qualified SAN, and checks the
  embedded compressed logotype and its digest. The injected validator checks
  the certificate path, revocation evidence, and CT evidence.

The readiness policy uses bounded RFC 9989 discovery by default and accepts a
known organizational domain for deployments that need to reproduce a specific
boundary. It checks the legacy `pct` tag and the current `t` testing tag.
The lookup is domain-level and does not process message-local selectors or
SPF/DKIM alignment. The embedded-logo check covers format markers and basic
safety checks. Full SVG schema validation, remote asset retrieval, and mailbox
display are separate checks.

## AEO Summary

- Package: `tba-profile-communications-identity-bimi`
- Layer: `055-profiles`
- Responsibility: Optional BIMI Mark Certificate and DNS readiness profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-profile-communications-identity-bimi` for this responsibility: Optional BIMI Mark Certificate and DNS readiness profile. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

## Installation

Install the selected PyPI release of `tba-profile-communications-identity-bimi`:

```bash
uv pip install tba-profile-communications-identity-bimi
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-communications-identity-bimi
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/055-profiles/tba-profile-communications-identity-bimi
```

## Usage

The following public-entry-point example belongs to `tba-profile-communications-identity-bimi`. Optional BIMI Mark Certificate and DNS readiness profile. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_capability_communications_identity import assess_domain_onboarding, recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async
from tba_profile_communications_identity_bimi import BimiProfile
from tba_profile_communications_identity_bimi.capability_adapter import BimiDomainChecker
from tba_provider_dns_txt import DnsTxtResolver

bimi = BimiProfile(dns=DnsTxtResolver(), validator=validator)
checker = BimiDomainChecker(bimi, evidence=lambda assertion: bundles.get(assertion.name))
initial = await assess_domain_onboarding(
    sending_domain, checker=checker, audit=append_audit_event_async,
    db=db, tenant_id=tenant_id,
)
latest = await recheck_domain(
    sending_domain, checker=checker, audit=append_audit_event_async,
    db=db, tenant_id=tenant_id,
)
```

## Run the example

`scripts/bimi_check.py` composes the profile with the live TXT resolver or
with TBA's existing `ProfiledTrustAnchorProvider` and the Mark Certificate
backend. Use the `assertion.name` returned by the DNS check for the certificate
check. Pass locally obtained evidence and trust material.

```console
uv run --extra bimi python scripts/bimi_check.py dns news.example.com --selector default
uv run --extra bimi python scripts/bimi_check.py verify default._bimi.example.com mark-chain.pem --root mva-root.pem --ct-log ct-log.pem --crl http://ca.example/leaf.crl=leaf.crl --crl http://ca.example/issuer.crl=issuer.crl
```

In a TBA tenant-admin application, authorize the caller for the sending domain
first. The workspace `bimi` extra includes the optional `workflow` adapter.
It composes the profile with the shared communications identity assessment
and TBA's existing durable audit writer. The evidence callback can look up a
local bundle keyed by the discovered assertion owner.

```python
from tba_capability_communications_identity import assess_domain_onboarding, recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async
from tba_profile_communications_identity_bimi import BimiProfile
from tba_profile_communications_identity_bimi.capability_adapter import BimiDomainChecker
from tba_provider_dns_txt import DnsTxtResolver

bimi = BimiProfile(dns=DnsTxtResolver(), validator=validator)
checker = BimiDomainChecker(bimi, evidence=lambda assertion: bundles.get(assertion.name))
initial = await assess_domain_onboarding(
    sending_domain, checker=checker, audit=append_audit_event_async,
    db=db, tenant_id=tenant_id,
)
latest = await recheck_domain(
    sending_domain, checker=checker, audit=append_audit_event_async,
    db=db, tenant_id=tenant_id,
)
```

References include the [BIMI draft](https://datatracker.ietf.org/doc/html/draft-brand-indicators-for-message-identification-15),
the [Mark Certificate verification draft](https://datatracker.ietf.org/doc/html/draft-fetch-validation-vmc-wchuang-12),
the [v1.8 Mark Certificate requirements](https://bimigroup.org/resources/VMC_Requirements_latest.pdf),
and [DMARC RFC 9989](https://www.rfc-editor.org/rfc/rfc9989.html).

## Package Boundary

`tba-profile-communications-identity-bimi` belongs to `055-profiles` and owns focused protocol and credential profiles: Optional BIMI Mark Certificate and DNS readiness profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py). Public exports include `AssertionCheck`, `BimiAssertion`, `BimiProfile`, `CertificateOutcome`, `CheckOutcome`, `DmarcCheck`, `MarkType`, `MarkVerification`, `ReadinessResult`, `check_readiness`, `verify_certificate`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

Explicit construction inputs and collaborators for `tba-profile-communications-identity-bimi`:

- `BimiProfile` construction inputs: `dns`, `validator`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- `verify_certificate` construction inputs: `assertion_name`, `validator`, `validation_time`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/certificate.py).
- `check_readiness` construction inputs: `dns`, `selector`, `organizational_domain`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/readiness.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-profile-communications-identity-bimi` exposes focused protocol and credential profiles. Public operations found in its source:

- `BimiProfile.check_readiness` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- `BimiProfile.verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- `verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/certificate.py).
- `check_readiness` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/readiness.py).
- `ReadinessResult.assertion_name` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/types.py).
- `ReadinessResult.ready` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/types.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-profile-communications-identity-bimi`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

## Non-goals

`tba-profile-communications-identity-bimi` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-contracts-dns](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-dns/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)
- [tba-protocol-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-bimi/README.md)
- [tba-protocol-dmarc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dmarc/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-communications-identity-bimi)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-communications-identity-bimi/)

## Governance

`tba-profile-communications-identity-bimi` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
