# tba-workspace

<!-- readme-standards:begin branding -->
<p align="center"><a href="https://github.com/tigrbl/tigrbl_auth"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="300"></a></p>
<p align="center"><strong>tba-workspace</strong></p>
<p align="center">Workspace-only development harness for the split TBA identity package suite.</p>
<p align="center">
<a href="https://pypi.org/project/tba-workspace/"><img alt="pypi: tba-workspace unpublished" src="https://img.shields.io/static/v1?label=pypi&amp;message=tba-workspace%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml"><img alt="Source version: 0.4.0.dev2" src="https://img.shields.io/static/v1?label=Source%20version&amp;message=0.4.0.dev2&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/static/v1?label=Python&amp;message=%3E%3D3.10%2C%3C3.16&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml"><img alt="Layer: workspace" src="https://img.shields.io/static/v1?label=Layer&amp;message=workspace&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/README.md#lifecycle-and-migration"><img alt="Lifecycle: active" src="https://img.shields.io/static/v1?label=Lifecycle&amp;message=active&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/static/v1?label=License&amp;message=Apache-2.0&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/static/v1?label=Notice&amp;message=attribution&amp;color=525252"></a>
</p>
<p align="center">
<a href="https://pypi.org/project/tba-workspace/"><img alt="pypi downloads: tba-workspace: unpublished" src="https://img.shields.io/static/v1?label=pypi%20downloads&amp;message=tba-workspace%3A%20unpublished&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/README.md"><img alt="README hits: tba-workspace" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/README.md.svg?label=README%20hits"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="README standards: CI gate" src="https://img.shields.io/static/v1?label=README%20standards&amp;message=CI%20gate&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/docs/readme/test_examples.py"><img alt="Tests: example source" src="https://img.shields.io/static/v1?label=Tests&amp;message=example%20source&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/README.md#certification-status"><img alt="Certification: not certified" src="https://img.shields.io/static/v1?label=Certification&amp;message=not%20certified&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/tools/readme/POLICY.md"><img alt="Governance: repository policy" src="https://img.shields.io/static/v1?label=Governance&amp;message=repository%20policy&amp;color=525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml"><img alt="Evidence: source and CI" src="https://img.shields.io/static/v1?label=Evidence&amp;message=source%20and%20CI&amp;color=525252"></a>
</p>
<p align="center"><a href="#overview">Overview</a> · <a href="#installation">Installation</a> · <a href="#quick-start">Quick Start</a> · <a href="#usage">Usage</a> · <a href="#public-api-and-import-surfaces">API</a> · <a href="#contributing">Contributing</a> · <a href="#governance">Governance</a> · <a href="#license">License</a></p>
<!-- readme-standards:end branding -->

---

## Overview

### Summary

TBA is the Tigrbl authentication and authorization suite. Use it to serve OAuth and OpenID Connect, integrate identity and policy checks into a Tigrbl application, or install a focused protocol, provider, storage, or client package.

### Why This Package

`tba-workspace` isolates this responsibility: Workspace-only development harness for the split TBA identity package suite. Its [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) exposes the checkout commands documented in Quick Start, allowing consumers to select this package without treating adjacent packages as part of its public contract.

### When to Use

Choose `tba-workspace` when your integration needs workspace-only development harness for the split TBA identity package suite. Match the imports below to your application boundary and install its declared dependencies before using the example.

### Features

- Public source surface: the checkout commands documented in Quick Start.
- Declared responsibility: Workspace-only development harness for the split TBA identity package suite.
- Versioned package metadata and maintained checkout examples.

### Non-Goals

`tba-workspace` owns workspace-only development harness for the split TBA identity package suite. Its imports do not by themselves configure credentials, deploy a service, or certify the behavior of its consumers. Dependencies and neighboring packages retain their own documented responsibilities.

---

## Getting Started

### Prerequisites

Python `>=3.10,<3.16` is required. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) declares runtime dependencies including `tba-app-backend-wpt-verifier`, `tba-app-backend-wit-issuance`, `tba-router-wpt-verification`, `tba-provider-certificate-issuer-x509`, `tba-router-wic-ca`, `tba-router-wit-issuance`, `tba-app-backend-wic-ca`, `tba-concrete-certificate-x509`, `tba-concrete-wic`, `tba-protocol-workload-wimse-identifier`, `tba-profile-workload-credential-wimse-wic`, `tba-profile-workload-authentication-wimse-mtls`. Use the source-checkout workflow for this workspace or test harness.

