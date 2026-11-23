# tba-profile-communications-identity-bimi

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-profile-communications-identity-bimi</strong></p>
<p align="center">Optional BIMI Mark Certificate and DNS readiness profile.</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-communications-identity-bimi/"><img alt="pypi: tba-profile-communications-identity-bimi" src="https://img.shields.io/pypi/v/tba-profile-communications-identity-bimi"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml"><img alt="Source version: 0.4.0.dev3" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev3&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml"><img alt="Layer: 055-profiles" src="https://img.shields.io/static/v1?label=Layer&amp;message=055-profiles&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-profile-communications-identity-bimi/"><img alt="Monthly PyPI downloads: tba-profile-communications-identity-bimi" src="https://img.shields.io/pypi/dm/tba-profile-communications-identity-bimi"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/README.md"><img alt="README hits: tba-profile-communications-identity-bimi" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/055-profiles/tba-profile-communications-identity-bimi/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

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

- Package: `tba-profile-communications-identity-bimi`
- Layer: `055-profiles`
- Responsibility: Optional BIMI Mark Certificate and DNS readiness profile.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- Distribution: Python package on PyPI.

### Why This Package

`tba-profile-communications-identity-bimi` isolates this responsibility: Optional BIMI Mark Certificate and DNS readiness profile. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py) exposes `AssertionCheck`, `BimiAssertion`, `BimiProfile`, `CertificateOutcome`, `CheckOutcome`, `DmarcCheck`, `MarkType`, `MarkVerification`, `ReadinessResult`, `check_readiness`, `verify_certificate`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-profile-communications-identity-bimi` for this responsibility: Optional BIMI Mark Certificate and DNS readiness profile. Its `055-profiles` placement keeps focused protocol and credential profiles separate from a universal deployment or implicit trust-policy selection.

### Features

- `BimiProfile`: declared in src/tba_profile_communications_identity_bimi/__init__.py
- `BimiDomainChecker`: Adapt BIMI to the shared domain assessment workflow.
- `CheckOutcome`: declared in src/tba_profile_communications_identity_bimi/types.py
- `CertificateOutcome`: declared in src/tba_profile_communications_identity_bimi/types.py
- `MarkType`: declared in src/tba_profile_communications_identity_bimi/types.py
- `AssertionCheck`: declared in src/tba_profile_communications_identity_bimi/types.py
- `DmarcCheck`: declared in src/tba_profile_communications_identity_bimi/types.py
- `ReadinessResult`: declared in src/tba_profile_communications_identity_bimi/types.py

### Non-Goals

`tba-profile-communications-identity-bimi` does not take ownership of a universal deployment or implicit trust-policy selection.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml) declares runtime dependencies including `cryptography`, `tba-contracts-security-trust`, `tba-contracts-dns`, `tba-protocol-bimi`, `tba-protocol-dmarc`. Read the example’s inputs and service requirements before execution.

### Installation

Install the selected PyPI release of `tba-profile-communications-identity-bimi`:

```bash
uv pip install tba-profile-communications-identity-bimi
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/055-profiles/tba-profile-communications-identity-bimi
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-profile-communications-identity-bimi
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-profile-communications-identity-bimi
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-profile-communications-identity-bimi
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

Build the package from the repository root.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/docs/readme/quick_start.sh).

```bash
uv build --wheel pkgs/055-profiles/tba-profile-communications-identity-bimi
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-profile-communications-identity-bimi` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/docs/readme/usage.sh).

```bash
uv build --wheel pkgs/055-profiles/tba-profile-communications-identity-bimi
```
<!-- readme-standards:end example.usage -->

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

### Configuration

