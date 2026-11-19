# tba-contracts-workload-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-workload-identity%3D%3D0.4.0.dev3/pkgs/002-contracts/tba-contracts-workload-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-workload-identity%3D%3D0.4.0.dev3/pkgs/002-contracts/tba-contracts-workload-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts"><img alt="Layer: 002 contracts" src="https://img.shields.io/badge/Layer-002%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-workload-identity/"><img alt="PyPI version for tba-contracts-workload-identity" src="https://img.shields.io/pypi/v/tba-contracts-workload-identity?label=tba-contracts-workload-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-workload-identity"><img alt="Monthly PyPI downloads for tba-contracts-workload-identity" src="https://static.pepy.tech/badge/tba-contracts-workload-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md"><img alt="README hits for tba-contracts-workload-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Owns workload identifiers, selectors, SVIDs, trust bundles, and their semantic ports.

## AEO Summary

- Package: `tba-contracts-workload-identity`
- Layer: `002-contracts`
- Responsibility: Protocol-neutral workload identity, credential, trust, and delegation contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-workload-identity` for this responsibility: Protocol-neutral workload identity, credential, trust, and delegation contracts. Its `002-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-workload-identity`:

```bash
uv pip install tba-contracts-workload-identity
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-workload-identity
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_workload_identity import DelegatedWorkloadCredentialProviderPort

assert callable(DelegatedWorkloadCredentialProviderPort)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-workload-identity==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the DelegatedWorkloadCredentialProviderPort entry point is available.

## Usage

The following public-entry-point example belongs to `tba-contracts-workload-identity`. Protocol-neutral workload identity, credential, trust, and delegation contracts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_workload_identity import DelegatedWorkloadCredentialProviderPort

assert callable(DelegatedWorkloadCredentialProviderPort)
```

## Package Boundary

`tba-contracts-workload-identity` belongs to `002-contracts` and owns shared types and structural ports: Protocol-neutral workload identity, credential, trust, and delegation contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py). Public exports include `DelegatedWorkloadCredentialProviderPort`, `DelegatedWorkloadCredentialRequest`, `ResolvedWorkload`, `SpiffeId`, `SpiffeTrustBundle`, `Svid`, `SvidFormat`, `SvidProviderPort`, `SvidVerifierPort`, `TrustBundleProviderPort`, `TrustDomain`, `WorkloadCredential`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py) for `tba-contracts-workload-identity` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-workload-identity` exposes shared types and structural ports. Public operations found in its source:

- `TrustBundleProviderPort.bundle_for` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/bundles.py).
- `WorkloadReferenceResolverPort.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `WorkloadCredentialProviderPort.obtain` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `DelegatedWorkloadCredentialProviderPort.obtain_for` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `WorkloadCredentialVerifierPort.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `WorkloadTrustMaterialProviderPort.trust_material_for` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/ports.py).
- `SpiffeId.parse` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/spiffe.py).
- `SvidProviderPort.fetch_svid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/svid.py).
- `SvidVerifierPort.verify_svid` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/svid.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-contracts-workload-identity`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-workload-identity/README.md), [tba-capability-workload-credential-brokering](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/README.md), [tba-capability-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-identity/README.md), [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt-svid-credential/README.md), [tba-concrete-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-svid/README.md), [tba-concrete-wit-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wit-svid-credential/README.md), [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-x509-svid-credential/README.md), [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md).

## Non-goals

`tba-contracts-workload-identity` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-workload-identity/README.md)
- [tba-capability-workload-credential-brokering](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-credential-brokering/README.md)
- [tba-capability-workload-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-workload-identity/README.md)
- [tba-concrete-jwt-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-jwt-svid-credential/README.md)
- [tba-concrete-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-svid/README.md)
- [tba-concrete-wit-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-wit-svid-credential/README.md)
- [tba-concrete-x509-svid-credential](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-x509-svid-credential/README.md)
- [tba-contracts-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity/README.md)
- [tba-credentials](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/070-facade/tba-credentials/README.md)
- [tba-provider-spiffe-bundle](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-bundle/README.md)
- [tba-provider-spiffe-workload-api](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/020-providers/tba-provider-spiffe-workload-api/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-workload-identity)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-workload-identity/)

## Governance

`tba-contracts-workload-identity` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-workload-identity/src/tba_contracts_workload_identity/__init__.py).
