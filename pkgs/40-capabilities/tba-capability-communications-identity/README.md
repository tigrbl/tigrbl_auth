# tba-capability-communications-identity

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-communications-identity/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-communications-identity/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-communications-identity%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-communications-identity/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-capability-communications-identity%3D%3D0.4.0.dev3/pkgs/40-capabilities/tba-capability-communications-identity/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities"><img alt="Layer: 40 capabilities" src="https://img.shields.io/badge/Layer-40%20capabilities-0a7f5a"></a>
<a href="https://pypi.org/project/tba-capability-communications-identity/"><img alt="PyPI version for tba-capability-communications-identity" src="https://img.shields.io/pypi/v/tba-capability-communications-identity?label=tba-capability-communications-identity%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-capability-communications-identity"><img alt="Monthly PyPI downloads for tba-capability-communications-identity" src="https://static.pepy.tech/badge/tba-capability-communications-identity/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-communications-identity/README.md"><img alt="README hits for tba-capability-communications-identity" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-communications-identity/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/40-capabilities/tba-capability-communications-identity/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Shared domain onboarding and recheck workflows.

Implement `DomainChecker` to supply a channel-specific assessment, and pass
an async audit writer such as `tba_durability_audit.operations.audit.append_audit_event_async`.
`assess_domain_onboarding` records an initial assessment, and
`recheck_domain` records a follow-up. Both require an explicit tenant UUID.
The calling application authorizes the domain operation and owns persistence
and scheduling.

```python
from tba_capability_communications_identity import recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async

result = await recheck_domain(
    domain,
    checker=channel_checker,
    audit=append_audit_event_async,
    db=db,
    tenant_id=tenant_id,
)
```

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/40-capabilities/tba-capability-communications-identity
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
