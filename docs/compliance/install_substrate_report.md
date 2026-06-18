# Install Substrate Report

- Generated at: `20260618T185123Z`
- Passed: `True`
- Static manifest passed: `True`
- Profile: `base`
- Profile identity: `base@py312`
- Environment identity present: `True`
- Current Python: `3.12.5`
- Current Python supported: `True`
- Expected supported Python versions: `3.10, 3.11, 3.12`
- Detected supported Python binaries: `2` / `3`
- Certification tox envs declared: `33`
- Runtime matrix envs declared: `14`
- Test lane envs declared: `15`
- Tox templates with pip check: `14` / `14`
- Tox templates with install probe: `14` / `14`
- Current profile import probe passed: `True`
- Runtime surface probe passed: `True`

## Warnings

- The current container does not provide supported interpreter binaries for: 3.11.

## Current environment import probe

- `tigrbl` (tigrbl) → passed=`True` message=`import ok`
- `swarmauri_core` (swarmauri_core) → passed=`True` message=`import ok`
- `swarmauri_base` (swarmauri_base) → passed=`True` message=`import ok`
- `swarmauri_standard` (swarmauri_standard) → passed=`True` message=`import ok`
- `swarmauri_tokens_jwt` (swarmauri_tokens_jwt) → passed=`True` message=`import ok`
- `swarmauri_signing_jws` (swarmauri_signing_jws) → passed=`True` message=`import ok`
- `swarmauri_signing_ed25519` (swarmauri_signing_ed25519) → passed=`True` message=`import ok`
- `swarmauri_signing_dpop` (swarmauri_signing_dpop) → passed=`True` message=`import ok`
- `pqcrypto` (pqcrypto) → passed=`True` message=`import ok`
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

- `tigrbl_identity_server.api.app` → passed=`True` message=`import surface resolvable`
- `tigrbl_auth.app` → passed=`True` message=`import surface resolvable`
- `tigrbl_auth.plugin` → passed=`True` message=`import surface resolvable`
- `tigrbl_auth.gateway` → passed=`True` message=`import surface resolvable`

## Detected supported interpreters

- `3.10` → available=`True` path=`py -3.10`
- `3.11` → available=`False` path=`None`
- `3.12` → available=`True` path=`<repo>/.tmp/uv-rest-only-py312/Scripts/python.exe`

## Workflow coverage

- install_profiles_workflow_present: `True`
- release_gates_workflow_present: `True`
- install_profiles_runtime_env_present_count: `14`
- release_gates_runtime_env_present_count: `14`
- release_gates_test_lane_env_present_count: `15`
- release_gates_extra_env_present_count: `2`
- install_profiles_artifact_upload_present: `True`
- release_gates_artifact_upload_present: `True`
