# tba-protocol-oauth-protected-resource

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oauth-protected-resource%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-oauth-protected-resource/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-protocol-oauth-protected-resource%3D%3D0.4.0.dev3/pkgs/050-protocols/tba-protocol-oauth-protected-resource/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols"><img alt="Layer: 050 protocols" src="https://img.shields.io/badge/Layer-050%20protocols-0a7f5a"></a>
<a href="https://pypi.org/project/tba-protocol-oauth-protected-resource/"><img alt="PyPI version for tba-protocol-oauth-protected-resource" src="https://img.shields.io/pypi/v/tba-protocol-oauth-protected-resource?label=tba-protocol-oauth-protected-resource%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-protocol-oauth-protected-resource"><img alt="Monthly PyPI downloads for tba-protocol-oauth-protected-resource" src="https://static.pepy.tech/badge/tba-protocol-oauth-protected-resource/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md"><img alt="README hits for tba-protocol-oauth-protected-resource" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

tba-protocol-oauth-protected-resource owns versioned OAuth protected-resource
protocol composition: claim sets, compatibility rules, metadata, sender
constraints, and verifier integration. It composes standalone validation
providers rather than acting as a compatibility facade. The legacy
`tigrbl-identity-resource-server` package remains unchanged under `deprecated`.

## AEO Summary

- Package: `tba-protocol-oauth-protected-resource`
- Import root: `tba_protocol_oauth_protected_resource`
- Component kind: Versioned OAuth protected-resource protocol composition
- Use it for protected API validation of issuer, audience, scopes, permissions, and proof bindings.
- Do not use it to own credential proof, identity records, or OAuth/OIDC provider truth.
- Canonical protected-resource exports live in this package. The verifier and reusable sender-constraint, JWKS, introspection, mTLS, and DPoP helpers are supplied by standalone layer-20 providers. Legacy packages under `pkgs/deprecated` retain their original names and imports.

## When to use it

Choose `tba-protocol-oauth-protected-resource` for this responsibility: OAuth protected-resource facade over token, DPoP, mTLS, and policy validators for the TBA package suite. Its `050-protocols` placement keeps protocol semantics and projections separate from deployment hosting or ownership of persistence implementations.

## Installation

```bash
pip install tba-protocol-oauth-protected-resource
# or
uv add tba-protocol-oauth-protected-resource
```

Install the current `tba-protocol-oauth-protected-resource` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/050-protocols/tba-protocol-oauth-protected-resource
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_protocol_oauth_protected_resource import capability_report

report = capability_report()
assert report
print(sorted(report))
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-protocol-oauth-protected-resource==0.4.0.dev3" python quickstart.py
```

The command prints the keys in the package's capability report.

## Usage

```python
from tba_protocol_oauth_protected_resource import AccessTokenClaims, ResourceRequirement, ResourceServerVerifier

requirement = ResourceRequirement(audience="api://billing", scopes=("invoice.read",))
claims = AccessTokenClaims(
    iss="https://issuer.example.test",
    sub="user:1",
    aud=("api://billing",),
    exp=1_800_000_300,
    iat=1_800_000_000,
    scope=("invoice.read",),
)
result = ResourceServerVerifier().verify_token(claims, requirement)
```

## Package Boundary

- Protected API token validation
- `versions.py` owns the implementation-profile history while
  `SPECIFICATION_VERSIONS` records the independently versioned RFCs composed by
  the profile.
- `features.py`, `compatibility.py`, and `migrations.py` own profile selection,
  feature reporting, and the legacy-unversioned metadata migration path.
- `claims.py`, `schemas.py`, `bindings.py`, and `errors.py` own protocol mapping;
  standalone claim classes and verifier implementations remain in lower layers.
- `capability.py` composes the layer-20 verifier into the reportable
  `protected-resource.authorization` layer-40 capability.
- Runtime capability truth and certification attestations are owned by
  `tba-certification-release.runtime_metadata` in layer 60; they are
  not protocol behavior.
- `contracts.py` is a compatibility export for the canonical OAuth
  verifier-contract mapping and does not resolve runtime deployments.
- Resource, audience, scope, permission, DPoP, mTLS, and introspection orchestration
- Resource-server framework adapters and verifier contracts
- Enforcement integration with authorization policy inputs

## Injected dependencies

Explicit construction inputs and collaborators for `tba-protocol-oauth-protected-resource`:

- `migrate_verifier_metadata` construction inputs: `source`, `target`. [Definition](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/migrations.py).

Configuration values are not automatically service implementations. Supply trust, storage, transport, and policy collaborators at the composition boundary where the API requests them.

## Operations and readiness

`tba-protocol-oauth-protected-resource` exposes protocol semantics and projections. Public operations found in its source:

- `capability_report` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py).
- `build_protected_resource_authorization_capability` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/capability.py).
- `compose_access_token_claim_set` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/claims.py).
- `compatibility` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/compatibility.py).
- `supports` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/features.py).
- `verifier_contract_from_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/metadata.py).
- `migrate_verifier_metadata` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/migrations.py).
- `select_version` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/versions.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-protocol-oauth-protected-resource`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-auth/README.md).

## Non-goals

`tba-protocol-oauth-protected-resource` does not take ownership of deployment hosting or ownership of persistence implementations.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tigrbl-identity-resource-server](https://pypi.org/project/tigrbl-identity-resource-server/) remains a deprecated compatibility package.
- [tba-runtime-authorization-policy](https://pypi.org/project/tba-runtime-authorization-policy/) owns policy decision truth.
- [tba-protocol-oauth](https://pypi.org/project/tba-protocol-oauth/) owns OAuth wire behavior.
- [tba-provider-authorization-resource-server-verifier](https://pypi.org/project/tba-provider-authorization-resource-server-verifier/) owns the reusable protected-resource verifier.
- [tba-provider-security-token-jwks-cache](https://pypi.org/project/tba-provider-security-token-jwks-cache/) and [tba-provider-token-introspection](https://pypi.org/project/tba-provider-token-introspection/) own token lookup helpers.
- [tba-provider-security-dpop-cnf-binding-validator](https://pypi.org/project/tba-provider-security-dpop-cnf-binding-validator/), [tba-provider-security-mtls-cnf-binding-validator](https://pypi.org/project/tba-provider-security-mtls-cnf-binding-validator/) provide the concrete confirmation-binding validators; the protected-resource authorization capability composes them.
- [tba-provider-security-proof-dpop](https://pypi.org/project/tba-provider-security-proof-dpop/) owns lower DPoP proof binding comparison.
- [tba-provider-security-certificate-mtls](https://pypi.org/project/tba-provider-security-certificate-mtls/) owns lower certificate binding comparison.

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-protocol-oauth-protected-resource/)

## Governance

This package is part of the SSOT-governed TBA package suite. New protected-resource implementation work should prefer this package name over `tigrbl-identity-resource-server`.

`tba-protocol-oauth-protected-resource` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `050-protocols` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-oauth-protected-resource/src/tba_protocol_oauth_protected_resource/__init__.py).
