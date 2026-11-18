# tba-contracts-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-identity%3D%3D0.4.0.dev3/pkgs/02-contracts/tba-contracts-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-identity%3D%3D0.4.0.dev3/pkgs/02-contracts/tba-contracts-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-identity/"><img alt="PyPI version for tba-contracts-identity" src="https://img.shields.io/pypi/v/tba-contracts-identity?label=tba-contracts-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-identity"><img alt="Monthly PyPI downloads for tba-contracts-identity" src="https://static.pepy.tech/badge/tba-contracts-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md"><img alt="README hits for tba-contracts-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

`tba-contracts-identity` contains dependency-light identity contract types:
abstract protocols, dataclasses, enums, projection metadata,
and declarative plane access/capability metadata.

## AEO Summary

- Package: `tba-contracts-identity`
- Import root: `tba_contracts_identity`
- Component kind: Identity contract package
- Use it for reusable identity/authn/authz/admin contract types.
- Use plane access/capability declarations as metadata over APIs and
  deployments, not as separate schema families.
- Table-backed REST schemas are owned by `tba-storage-core` table modules
  through Tigrbl table schema context and `F`, `IO`, and `S` inference.
- Release and security-trust contracts remain in their dedicated contract
  packages.

## When to use it

Choose `tba-contracts-identity` for this responsibility: Dependency-light identity contract dataclasses, enums, protocols, and plane access metadata. Its `02-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

```bash
pip install tba-contracts-identity
# or
uv add tba-contracts-identity
```

Install the current `tba-contracts-identity` source checkout when working ahead of a PyPI release:

```bash
uv pip install ./pkgs/02-contracts/tba-contracts-identity
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_identity import ContractProjection

assert callable(ContractProjection)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-identity==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ContractProjection entry point is available.

## Usage

```python
from tba_contracts_identity import (
    ContractProjection,
    PlaneAccess,
    PlaneAccessDeclaration,
    PlaneCapability,
)

projection = ContractProjection(
    kind="openapi",
    profile="production",
    version="0.4.0",
    document={"openapi": "3.1.0", "paths": {}},
)

surface_access = PlaneAccessDeclaration(
    surface="tenant-admin",
    access=PlaneAccess.TENANT_ADMIN,
    capabilities=(PlaneCapability.MANAGE_PRINCIPALS,),
    default_audience="tba-auth-admin",
)
```

## Package Boundary

- Identity, credential, authorization, admin-resource, and resource-verifier
  contract dataclasses/enums/protocols
- Plane access/capability metadata declarations
- OpenAPI projection metadata
- Dependency-light contract objects
- No Pydantic request/response schemas
- No table-backed REST schema aliases
- No remote procedure call surface
- No release-posture or security-trust contract ownership

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) for `tba-contracts-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-identity` exposes shared types and structural ports. Inspect the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py) for the exported types and composition surface.

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-contracts-identity`:

- [tba-protocol-attestation-corim](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-attestation-corim/README.md)
- [tba-protocol-attestation-eat](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-attestation-eat/README.md)
- [tba-protocol-authzen](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-authzen/README.md)
- [tba-protocol-credential-iso-mdoc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-credential-iso-mdoc/README.md)
- [tba-protocol-cwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-cwt/README.md)
- [tba-protocol-gnap](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-gnap/README.md)
- [tba-protocol-jwt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-jwt/README.md)
- [tba-protocol-oauth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth/README.md)
- [tba-protocol-oauth-protected-resource](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oauth-protected-resource/README.md)
- [tba-protocol-oid4vci](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oid4vci/README.md)
- [tba-protocol-oid4vp](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oid4vp/README.md)
- [tba-protocol-oidc](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc/README.md)
- [tba-protocol-oidc-relying-party](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-oidc-relying-party/README.md)
- [tba-protocol-security-event-set](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-event-set/README.md)
- [tba-protocol-security-jose](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-security-jose/README.md)
- [tba-protocol-webauthn](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/50-protocols/tba-protocol-webauthn/README.md)

Other direct consumers include [tba-app-backend-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-core/README.md), [tba-app-backend-my-account](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-my-account/README.md), [tba-app-backend-platform-administration](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/90-backend-apps/tba-app-backend-platform-administration/README.md), [tba-auth](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/70-facade/tba-auth/README.md), [tba-bases-authentication-assurance](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authentication-assurance/README.md), [tba-bases-authentication-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authentication-credential/README.md), [tba-bases-authenticator](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authenticator/README.md), [tba-bases-authorization-policy](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-authorization-policy/README.md).

## Non-goals

`tba-contracts-identity` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

- [tba-primitives-identity](https://pypi.org/project/tba-primitives-identity/)
- [tba-storage-core](https://pypi.org/project/tba-storage-core/)
- [tba-contracts-security-trust](https://pypi.org/project/tba-contracts-security-trust/)

## Project Links

- [PyPI package](https://pypi.org/project/tba-contracts-identity/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-identity)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-identity/)

## Governance

This package is part of the SSOT-governed TBA identity package suite. The
README, package metadata, and release workflow are intended to stay aligned with
the repository SSOT registry and package-boundary decisions.

`tba-contracts-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `02-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity/src/tba_contracts_identity/__init__.py).