Configure `tba-profile-communications-identity-bimi` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-profile-communications-identity-bimi` source raises `ValueError`. Handle these at the calling boundary and consult the implementation for the triggering conditions.

### Best Practices

Use the explicit `tba-profile-communications-identity-bimi` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `AssertionCheck`, `BimiAssertion`, `BimiProfile`, `CertificateOutcome`, `CheckOutcome`, `DmarcCheck`, `MarkType`, `MarkVerification`, `ReadinessResult`, `check_readiness`, `verify_certificate`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-profile-communications-identity-bimi` belongs to `055-profiles` and owns focused protocol and credential profiles: Optional BIMI Mark Certificate and DNS readiness profile.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py). Public exports include `AssertionCheck`, `BimiAssertion`, `BimiProfile`, `CertificateOutcome`, `CheckOutcome`, `DmarcCheck`, `MarkType`, `MarkVerification`, `ReadinessResult`, `check_readiness`, `verify_certificate`.

Keep a universal deployment or implicit trust-policy selection in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

### Public API and Import Surfaces

Import namespace: `tba_profile_communications_identity_bimi`.

Source-declared exports or types: `AssertionCheck`, `BimiAssertion`, `BimiProfile`, `CertificateOutcome`, `CheckOutcome`, `DmarcCheck`, `MarkType`, `MarkVerification`, `ReadinessResult`, `check_readiness`, `verify_certificate`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

Explicit construction inputs and collaborators for `tba-profile-communications-identity-bimi`:

- `BimiProfile` construction inputs: `dns`, `validator`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- `verify_certificate` construction inputs: `assertion_name`, `validator`, `validation_time`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/certificate.py).
- `check_readiness` construction inputs: `dns`, `selector`, `organizational_domain`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/readiness.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

### Protocol Consumers

No direct package-manifest dependency on `tba-profile-communications-identity-bimi` was found in the audited three-repository inventory. External consumers may still use its documented imports or commands.

### Extensions

For `tba-profile-communications-identity-bimi`, use the source-declared public interfaces (`AssertionCheck`, `BimiAssertion`, `BimiProfile`, `CertificateOutcome`, `CheckOutcome`, `DmarcCheck`, `MarkType`, `MarkVerification`, `ReadinessResult`, `check_readiness`, `verify_certificate`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-profile-communications-identity-bimi` exposes focused protocol and credential profiles. Public operations found in its source:

- `BimiProfile.check_readiness` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- `BimiProfile.verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py).
- `verify_certificate` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/certificate.py).
- `check_readiness` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/readiness.py).
- `ReadinessResult.assertion_name` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/types.py).
- `ReadinessResult.ready` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/types.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-profile-communications-identity-bimi`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py). The `tba-profile-communications-identity-bimi` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-profile-communications-identity-bimi` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Check that the build produces a wheel with the package version declared in `pyproject.toml`.

### Certification Status

No external certification is asserted for `tba-profile-communications-identity-bimi` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-profile-communications-identity-bimi` provides optional BIMI Mark Certificate and DNS readiness profile; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-profile-communications-identity-bimi`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-profile-communications-identity-bimi` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/src/tba_profile_communications_identity_bimi/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml) provide the supporting context for `tba-profile-communications-identity-bimi`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

Declared local runtime dependencies:

- [tba-contracts-dns](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-dns/README.md)
- [tba-contracts-security-trust](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-security-trust/README.md)
- [tba-protocol-bimi](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-bimi/README.md)
- [tba-protocol-dmarc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-dmarc/README.md)

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-communications-identity-bimi#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-communications-identity-bimi#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-profile-communications-identity-bimi/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-communications-identity-bimi)
- [pypi: tba-profile-communications-identity-bimi](https://pypi.org/project/tba-profile-communications-identity-bimi/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/055-profiles/tba-profile-communications-identity-bimi)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-profile-communications-identity-bimi/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-profile-communications-identity-bimi`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/055-profiles/tba-profile-communications-identity-bimi` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

**Run the example**

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

---

## Governance

### Ownership and Decision Making

Changes to `tba-profile-communications-identity-bimi` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-profile-communications-identity-bimi` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `055-profiles` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-profile-communications-identity-bimi` source version is `0.4.0.dev3`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/055-profiles/tba-profile-communications-identity-bimi/NOTICE) for attribution.
<!-- readme-standards:end notices -->
