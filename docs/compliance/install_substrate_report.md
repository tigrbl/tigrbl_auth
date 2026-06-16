# Install Substrate Report

- Generated at: `20260616T201636Z`
- Passed: `False`
- Static manifest passed: `True`
- Profile: `base`
- Profile identity: `base@py312`
- Environment identity present: `True`
- Current Python: `3.12.5`
- Current Python supported: `True`
- Expected supported Python versions: `3.10, 3.11, 3.12, 3.13, 3.14`
- Detected supported Python binaries: `2` / `5`
- Certification tox envs declared: `53`
- Runtime matrix envs declared: `24`
- Test lane envs declared: `25`
- Tox templates with pip check: `14` / `14`
- Tox templates with install probe: `14` / `14`
- Current profile import probe passed: `True`
- Runtime surface probe passed: `False`

## Failures

- The current environment does not provide the full supported interpreter matrix required for clean-room certification.
- One or more runtime import surfaces could not be resolved from the source tree.

## Warnings

- The current container does not provide supported interpreter binaries for: 3.11, 3.13, 3.14.
- Pinned tigrbl==0.4.0 declares Requires-Python >=3.10,<3.14, blocking Python 3.14.
- Pinned Swarmauri core/base/standard/JWT/JWS/Ed25519/DPoP/JWE/Paramiko/keyprovider packages declare Requires-Python >=3.10,<3.13, blocking Python 3.13 and 3.14.

## Current environment import probe

- `tigrbl` (tigrbl) → passed=`True` message=`import ok`
- `swarmauri_core` (swarmauri_core) → passed=`True` message=`import ok`
- `swarmauri_base` (swarmauri_base) → passed=`True` message=`import ok`
- `swarmauri_standard` (swarmauri_standard) → passed=`True` message=`import ok`
- `swarmauri_tokens_jwt` (swarmauri_tokens_jwt) → passed=`True` message=`import ok`
- `swarmauri_signing_jws` (swarmauri_signing_jws) → passed=`True` message=`import ok`
- `swarmauri_signing_ed25519` (swarmauri_signing_ed25519) → passed=`True` message=`import ok`
- `swarmauri_signing_dpop` (swarmauri_signing_dpop) → passed=`True` message=`import ok`
- `swarmauri_crypto_jwe` (swarmauri_crypto_jwe) → passed=`True` message=`import ok`
- `swarmauri_crypto_paramiko` (swarmauri_crypto_paramiko) → passed=`True` message=`import ok`
- `swarmauri_keyprovider_file` (swarmauri_keyprovider_file) → passed=`True` message=`import ok`
- `swarmauri_keyprovider_local` (swarmauri_keyprovider_local) → passed=`True` message=`import ok`
- `sqlalchemy` (sqlalchemy) → passed=`True` message=`import ok`
- `bcrypt` (bcrypt) → passed=`True` message=`import ok`
- `httpx` (httpx) → passed=`True` message=`import ok`
- `yaml` (PyYAML) → passed=`True` message=`import ok`
- `pydantic` (pydantic) → passed=`True` message=`import ok`
- `pydantic_settings` (pydantic-settings) → passed=`True` message=`import ok`
- `dotenv` (python-dotenv) → passed=`True` message=`import ok`
- `multipart` (python-multipart) → passed=`True` message=`import ok`
- `aiosqlite` (aiosqlite) → passed=`True` message=`import ok`

## Runtime import surfaces

- `tigrbl_identity_server.api.app` → passed=`False` message=`module source missing`
- `tigrbl_auth.app` → passed=`True` message=`import surface resolvable`
- `tigrbl_auth.plugin` → passed=`True` message=`import surface resolvable`
- `tigrbl_auth.gateway` → passed=`True` message=`import surface resolvable`

## Detected supported interpreters

- `3.10` → available=`True` path=`py -3.10`
- `3.11` → available=`False` path=`None`
- `3.12` → available=`True` path=`<repo>/.venv/Scripts/python.exe`
- `3.13` → available=`False` path=`None`
- `3.14` → available=`False` path=`None`

## Workflow coverage

- install_profiles_workflow_present: `True`
- release_gates_workflow_present: `True`
- install_profiles_runtime_env_present_count: `24`
- release_gates_runtime_env_present_count: `24`
- release_gates_test_lane_env_present_count: `25`
- release_gates_extra_env_present_count: `2`
- install_profiles_artifact_upload_present: `True`
- release_gates_artifact_upload_present: `True`
