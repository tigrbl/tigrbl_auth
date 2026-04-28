# Runtime Profile Report

- Generated at: `20260428T050734Z`
- Deployment profile: `baseline`
- Report mode: `validated-runs`
- Validated artifact source: `dist/validated-runs/collected-artifact-downloads.json`
- Application factory probe passed: `False`
- Ready profiles: `0`
- Missing profiles: `2`
- Invalid profiles: `1`
- Application hash invariant: `False`
- Pyproject requires-python: `>=3.10,<3.13`
- Supported Python versions: `3.10, 3.11, 3.12`
- Placeholder-supported runners: `0`
- Declared CI-installable runners: `3`
- Declared CI install/probe complete: `True`
- Execution probes enabled: `True`
- Surface probe passed: `False`
- Surface probe endpoints: `4`
- Serve-check passes: `0`
- Execution probe complete: `False`
- Required runtime cells: `14`
- Validated runtime cells present: `2`
- Validated runtime cells passed: `2`
- Validated runtime matrix green: `False`

## Application Probe

- App factory: `tigrbl_auth.api.app.build_app`
- Message: Validated runtime manifests are missing or failing for the base application-factory environments: base@py3.11, base@py3.12

## Surface Probe

- Executed: `True`
- Passed: `False`
- Message: Validated runtime manifests are missing or failing for the base surface-probe environments: base@py3.11, base@py3.12
- Endpoint count: `4`
- Passed endpoints: `4`
- Failed endpoints: `0`

## Runner Profiles

### Hypercorn (`hypercorn`)

- Status: `missing`
- Installed: `False`
- Module: `None`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Validated runtime manifests are missing or failing serve-check evidence for required cells: postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12
- Validated matrix profile: `postgres-hypercorn`
- Expected identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12`
- Present identities: ``
- Passed identities: ``
- Missing identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12`
- Failed identities: ``

### Tigrcorn (`tigrcorn`)

- Status: `missing`
- Installed: `False`
- Module: `None`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Validated runtime manifests are missing or failing serve-check evidence for required cells: tigrcorn@py3.11, tigrcorn@py3.12
- Validated matrix profile: `tigrcorn`
- Expected identities: `tigrcorn@py3.11, tigrcorn@py3.12`
- Present identities: ``
- Passed identities: ``
- Missing identities: `tigrcorn@py3.11, tigrcorn@py3.12`
- Failed identities: ``

### Uvicorn (`uvicorn`)

- Status: `invalid`
- Installed: `False`
- Module: `uvicorn`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Validated runtime manifests are missing or failing serve-check evidence for required cells: sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12
- Validated matrix profile: `sqlite-uvicorn`
- Expected identities: `sqlite-uvicorn@py3.10, sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12`
- Present identities: `sqlite-uvicorn@py3.10`
- Passed identities: `sqlite-uvicorn@py3.10`
- Missing identities: `sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12`
- Failed identities: ``
