# Runtime Profile Report

- Generated at: `20260407T091615Z`
- Deployment profile: `baseline`
- Report mode: `validated-runs`
- Validated artifact source: `dist\validated-runs\collected-artifact-downloads.json`
- Application factory probe passed: `True`
- Ready profiles: `3`
- Missing profiles: `0`
- Invalid profiles: `0`
- Application hash invariant: `True`
- Pyproject requires-python: `>=3.10,<3.13`
- Supported Python versions: `3.10, 3.11, 3.12`
- Placeholder-supported runners: `0`
- Declared CI-installable runners: `3`
- Declared CI install/probe complete: `True`
- Execution probes enabled: `True`
- Surface probe passed: `True`
- Surface probe endpoints: `3`
- Serve-check passes: `3`
- Execution probe complete: `True`
- Required runtime cells: `14`
- Validated runtime cells present: `14`
- Validated runtime cells passed: `14`
- Validated runtime matrix green: `True`

## Application Probe

- App factory: `tigrbl_auth.api.app.build_app`
- Message: Validated runtime manifests confirm application-factory materialization for 3/3 base environments.

## Surface Probe

- Executed: `True`
- Passed: `True`
- Message: Validated runtime manifests confirm surface probes for 3/3 base environments.
- Endpoint count: `3`
- Passed endpoints: `3`
- Failed endpoints: `0`

## Runner Profiles

### Hypercorn (`hypercorn`)

- Status: `ready`
- Installed: `True`
- Module: `None`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `True`
- Serve check message: Validated manifests confirm serve-check success for 3/3 required cells.
- Validated matrix profile: `postgres-hypercorn`
- Expected identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12`
- Present identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12`
- Passed identities: `postgres-hypercorn@py3.10, postgres-hypercorn@py3.11, postgres-hypercorn@py3.12`
- Missing identities: ``
- Failed identities: ``

### Tigrcorn (`tigrcorn`)

- Status: `ready`
- Installed: `True`
- Module: `None`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `True`
- Serve check message: Validated manifests confirm serve-check success for 2/2 required cells.
- Validated matrix profile: `tigrcorn`
- Expected identities: `tigrcorn@py3.11, tigrcorn@py3.12`
- Present identities: `tigrcorn@py3.11, tigrcorn@py3.12`
- Passed identities: `tigrcorn@py3.11, tigrcorn@py3.12`
- Missing identities: ``
- Failed identities: ``

### Uvicorn (`uvicorn`)

- Status: `ready`
- Installed: `True`
- Module: `uvicorn`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `True`
- Serve check message: Validated manifests confirm serve-check success for 3/3 required cells.
- Validated matrix profile: `sqlite-uvicorn`
- Expected identities: `sqlite-uvicorn@py3.10, sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12`
- Present identities: `sqlite-uvicorn@py3.10, sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12`
- Passed identities: `sqlite-uvicorn@py3.10, sqlite-uvicorn@py3.11, sqlite-uvicorn@py3.12`
- Missing identities: ``
- Failed identities: ``
