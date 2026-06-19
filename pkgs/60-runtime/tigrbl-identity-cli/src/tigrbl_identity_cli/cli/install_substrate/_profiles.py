from __future__ import annotations

from typing import Any

SUPPORTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12")
_SUPPORTED_PYTHON_TAGS = tuple(version.replace(".", "") for version in SUPPORTED_PYTHON_VERSIONS)
_TIGRCORN_PYTHON_TAGS = tuple(version.replace(".", "") for version in SUPPORTED_PYTHON_VERSIONS if version != "3.10")
RUNTIME_MATRIX_ENVS = (
    *(f"py{tag}-base" for tag in _SUPPORTED_PYTHON_TAGS),
    *(f"py{tag}-sqlite-uvicorn" for tag in _SUPPORTED_PYTHON_TAGS),
    *(f"py{tag}-postgres-hypercorn" for tag in _SUPPORTED_PYTHON_TAGS),
    *(f"py{tag}-tigrcorn" for tag in _TIGRCORN_PYTHON_TAGS),
    *(f"py{tag}-devtest" for tag in _SUPPORTED_PYTHON_TAGS),
)
TEST_LANE_ENVS = tuple(
    f"py{tag}-test-{lane}"
    for lane in ("core", "integration", "conformance", "security-negative", "interop")
    for tag in _SUPPORTED_PYTHON_TAGS
)
ADDITIONAL_CERTIFICATION_ENVS = (
    "py311-gates",
    "py311-test-extension",
    "py311-migration-portability",
    "py311-final-certification",
)
CERTIFICATION_TOX_ENVS = RUNTIME_MATRIX_ENVS + TEST_LANE_ENVS + ADDITIONAL_CERTIFICATION_ENVS
RUNTIME_IMPORT_SURFACES = (
    "tigrbl_identity_server.api.app",
    "tigrbl_auth.app",
    "tigrbl_auth.plugin",
    "tigrbl_auth.gateway",
)

_BASE_MODULES: tuple[dict[str, Any], ...] = (
    {"module": "tigrbl", "package": "tigrbl", "category": "runtime"},
    {"module": "swarmauri_core", "package": "swarmauri_core", "category": "runtime"},
    {"module": "swarmauri_base", "package": "swarmauri_base", "category": "runtime"},
    {"module": "swarmauri_standard", "package": "swarmauri_standard", "category": "runtime"},
    {"module": "swarmauri_tokens_jwt", "package": "swarmauri_tokens_jwt", "category": "runtime"},
    {"module": "swarmauri_signing_jws", "package": "swarmauri_signing_jws", "category": "runtime"},
    {"module": "swarmauri_signing_ed25519", "package": "swarmauri_signing_ed25519", "category": "runtime"},
    {"module": "swarmauri_signing_dpop", "package": "swarmauri_signing_dpop", "category": "runtime"},
    {"module": "pqcrypto", "package": "pqcrypto", "category": "runtime"},
    {"module": "swarmauri_crypto_jwe", "package": "swarmauri_crypto_jwe", "category": "runtime"},
    {"module": "swarmauri_crypto_paramiko", "package": "swarmauri_crypto_paramiko", "category": "runtime"},
    {"module": "swarmauri_keyprovider_file", "package": "swarmauri_keyprovider_file", "category": "runtime"},
    {"module": "swarmauri_keyprovider_local", "package": "swarmauri_keyprovider_local", "category": "runtime"},
    {"module": "sqlalchemy", "package": "sqlalchemy", "category": "runtime"},
    {"module": "bcrypt", "package": "bcrypt", "category": "runtime"},
    {"module": "httpx", "package": "httpx", "category": "runtime"},
    {"module": "yaml", "package": "PyYAML", "category": "runtime"},
    {"module": "pydantic", "package": "pydantic", "category": "runtime"},
    {"module": "pydantic_settings", "package": "pydantic-settings", "category": "runtime"},
    {"module": "dotenv", "package": "python-dotenv", "category": "runtime"},
    {"module": "multipart", "package": "python-multipart", "category": "runtime"},
    {"module": "aiosqlite", "package": "aiosqlite", "category": "runtime"},
)
_TEST_MODULES: tuple[dict[str, Any], ...] = (
    {"module": "pytest", "package": "pytest", "category": "test"},
    {"module": "xdist", "package": "pytest-xdist", "category": "test"},
    {"module": "pytest_jsonreport", "package": "pytest-json-report", "category": "test"},
    {"module": "pytest_timeout", "package": "pytest-timeout", "category": "test"},
    {"module": "pytest_benchmark", "package": "pytest-benchmark", "category": "test"},
    {"module": "requests", "package": "requests", "category": "test"},
)
_SQLITE_MODULES: tuple[dict[str, Any], ...] = ()
_POSTGRES_MODULES = ({"module": "asyncpg", "package": "asyncpg", "category": "storage"},)
_UVICORN_MODULES = ({"module": "uvicorn", "package": "uvicorn", "category": "runner"},)
_HYPERCORN_MODULES = ({"module": "hypercorn", "package": "hypercorn", "category": "runner"},)
_TIGRCORN_MODULES = (
    {
        "module": "tigrcorn",
        "package": "tigrcorn",
        "category": "runner",
        "python_min": (3, 11),
        "python_max_exclusive": (3, 15),
    },
)

