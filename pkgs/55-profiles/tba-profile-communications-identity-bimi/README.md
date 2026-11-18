# tba-profile-communications-identity-bimi

<!-- BEGIN TBA README HEADER -->
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth#readme"><img src="https://raw.githubusercontent.com/tigrbl/tigrbl_auth/master/docs/assets/tba-brand.png" alt="TBA · Tigrbl Auth" width="240"></a>
</p>
<p align="center">
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/pyproject.toml"><img alt="Checkout: 0.4.0.dev3" src="https://img.shields.io/badge/Checkout-0.4.0.dev3-1f6feb"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/pyproject.toml"><img alt="Python: &gt;=3.10,&lt;3.16" src="https://img.shields.io/badge/Python-%3E%3D3.10%2C%3C3.16-3776ab"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-communications-identity-bimi%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-communications-identity-bimi/LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/tba-profile-communications-identity-bimi%3D%3D0.4.0.dev3/pkgs/55-profiles/tba-profile-communications-identity-bimi/NOTICE"><img alt="Notice: attribution" src="https://img.shields.io/badge/Notice-attribution-525252"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/55-profiles"><img alt="Layer: 55 profiles" src="https://img.shields.io/badge/Layer-55%20profiles-0a7f5a"></a>
<a href="https://pypi.org/project/tba-profile-communications-identity-bimi/"><img alt="PyPI version for tba-profile-communications-identity-bimi" src="https://img.shields.io/pypi/v/tba-profile-communications-identity-bimi?label=tba-profile-communications-identity-bimi%20PyPI"></a>
</p>
<p align="center">
<a href="https://pepy.tech/project/tba-profile-communications-identity-bimi"><img alt="Monthly PyPI downloads for tba-profile-communications-identity-bimi" src="https://static.pepy.tech/badge/tba-profile-communications-identity-bimi/month"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/README.md"><img alt="README hits for tba-profile-communications-identity-bimi" src="https://hits.sh/github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/README.md.svg?label=hits"></a>
<a href="https://github.com/tigrbl/tigrbl_auth/blob/master/pkgs/55-profiles/tba-profile-communications-identity-bimi/README.md#verification"><img alt="Evidence: verification" src="https://img.shields.io/badge/Evidence-verification-8250df"></a>
</p>
<!-- END TBA README HEADER -->

Optional BIMI Mark Certificate and DNS readiness profile.

Install from the TBA workspace with `uv sync --extra bimi`.

- `check_readiness` inspects the selected BIMI TXT record and the sender and
  organizational domains' DMARC enforcement. It returns separate DNS and DMARC
  findings, the assertion owner after any fallback, and the published asset
  URLs. `ready` describes DNS/DMARC preflight for a mark-backed deployment.
- `verify_certificate` takes a leaf-first PEM bundle and the assertion owner.
  It checks the certificate policy, classifies CMC/VMC from the signed mark
  type, matches the assertion domain or selector-qualified SAN, and checks the
  embedded compressed logotype and its digest. The injected validator checks
  the certificate path, revocation evidence, and CT evidence.

The readiness policy uses bounded RFC 9989 discovery by default and accepts a
known organizational domain for deployments that need to reproduce a specific
boundary. It checks the legacy `pct` tag and the current `t` testing tag.
The lookup is domain-level and does not process message-local selectors or
SPF/DKIM alignment. The embedded-logo check covers format markers and basic
safety checks. Full SVG schema validation, remote asset retrieval, and mailbox
display are separate checks.

## Run the example

`scripts/bimi_check.py` composes the profile with the live TXT resolver or
with TBA's existing `ProfiledTrustAnchorProvider` and the Mark Certificate
backend. Use the `assertion.name` returned by the DNS check for the certificate
check. Pass locally obtained evidence and trust material.

```console
uv run --extra bimi python scripts/bimi_check.py dns news.example.com --selector default
uv run --extra bimi python scripts/bimi_check.py verify default._bimi.example.com mark-chain.pem --root mva-root.pem --ct-log ct-log.pem --crl http://ca.example/leaf.crl=leaf.crl --crl http://ca.example/issuer.crl=issuer.crl
```

In a TBA tenant-admin application, authorize the caller for the sending domain
first. The workspace `bimi` extra includes the optional `workflow` adapter.
It composes the profile with the shared communications identity assessment
and TBA's existing durable audit writer. The evidence callback can look up a
local bundle keyed by the discovered assertion owner.

```python
from tba_capability_communications_identity import assess_domain_onboarding, recheck_domain
from tba_durability_audit.operations.audit import append_audit_event_async
from tba_profile_communications_identity_bimi import BimiProfile
from tba_profile_communications_identity_bimi.capability_adapter import BimiDomainChecker
from tba_provider_dns_txt import DnsTxtResolver

bimi = BimiProfile(dns=DnsTxtResolver(), validator=validator)
checker = BimiDomainChecker(bimi, evidence=lambda assertion: bundles.get(assertion.name))
initial = await assess_domain_onboarding(
    sending_domain, checker=checker, audit=append_audit_event_async,
    db=db, tenant_id=tenant_id,
)
latest = await recheck_domain(
    sending_domain, checker=checker, audit=append_audit_event_async,
    db=db, tenant_id=tenant_id,
)
```

References include the [BIMI draft](https://datatracker.ietf.org/doc/html/draft-brand-indicators-for-message-identification-15),
the [Mark Certificate verification draft](https://datatracker.ietf.org/doc/html/draft-fetch-validation-vmc-wchuang-12),
the [v1.8 Mark Certificate requirements](https://bimigroup.org/resources/VMC_Requirements_latest.pdf),
and [DMARC RFC 9989](https://www.rfc-editor.org/rfc/rfc9989.html).

## Quick start

Build the package from the repository root.

```bash
uv build --wheel pkgs/55-profiles/tba-profile-communications-identity-bimi
```

## Verification

Check that the build produces a wheel with the package version declared in `pyproject.toml`.
