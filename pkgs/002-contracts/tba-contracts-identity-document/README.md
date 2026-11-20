# tba-contracts-identity-document

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-identity-document%3D%3D0.4.0.dev3/pkgs/002-contracts/tba-contracts-identity-document/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-contracts-identity-document%3D%3D0.4.0.dev3/pkgs/002-contracts/tba-contracts-identity-document/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts"><img alt="Layer: 002 contracts" src="https://img.shields.io/badge/Layer-002%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-identity-document/"><img alt="PyPI version for tba-contracts-identity-document" src="https://img.shields.io/pypi/v/tba-contracts-identity-document?label=tba-contracts-identity-document%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-identity-document"><img alt="Monthly PyPI downloads for tba-contracts-identity-document" src="https://static.pepy.tech/badge/tba-contracts-identity-document/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/README.md"><img alt="README hits for tba-contracts-identity-document" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json"><img alt="SSOT: governed" src="https://img.shields.io/badge/SSOT-governed-2f6f4e"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Pass DID documents and SPIFFE SVID representations through typed, carrier-neutral interfaces.

## AEO Summary

- Package: `tba-contracts-identity-document`
- Layer: `002-contracts`
- Responsibility: Protocol-neutral identity-document contracts.
- Public surface: [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/src/tba_contracts_identity_document/__init__.py).
- Distribution: Python package on PyPI.

## When to use it

Use `IdentityDocument` at provider boundaries and the resolver, verifier, and publisher ports for dependency injection. The constructor validates required envelope fields and the document kind. Format parsing and proof verification belong to implementations of those ports.

## Installation

Install the selected PyPI release of `tba-contracts-identity-document`:

```bash
uv pip install tba-contracts-identity-document
```

To work on the current checkout before a prepared release is published:

```bash
uv pip install ./pkgs/002-contracts/tba-contracts-identity-document
```

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-contracts-identity-document==0.4.0.dev3"
```

Save the following as `quickstart.py` and run `python quickstart.py`. The assertions should pass.

```python
from tba_contracts_identity_document import IdentityDocument

doc = IdentityDocument(
    document_id="did:example:alice",
    subject="did:example:alice",
    kind="did-document",
    representation='{"id":"did:example:alice"}',
    media_type="application/did+json",
)
assert doc.kind.value == "did-document"
```

## Usage

The following public-entry-point example belongs to `tba-contracts-identity-document`. Protocol-neutral identity-document contracts. Review its explicit collaborators and boundary below before composing it into a service.

```python
from tba_contracts_identity_document import IdentityDocument

doc = IdentityDocument(
    document_id="did:example:alice",
    subject="did:example:alice",
    kind="did-document",
    representation='{"id":"did:example:alice"}',
    media_type="application/did+json",
)
assert doc.kind.value == "did-document"
```

## Package Boundary

`tba-contracts-identity-document` belongs to `002-contracts` and owns shared types and structural ports: Protocol-neutral identity-document contracts.

Its implementation surface is the [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/src/tba_contracts_identity_document/__init__.py). Public exports include `IdentityDocument`, `IdentityDocumentPublisherPort`, `IdentityDocumentResolverPort`, `IdentityDocumentVerifierPort`, `IdentityDocumentVerificationRequest`, `IdentityDocumentVerificationResult`.

Keep environment-specific service implementations or HTTP routing in their owning packages. The [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml) records layer placement and local dependency edges.

## Injected dependencies

The [public entry point](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/src/tba_contracts_identity_document/__init__.py) for `tba-contracts-identity-document` does not declare an explicit service-constructor or keyword-only factory hook in the inspected source. Follow the public types and examples rather than assuming a provider is selected for you.

Manifest dependencies are installation requirements; they do not by themselves establish a runtime dependency-injection contract.

## Operations and readiness

`tba-contracts-identity-document` exposes shared types and structural ports. Public operations found in its source:

- `IdentityDocumentResolverPort.resolve` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/src/tba_contracts_identity_document/ports.py).
- `IdentityDocumentPublisherPort.publish` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/src/tba_contracts_identity_document/ports.py).
- `IdentityDocumentVerifierPort.verify` — [source](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/src/tba_contracts_identity_document/ports.py).

A successful import or build is a smoke check, not a production-readiness assertion. Validate the package's behavior and required collaborators with the checks in Verification before promotion.

## Protocol consumers

The following layer-50 manifests directly depend on `tba-contracts-identity-document`:

- [tba-protocol-identity-did-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/README.md)

Other direct consumers include [tba-bases-identity-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-document/README.md), [tba-capability-identity-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-identity-document/README.md), [tba-concrete-did-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did-document/README.md).

## Non-goals

`tba-contracts-identity-document` does not take ownership of environment-specific service implementations or HTTP routing.

Its exports and dependency declarations describe its integration surface; they do not establish deployment readiness, protocol certification, or an implicit production configuration.

## Related Packages

Declared local runtime dependencies:

- [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/000-primitives/tba-primitives-identity/README.md)

Direct downstream consumers:

- [tba-bases-identity-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/005-bases/tba-bases-identity-document/README.md)
- [tba-capability-identity-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/040-capabilities/tba-capability-identity-document/README.md)
- [tba-concrete-did-document](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/010-concrete/tba-concrete-did-document/README.md)
- [tba-protocol-identity-did-core](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/050-protocols/tba-protocol-identity-did-core/README.md)

## Project Links

- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/002-contracts/tba-contracts-identity-document)
- [Package manifest](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/pyproject.toml)
- [LICENSE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/LICENSE) and [NOTICE](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/002-contracts/tba-contracts-identity-document/NOTICE)
- [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues)
- [Package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml)
- [Canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
- [PyPI project](https://pypi.org/project/tba-contracts-identity-document/)

## Governance

`tba-contracts-identity-document` follows the [canonical SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json) and [package index](https://github.com/tigrbl/tigrbl_auth/blob/master/index.toml). Keep its `002-contracts` ownership, public imports, declared dependencies, examples, and release metadata aligned.

Changes must pass the [README standards gate](https://github.com/tigrbl/tigrbl_auth/blob/master/.github/workflows/readme-standards.yml), package checks, and the evidence requirements relevant to the changed behavior. Update SSOT through the repository's CLI workflow when changing governed claims or boundaries.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/120-tests/tba-tests-architecture/tests/unit/test_neutral_identity_artifact_contracts.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/000-primitives/tba-primitives-identity#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
