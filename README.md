# TBA · Tigrbl Auth

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="360"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml"><img alt="Workspace: 0.4.0.dev2" src="https://img.shields.io/badge/Workspace-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://pypi.org/project/tba-auth/"><img alt="PyPI version for tba-auth" src="https://img.shields.io/pypi/v/tba-auth?label=tba-auth%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-auth"><img alt="Monthly PyPI downloads for tba-auth" src="https://static.pepy.tech/badge/tba-auth/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/actions/workflows/master.yml"><img alt="Workspace CI on master" src="https://github.com/tigrbl/tigrbl_auth/actions/workflows/master.yml/badge.svg?branch=master"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: registry" src="https://img.shields.io/badge/SSOT-registry-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/CERTIFICATION_STATUS.md"><img alt="Certification: status report" src="https://img.shields.io/badge/Certification-status%20report-8250df"></a>
</p>
<!-- END TBA README HEADER -->

TBA is the Tigrbl authentication and authorization suite. Use it to serve OAuth and OpenID Connect, integrate identity and policy checks into a Tigrbl application, or install a focused protocol, provider, storage, or client package.

## Quick start

From a checkout, use [uv](https://docs.astral.sh/uv/) to inspect the baseline OAuth and OpenID Connect discovery snapshots. This runs the published TBA distribution in an isolated Python 3.12 environment and reads the snapshots in this repository.

```bash
uv run --isolated --no-project --python 3.12 --with tba-auth==0.4.0.dev2 tba-auth discovery --format json show --repo-root .
```

Expect a JSON object with `"command": "discovery.show"` and a `documents` object containing `openid-configuration.json`, `oauth-authorization-server.json`, and `jwks.json`. The baseline snapshots use an example issuer and an empty key set.

## Choose an integration

| If you want to… | Start here |
| --- | --- |
| Run a public OAuth/OIDC API | [Public backend app](pkgs/90-backend-apps/tba-app-backend-public/README.md) and the [local Compose configuration](docker/docker-compose.public-app.yml) |
| Embed identity in a Tigrbl app | [Tigrbl plugin](pkgs/60-runtime/tba-plugin-tigrbl/README.md) |
| Maintain an app using `tba_auth` imports | [Compatibility facade](pkgs/70-facade/tba-auth/README.md) |
| Try a client-side login flow | [OAuth device authorization CLI](pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md) |
| Operate a deployment | [Identity CLI](pkgs/60-runtime/tba-cli-identity/README.md) and [CLI command reference](docs/reference/CLI_SURFACE.md) |

## Architecture

Applications compose routers and runtime services over protocol packages, capabilities, providers, and storage. The runtime supplies the persistence and configuration those components need. Downstream products can use the upstream tables and bootstrap operations when provisioning realms, tenants, principals, roles, clients, sessions, and keys.

![TBA package dependency graph](docs/architecture/tba-auth-package-graph.png)

## Package catalog

Start with a representative package below or browse the [full package tree](pkgs/). Each active package has its own README. Active Python distributions and imports use `tba-*` and `tba_*`. UI packages use `@tba/*`. See the [namespace migration guide](docs/packaging/tba-namespace-migration.md) for legacy names and environment variables.

| Layer | Start here |
| --- | --- |
| 00 · Primitives | [tba-primitives-identity](pkgs/00-primitives/tba-primitives-identity/README.md) |
| 01 · Storage | [tba-storage-core](pkgs/01-storage/tba-storage-core/README.md) |
| 02 · Contracts | [tba-contracts-identity-document](pkgs/02-contracts/tba-contracts-identity-document/README.md) |
| 05 · Base classes | [tba-bases-authenticator](pkgs/05-bases/tba-bases-authenticator/README.md) |
| 10 · Concrete implementations | [tba-concrete-amr-evaluator-basic](pkgs/10-concrete/tba-concrete-amr-evaluator-basic/README.md) |
| 20 · Providers | [tba-provider-authenticator-password-local](pkgs/20-providers/tba-provider-authenticator-password-local/README.md) |
| 30 · Durable operations | [tba-durability-replay-protection](pkgs/30-storage-runtime/tba-durability-replay-protection/README.md) |
| 40 · Capabilities | [tba-capability-account-self-service](pkgs/40-capabilities/tba-capability-account-self-service/README.md) |
| 50 · Protocols | [tba-protocol-cwt](pkgs/50-protocols/tba-protocol-cwt/README.md) |
| 55 · Profiles | [tba-profile-oauth-jwt-access-token](pkgs/55-profiles/tba-profile-oauth-jwt-access-token/README.md) |
| 60 · Runtime and CLI | [tba-cli-identity](pkgs/60-runtime/tba-cli-identity/README.md) |
| 70 · Facade | [tba-auth](pkgs/70-facade/tba-auth/README.md) |
| 75 · Clients | [tba-client-policy-decision](pkgs/75-clients/tba-client-policy-decision/README.md) |
| 80 · Routers | [tba-router-oauth-protected-resource-metadata](pkgs/80-routers/tba-router-oauth-protected-resource-metadata/README.md) |
| 85 · Middleware | [tba-middleware-policy-enforcement-asgi](pkgs/85-middleware/tba-middleware-policy-enforcement-asgi/README.md) |
| 90 · Backend apps | [tba-app-backend-public](pkgs/90-backend-apps/tba-app-backend-public/README.md) |
| 100 · UI primitives | [@tba/ui-primitives](pkgs/100-uix-core/tba-ui-primitives/README.md) |
| 104 · Authenticator UIs | [@tba/ui-mfa-authenticator-assurance-console](pkgs/104-authenticator-uis/tba-ui-mfa-authenticator-assurance-console/README.md) |
| 105 · Product UIs | [@tba/ui-my-account](pkgs/105-ui/tba-ui-my-account/README.md) |
| 106 · UI prototypes | [@tba/ui-trust-center](pkgs/106-ui/tba-ui-trust-center/README.md) |
| 110 · Examples | [tba-example-oauth-device-authorization-cli](pkgs/110-examples/tba-example-oauth-device-authorization-cli/README.md) |
| 120 · Testkits | [tba-testkit-identity](pkgs/120-tests/tba-testkit-identity/README.md) |

## Release and certification evidence

The published version badge refers to the `tba-auth` facade on PyPI. The workspace version badge refers to this checkout. The certification reports describe the exact scope of validated claims. Final certification and strict independent claims remain open in the current checkpoint.

- [Current state](CURRENT_STATE.md) and [certification status](CERTIFICATION_STATUS.md)
- [Document authority and truth chain](docs/compliance/truth_chain.md)
- [Validated execution report](docs/compliance/validated_execution_report.md) and [final release gate](docs/compliance/final_release_gate_report.md)
- [Canonical reference docs](docs/reference/README.md) and [package release process](docs/packaging/monorepo-release.md)

## README maintenance

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

## Notes

- OAuth 2.1 alignment is tracked as a profile, not as a formal RFC claim.
- `keys` is the canonical certified command family; `key` is no longer part of the certified operator surface.
- public "independent" wording remains disallowed until preserved Tier 4 external peer bundles exist and promote the retained boundary.
- The authoritative executable CLI surface is `pkgs/60-runtime/tba-cli-identity/src/tba_cli_identity/cli/metadata/` plus the generated `docs/reference/CLI_SURFACE.md`.
- A current checkpoint gap review remains published at `docs/compliance/PACKAGE_REVIEW_GAP_ANALYSIS.md`.
- Supplemental supporting review/plan docs remain available at `docs/compliance/INDEPENDENT_PACKAGE_REVIEW_2026-03-27.md` and `docs/compliance/CERTIFIABLE_DELIVERY_PLAN_2026-03-27.md`; the authoritative active document is the SSOT, and the generated reports and top-level current-state docs are its current projections.
- Dependency provenance for this checkpoint is preserved in `pyproject.toml`, `pkgs/60-runtime/tba-runtime-identity/pyproject.toml`, and `uv.lock`.

## Known current blockers

- preserved Tier 4 external peer bundles are still absent and `strict_independent_claims_ready` remains `false`
- the package is still **not** truthfully certifiably fully featured or fully RFC/spec compliant because the fail-closed validated execution gates remain red
- validated clean-room runtime matrix evidence is not yet fully preserved as passing
- validated in-scope certification lane evidence is not yet fully preserved as passing
- SQLite and PostgreSQL migration portability has not yet been preserved as passing in the final validated execution report
- Tier 3 evidence has not yet been explicitly rebuilt from validated-run manifests in a fully green final gate set
- preserved execution evidence is still required for the clean-room runtime profiles listed under [Python support](#python-support)
- release bundles and attestation verification can be rebuilt from this checkpoint, but the result remains a final-release **candidate**, not a truthful final certification release

## License

Apache-2.0

## Clean-room certification matrix

Use `tox.ini` for the same profile commands locally and in CI.

Examples:

- `tox -e py310-base`
- `tox -e py311-sqlite-uvicorn`
- `tox -e py312-postgres-hypercorn`
- `tox -e py311-tigrcorn`
- `tox -e py312-devtest`
- `tox -e py311-gates`

The Tier 4 peer-execution handoff package for the full supported peer-profile set is emitted under `dist/tier4-external-handoff/`, but preserved independent external bundles are still absent in this checkpoint, so strict independent public claims remain blocked.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the prerequisites, the `uv` setup commands for a fresh clone, and one focused test to run first.

## Repository state

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

## Runtime entrypoints

- standalone gateway/application export: `tba_auth.gateway:app`
- application factory export: `tba_app_backend_public:app`
- plugin installation: `tba_auth.plugin:TbaPlugin`

## Current runtime model

The package is treated as an **ASGI 3 application package**, not as a single bundled server. Runtime-serving claims are separated into runner profiles. `Uvicorn`, `Hypercorn`, and `Tigrcorn` are declared as runner-qualified certification targets, and the `serve` operator can launch runtime **when** the selected runner profile is installed and the Tigrbl runtime stack is importable in the active environment.

## Tigrbl-only policy

This checkpoint remains intentionally aligned to Tigrbl guidance:

- prefer Tigrbl exports and Tigrbl type exports,
- use Tigrbl ops and surfaces rather than ad-hoc framework routes,
- avoid direct FastAPI or Starlette imports and dependencies in verified release scopes.

## Downstream implementation best practices

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

## Installation profiles

### Python support

- **Declared package range** — the root `pyproject.toml` declares Python `>=3.10,<3.16`. A checkout also needs an interpreter compatible with its pinned dependencies.
- **Clean-room runtime profiles** — `tox.ini` defines CPython 3.10, 3.11, and 3.12 lanes for base, `sqlite-uvicorn`, and `postgres-hypercorn`. The `tigrcorn` profile has 3.11 and 3.12 lanes.
- **Package CI** — the separate package matrix covers CPython 3.10 through 3.14 for eligible packages, subject to each package's Python metadata.
- **Certification evidence** — preserved runtime evidence is incomplete. The Tigrcorn lanes are pinned and included in the clean-room matrix, with independent validation artifacts still missing. See [CERTIFICATION_STATUS.md](CERTIFICATION_STATUS.md) and the [certification state report](docs/compliance/certification_state_report.md) for the evidence and remaining gaps.


For installation and development commands, see [CONTRIBUTING.md](CONTRIBUTING.md).
