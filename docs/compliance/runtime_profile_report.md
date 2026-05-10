# Runtime Profile Report

- Generated at: `20260509T204812Z`
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
- Execution probes enabled: `False`
- Surface probe passed: `False`
- Surface probe endpoints: `0`
- Serve-check passes: `0`
- Execution probe complete: `False`
- Required runtime cells: `14`
- Validated runtime cells present: `0`
- Validated runtime cells passed: `0`
- Validated runtime matrix green: `False`

## Application Probe

- App factory: `tigrbl_auth.api.app.build_app`
- Message: Application factory materialized successfully with 7 active routes and 25 active targets.

## Surface Probe

- Executed: `False`
- Passed: `False`
- Message: Execution probes were disabled for this invocation.
- Endpoint count: `0`
- Passed endpoints: `0`
- Failed endpoints: `0`

## Runner Profiles

### Hypercorn (`hypercorn`)

- Status: `missing`
- Installed: `False`
- Module: `None`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Execution probes were disabled for this invocation.

### Tigrcorn (`tigrcorn`)

- Status: `missing`
- Installed: `False`
- Module: `None`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Execution probes were disabled for this invocation.

### Uvicorn (`uvicorn`)

- Status: `ready`
- Installed: `True`
- Module: `uvicorn`
- Placeholder-supported: `False`
- Declared CI-installable: `True`
- Serve check passed: `False`
- Serve check message: Execution probes were disabled for this invocation.
