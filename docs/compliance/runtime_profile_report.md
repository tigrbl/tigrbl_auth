# Runtime Profile Report

- Generated at: `20260513T121956Z`
- Deployment profile: `baseline`
- Report mode: `validated-runs`
- Validated artifact source: `dist/validated-runs/collected-artifact-downloads.json`
- Application factory probe passed: `False`
- Ready profiles: `0`
- Missing profiles: `0`
- Invalid profiles: `3`
- Application hash invariant: `True`
- Pyproject requires-python: `>=3.10,<3.15`
- Supported Python versions: `3.10, 3.11, 3.12, 3.13, 3.14`
- Placeholder-supported runners: `0`
- Declared CI-installable runners: `3`
- Declared CI install/probe complete: `True`
- Execution probes enabled: `True`
- Surface probe passed: `False`
- Surface probe endpoints: `4`
- Serve-check passes: `0`
- Execution probe complete: `False`
- Required runtime cells: `24`
- Validated runtime cells present: `14`
- Validated runtime cells passed: `14`
- Validated runtime matrix green: `False`

## Application Probe

- App factory: `tigrbl_auth.api.app.build_app`
- Message: Validated runtime manifests are missing or failing for the base application-factory environments: base@py3.13, base@py3.14

## Surface Probe

- Executed: `True`
- Passed: `False`
- Message: Validated runtime manifests are missing or failing for the base surface-probe environments: base@py3.13, base@py3.14
- Endpoint count: `4`
- Passed endpoints: `4`
- Failed endpoints: `0`

## Runner Profiles

### Hypercorn (`hypercorn`)

- Status: `invalid`
- Installed: `False`
- Module: `hypercorn`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Validated runtime manifests are missing or failing serve-check evidence for required cells: postgres-hypercorn@py3.13, postgres-hypercorn@py3.14
- Validated matrix profile: `postgres-hypercorn`
- Expected identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12, postgres-hypercorn@py3.13, postgres-hypercorn@py3.14`
- Present identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12`
- Passed identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12`
- Missing identities: `postgres-hypercorn@py3.13, postgres-hypercorn@py3.14`
- Failed identities: ``

### Tigrcorn (`tigrcorn`)

- Status: `invalid`
- Installed: `False`
- Module: `tigrcorn`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Validated runtime manifests are missing or failing serve-check evidence for required cells: tigrcorn@py3.13, tigrcorn@py3.14
- Validated matrix profile: `tigrcorn`
- Expected identities: `tigrcorn@py3.11, tigrcorn@py3.12, tigrcorn@py3.13, tigrcorn@py3.14`
- Present identities: `tigrcorn@py3.11, tigrcorn@py3.12`
- Passed identities: `tigrcorn@py3.11, tigrcorn@py3.12`
- Missing identities: `tigrcorn@py3.13, tigrcorn@py3.14`
- Failed identities: ``

### Uvicorn (`uvicorn`)

- Status: `invalid`
- Installed: `False`
- Module: `uvicorn`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Validated runtime manifests are missing or failing serve-check evidence for required cells: sqlite-uvicorn@py3.13, sqlite-uvicorn@py3.14
- Validated matrix profile: `sqlite-uvicorn`
- Expected identities: `sqlite-uvicorn@py3.10, sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12, sqlite-uvicorn@py3.13, sqlite-uvicorn@py3.14`
- Present identities: `sqlite-uvicorn@py3.10, sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12`
- Passed identities: `sqlite-uvicorn@py3.10, sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12`
- Missing identities: `sqlite-uvicorn@py3.13, sqlite-uvicorn@py3.14`
- Failed identities: ``
