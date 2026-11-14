# tba-contracts-identity-document

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity-document/pyproject.toml"><img alt="Checkout: 0.4.0.dev2" src="https://img.shields.io/badge/Checkout-0.4.0.dev2-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity-document/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity-document/pyproject.toml"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/02-contracts"><img alt="Layer: 02 contracts" src="https://img.shields.io/badge/Layer-02%20contracts-0a7f5a"></a>
<a href="https://pypi.org/project/tba-contracts-identity-document/"><img alt="PyPI version for tba-contracts-identity-document" src="https://img.shields.io/pypi/v/tba-contracts-identity-document?label=tba-contracts-identity-document%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-contracts-identity-document"><img alt="Monthly PyPI downloads for tba-contracts-identity-document" src="https://static.pepy.tech/badge/tba-contracts-identity-document/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/02-contracts/tba-contracts-identity-document/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Pass DID documents and SPIFFE SVID representations through typed, carrier-neutral interfaces.

## Quick start

Install the version used by this example.

```bash
python -m pip install "tba-contracts-identity-document==0.4.0.dev2"
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

## When to use it

Use `IdentityDocument` at provider boundaries and the resolver, verifier, and publisher ports for dependency injection. The constructor validates required envelope fields and the document kind. Format parsing and proof verification belong to implementations of those ports.

## Verification

See the [related repository tests](https://github.com/tigrbl/tigrbl_auth/blob/master/tests/unit/test_neutral_identity_artifact_contracts.py) for the implementation scope covered by this example.

[Workspace and package catalog](https://github.com/tigrbl/tigrbl_auth#package-catalog) · [tba-primitives-identity](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/00-primitives/tba-primitives-identity#readme) · [Report an issue](https://github.com/tigrbl/tigrbl_auth/issues) · [Repository license](https://github.com/tigrbl/tigrbl_auth/blob/master/LICENSE)
