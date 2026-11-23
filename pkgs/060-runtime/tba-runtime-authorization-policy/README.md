# tba-runtime-authorization-policy

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-runtime-authorization-policy</strong></p>
<p align="center">Authorization policy, authority, grants, permissions, decisions, and governance implementation package for the TBA package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-authorization-policy/"><img alt="pypi: tba-runtime-authorization-policy" src="https://img.shields.io/pypi/v/tba-runtime-authorization-policy"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml"><img alt="Source version: 0.4.0.dev4" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev4&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml"><img alt="Layer: 060-runtime" src="https://img.shields.io/static/v1?label=Layer&amp;message=060-runtime&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-runtime-authorization-policy/"><img alt="Monthly PyPI downloads: tba-runtime-authorization-policy" src="https://img.shields.io/pypi/dm/tba-runtime-authorization-policy"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/README.md"><img alt="README hits: tba-runtime-authorization-policy" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/pkgs/060-runtime/tba-runtime-authorization-policy/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

tba-runtime-authorization-policy is the authorization-facing package name for authority, policy, grants, permissions, replay, and governance controls. It is introduced as the preferred name for new work while `tigrbl-identity-policy` remains available as a deprecated compatibility package during the migration window.

- Package: `tba-runtime-authorization-policy`
- Import root: `tba_runtime_authorization_policy`
- Component kind: Authorization package
- Use it for authorization policy surfaces rather than credential verification or token signing.
- It owns authority roles, RBAC, ABAC, delegation, policy replay, and decision audit concepts.
- Administrator objects, `PolicyEngine`, `ServiceIdentityRegistry`, and `AdminGate` are implemented in this package as storage-backed programmatic surfaces.
- Deterministic rule objects live in `tba-concrete-authorization-policy-rules`; the decision engine, authority derivation graph, and invariant registry each live in their own 10-layer concrete package.
- Canonical authz-policy surfaces live in this package; `tigrbl-identity-policy` re-exports this package from `pkgs/deprecated` for compatibility.

### Why This Package

`tba-runtime-authorization-policy` isolates this responsibility: Authorization policy, authority, grants, permissions, decisions, and governance implementation package for the TBA package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) exposes `ABACAdministrator`, `ADMIN_CLIENT_FIELDS`, `AccessReviewCampaign`, `AccessReviewDecision`, `AccessReviewItem`, `AccessReviewWorkflow`, `AdminPolicy`, `AttributePolicy`, `AuthorityClosure`, `AuthorityDerivationGraph`, `AuthorityEdge`, `AuthorityGraphIntegrityReport`, `AuthorityMonotonicityReport`, `AuthorityMutationKind`, `AuthorityNode`, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-runtime-authorization-policy` for this responsibility: Authorization policy, authority, grants, permissions, decisions, and governance implementation package for the TBA package suite. Its `060-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

### Features

- Public source surface: `ABACAdministrator`, `ADMIN_CLIENT_FIELDS`, `AccessReviewCampaign`, `AccessReviewDecision`, `AccessReviewItem`, `AccessReviewWorkflow`, `AdminPolicy`, `AttributePolicy`, `AuthorityClosure`, `AuthorityDerivationGraph`, `AuthorityEdge`, `AuthorityGraphIntegrityReport`, `AuthorityMonotonicityReport`, `AuthorityMutationKind`, `AuthorityNode`.
- Declared responsibility: Authorization policy, authority, grants, permissions, decisions, and governance implementation package for the TBA package suite.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-runtime-authorization-policy` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml) declares runtime dependencies including `tba-provider-authorization-policy-decision-engine`, `tba-capability-access-governance`, `tba-capability-policy-administration`, `tba-capability-policy-assurance`, `tba-concrete-authorization-policy-rules`, `tba-provider-security-authorization-provenance-builder`, `tigrbl`, `tba-primitives-identity`, `tba-contracts-identity`, `tba-concrete-authority-graph`, `tba-concrete-policy-decision-engine-default`, `tba-contracts-release`. Read the example’s inputs and service requirements before execution.

### Installation

```bash
pip install tba-runtime-authorization-policy
# or
uv add tba-runtime-authorization-policy
```

Install the current `tba-runtime-authorization-policy` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/060-runtime/tba-runtime-authorization-policy
```