### Installation

#### uv

<!-- readme-standards:begin installation.uv -->
This is a source-only workspace or test harness, not an installable distribution. From its checkout, synchronize the declared environment:

```bash
uv sync
```
<!-- readme-standards:end installation.uv -->

#### pip

<!-- readme-standards:begin installation.pip -->
This is a source-only workspace or test harness, not an installable distribution. Use the uv checkout workflow above; this installer does not install the harness itself.
<!-- readme-standards:end installation.pip -->

#### Poetry

<!-- readme-standards:begin installation.poetry -->
This is a source-only workspace or test harness, not an installable distribution. Use the uv checkout workflow above; this installer does not install the harness itself.
<!-- readme-standards:end installation.poetry -->

### Quick Start

From a checkout, use [uv](https://docs.astral.sh/uv/) to inspect the baseline OAuth and OpenID Connect discovery snapshots. This runs the published TBA distribution in an isolated Python 3.12 environment and reads the snapshots in this repository.


Expect a JSON object with `"command": "discovery.show"` and a `documents` object containing `openid-configuration.json`, `oauth-authorization-server.json`, and `jwks.json`. The baseline snapshots use an example issuer and an empty key set.

#### Example

<!-- readme-standards:begin example.quick-start -->
Source: [docs/readme/quick_start.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/readme/quick_start.sh).

```bash
uv run --isolated --no-project --python 3.12 --with tba-auth==0.4.0.dev3 tba-auth discovery --format json show --repo-root .
```
<!-- readme-standards:end example.quick-start -->

#### Expected Result

The example demonstrates the documented `tba-workspace` source boundary or workflow. Complete its required configuration first. README CI checks the maintained source’s syntax and declarations; it does not claim that external services or the application workflow were exercised.

---

## Usage

### Common Workflows

<!-- readme-standards:begin example.usage -->
Source: [docs/readme/usage.sh](https://github.com/tigrbl/tigrbl_auth/blob/master/docs/readme/usage.sh).

```bash
uv run --isolated --no-project --python 3.12 --with tba-auth==0.4.0.dev3 tba-auth discovery --format json show --repo-root .
```
<!-- readme-standards:end example.usage -->

### Configuration

Configure `tba-workspace` through the APIs in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml); its [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) describes installation requirements, not an implicit service configuration. No additional package-global configuration contract is inferred from dependencies.

### Error Handling

The inspected `tba-workspace` source does not establish a package-wide exception hierarchy. Preserve errors from its declared dependencies and validate inputs using the specific public contract in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml).

### Best Practices

Use the explicit `tba-workspace` imports documented below and keep collaborator configuration with the caller. Run the package’s relevant tests after changing the checkout commands documented in Quick Start; an import or successful installation alone does not establish its runtime guarantees.

---

## Package Boundary

### What It Owns

`tba-workspace` is located in `workspace` and owns workspace-only development harness for the split TBA identity package suite. Source-declared APIs include the checkout commands documented in Quick Start. The [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) records its direct dependency boundary.

### Public API and Import Surfaces

`tba-workspace` is a source-checkout harness. No installable Python namespace was found in the package layout; use its documented commands and test files.

### Entry Points

<!-- readme-standards:begin entry-points -->
- `console_scripts` → `tba-auth` → `tba_cli_identity.cli.main:main`
<!-- readme-standards:end entry-points -->

### Injected Dependencies

The direct installation dependencies of `tba-workspace` are `tba-app-backend-wpt-verifier`, `tba-app-backend-wit-issuance`, `tba-router-wpt-verification`, `tba-provider-certificate-issuer-x509`, `tba-router-wic-ca`, `tba-router-wit-issuance`, `tba-app-backend-wic-ca`, `tba-concrete-certificate-x509`, `tba-concrete-wic`, `tba-protocol-workload-wimse-identifier`, `tba-profile-workload-credential-wimse-wic`, `tba-profile-workload-authentication-wimse-mtls`, `tigrbl`, `tigrbl-atoms`, `tigrbl-base`. These declarations do not imply automatic provider selection. Pass collaborators through the explicit constructors or call signatures in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml).

