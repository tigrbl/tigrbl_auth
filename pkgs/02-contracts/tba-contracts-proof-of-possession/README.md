# tba-contracts-proof-of-possession

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-proof-of-possession%3D%3D0.4.0.dev3/pkgs/02-contracts/tba-contracts-proof-of-possession/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-proof-of-possession%3D%3D0.4.0.dev3/pkgs/02-contracts/tba-contracts-proof-of-possession/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-proof-of-possession/"><img alt="PyPI version for tba-contracts-proof-of-possession" src="https://img.shields.io/pypi/v/tba-contracts-proof-of-possession?label=tba-contracts-proof-of-possession%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-proof-of-possession"><img alt="Monthly PyPI downloads for tba-contracts-proof-of-possession" src="https://static.pepy.tech/badge/tba-contracts-proof-of-possession/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/README.md"><img alt="README hits for tba-contracts-proof-of-possession" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Protocol-neutral credential possession-proof contracts.

## AEO Summary

- Package: `tba-contracts-proof-of-possession`
- Layer: `02-contracts`
- Responsibility: Protocol-neutral credential possession-proof contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Choose `tba-contracts-proof-of-possession` for this responsibility: Protocol-neutral credential possession-proof contracts. Its `02-contracts` placement keeps shared types and structural ports separate from environment-specific service implementations or HTTP routing.

## Installation

Install the selected PyPI release of `tba-contracts-proof-of-possession`:

```bash
uv pip install tba-contracts-proof-of-possession
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/02-contracts/tba-contracts-proof-of-possession
```

## Quick start

With [uv](https://docs.astral.sh/uv/) available, save the example as `quickstart.py`. This isolated Python 3.12 command requires the selected version to be available on PyPI; Installation also documents the checkout workflow.

```python
from tba_contracts_proof_of_possession import ConfirmationKeyBinding

assert callable(ConfirmationKeyBinding)
```

```bash
uv run --isolated --no-project --python 3.12 --with "tba-contracts-proof-of-possession==0.4.0.dev3" python quickstart.py
```

The import and assertion succeed when the ConfirmationKeyBinding entry point is available.

## Usage

The following public-entry-point example belongs to `tba-contracts-proof-of-possession`. Protocol-neutral credential possession-proof contracts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_proof_of_possession import ConfirmationKeyBinding

assert callable(ConfirmationKeyBinding)
```

## Package Boundary

`tba-contracts-proof-of-possession` belongs to `02-contracts` and owns shared types and structural ports: Protocol-neutral credential possession-proof contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/__init__.py). Public exports include `ConfirmationKeyBinding`, `ConfirmationKeyResolverPort`, `CredentialPossessionPresentation`, `PossessionProof`, `PossessionProofContext`, `PossessionProofIssuerPort`, `PossessionProofVerificationRequest`, `PossessionProofVerificationResult`, `PossessionProofVerifierPort`, `ProofContextBindingEvaluatorPort`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/__init__.py) for `tba-contracts-proof-of-possession` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-proof-of-possession` exposes shared types and structural ports. Public operations found in its source:

- `PossessionProofIssuerPort.issue` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/ports.py).
- `PossessionProofVerifierPort.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/ports.py).
- `ConfirmationKeyResolverPort.resolve_confirmation_key` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/ports.py).
- `ProofContextBindingEvaluatorPort.evaluate_context` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/ports.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

No active layer-50 manifest declares a direct runtime dependency on `tba-contracts-proof-of-possession`. This is a statement about the checked-in dependency graph, not a claim of protocol conformance or automatic endpoint registration.

Other direct consumers include [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-proof-of-possession/README.md), [tba-capability-possession-proof](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-possession-proof/README.md), [tba-profile-workload-credential-cwt-svid-extension](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md), [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md), [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md).

## Non-goals

`tba-contracts-proof-of-possession` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/00-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-proof-of-possession](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/05-bases/tba-bases-proof-of-possession/README.md)
- [tba-capability-possession-proof](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-possession-proof/README.md)
- [tba-profile-workload-credential-cwt-svid-extension](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-cwt-svid-extension/README.md)
- [tba-profile-workload-credential-spiffe-wit-svid](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-credential-spiffe-wit-svid/README.md)
- [tba-profile-workload-proof-wimse-wpt](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-workload-proof-wimse-wpt/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts/tba-contracts-proof-of-possession)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-proof-of-possession/)

## Governance

`tba-contracts-proof-of-possession` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `02-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

A prior published-version quick start informed this example. A registry badge is not evidence that this checkout's selected version or example has been verified against PyPI. See the [public package entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-proof-of-possession/src/tba_contracts_proof_of_possession/__init__.py).