#### uv

<!-- readme-standards:begin installation.uv -->
```bash
uv add tba-runtime-authorization-policy
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
```bash
python -m pip install tba-runtime-authorization-policy
```
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
```bash
poetry add tba-runtime-authorization-policy
```
<!-- readme-standards:end installation.poetry -->

### Quick Start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.


```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-authorization-policy==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the ABACAdministrator entry point is available.

#### Example

The maintained integration example defines `configure_authorization` with explicit caller-owned inputs: `app, db, deployment`. Invoke it with those inputs; loading the example file alone does not execute the integration.

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/docs/readme/quick_start.py).

```python
from tba_runtime_authorization_policy import ABACAdministrator

assert callable(ABACAdministrator)
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-runtime-authorization-policy` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

The maintained integration example defines `configure_authorization` with explicit caller-owned inputs: `app, db, deployment`. Invoke it with those inputs; loading the example file alone does not execute the integration.

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.py](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/docs/readme/usage.py).

```python
from tba_runtime_authorization_policy import AuthorityRole, AuthorityScope
from tba_runtime_authorization_policy import (
    AdminGate,
    ABACAdministrator,
    DelegatedAdministrator,
)
from tba_runtime_authorization_policy import (
    PolicyEngine,
    RBACAdministrator,
    ServiceIdentityRegistry,
)
from tba_runtime_authorization_policy import (
    AuthorityDerivationGraph,
    PolicyDecisionEngine,
)
from tba_runtime_authorization_policy import (
    AuthorizationInvariant,
    AuthorizationSafetyPropertyEvaluator,
)


def configure_authorization(*, app, db, deployment):
    """Supply caller-owned integration inputs; this definition does not execute a deployment."""
    assert AuthorityRole.ADMIN.value == "admin"
    scope = AuthorityScope("tenant-a", "client.read")
    graph = AuthorityDerivationGraph()
    abac = ABACAdministrator(db)
    delegated = DelegatedAdministrator(db)
    engine = PolicyDecisionEngine()
    gate = AdminGate(app, deployment=deployment)
    orchestrator = PolicyEngine(db=db)
    invariants = (
        AuthorizationInvariant(
            invariant_id="authz.non_escalation",
            title="No escalation",
            property_family="safety",
            statement="Effective authority cannot exceed granted closure.",
            verification_method="graph",
        ),
    )
    rbac = RBACAdministrator(db)
    services = ServiceIdentityRegistry()
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-runtime-authorization-policy` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-runtime-authorization-policy` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py).

### Best Practices

Use the explicit `tba-runtime-authorization-policy` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing `ABACAdministrator`, `ADMIN_CLIENT_FIELDS`, `AccessReviewCampaign`, `AccessReviewDecision`, `AccessReviewItem`, `AccessReviewWorkflow`, `AdminPolicy`, `AttributePolicy`, `AuthorityClosure`, `AuthorityDerivationGraph`, `AuthorityEdge`, `AuthorityGraphIntegrityReport`, `AuthorityMonotonicityReport`, `AuthorityMutationKind`, `AuthorityNode`; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

- Authority roles, grants, permissions, scopes, and decision inputs
- RBAC and ABAC policy surfaces backed by `tba-storage-core`
- AdminGate ASGI control-plane gating
- ABAC Administrator attribute policy behavior
- Delegated Administrator tenant visibility, client exposure, and mutation authority
- PolicyEngine storage-backed decision orchestration
- RBAC Administrator role and assignment behavior
- Service identity registry behavior
- Deterministic engine, invariant, and authority graph imports re-exported from standalone 10-layer concrete packages
- Delegated administration and attenuation
- Decision logs, replay, stability, and determinism helpers
- Governance policy lifecycle, provenance, and release posture

### Public API and Import Surfaces

Import namespace: `tba_runtime_authorization_policy`.

Source-declared exports or types: `ABACAdministrator`, `ADMIN_CLIENT_FIELDS`, `AccessReviewCampaign`, `AccessReviewDecision`, `AccessReviewItem`, `AccessReviewWorkflow`, `AdminPolicy`, `AttributePolicy`, `AuthorityClosure`, `AuthorityDerivationGraph`, `AuthorityEdge`, `AuthorityGraphIntegrityReport`, `AuthorityMonotonicityReport`, `AuthorityMutationKind`, `AuthorityNode`.

Inspect [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) for exact signatures; this inventory does not designate every internal module as stable.

### Entry Points

<!-- readme-standards:begin entry-points -->
This package declares no command-line, GUI, or plugin entry points in its manifest.
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) for `tba-runtime-authorization-policy` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

### Protocol Consumers

Direct consumers in this checkout’s package manifests include `tba-operator-identity`, `tba-auth`, `tba-workspace`. These edges describe declared dependencies, not protocol-conformance evidence.

### Extensions

For `tba-runtime-authorization-policy`, use the source-declared public interfaces (`ABACAdministrator`, `ADMIN_CLIENT_FIELDS`, `AccessReviewCampaign`, `AccessReviewDecision`, `AccessReviewItem`, `AccessReviewWorkflow`, `AdminPolicy`, `AttributePolicy`, `AuthorityClosure`, `AuthorityDerivationGraph`, `AuthorityEdge`, `AuthorityGraphIntegrityReport`, `AuthorityMonotonicityReport`, `AuthorityMutationKind`, `AuthorityNode`) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

`tba-runtime-authorization-policy` exposes runtime composition and operator entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-runtime-authorization-policy`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py). The `tba-runtime-authorization-policy` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-runtime-authorization-policy` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py).

### Certification Status

No external certification is asserted for `tba-runtime-authorization-policy` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-runtime-authorization-policy` provides authorization policy, authority, grants, permissions, decisions, and governance implementation package for the TBA package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-runtime-authorization-policy`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-runtime-authorization-policy` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml) provide the supporting context for `tba-runtime-authorization-policy`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/) remains a deprecated compatibility package.
- [tba-concrete-authorization-policy-rules](https://pypi.org/project/tba-concrete-authorization-policy-rules/) owns deterministic rule implementations.
- [tba-provider-authorization-policy-decision-engine](https://pypi.org/project/tba-provider-authorization-policy-decision-engine/), [tba-durability-authorization-policy-authority-derivation-graph](https://pypi.org/project/tba-durability-authorization-policy-authority-derivation-graph/), and [tigrbl-authz-policy-invariant-registry](https://pypi.org/project/tigrbl-authz-policy-invariant-registry/) own their respective concrete implementations.
- [tba-storage-core](https://pypi.org/project/tba-storage-core/) owns durable role, tenant membership, attribute policy, policy condition, and delegated admin scope records.
- [tba-credentials](https://pypi.org/project/tba-credentials/) provides the credential facade.
- [tba-protocol-oauth-protected-resource](https://pypi.org/project/tba-protocol-oauth-protected-resource/) owns protected-resource token validation and enforcement integration.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-authorization-policy#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-authorization-policy#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [PyPI](https://pypi.org/project/tba-runtime-authorization-policy/)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [SSOT](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [Source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-authorization-policy)
- [pypi: tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/)
<!-- readme-standards:end project-links -->

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/060-runtime/tba-runtime-authorization-policy)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-authorization-policy/)

---

## Contributing

### How to Contribute

Follow the [contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md) and include a focused example or regression for changes to `tba-runtime-authorization-policy`. Keep package behavior, its documented boundary, and its tests aligned.

### Development Setup

Work from the `pkgs/060-runtime/tba-runtime-authorization-policy` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

Edit authored prose directly in this `tba-runtime-authorization-policy` README. Update source examples in `docs/readme/`, then run `readme-standards render --root . --write` from the package directory and review the diff. Required headings and generated blocks come from package-guide-v1.

---

## Governance

### Ownership and Decision Making

Changes to `tba-runtime-authorization-policy` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

This package is part of the SSOT-governed TBA package suite. New authorization implementation work should prefer this package name over `tigrbl-identity-policy`.

`tba-runtime-authorization-policy` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `060-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

### Lifecycle and Migration

The `tba-runtime-authorization-policy` source version is `0.4.0.dev4`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/LICENSE).
<!-- readme-standards:end license -->

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/060-runtime/tba-runtime-authorization-policy/NOTICE) for attribution.
<!-- readme-standards:end notices -->