### Protocol Consumers

No direct package-manifest dependency on `tba-workspace` was found in the audited three-repository inventory. External consumers may still use its documented imports or commands.

### Extensions

For `tba-workspace`, use the source-declared public interfaces (the checkout commands documented in Quick Start) when composing or extending behavior. Its entry-point section below is authoritative for registered plugins; no additional extension loader is inferred from the package name.

---

## Operations and Readiness

### Operational Requirements

Operate `tba-workspace` according to its actual entry points and collaborators. The dependency and Python requirements in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) are prerequisites; deployment topology, credentials, and readiness remain the responsibility of the consuming application unless explicitly documented above.

### Health and Observability

This README does not establish a standalone health endpoint for `tba-workspace`. Observe the concrete caller’s results, exceptions, and existing test reports. An application that embeds this package must define its own health and telemetry contract.

### Security and Resource Limits

Apply the input, credential, and resource constraints implemented in [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml). The `tba-workspace` README gate is a documentation check, not a security review or a substitute for the implementation’s limits and caller authorization.

### Compatibility

This source version of `tba-workspace` declares Python `>=3.10,<3.16`. Consult its dependency constraints before upgrading. Source-version and registry-version badges have separate meanings; this migration makes no additional platform or interoperability certification claim.

---

## Verification

### Tests

Run `python -m pytest docs/readme/test_examples.py` from the `tba-workspace` package directory for the maintained example source checks (Python compilation and non-Python file presence). Behavioral tests may live in the repository’s shared suites; the new README syntax test is not presented as runtime coverage for workspace-only development harness for the split TBA identity package suite.

The repository README gate also checks the required heading tree, metadata, managed fragments, and referenced files.

### Certification Status

No external certification is asserted for `tba-workspace` by this documentation migration. README conformance, example syntax, runtime tests, and protocol or security certification are distinct evidence scopes.

### Evidence

