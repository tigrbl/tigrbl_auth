# Runtime Profile Report

- Generated at: `20260510T100313Z`
- Deployment profile: `baseline`
- Report mode: `live-probe`
- Validated artifact source: `None`
- Application factory probe passed: `True`
- Ready profiles: `1`
- Missing profiles: `2`
- Invalid profiles: `0`
- Application hash invariant: `True`
- Pyproject requires-python: `>=3.10,<3.13`
- Supported Python versions: `3.10, 3.11, 3.12`
- Placeholder-supported runners: `0`
- Declared CI-installable runners: `3`
- Declared CI install/probe complete: `True`
- Execution probes enabled: `True`
- Surface probe passed: `True`
- Surface probe endpoints: `4`
- Serve-check passes: `1`
- Execution probe complete: `True`
- Required runtime cells: `14`
- Validated runtime cells present: `0`
- Validated runtime cells passed: `0`
- Validated runtime matrix green: `False`

## Application Probe

- App factory: `tigrbl_auth.api.app.build_app`
- Message: Application factory materialized successfully with 8 active routes and 24 active targets.

## Surface Probe

- Executed: `True`
- Passed: `True`
- Message: Runtime HTTP surface probes completed successfully.
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
- Serve check message: Skipped because the runner is not installed in this environment.

### Tigrcorn (`tigrcorn`)

- Status: `missing`
- Installed: `False`
- Module: `None`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Skipped because the runner is not installed in this environment.

### Uvicorn (`uvicorn`)

- Status: `ready`
- Installed: `True`
- Module: `uvicorn`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `True`
- Serve check message: Application factory materialized successfully with 9 active routes and 25 active targets.
