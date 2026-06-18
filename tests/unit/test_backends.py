"""
Unit tests for tigrbl_auth.backends module.

Tests authentication backends for password and API key authentication.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from tigrbl_auth.backends import AuthError, PasswordBackend, ApiKeyBackend
from tigrbl_auth.crypto import hash_pw
from tigrbl_auth.tables import User, ApiKey, ServiceKey, Service


@pytest.mark.unit
class TestAuthError:
    """Test AuthError exception class."""

    def test_auth_error_default_message(self):
        """Test AuthError with default message."""
        error = AuthError()
        assert str(error) == "authentication failed"
        assert error.reason == "authentication failed"

    def test_auth_error_custom_message(self):
        """Test AuthError with custom message."""
        custom_message = "invalid credentials"
        error = AuthError(custom_message)
        assert str(error) == custom_message
        assert error.reason == custom_message

    def test_auth_error_inheritance(self):
        """Test that AuthError inherits from Exception."""
        error = AuthError()
        assert isinstance(error, Exception)


@pytest.mark.unit
class TestPasswordBackend:
    """Test password authentication backend."""

    def setup_method(self):
        """Set up test fixtures for each test method."""
        self.backend = PasswordBackend()
        self.mock_db = AsyncMock()
        self.user_rows = []

    @pytest.fixture(autouse=True)
    def _patch_user_handlers(self, monkeypatch):
        async def _list_core(ctx):
            return list(self.user_rows)

        monkeypatch.setattr(User.handlers.list, "core", _list_core)

    def create_mock_user(self, mock_data_factory, **overrides):
        """Create a mock user using data factory for consistency."""
        user_data = mock_data_factory.create_user_data(**overrides)
        user = MagicMock(spec=User)
        user.id = uuid4()
        user.username = user_data["username"]
        user.email = user_data["email"]
        user.password_hash = (
            hash_pw(user_data["password"]) if user_data.get("password") else None
        )
        user.is_active = user_data["is_active"]
        user.tenant_id = uuid4()
        return user

    @pytest.mark.asyncio
    async def test_authenticate_with_valid_username_password(self, mock_data_factory):
        """Test successful authentication with username."""
        mock_user = self.create_mock_user(mock_data_factory)
        self.user_rows = [mock_user]

        # Use the password from the mock user creation
        test_password = "SecurePassword123!"  # Default from factory
        result = await self.backend.authenticate(
            self.mock_db, mock_user.username, test_password
        )

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_authenticate_with_valid_email_password(self, mock_data_factory):
        """Test successful authentication with email."""
        mock_user = self.create_mock_user(mock_data_factory)
        self.user_rows = [mock_user]

        test_password = "SecurePassword123!"
        result = await self.backend.authenticate(
            self.mock_db, mock_user.email, test_password
        )

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_authenticate_with_invalid_credentials(self, mock_data_factory):
        """Test authentication with invalid password."""
        mock_user = self.create_mock_user(mock_data_factory)
        self.user_rows = [mock_user]

        # Test authentication with wrong password
        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(
                self.mock_db, mock_user.username, "WrongPassword!"
            )

        assert exc_info.value.reason == "invalid username/email or password"

    @pytest.mark.asyncio
    async def test_authenticate_with_nonexistent_user(self):
        """Test authentication with nonexistent user."""
        self.user_rows = []

        # Test authentication
        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, "nonexistent", "password")

        assert exc_info.value.reason == "invalid username/email or password"

    @pytest.mark.asyncio
    async def test_authenticate_with_inactive_user(self):
        """Test authentication with inactive user."""
        self.user_rows = [MagicMock(username="testuser", email="test@example.com", is_active=False)]

        # Test authentication
        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(
                self.mock_db, "testuser", "TestPassword123!"
            )

        assert exc_info.value.reason == "invalid username/email or password"

    @pytest.mark.asyncio
    async def test_authenticate_with_none_password_hash(self, mock_data_factory):
        """Test authentication when user has no password hash."""
        # Create mock user with None password hash
        mock_user = self.create_mock_user(mock_data_factory, password=None)
        mock_user.password_hash = None
        self.user_rows = [mock_user]

        # Test authentication
        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(
                self.mock_db, mock_user.username, "TestPassword123!"
            )

        assert exc_info.value.reason == "invalid username/email or password"

    @pytest.mark.asyncio
    async def test_get_user_candidates_filter_identifier_and_active(self, mock_data_factory):
        """Candidate lookup returns active users matched by username or email."""
        active_user = self.create_mock_user(mock_data_factory, username="testuser", email="test@example.com")
        inactive_user = self.create_mock_user(mock_data_factory, username="testuser", is_active=False)
        other_user = self.create_mock_user(mock_data_factory, username="other")
        self.user_rows = [inactive_user, other_user, active_user]

        result = await self.backend._get_user_candidates(self.mock_db, "testuser")

        assert result == [active_user]

    @pytest.mark.asyncio
    async def test_authenticate_with_empty_identifier(self):
        """Test authentication with empty identifier."""
        self.user_rows = []

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, "", "password")

        assert exc_info.value.reason == "invalid username/email or password"

    @pytest.mark.asyncio
    async def test_authenticate_with_empty_password(self, mock_data_factory):
        """Test authentication with empty password."""
        mock_user = self.create_mock_user(mock_data_factory)
        self.user_rows = [mock_user]

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, mock_user.username, "")

        assert exc_info.value.reason == "invalid username/email or password"


@pytest.mark.unit
class TestApiKeyBackend:
    """Test API key authentication backend."""

    def setup_method(self):
        """Set up test fixtures for each test method."""
        self.backend = ApiKeyBackend()
        self.mock_db = AsyncMock()
        self.api_key_rows = []
        self.service_key_rows = []
        self.client_rows = []

    @pytest.fixture(autouse=True)
    def _patch_key_handlers(self, monkeypatch):
        async def _api_key_list_core(ctx):
            return list(self.api_key_rows)

        async def _service_key_list_core(ctx):
            return list(self.service_key_rows)

        async def _client_list_core(ctx):
            return list(self.client_rows)

        monkeypatch.setattr(ApiKey.handlers.list, "core", _api_key_list_core)
        monkeypatch.setattr(ServiceKey.handlers.list, "core", _service_key_list_core)
        from tigrbl_auth.tables import Client

        monkeypatch.setattr(Client.handlers.list, "core", _client_list_core)

    def create_mock_user(self, mock_data_factory, **overrides):
        """Create a mock user using data factory for consistency."""
        user_data = mock_data_factory.create_user_data(**overrides)
        user = MagicMock(spec=User)
        user.id = uuid4()
        user.username = user_data["username"]
        user.email = user_data["email"]
        user.is_active = user_data["is_active"]
        user.tenant_id = uuid4()
        return user

    def create_mock_service(self, mock_data_factory, **overrides):
        """Create a mock service using data factory patterns."""
        service_data = {"name": f"service-{uuid4().hex[:8]}", "is_active": True}
        service_data.update(overrides)

        service = MagicMock(spec=Service)
        service.id = uuid4()
        service.name = service_data["name"]
        service.is_active = service_data["is_active"]
        service.tenant_id = uuid4()
        return service

    def create_mock_api_key(
        self, mock_data_factory, user=None, raw_key=None, **overrides
    ):
        """Create a mock API key using data factory patterns."""
        if raw_key is None:
            api_key_data = mock_data_factory.create_api_key_data(**overrides)
            raw_key = api_key_data["raw_key"]

        api_key = MagicMock(spec=ApiKey)
        api_key.id = uuid4()
        api_key.user = user or self.create_mock_user(mock_data_factory)
        api_key.label = f"Test API Key {uuid4().hex[:8]}"
        api_key.digest = ApiKey.digest_of(raw_key)
        api_key.valid_to = overrides.get("valid_to")
        api_key.touch = MagicMock()
        api_key.valid_from = None
        return api_key

    def create_mock_service_key(
        self, mock_data_factory, service=None, raw_key=None, **overrides
    ):
        """Create a mock service key using data factory patterns."""
        if raw_key is None:
            raw_key = f"service-key-{uuid4().hex[:8]}"

        service_key = MagicMock(spec=ServiceKey)
        service_key.id = uuid4()
        service_key.service = service or self.create_mock_service(mock_data_factory)
        service_key.label = f"Test Service Key {uuid4().hex[:8]}"
        service_key.digest = ServiceKey.digest_of(raw_key)
        service_key.valid_to = overrides.get("valid_to")
        service_key.touch = MagicMock()
        service_key.valid_from = None
        return service_key

    def create_mock_client(self, mock_data_factory, **overrides):
        """Create a Client instance with hashed secret."""
        client_data = mock_data_factory.create_client_data(**overrides)
        client_secret = client_data["client_secret"]
        client = MagicMock()
        client.is_active = client_data["is_active"]
        client.verify_secret = MagicMock(side_effect=lambda s: s == client_secret)
        return client, client_secret

    @pytest.mark.asyncio
    async def test_authenticate_with_valid_api_key(self, mock_data_factory):
        """Test successful authentication with valid API key."""
        api_key_data = mock_data_factory.create_api_key_data()
        raw_key = api_key_data["raw_key"]

        mock_user = self.create_mock_user(mock_data_factory)
        mock_api_key = self.create_mock_api_key(
            mock_data_factory, user=mock_user, raw_key=raw_key
        )

        self.api_key_rows = [mock_api_key]

        principal, key_type = await self.backend.authenticate(self.mock_db, raw_key)

        assert principal == mock_user
        assert key_type == "user"
        mock_api_key.touch.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_with_valid_service_key(self, mock_data_factory):
        """Test successful authentication with valid service key."""
        raw_key = f"service-key-{uuid4().hex[:8]}"
        mock_service = self.create_mock_service(mock_data_factory)
        mock_service_key = self.create_mock_service_key(
            mock_data_factory, service=mock_service, raw_key=raw_key
        )

        self.service_key_rows = [mock_service_key]

        principal, key_type = await self.backend.authenticate(self.mock_db, raw_key)

        assert principal == mock_service
        assert key_type == "service"
        mock_service_key.touch.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_with_invalid_api_key(self):
        """Test authentication with invalid API key."""
        self.api_key_rows = []
        self.service_key_rows = []

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, "invalid-key")

        assert exc_info.value.reason == "API key invalid, revoked, or expired"

    @pytest.mark.asyncio
    async def test_authenticate_with_expired_api_key(self, mock_data_factory):
        """Test authentication with expired API key."""
        raw_key = "expired-api-key-12345"

        self.api_key_rows = [
            self.create_mock_api_key(
                mock_data_factory,
                raw_key=raw_key,
                valid_to=datetime.now(timezone.utc) - timedelta(seconds=1),
            )
        ]

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, raw_key)

        assert exc_info.value.reason == "API key invalid, revoked, or expired"

    @pytest.mark.asyncio
    async def test_authenticate_with_inactive_user(self, mock_data_factory):
        """Test authentication with API key for inactive user."""
        api_key_data = mock_data_factory.create_api_key_data()
        raw_key = api_key_data["raw_key"]

        mock_user = self.create_mock_user(mock_data_factory, is_active=False)
        mock_api_key = self.create_mock_api_key(
            mock_data_factory, user=mock_user, raw_key=raw_key
        )

        self.api_key_rows = [mock_api_key]

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, raw_key)

        assert exc_info.value.reason == "user is inactive"
        # touch should not be called for inactive users
        mock_api_key.touch.assert_not_called()

    @pytest.mark.asyncio
    async def test_authenticate_with_inactive_service(self, mock_data_factory):
        """Test authentication with service key for inactive service."""
        raw_key = f"service-key-{uuid4().hex[:8]}"
        mock_service = self.create_mock_service(mock_data_factory, is_active=False)
        mock_service_key = self.create_mock_service_key(
            mock_data_factory, service=mock_service, raw_key=raw_key
        )

        self.service_key_rows = [mock_service_key]

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, raw_key)

        assert exc_info.value.reason == "service is inactive"
        # touch should not be called for inactive services
        mock_service_key.touch.assert_not_called()

    @pytest.mark.asyncio
    async def test_key_last_used_timestamp_updated(self, mock_data_factory):
        """Test that API key last_used timestamp is updated via touch()."""
        api_key_data = mock_data_factory.create_api_key_data()
        raw_key = api_key_data["raw_key"]

        mock_user = self.create_mock_user(mock_data_factory)
        mock_api_key = self.create_mock_api_key(
            mock_data_factory, user=mock_user, raw_key=raw_key
        )

        self.api_key_rows = [mock_api_key]

        await self.backend.authenticate(self.mock_db, raw_key)

        # Verify touch was called to update last_used timestamp
        mock_api_key.touch.assert_called_once()

    @pytest.mark.asyncio
    async def test_service_key_last_used_timestamp_updated(self, mock_data_factory):
        """Test that service key last_used timestamp is updated via touch()."""
        raw_key = f"service-key-{uuid4().hex[:8]}"
        mock_service = self.create_mock_service(mock_data_factory)
        mock_service_key = self.create_mock_service_key(
            mock_data_factory, service=mock_service, raw_key=raw_key
        )

        self.service_key_rows = [mock_service_key]

        await self.backend.authenticate(self.mock_db, raw_key)

        # Verify touch was called to update last_used timestamp
        mock_service_key.touch.assert_called_once()

    @pytest.mark.asyncio
    async def test_authenticate_with_valid_client_key(self, mock_data_factory):
        """Authenticate using a Client's API key."""
        client, raw_secret = self.create_mock_client(mock_data_factory)
        self.client_rows = [client]
        client.verify_secret = MagicMock(wraps=client.verify_secret)

        principal, key_type = await self.backend.authenticate(
            self.mock_db, raw_secret
        )

        assert principal == client
        assert key_type == "client"
        client.verify_secret.assert_called_once_with(raw_secret)

    @pytest.mark.asyncio
    async def test_authenticate_with_invalid_client_secret(self, mock_data_factory):
        """Invalid secret for a Client should raise AuthError."""
        client, raw_secret = self.create_mock_client(mock_data_factory)
        self.client_rows = [client]
        client.verify_secret = MagicMock(wraps=client.verify_secret)

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, "wrong-secret")

        assert exc_info.value.reason == "API key invalid, revoked, or expired"
        client.verify_secret.assert_called_once_with("wrong-secret")

    @pytest.mark.asyncio
    async def test_authenticate_with_inactive_client(self, mock_data_factory):
        """Inactive clients should not authenticate."""
        client, raw_secret = self.create_mock_client(mock_data_factory, is_active=False)
        self.client_rows = [client]

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, raw_secret)

        assert exc_info.value.reason == "API key invalid, revoked, or expired"

    @pytest.mark.asyncio
    async def test_get_client_rows_filters_inactive_clients(self, mock_data_factory):
        """Client lookup returns only active clients."""
        active_client, _ = self.create_mock_client(mock_data_factory, is_active=True)
        inactive_client, _ = self.create_mock_client(mock_data_factory, is_active=False)
        self.client_rows = [inactive_client, active_client]

        rows = await self.backend._get_client_rows(self.mock_db)

        assert rows == [active_client]

    @pytest.mark.asyncio
    async def test_get_key_row_filters_expired_keys(self, mock_data_factory):
        """API key lookup rejects expired keys."""
        test_digest = "test-digest"
        expired = self.create_mock_api_key(
            mock_data_factory,
            raw_key="raw",
            valid_to=datetime.now(timezone.utc) - timedelta(seconds=1),
        )
        expired.digest = test_digest
        self.api_key_rows = [expired]

        row = await self.backend._get_key_row(self.mock_db, test_digest)

        assert row is None

    @pytest.mark.asyncio
    async def test_get_service_key_row_filters_expired_keys(self, mock_data_factory):
        """Service key lookup rejects expired keys."""
        test_digest = "test-digest"
        expired = self.create_mock_service_key(
            mock_data_factory,
            raw_key="raw",
            valid_to=datetime.now(timezone.utc) - timedelta(seconds=1),
        )
        expired.digest = test_digest
        self.service_key_rows = [expired]

        row = await self.backend._get_service_key_row(self.mock_db, test_digest)

        assert row is None

    @pytest.mark.asyncio
    async def test_authenticate_with_empty_api_key(self):
        """Test authentication with empty API key."""
        self.api_key_rows = []
        self.service_key_rows = []

        with pytest.raises(AuthError) as exc_info:
            await self.backend.authenticate(self.mock_db, "")

        assert exc_info.value.reason == "API key invalid, revoked, or expired"

    @pytest.mark.asyncio
    async def test_digest_of_called_correctly(self, monkeypatch):
        """Test that ApiKey.digest_of is called with the raw key."""
        raw_key = "test-api-key-12345"
        calls = []

        def _digest_of(value):
            calls.append(value)
            return "mocked-digest"

        monkeypatch.setattr("tigrbl_auth.services.auth_backends.ApiKey.digest_of", staticmethod(_digest_of))

        try:
            await self.backend.authenticate(self.mock_db, raw_key)
        except AuthError:
            pass  # Expected

        assert calls == [raw_key]


@pytest.mark.unit
class TestBackendIntegration:
    """Integration tests for backend components working together."""

    @pytest.mark.asyncio
    async def test_password_and_api_key_backends_work_independently(self):
        """Test that both backends can be used independently."""
        password_backend = PasswordBackend()
        api_key_backend = ApiKeyBackend()

        # Verify they are different instances
        assert password_backend is not api_key_backend
        assert isinstance(password_backend, PasswordBackend)
        assert isinstance(api_key_backend, ApiKeyBackend)

        # Verify they have different methods
        assert hasattr(password_backend, "authenticate")
        assert hasattr(api_key_backend, "authenticate")
        assert hasattr(password_backend, "_get_user_candidates")
        assert hasattr(api_key_backend, "_get_key_row")
        assert hasattr(api_key_backend, "_get_service_key_row")

    def test_auth_error_consistency(self):
        """Test that AuthError is consistent across backends."""
        # Both backends should raise the same AuthError type
        error1 = AuthError("password error")
        error2 = AuthError("api key error")

        assert isinstance(error1, type(error2))
        assert isinstance(error1, AuthError)
        assert isinstance(error2, AuthError)