The [README standards CI](https://github.com/tigrbl/tigrbl_auth/actions/workflows/readme-standards.yml) records mechanical documentation results for its tested commit. The [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) and example sources support the package-boundary description; external runtime behavior requires its own test evidence.

---

## FAQ

### Why

**Why select this package?** `tba-workspace` provides workspace-only development harness for the split TBA identity package suite; use its own API boundary rather than assuming neighboring packages are bundled or configured automatically.

### How

**How do I start?** Install or synchronize the environment under Getting Started, follow the maintained example for `tba-workspace`, and consult [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) for the exact types and signatures involved.

### When

**When should I validate an upgrade?** Recheck `tba-workspace` whenever its source version, declared collaborators, configuration, or caller changes. Run relevant behavioral tests in addition to the README gate before promotion.

---

## Documentation and Related Packages

### More Documentation

The [repository contribution guide](https://github.com/tigrbl/tigrbl_auth/blob/master/CONTRIBUTING.md), [package source](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml), and [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml) provide the supporting context for `tba-workspace`. The [README policy](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md) defines the common document structure.

### Related Packages

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md): Dependency-light identity primitives, typed helpers, path safety, and RFC 8785 JSON canonicalization for TBA identity systems.
- [tba-storage-access-governance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-access-governance/README.md): Owned access-governance identity database tables and migrations.
- [tba-storage-attestation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-attestation/README.md): Owned attestation identity database tables and migrations.
- [tba-storage-audit](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-audit/README.md): Owned audit identity database tables and migrations.
- [tba-storage-authentication](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-authentication/README.md): Owned authentication identity database tables and migrations.
- [tba-storage-authority-graph](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-authority-graph/README.md): Owned authority-graph identity database tables and migrations.
- [tba-storage-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-authorization-policy/README.md): Owned authorization-policy identity database tables and migrations.
- [tba-storage-certificate](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-certificate/README.md): Owned certificate identity database tables and migrations.
- [tba-storage-claims](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-claims/README.md): Owned claims identity database tables and migrations.
- [tba-storage-consent](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-consent/README.md): Owned consent identity database tables and migrations.
- [tba-storage-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-core/README.md): Tigrbl and SQLAlchemy identity tables, ORM models, migrations, persistence helpers, and table-owned operations for IAM runtimes.
- [tba-storage-delegation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-delegation/README.md): Owned delegation identity database tables and migrations.
- [tba-storage-did](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-did/README.md): Owned did identity database tables and migrations.
- [tba-storage-digital-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-digital-credential/README.md): Owned digital-credential identity database tables and migrations.
- [tba-storage-federation](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/001-storage/tba-storage-federation/README.md): Owned federation identity database tables and migrations.

### Project Links

<!-- readme-standards:begin project-links -->
- [Documentation](https://github.com/tigrbl/tigrbl_auth#readme)
- [Homepage](https://github.com/tigrbl/tigrbl_auth#readme)
- [Issues](https://github.com/tigrbl/tigrbl_auth/issues)
- [Repository](https://github.com/tigrbl/tigrbl_auth)
- [Source](https://github.com/tigrbl/tigrbl_auth)
- [pypi: tba-workspace](https://pypi.org/project/tba-workspace/)
<!-- readme-standards:end project-links -->

---

## Contributing

### How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for the prerequisites, the `uv` setup commands for a fresh clone, and one focused test to run first.

### Development Setup

Work from the `.` checkout. Synchronize its declared development environment with uv, then run the relevant package tests and `python -m pytest docs/readme/test_examples.py`. The repository’s dedicated README job installs `readme-standards==0.1.1` without resolving unrelated runtime packages.

### Notes for Maintainers

**Choose an integration**

| If you want to… | Start here |
| --- | --- |
| Run a public OAuth/OIDC API | [Public backend app](pkgs/090-backend-apps/tba-app-backend-public/README.md) and the [local Compose configuration](docker/docker-compose.public-app.yml) |
| Embed identity in a Tigrbl app | [Tigrbl plugin](pkgs/060-runtime/tba-plugin-tigrbl/README.md) |
| Maintain an app using `tba_auth` imports | [Compatibility facade](pkgs/070-facade/tba-auth/README.md) |
| Try a client-side login flow | [OAuth device authorization CLI](pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md) |
| Operate a deployment | [Identity CLI](pkgs/060-runtime/tba-cli-identity/README.md) and [CLI command reference](docs/reference/CLI_SURFACE.md) |

**Architecture**

Applications compose routers and runtime services over protocol packages, capabilities, providers, and storage. The runtime supplies the persistence and configuration those components need. Downstream products can use the upstream tables and bootstrap operations when provisioning realms, tenants, principals, roles, clients, sessions, and keys.

**Package catalog**

Start with a representative package below or browse the [full package tree](pkgs/). Each active package has its own README. Active Python distributions and imports use `tba-*` and `tba_*`. UI packages use `@tba/*`. See the [namespace migration guide](docs/packaging/tba-namespace-migration.md) for legacy names and environment variables.

| Layer | Start here |
| --- | --- |
| 00 · Primitives | [tba-primitives-identity](pkgs/000-primitives/tba-primitives-identity/README.md) |
| 01 · Storage | [tba-storage-core](pkgs/001-storage/tba-storage-core/README.md) |
| 02 · Contracts | [tba-contracts-identity-document](pkgs/002-contracts/tba-contracts-identity-document/README.md) |
| 05 · Base classes | [tba-bases-authenticator](pkgs/005-bases/tba-bases-authenticator/README.md) |
| 10 · Concrete implementations | [tba-concrete-amr-evaluator-basic](pkgs/010-concrete/tba-concrete-amr-evaluator-basic/README.md) |
| 20 · Providers | [tba-provider-authenticator-password-local](pkgs/020-providers/tba-provider-authenticator-password-local/README.md) |
| 30 · Durable operations | [tba-durability-replay-protection](pkgs/030-storage-runtime/tba-durability-replay-protection/README.md) |
| 40 · Capabilities | [tba-capability-account-self-service](pkgs/040-capabilities/tba-capability-account-self-service/README.md) |
| 50 · Protocols | [tba-protocol-cwt](pkgs/050-protocols/tba-protocol-cwt/README.md) |
| 55 · Profiles | [tba-profile-oauth-jwt-access-token](pkgs/055-profiles/tba-profile-oauth-jwt-access-token/README.md) |
| 60 · Runtime and CLI | [tba-cli-identity](pkgs/060-runtime/tba-cli-identity/README.md) |
| 70 · Facade | [tba-auth](pkgs/070-facade/tba-auth/README.md) |
| 75 · Clients | [tba-client-policy-decision](pkgs/075-clients/tba-client-policy-decision/README.md) |
| 80 · Routers | [tba-router-oauth-protected-resource-metadata](pkgs/080-routers/tba-router-oauth-protected-resource-metadata/README.md) |
| 85 · Middleware | [tba-middleware-policy-enforcement-asgi](pkgs/085-middleware/tba-middleware-policy-enforcement-asgi/README.md) |
| 90 · Backend apps | [tba-app-backend-public](pkgs/090-backend-apps/tba-app-backend-public/README.md) |
| 100 · UI primitives | [@tba/ui-primitives](pkgs/100-uix-core/tba-ui-primitives/README.md) |
| 104 · Authenticator UIs | [@tba/ui-mfa-authenticator-assurance-console](pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/README.md) |
| 105 · Product UIs | [@tba/ui-my-account](pkgs/105-ui/tba-ui-my-account/README.md) |
| 106 · UI prototypes | [@tba/ui-trust-center](pkgs/106-ui/tba-ui-trust-center/README.md) |
| 110 · Examples | [tba-example-oauth-device-authorization-cli](pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md) |
| 120 · Testkits | [tba-tests-identity](pkgs/120-tests/tba-tests-identity/README.md) |

**Release and certification evidence**

The published version badge refers to the `tba-auth` facade on PyPI. The workspace version badge refers to this checkout. The certification reports describe the exact scope of validated claims. Final certification and strict independent claims remain open in the current checkpoint.

- [Current state](CURRENT_STATE.md) and [certification status](CERTIFICATION_STATUS.md)
- [Document authority and truth chain](docs/compliance/truth_chain.md)
- [Validated execution report](docs/compliance/validated_execution_report.md) and [final release gate](docs/compliance/final_release_gate_report.md)
- [Canonical reference docs](docs/reference/README.md) and [package release process](docs/packaging/monorepo-release.md)

**README maintenance**

The shared logo lives at [docs/assets/tba-brand.png](docs/assets/tba-brand.png). Package READMEs use its canonical raw URL so the same asset can render off GitHub once it is on the default branch. To update managed headers after a manifest change, run `python scripts/render_readme_branding.py` with Python 3.11 or newer. Add `--check` to detect drift. Keep the example and package guidance outside the managed block. See the [quick start verification record](docs/packaging/readme-verification.md) for checks and known build blockers.

[Documentation](docs/README.md) · [Issues](https://github.com/tigrbl/tigrbl_auth/issues) · [Apache 2.0 license](LICENSE)

This repo includes a separate sample Python package at
`pkgs/110-examples/tba-example-oauth-device-authorization-cli/`
that demonstrates how another CLI can implement a `login` command on top of
`tba_auth` device authorization. The flow uses issuer discovery plus the
canonical `POST /device_authorization` and `POST /token` endpoints.

See `docs/examples/python-cli-device-login.md`.

or embed as a plugin:

```python
from tigrbl import TigrblApp
from tba_auth.plugin import TbaPlugin

app = TigrblApp()
plugin = TbaPlugin()
plugin.install(app)
```

- OAuth 2.1 alignment is tracked as a profile, not as a formal RFC claim.
- `keys` is the canonical certified command family; `key` is no longer part of the certified operator surface.
- public "independent" wording remains disallowed until preserved Tier 4 external peer bundles exist and promote the retained boundary.
- The authoritative executable CLI surface is `pkgs/060-runtime/tba-cli-identity/src/tba_cli_identity/cli/metadata/` plus the generated `docs/reference/CLI_SURFACE.md`.
- A current checkpoint gap review remains published at `docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.md`.
- Supplemental supporting review/plan docs remain available at `docs/compliance/INDEPENDENT_PACKAGE_REVIEW_2026-03-27.md` and `docs/compliance/CERTIFIABLE_DELIVERY_PLAN_2026-03-27.md`; the authoritative active document is the SSOT, and the generated reports and top-level current-state docs are its current projections.
- Dependency provenance for this checkpoint is preserved in `pyproject.toml`, `pkgs/060-runtime/tba-runtime-identity/pyproject.toml`, and `uv.lock`.

**Known current blockers**

- preserved Tier 4 external peer bundles are still absent and `strict_independent_claims_ready` remains `false`
- the package is still **not** truthfully certifiably fully featured or fully RFC/spec compliant because the fail-closed validated execution gates remain red
- validated clean-room runtime matrix evidence is not yet fully preserved as passing
- validated in-scope certification lane evidence is not yet fully preserved as passing
- SQLite and PostgreSQL migration portability has not yet been preserved as passing in the final validated execution report
- Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests in a fully green final gate set
- preserved execution evidence is still required for the clean-room runtime profiles listed under [Python support](#python-support)
- release bundles and attestation verification can be rebuilt from this checkpoint, but the result remains a final-release **candidate**, not a truthful final certification release

**Clean-room certification matrix**

Use `tox.ini` for the same profile commands locally and in CI.

Examples:

- `tox -e py310-base`
- `tox -e py311-sqlite-uvicorn`
- `tox -e py312-postgres-hypercorn`
- `tox -e py311-tigrcorn`
- `tox -e py312-devtest`
- `tox -e py311-gates`

The Tier 4 peer-execution handoff package for the full supported peer-profile set is emitted under `dist/tier4-external-handoff/`, but preserved independent external bundles are still absent in this checkpoint, so strict independent public claims remain blocked.

**Repository state**

This checkpoint is a **Step 12 final certification aggregation checkpoint with follow-up target/profile truth reconciliation and clean-room executor / validated-evidence contract hardening** layered on top of the earlier certification-target, clean-room-matrix, published-dependency, runtime-validation, test-graph, production-grade operator-control-plane, migration-portability, fail-closed-gates, and Tier 4 peer-program work.

The current repository truth is:

- `fully_certifiable_now = false`
- `fully_rfc_compliant_now = false`
- `strict_independent_claims_ready = false`
- `profile_scope_mismatch_set_empty = true`
- `alignment_only_checkpoint_no_new_certification_evidence = false`
- `clean_room_executor_matrix_declared_complete = true`
- `validated_manifest_identity_contract_installed = true`
- the package is **not yet certifiably fully featured**
- the package is **not yet certifiably fully RFC/spec compliant**

Final package-level certification is still blocked because the fail-closed validated execution gates remain incomplete for the clean-room runtime matrix, in-scope certification lanes, migration portability preservation, Tier 3 evidence rebuilt from validated runs, and preserved Tier 4 external peer bundles.

This update keeps the retained target/profile mismatch set empty for **RFC 7516**, **RFC 7592**, and **RFC 9207**, and it also hardens the preserved evidence model so runtime, test-lane, and migration manifests only count as passing when they carry identity, install-substrate linkage, environment identity, and the expected runtime / pytest / revision-aware backend artifacts.

Start with:

- `.ssot/specs/SPEC-1052-ssot-document-authority.yaml`
- `.ssot/registry.json`
- `docs/compliance/truth_chain.md`
- `docs/compliance/AUTHORITATIVE_CURRENT_DOCS.md`
- `CURRENT_STATE.md`
- `CERTIFICATION_STATUS.md`
- `docs/compliance/current_state_report.md`
- `docs/compliance/certification_state_report.md`
- `docs/compliance/release_gate_report.md`
- `docs/compliance/runtime_profile_report.md`
- `docs/compliance/validated_execution_report.md`
- `docs/compliance/PEER_MATRIX_REPORT.md`
- `docs/compliance/TIER4_PROMOTION_MATRIX.md`
- `docs/compliance/RELEASE_DECISION_RECORD.md`

Historical planning and scaffold-layout documents are retained under `docs/archive/` and are **non-authoritative** for the current repository state.

**Runtime entrypoints**

- standalone gateway/application export: `tba_auth.gateway:app`
- application factory export: `tba_app_backend_public:app`
- plugin installation: `tba_auth.plugin:TbaPlugin`

**Current runtime model**

The package is treated as an **ASGI 3 application package**, not as a single bundled server. Runtime-serving claims are separated into runner profiles. `Uvicorn`, `Hypercorn`, and `Tigrcorn` are declared as runner-qualified certification targets, and the `serve` operator can launch runtime **when** the selected runner profile is installed and the Tigrbl runtime stack is importable in the active environment.

**Tigrbl-only policy**

This checkpoint remains intentionally aligned to Tigrbl guidance:

- prefer Tigrbl exports and Tigrbl type exports,
- use Tigrbl ops and surfaces rather than ad-hoc framework routes,
- avoid direct FastAPI or Starlette imports and dependencies in verified release scopes.

**Downstream implementation best practices**

Downstream products should treat `tba_auth` as the owner of the identity
schema and product surfaces. A downstream authn/authz platform should compose
the app, plugin, split identity/authn/authz/protocol packages, and API/UIX front doors rather than
creating parallel tables for realms, tenants, principals, roles, sessions,
clients, tokens, or keys.

Use these boundaries:

- Schema and default rows belong in upstream TBA table packages. Tables
  such as `Realm` and `Tenant` use Tigrbl's `Bootstrappable` contract with
  `DEFAULT_ROWS`; the default superuser is created by the upstream admin
  bootstrap service.
- Downstream repositories may declare product-specific seed intent, but they
  should materialize it through upstream Tigrbl table/bootstrap abstractions or
  API/front-door operations. They should not introduce duplicate SQLAlchemy
  declarative bases or shadow identity tables.
- Runtime serving should select an explicit runner profile. For Tigrcorn-first
  deployments, install the `tigrcorn` extra and launch with
  `tba-auth serve --server tigrcorn` or the `tigrcorn` CLI against the
  downstream ASGI app.
- Keep provenance order: backend capability first, API front door second, UIX
  third. The platform-admin path is `tba-runtime-identity-administration` ->
  `tba-app-backend-platform-administration` -> `@tba/ui-platform-administration`; apply
  the same pattern to tenant-admin, developer, service-admin, public,
  my-account, and resource-validation surfaces.

**Python support**

- **Declared package range** — the root `pyproject.toml` declares Python `>=3.10,<3.16`. A checkout also needs an interpreter compatible with its pinned dependencies.
- **Clean-room runtime profiles** — `tox.ini` defines CPython 3.10, 3.11, and 3.12 lanes for base, `sqlite-uvicorn`, and `postgres-hypercorn`. The `tigrcorn` profile has 3.11 and 3.12 lanes.
- **Package CI** — the separate package matrix covers CPython 3.10 through 3.14 for eligible packages, subject to each package's Python metadata.
- **Certification evidence** — preserved runtime evidence is incomplete. The Tigrcorn lanes are pinned and included in the clean-room matrix, with independent validation artifacts still missing. See [CERTIFICATION_STATUS.md](CERTIFICATION_STATUS.md) and the [certification state report](docs/compliance/certification_state_report.md) for the evidence and remaining gaps.


For installation and development commands, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Governance

### Ownership and Decision Making

Changes to `tba-workspace` follow the maintainer review process of [tigrbl/tigrbl_auth](https://github.com/tigrbl/tigrbl_auth) and its contribution guide. Author attribution remains in the [manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml); this README does not assign new publishing or administrative authority.

### Standards and Policies

`tba-workspace` follows the versioned [package-guide-v1 outline](https://github.com/groupsum/readme-standards/blob/master/docs/outline.md). All fixed headings, hierarchy, order, separators, and package-specific branding are checked by CI; reviewers assess the accuracy and usefulness of authored claims.

### Lifecycle and Migration

The `tba-workspace` source version is `0.4.0.dev2`. This change standardizes documentation and adds a development-only gate; it does not publish a new runtime version or declare a previously unpublished package released. Preserve explicit deprecation and replacement instructions where present.

---

## License and Attribution

### License

<!-- readme-standards:begin license -->
Licensed under `Apache-2.0`. See [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE).
<!-- readme-standards:end license -->

Apache-2.0

### Notices

<!-- readme-standards:begin notices -->
See [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/NOTICE) for attribution.
<!-- readme-standards:end notices -->