PROFILE_IMPORT_GROUPS: dict[str, tuple[tuple[dict[str, Any], ...], ...]] = {
    "base": (_BASE_MODULES,),
    "sqlite-uvicorn": (_BASE_MODULES, _SQLITE_MODULES, _UVICORN_MODULES),
    "postgres-hypercorn": (_BASE_MODULES, _POSTGRES_MODULES, _HYPERCORN_MODULES),
    "tigrcorn": (_BASE_MODULES, _TIGRCORN_MODULES),
    "devtest": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _UVICORN_MODULES),
    "release-gates": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-core": (_BASE_MODULES, _TEST_MODULES),
    "test-integration": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-conformance": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-security-negative": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-interop": (_BASE_MODULES, _TEST_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "test-extension": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "migration-portability": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
    "final-certification": (_BASE_MODULES, _TEST_MODULES, _SQLITE_MODULES, _POSTGRES_MODULES, _UVICORN_MODULES, _HYPERCORN_MODULES, _TIGRCORN_MODULES),
}

PROFILE_TOGGLES: dict[str, dict[str, Any]] = {
    "base": {"constraints": [], "extras": []},
    "sqlite-uvicorn": {"constraints": ["constraints/runner-uvicorn.txt"], "extras": ["sqlite", "uvicorn"]},
    "postgres-hypercorn": {"constraints": ["constraints/runner-hypercorn.txt"], "extras": ["postgres", "hypercorn"]},
    "tigrcorn": {"constraints": ["constraints/runner-tigrcorn.txt"], "extras": ["tigrcorn"]},
    "devtest": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt"], "extras": ["test", "sqlite", "uvicorn"]},
    "release-gates": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-core": {"constraints": ["constraints/test.txt"], "extras": ["test"]},
    "test-integration": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-conformance": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-security-negative": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "test-interop": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "servers"]},
    "test-extension": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "migration-portability": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
    "final-certification": {"constraints": ["constraints/test.txt", "constraints/runner-uvicorn.txt", "constraints/runner-hypercorn.txt", "constraints/runner-tigrcorn.txt"], "extras": ["test", "sqlite", "postgres", "servers"]},
}

INSTALL_WORKFLOW_RUNTIME_ENVS = set(RUNTIME_MATRIX_ENVS)
RELEASE_WORKFLOW_RUNTIME_ENVS = set(RUNTIME_MATRIX_ENVS)
RELEASE_WORKFLOW_TEST_LANE_ENVS = set(TEST_LANE_ENVS)
RELEASE_WORKFLOW_EXTRA_ENVS = {"py311-migration-portability", "py311-final-certification"}

TOX_PROFILE_SECTION_EXPECTATIONS = {
    "[testenv]": "base",
    "[testenv:py{310,311,312}-sqlite-uvicorn]": "sqlite-uvicorn",
    "[testenv:py{310,311,312}-postgres-hypercorn]": "postgres-hypercorn",
    "[testenv:py{311,312}-tigrcorn]": "tigrcorn",
    "[testenv:py{310,311,312}-devtest]": "devtest",
    "[testenv:py311-gates]": "release-gates",
    "[testenv:py{310,311,312}-test-core]": "test-core",
    "[testenv:py{310,311,312}-test-integration]": "test-integration",
    "[testenv:py{310,311,312}-test-conformance]": "test-conformance",
    "[testenv:py{310,311,312}-test-security-negative]": "test-security-negative",
    "[testenv:py{310,311,312}-test-interop]": "test-interop",
    "[testenv:py311-test-extension]": "test-extension",
    "[testenv:py311-migration-portability]": "migration-portability",
    "[testenv:py311-final-certification]": "final-certification",
}

__all__ = [
    "CERTIFICATION_TOX_ENVS",
    "INSTALL_WORKFLOW_RUNTIME_ENVS",
    "PROFILE_IMPORT_GROUPS",
    "PROFILE_TOGGLES",
    "RELEASE_WORKFLOW_EXTRA_ENVS",
    "RELEASE_WORKFLOW_RUNTIME_ENVS",
    "RELEASE_WORKFLOW_TEST_LANE_ENVS",
    "RUNTIME_IMPORT_SURFACES",
    "RUNTIME_MATRIX_ENVS",
    "SUPPORTED_PYTHON_VERSIONS",
    "TEST_LANE_ENVS",
    "TOX_PROFILE_SECTION_EXPECTATIONS",
]
