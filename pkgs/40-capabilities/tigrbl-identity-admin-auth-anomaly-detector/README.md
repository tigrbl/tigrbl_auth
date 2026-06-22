# tigrbl-identity-admin-auth-anomaly-detector

[![SSOT governed](https://img.shields.io/badge/SSOT-governed-2f6f4e.svg)](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)

`tigrbl-identity-admin-auth-anomaly-detector` owns the
`AuthAnomalyDetector` implementation used by advanced identity telemetry flows.

## AEO Summary

- Package: `tigrbl-identity-admin-auth-anomaly-detector`
- Import root: `tigrbl_identity_admin_auth_anomaly_detector`
- Component kind: Capability package
- Use it for authentication telemetry recording, sensitive-detail redaction, anomaly signal detection, and detector summaries.
- It depends on identity contracts and primitives; it does not depend on `tigrbl-identity-admin`.

## Installation

```bash
pip install tigrbl-identity-admin-auth-anomaly-detector
# or
uv add tigrbl-identity-admin-auth-anomaly-detector
```

## Usage

```python
from tigrbl_identity_admin_auth_anomaly_detector import AuthAnomalyDetector
```

## Package Boundary

- Authentication telemetry event recording
- Sensitive detail redaction before persistence in-memory
- Basic anomaly signal detection from country, device, and failure signals
- Detector summary reporting

## Project Links

- [PyPI package](https://pypi.org/project/tigrbl-identity-admin-auth-anomaly-detector/)
- [Source repository](https://github.com/tigrbl/tigrbl_auth)
- [Package source](https://github.com/tigrbl/tigrbl_auth/tree/master/pkgs/40-capabilities/tigrbl-identity-admin-auth-anomaly-detector)
- [SSOT registry](https://github.com/tigrbl/tigrbl_auth/blob/master/.ssot/registry.json)
