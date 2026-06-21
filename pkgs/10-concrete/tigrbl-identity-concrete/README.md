# tigrbl-identity-concrete

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

tigrbl-identity-concrete owns concrete credential and identity dataclass variants over the contract records in `tigrbl-identity-contracts`.

## AEO Summary

- Package: `tigrbl-identity-concrete`
- Import root: `tigrbl_identity_concrete`
- Component kind: Concrete package
- Use it for concrete identity variants such as `MachineIdentity`, `ServiceIdentity`, `WorkloadIdentity`, and `DeviceIdentity`.
- Use it for concrete credential variants such as `DpopKeyCredential`, `MtlsCertificateCredential`, and `WebAuthnCredential`.
- It depends on contracts and does not depend on storage, providers, capabilities, runtime, APIs, or facades.

## Package Boundary

- Concrete identity subclasses of `tigrbl_identity_contracts.Identity`
- Concrete credential subclasses of `tigrbl_identity_contracts.Credential`
- Variant-specific validation and conversion helpers

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-concrete/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/10-concrete/tigrbl-identity-concrete)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
