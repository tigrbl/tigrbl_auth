"""
Shared test configuration and fixtures for tigrbl_auth test suite.
"""

import inspect
import os
import shutil
import sys
import time
import types
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import Any, AsyncGenerator, Generator

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
for _api_src in sorted((_REPO_ROOT / "pkgs" / "80-apis").glob("*/src")):
    if str(_api_src) not in sys.path:
        sys.path.insert(0, str(_api_src))

from tigrbl_identity_contracts.protocol_configuration import bind_protocol_settings
from tigrbl_identity_runtime.settings import settings as _protocol_test_settings

bind_protocol_settings(_protocol_test_settings)

import pytest_asyncio
from httpx import AsyncClient
from tests.lanes import (
    active_lane,
    certification_python_supported,
    classify_test_path,
    lane_allows_path,
    missing_optional_runtime_modules,
    skip_reason_for_test_path,
)
from tests.support import TestClient


@pytest.fixture(autouse=True)
def _isolate_protocol_settings_binding():
    """Keep app-factory tests from leaking their composition target globally."""

    bind_protocol_settings(_protocol_test_settings)
    yield
    bind_protocol_settings(_protocol_test_settings)


if sys.version_info < (3, 11) and "tomllib" not in sys.modules:
    _tomllib = types.ModuleType("tomllib")

    class TOMLDecodeError(ValueError):
        pass

    def _loads(_source: str | bytes, /, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return {}

    def _load(fp: Any, /, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return _loads(fp.read())

    _tomllib.TOMLDecodeError = TOMLDecodeError
    _tomllib.loads = _loads
    _tomllib.load = _load
    sys.modules["tomllib"] = _tomllib


class _MockDataFactory:
    def create_user_data(self, **overrides):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "is_active": True,
        }
        data.update(overrides)
        return data

    def create_api_key_data(self, **overrides):
        data = {
            "raw_key": "api-key-12345",
        }
        data.update(overrides)
        return data

    def create_client_data(self, **overrides):
        data = {
            "client_secret": "client-secret-12345",
            "is_active": True,
        }
        data.update(overrides)
        return data


class _InMemoryTableStorage:
    def __init__(self) -> None:
        self._rows: dict[type, list[dict[str, Any]]] = {}
        self._counters: dict[type, int] = {}

    def handlers_for(self, model: type) -> SimpleNamespace:
        async def list_core(request: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
            filters = dict((request.get("payload") or {}).get("filters") or {})
            return {"items": [dict(row) for row in self._bucket(model) if self._matches(row, filters)]}

        async def create_core(request: dict[str, Any]) -> dict[str, dict[str, Any]]:
            payload = dict(request.get("payload") or {})
            payload.setdefault("id", self._next_id(model))
            self._bucket(model).append(payload)
            return {"item": dict(payload)}

        async def read_core(request: dict[str, Any]) -> dict[str, Any] | None:
            ident = str((request.get("path_params") or {}).get("id"))
            for row in self._bucket(model):
                if str(row.get("id")) == ident:
                    return dict(row)
            return None

        async def update_core(request: dict[str, Any]) -> dict[str, dict[str, Any]]:
            ident = str((request.get("path_params") or {}).get("id"))
            payload = dict(request.get("payload") or {})
            for row in self._bucket(model):
                if str(row.get("id")) == ident:
                    row.update(payload)
                    return {"item": dict(row)}
            raise KeyError(ident)

        async def clear_core(request: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
            filters = dict((request.get("payload") or {}).get("filters") or {})
            bucket = self._bucket(model)
            removed = [row for row in bucket if self._matches(row, filters)]
            self._rows[model] = [row for row in bucket if not self._matches(row, filters)]
            return {"items": [dict(row) for row in removed]}

        async def delete_core(request: dict[str, Any]) -> dict[str, Any] | None:
            ident = str((request.get("path_params") or {}).get("id"))
            bucket = self._bucket(model)
            for index, row in enumerate(bucket):
                if str(row.get("id")) == ident:
                    return dict(bucket.pop(index))
            return None

        return SimpleNamespace(
            list=SimpleNamespace(core=list_core),
            create=SimpleNamespace(core=create_core),
            read=SimpleNamespace(core=read_core),
            update=SimpleNamespace(core=update_core),
            delete=SimpleNamespace(core=delete_core),
            clear=SimpleNamespace(core=clear_core),
        )

    def _bucket(self, model: type) -> list[dict[str, Any]]:
        return self._rows.setdefault(model, [])

    def _next_id(self, model: type) -> str:
        self._counters[model] = self._counters.get(model, 0) + 1
        return f"{getattr(model, '__tablename__', model.__name__)}-{self._counters[model]}"

    def _matches(self, row: dict[str, Any], filters: dict[str, Any]) -> bool:
        return all(self._value_matches(row.get(key), value) for key, value in filters.items())

    @staticmethod
    def _value_matches(actual: Any, expected: Any) -> bool:
        return actual == expected or (actual is not None and expected is not None and str(actual) == str(expected))


@pytest.fixture
def mock_data_factory():
    return _MockDataFactory()


@pytest.fixture
def administrator_storage(monkeypatch: pytest.MonkeyPatch):
    from tigrbl_identity_storage.tables.attribute_policy import AttributePolicy
    from tigrbl_identity_storage.tables.delegated_admin_scope import DelegatedAdminScope
    from tigrbl_identity_storage.tables.policy_condition import PolicyCondition
    from tigrbl_identity_storage.tables.role import Role
    from tigrbl_identity_storage.tables.tenant_membership import TenantMembership
    from tigrbl_identity_storage_runtime import (
        DelegatedAdminScopeRuntimeSpec,
        AttributePolicyRuntimeSpec,
        RoleRuntimeSpec,
        TenantMembershipRuntimeSpec,
        initializeIdentityRuntimeTables,
    )

    initializeIdentityRuntimeTables(
        (
            RoleRuntimeSpec,
            AttributePolicyRuntimeSpec,
            TenantMembershipRuntimeSpec,
            DelegatedAdminScopeRuntimeSpec,
        )
    )
    storage = _InMemoryTableStorage()
    for model in (Role, TenantMembership, AttributePolicy, PolicyCondition, DelegatedAdminScope):
        runtime_handlers = model.handlers
        test_handlers = storage.handlers_for(model)
        for name, value in vars(runtime_handlers).items():
            if not hasattr(test_handlers, name):
                setattr(test_handlers, name, value)
        monkeypatch.setattr(model, "handlers", test_handlers, raising=False)
    return storage


@pytest.fixture
def sample_tenant_data():
    return {"slug": "test-tenant", "name": "Test Tenant"}



def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--certification-lane",
        action="store",
        default=None,
        choices=["core", "integration", "conformance", "security-negative", "interop", "extension", "all"],
        help=(
            "Select the certification lane to collect and run. Defaults to the "
            "TIGRBL_AUTH_TEST_LANE environment variable, falling back to 'core'."
        ),
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "extension: optional extension lane tests")
    config.addinivalue_line("markers", "deferred: tests outside the default certification boundary")
    config.addinivalue_line("markers", "runtime_heavy: requires the full runtime dependency stack")


def pytest_report_header(config: pytest.Config) -> list[str]:
    lane = active_lane(config.getoption("--certification-lane"))
    header = [f"certification lane: {lane}"]
    if not certification_python_supported():
        header.append(
            f"certification python boundary: current interpreter {sys.version_info.major}.{sys.version_info.minor} is outside 3.10-3.14"
        )
    missing = missing_optional_runtime_modules()
    if missing:
        header.append("missing optional runtime modules: " + ", ".join(missing))
    return header


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool | None:
    path = Path(str(collection_path))
    if path.suffix != ".py" or not path.name.startswith("test_"):
        return None

    lane = active_lane(config.getoption("--certification-lane"))
    if not lane_allows_path(lane, path):
        return True

    reason = skip_reason_for_test_path(path)
    if reason is not None:
        return True
    return None


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        path = Path(str(item.fspath))
        lane = classify_test_path(path)
        if lane == "extension":
            item.add_marker(pytest.mark.extension)
            item.add_marker(pytest.mark.deferred)
        if skip_reason_for_test_path(path) is not None:
            item.add_marker(pytest.mark.runtime_heavy)

def _require_runtime_stack() -> None:
    pytest.importorskip("tigrbl")


def _import_runtime_objects() -> dict[str, Any]:
    _require_runtime_stack()
    from tigrbl.engine import Engine, EngineSpec
    from tigrbl_identity_server.app import app
    from tigrbl_identity_server.api.surfaces import surface_api as composed_surface_api
    from tigrbl_identity_storage.tables.engine import get_db
    from tigrbl_identity_runtime.engine_resolver import (
        register_api_provider,
        resolve_api_provider,
        resolve_default_provider,
        set_default_provider,
    )
    surface_api = composed_surface_api
    canonical_legacy_surface_api = composed_surface_api

    return {
        "Engine": Engine,
        "EngineSpec": EngineSpec,
        "canonical_legacy_surface_api": canonical_legacy_surface_api,
        "register_api_provider": register_api_provider,
        "resolve_api_provider": resolve_api_provider,
        "resolve_default_provider": resolve_default_provider,
        "set_default_provider": set_default_provider,
        "app": app,
        "composed_surface_api": composed_surface_api,
        "get_db": get_db,
        "surface_api": surface_api,
    }




@pytest.fixture(autouse=True)
def isolate_operator_plane_state(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    state_home = tmp_path.parent / "operator-plane-state"
    state_home.mkdir(exist_ok=True)
    monkeypatch.setenv("TIGRBL_AUTH_OPERATOR_STATE_DIR", str(state_home))
    yield

@pytest.fixture(scope="session", autouse=True)
def cleanup_runtime_secrets() -> Generator[None, None, None]:
    """Remove runtime key directories generated by JWT helper defaults."""
    yield
    package_root = Path(__file__).resolve().parents[1]
    candidate_paths = {
        Path.cwd() / "runtime_secrets",
        package_root / "runtime_secrets",
        package_root.parent / "runtime_secrets",
    }
    for path in candidate_paths:
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)


@pytest.fixture(autouse=True)
def disable_tls_requirement():
    from tigrbl_auth.runtime_cfg import settings

    original = settings.require_tls
    settings.require_tls = False
    try:
        yield
    finally:
        settings.require_tls = original


@asynccontextmanager
async def _runtime_engine_context(database_url: str):
    runtime = _import_runtime_objects()
    Engine = runtime["Engine"]
    EngineSpec = runtime["EngineSpec"]
    register_api_provider = runtime["register_api_provider"]
    resolve_api_provider = runtime["resolve_api_provider"]
    resolve_default_provider = runtime["resolve_default_provider"]
    set_default_provider = runtime["set_default_provider"]
    surface_api = runtime["surface_api"]
    composed_surface_api = runtime["composed_surface_api"]
    canonical_legacy_surface_api = runtime["canonical_legacy_surface_api"]
    app = runtime["app"]

    spec = EngineSpec.from_any(database_url)
    engine = Engine(spec)
    provider = engine.provider
    original_surface = resolve_api_provider(surface_api)
    original_composed_surface = resolve_api_provider(composed_surface_api)
    original_canonical_legacy_surface = resolve_api_provider(canonical_legacy_surface_api)
    original_app = resolve_api_provider(app)
    original_default_provider = resolve_default_provider()
    register_api_provider(surface_api, provider)
    register_api_provider(composed_surface_api, provider)
    register_api_provider(canonical_legacy_surface_api, provider)
    register_api_provider(app, provider)
    set_default_provider(provider)
    setattr(surface_api, "_ddl_executed", False)
    await surface_api.initialize()
    raw_engine, _ = provider.ensure()
    from tigrbl_identity_storage_runtime.migrations.runtime import (
        _bootstrap_sqlite_schema,
        _ensure_sqlite_attachment_on_connection,
    )

    sqlite_attachments = _bootstrap_sqlite_schema(raw_engine)

    def _create_runtime_tables(sync_conn):
        from tigrbl_auth.tables import RestOltpTable
        from tigrbl_identity_storage.migrations.helpers import ensure_schema

        _ensure_sqlite_attachment_on_connection(sync_conn, sqlite_attachments)
        ensure_schema(sync_conn)
        RestOltpTable.metadata.create_all(bind=sync_conn, checkfirst=True)

    begin_ctx = raw_engine.begin()
    if hasattr(begin_ctx, "__aenter__"):
        async with begin_ctx as conn:
            await conn.run_sync(_create_runtime_tables)
    else:
        with begin_ctx as conn:
            _create_runtime_tables(conn)
    try:
        yield engine
    finally:
        if str(database_url).startswith("postgresql"):
            try:
                cleanup_ctx = raw_engine.begin()
                if hasattr(cleanup_ctx, "__aenter__"):
                    async with cleanup_ctx as conn:
                        await conn.exec_driver_sql("DROP SCHEMA IF EXISTS authn CASCADE")
                else:
                    with cleanup_ctx as conn:
                        conn.exec_driver_sql("DROP SCHEMA IF EXISTS authn CASCADE")
            except Exception:
                pass
        dispose_result = raw_engine.dispose()
        if inspect.isawaitable(dispose_result):
            await dispose_result
        register_api_provider(surface_api, original_surface or provider)
        register_api_provider(composed_surface_api, original_composed_surface or provider)
        register_api_provider(
            canonical_legacy_surface_api,
            original_canonical_legacy_surface or provider,
        )
        register_api_provider(app, original_app or provider)
        set_default_provider(original_default_provider or provider)
        setattr(surface_api, "_ddl_executed", False)


@pytest.fixture
def runtime_engine_factory():
    return _runtime_engine_context


@pytest.fixture
def postgres_database_url() -> str | None:
    value = os.environ.get("POSTGRES_URL")
    return value.strip() if value else None


@pytest_asyncio.fixture
async def test_db_engine(tmp_path_factory: pytest.TempPathFactory) -> AsyncGenerator[Any, None]:
    """Create and initialize a test database engine."""
    db_path = tmp_path_factory.mktemp("runtime-db") / "tigrbl_auth_test.db"
    test_database_url = f"sqlite+aiosqlite:///{db_path}"
    async with _runtime_engine_context(test_database_url) as engine:
        try:
            yield engine
        finally:
            for artifact in (db_path, db_path.with_suffix(".db-shm"), db_path.with_suffix(".db-wal")):
                for _ in range(10):
                    try:
                        artifact.unlink(missing_ok=True)
                        break
                    except PermissionError:
                        time.sleep(0.1)
            shutil.rmtree(db_path.parent, ignore_errors=True)


@pytest_asyncio.fixture
async def db_session(test_db_engine: Any) -> AsyncGenerator[Any, None]:
    """Provide a database session for tests."""
    _, maker = test_db_engine.provider.ensure()
    async with maker() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def override_get_db(test_db_engine: Any):
    """Override database dependencies and tigrbl engine for tests."""
    runtime = _import_runtime_objects()
    app = runtime["app"]
    get_db = runtime["get_db"]
    from tigrbl_auth.db import get_db as legacy_get_db
    from tigrbl_auth.tables import get_db as tables_get_db
    from tigrbl_auth.tables.engine import get_db as engine_get_db

    _, maker = test_db_engine.provider.ensure()
    async with maker() as session:
        def _override_db():
            return session

        for dependency in {get_db, legacy_get_db, tables_get_db, engine_get_db}:
            app.router.dependency_overrides[dependency] = _override_db
            app.dependency_overrides[dependency] = _override_db
        try:
            yield
        finally:
            app.router.dependency_overrides.clear()
            app.dependency_overrides.clear()


@pytest.fixture
def test_client(override_get_db) -> TestClient:
    """Create an ASGI test client."""
    app = _import_runtime_objects()["app"]
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing."""
    from httpx import ASGITransport

    app = _import_runtime_objects()["app"]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://test") as client:
        yield client


@pytest.fixture
def enable_rfc7662():
    """Enable RFC 7662 token introspection for tests."""
    from tigrbl_auth.runtime_cfg import settings

    original = settings.enable_rfc7662
    settings.enable_rfc7662 = True
    try:
        yield
    finally:
        settings.enable_rfc7662 = original


@pytest.fixture
def enable_rfc7009():
    """Enable RFC 7009 token revocation for tests."""
    _require_runtime_stack()
    from tigrbl_auth.runtime_cfg import settings
    from tigrbl_auth.rfc.rfc7009 import include_rfc7009, reset_revocations

    app = _import_runtime_objects()["app"]
    original = settings.enable_rfc7009
    settings.enable_rfc7009 = True
    include_rfc7009(app)
    reset_revocations()
    try:
        yield
    finally:
        settings.enable_rfc7009 = original
        reset_revocations()


@pytest.fixture
def enable_rfc8693():
    """Enable RFC 8693 token exchange for tests."""
    _require_runtime_stack()
    from tigrbl_auth.runtime_cfg import settings
    from tigrbl_auth.rfc.rfc8693 import include_rfc8693

    app = _import_runtime_objects()["app"]
    original = settings.enable_rfc8693
    settings.enable_rfc8693 = True
    include_rfc8693(app)
    try:
        yield
    finally:
        settings.enable_rfc8693 = original


@pytest.fixture
def enable_rfc8414():
    """Enable RFC 8414 authorization server metadata for tests."""
    _require_runtime_stack()
    from tigrbl_auth.runtime_cfg import settings
    from tigrbl_auth.rfc.rfc8414 import include_rfc8414
    from tigrbl_auth_protocol_oidc.discovery import include_oidc_discovery

    app = _import_runtime_objects()["app"]
    original = settings.enable_rfc8414
    settings.enable_rfc8414 = True
    include_rfc8414(app)
    include_oidc_discovery(app)
    try:
        yield
    finally:
        settings.enable_rfc8414 = original


@pytest_asyncio.fixture
async def enable_rfc9126(db_session):
    """Enable RFC 9126 pushed authorization requests for tests."""
    from tigrbl_auth.runtime_cfg import settings

    original = settings.enable_rfc9126
    settings.enable_rfc9126 = True
    try:
        yield
    finally:
        settings.enable_rfc9126 = original


@pytest.fixture
def temp_key_file(tmp_path_factory: pytest.TempPathFactory):
    """Create a temporary key directory for testing."""
    temp_dir = tmp_path_factory.mktemp("runtime-keys")
    temp_kid = temp_dir / "jwt_ed25519.kid"

    import tigrbl_identity_jose.crypto as crypto_module
    import tigrbl_auth_protocol_oidc.id_token as oidc_module
    import tigrbl_auth_protocol_oidc.standards.id_token as canonical_oidc_module

    original_dir = crypto_module._DEFAULT_KEY_DIR
    original_path = crypto_module._DEFAULT_KEY_PATH
    original_rsa_path = oidc_module._RSA_KEY_PATH
    original_canonical_rsa_path = canonical_oidc_module._RSA_KEY_PATH

    crypto_module._DEFAULT_KEY_DIR = temp_dir
    crypto_module._DEFAULT_KEY_PATH = temp_kid
    crypto_module._provider.cache_clear()
    crypto_module._load_keypair.cache_clear()

    oidc_module._RSA_KEY_PATH = temp_dir / "jwt_rs256.kid"
    oidc_module._provider.cache_clear()
    oidc_module._service_cache = None
    canonical_oidc_module._RSA_KEY_PATH = oidc_module._RSA_KEY_PATH
    canonical_oidc_module._provider.cache_clear()
    canonical_oidc_module._service_cache = None

    yield temp_kid

    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    crypto_module._DEFAULT_KEY_DIR = original_dir
    crypto_module._DEFAULT_KEY_PATH = original_path
    crypto_module._provider.cache_clear()
    crypto_module._load_keypair.cache_clear()
    oidc_module._RSA_KEY_PATH = original_rsa_path
    oidc_module._provider.cache_clear()
    oidc_module._service_cache = None
    canonical_oidc_module._RSA_KEY_PATH = original_canonical_rsa_path
    canonical_oidc_module._provider.cache_clear()
    canonical_oidc_module._service_cache = None


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("TIGRBL_AUTH_ISSUER", "https://authn.example.com")
    monkeypatch.setenv("TIGRBL_AUTH_BASE_URL", "https://authn.example.com")
    monkeypatch.setenv("TIGRBL_AUTH_ENV", "test")
    yield {
        "TIGRBL_AUTH_ISSUER": "https://authn.example.com",
        "TIGRBL_AUTH_BASE_URL": "https://authn.example.com",
        "TIGRBL_AUTH_ENV": "test",
    }
