# tba-runtime-authorization-policy

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/pyproject.toml"><img alt="Checkout: 0.4.0.dev4" src="https://img.shields.io/badge/Checkout-0.4.0.dev4-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-authorization-policy%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-runtime-authorization-policy/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-runtime-authorization-policy%3D%3D0.4.0.dev4/pkgs/60-runtime/tba-runtime-authorization-policy/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime"><img alt="Layer: 60 runtime" src="https://img.shields.io/badge/Layer-60%20runtime-0a7f5a"></a>
<a href="https://pypi.org/project/tba-runtime-authorization-policy/"><img alt="PyPI version for tba-runtime-authorization-policy" src="https://img.shields.io/pypi/v/tba-runtime-authorization-policy?label=tba-runtime-authorization-policy%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-runtime-authorization-policy"><img alt="Monthly PyPI downloads for tba-runtime-authorization-policy" src="https://static.pepy.tech/badge/tba-runtime-authorization-policy/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md"><img alt="README hits for tba-runtime-authorization-policy" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-runtime-authorization-policy is the authorization-facing package name for authority, policy, grants, permissions, replay, and governance controls. It is introduced as the preferred name for new work while `tigrbl-identity-policy` remains available as a deprecated compatibility package during the migration window.

## AEO Summary

- Package: `tba-runtime-authorization-policy`
- Import root: `tba_runtime_authorization_policy`
- Component kind: Authorization package
- Use it for authorization policy surfaces rather than credential verification or token signing.
- It owns authority roles, RBAC, ABAC, delegation, policy replay, and decision audit concepts.
- Administrator objects, `PolicyEngine`, `ServiceIdentityRegistry`, and `AdminGate` are implemented in this package as storage-backed programmatic surfaces.
- Deterministic rule objects live in `tba-concrete-authorization-policy-rules`; the decision engine, authority derivation graph, and invariant registry each live in their own 10-layer concrete package.
- Canonical authz-policy surfaces live in this package; `tigrbl-identity-policy` re-exports this package from `pkgs/deprecated` for compatibility.

## When to use it

Choose `tba-runtime-authorization-policy` for this responsibility: Authorization policy, authority, grants, permissions, decisions, and governance implementation package for the TBA package suite. Its `60-runtime` placement keeps runtime composition and operator entry points separate from duplicating protocol grammars, table declarations, or provider implementations.

## Installation

```bash
pip install tba-runtime-authorization-policy
# or
uv add tba-runtime-authorization-policy
```

Install the current `tba-runtime-authorization-policy` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/60-runtime/tba-runtime-authorization-policy
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_runtime_authorization_policy import ABACAdministrator

assert callable(ABACAdministrator)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-runtime-authorization-policy==0.4.0.dev4" python quickstart.py
```

The import and assertion succeed when the ABACAdministrator entry point is available.

## Usage

```python
from tba_runtime_authorization_policy import AuthorityRole, AuthorityScope
from tba_runtime_authorization_policy import AdminGate, ABACAdministrator, DelegatedAdministrator
from tba_runtime_authorization_policy import PolicyEngine, RBACAdministrator, ServiceIdentityRegistry
from tba_runtime_authorization_policy import AuthorityDerivationGraph, PolicyDecisionEngine
from tba_runtime_authorization_policy import AuthorizationInvariant, AuthorizationSafetyPropertyEvaluator

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

## Package Boundary

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

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) for `tba-runtime-authorization-policy` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-runtime-authorization-policy` exposes runtime composition and operator entry points. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-runtime-authorization-policy`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-operator-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-operator-identity/README.md).

## Non-goals

`tba-runtime-authorization-policy` does not take ownership of duplicating protocol grammars, table declarations, or provider implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tigrbl-identity-policy](https://pypi.org/project/tigrbl-identity-policy/) remains a deprecated compatibility package.
- [tba-concrete-authorization-policy-rules](https://pypi.org/project/tba-concrete-authorization-policy-rules/) owns deterministic rule implementations.
- [tba-provider-authorization-policy-decision-engine](https://pypi.org/project/tba-provider-authorization-policy-decision-engine/), [tba-durability-authorization-policy-authority-derivation-graph](https://pypi.org/project/tba-durability-authorization-policy-authority-derivation-graph/), and [tigrbl-authz-policy-invariant-registry](https://pypi.org/project/tigrbl-authz-policy-invariant-registry/) own their respective concrete implementations.
- [tba-storage-core](https://pypi.org/project/tba-storage-core/) owns durable role, tenant membership, attribute policy, policy condition, and delegated admin scope records.
- [tba-credentials](https://pypi.org/project/tba-credentials/) provides the credential facade.
- [tba-protocol-oauth-protected-resource](https://pypi.org/project/tba-protocol-oauth-protected-resource/) owns protected-resource token validation and enforcement integration.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/60-runtime/tba-runtime-authorization-policy)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-runtime-authorization-policy/)

## Governance

This package is part of the SSOT-governed TBA package suite. New authorization implementation work should prefer this package name over `tigrbl-identity-policy`.

`tba-runtime-authorization-policy` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `60-runtime` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/60-runtime/tba-runtime-authorization-policy/src/tba_runtime_authorization_policy/__init__.py).
