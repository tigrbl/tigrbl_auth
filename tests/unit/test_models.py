"""
Unit tests for tigrbl_auth.tables module.

Tests ORM model creation, validation, relationships, hybrid properties, and methods.
"""

import uuid

import pytest

from tigrbl_identity_storage.tables import (
    Client,
    CredentialApiKey,
    CredentialServiceKey,
    ServiceIdentity,
    Tenant,
    User,
)
from tigrbl_identity_jose.key_management import hash_pw


@pytest.mark.unit
class TestTenantModel:
    """Test Tenant model functionality."""

    def test_tenant_basic_properties(self, sample_tenant_data):
        """Test tenant basic properties without database."""
        tenant = Tenant(**sample_tenant_data)

        assert tenant.slug == sample_tenant_data["slug"]
        assert tenant.name == sample_tenant_data["name"]


@pytest.mark.unit
class TestClientModel:
    """Test OAuth Client model functionality."""

    def test_invalid_client_id_format_raises_error(self):
        """Test that invalid client_id formats raise ValueError."""
        tenant_id = uuid.uuid4()

        invalid_client_ids = [
            "short",  # Too short (< 8 chars)
            "a" * 65,  # Too long (> 64 chars)
            "invalid@id",  # Invalid characters
            "has spaces",  # Spaces not allowed
            "has.dots",  # Dots not allowed
            "",  # Empty string
        ]

        for client_id in invalid_client_ids:
            with pytest.raises(ValueError, match="invalid client_id format"):
                Client.new(
                    tenant_id=tenant_id,
                    client_id=client_id,
                    client_secret="test-secret",
                    redirects=["https://example.com/callback"],
                )


@pytest.mark.unit
class TestUserModel:
    """Test User model functionality."""

    def test_user_new_method_basic(self):
        """Test creating a user using the new() class method."""
        tenant_id = uuid.uuid4()
        username = "testuser"
        email = "test@example.com"
        password = "TestPassword123!"

        user = User.new(
            tenant_id=tenant_id, username=username, email=email, password=password
        )

        assert user.tenant_id == tenant_id
        assert user.username == username
        assert user.email == email

    def test_user_password_verification_with_hash(self):
        """Test user password verification."""
        tenant_id = uuid.uuid4()
        password = "TestPassword123!"

        user = User.new(
            tenant_id=tenant_id,
            username="testuser",
            email="test@example.com",
            password=password,
        )
        # Set password hash manually since User.new doesn't set it
        user.password_hash = hash_pw(password)

        # Test correct password verification
        assert user.verify_password(password) is True

        # Test incorrect password verification
        assert user.verify_password("wrong-password") is False

    def test_user_password_verification_with_none_hash(self):
        """Test user password verification when password_hash is None."""
        user = User.new(
            tenant_id=uuid.uuid4(),
            username="testuser",
            email="test@example.com",
            password="TestPassword123!",
        )
        user.password_hash = None

        # Should return False when no password hash is set
        assert user.verify_password("TestPassword123!") is False


@pytest.mark.unit
class TestCredentialApiKeyModel:
    """Test CredentialApiKey model functionality."""

    def test_api_key_raw_key_getter_raises_error(self):
        """Test that accessing raw_key property raises AttributeError."""
        api_key = CredentialApiKey(principal_id=str(uuid.uuid4()), principal_kind="user", label="Test API Key")

        with pytest.raises(AttributeError, match="raw_key is write-only"):
            _ = api_key.raw_key

    def test_api_key_digest_of_static_method(self):
        """Test CredentialApiKey.digest_of static method."""
        test_key = "test-api-key-123"
        digest = CredentialApiKey.digest_of(test_key)

        assert isinstance(digest, str)
        assert len(digest) == 64  # blake2b with digest_size=32 produces 64 hex chars

        # Should be deterministic
        assert CredentialApiKey.digest_of(test_key) == digest

        # Different keys should produce different digests
        assert CredentialApiKey.digest_of("different-key") != digest

    def test_api_key_raw_key_setter(self):
        """Test API key raw_key setter updates digest."""
        api_key = CredentialApiKey(principal_id=str(uuid.uuid4()), principal_kind="user", label="Test API Key")
        raw_key = "test-api-key-123"

        api_key.raw_key = raw_key

        expected_digest = CredentialApiKey.digest_of(raw_key)
        assert api_key.digest == expected_digest


@pytest.mark.unit
class TestCredentialServiceKeyModel:
    """Test CredentialServiceKey model functionality."""

    def test_service_key_raw_key_getter_raises_error(self):
        """Test that accessing raw_key property raises AttributeError."""
        service_key = CredentialServiceKey(service_identity_id=uuid.uuid4(), label="Test Service Key")

        with pytest.raises(AttributeError, match="raw_key is write-only"):
            _ = service_key.raw_key

    def test_service_key_digest_of_static_method(self):
        """Test CredentialServiceKey.digest_of static method."""
        test_key = "test-service-key-123"
        digest = CredentialServiceKey.digest_of(test_key)

        assert isinstance(digest, str)
        assert len(digest) == 64

        # Should be deterministic
        assert CredentialServiceKey.digest_of(test_key) == digest

        # Different keys should produce different digests
        assert CredentialServiceKey.digest_of("different-key") != digest

    def test_service_key_raw_key_setter(self):
        """Test service key raw_key setter updates digest."""
        service_key = CredentialServiceKey(service_identity_id=uuid.uuid4(), label="Test Service Key")
        raw_key = "test-service-key-123"

        service_key.raw_key = raw_key

        expected_digest = CredentialServiceKey.digest_of(raw_key)
        assert service_key.digest == expected_digest

    def test_service_key_schema_uses_service_identity_id(self):
        """Ensure CredentialServiceKey API schema exposes correct fields."""
        from tigrbl_identity_server.surfaces import AdminRouter

        create_schema = AdminRouter.schemas.CredentialServiceKey.create.in_.model_json_schema()
        create_fields = AdminRouter.schemas.CredentialServiceKey.create.in_.model_fields
        read_schema = AdminRouter.schemas.CredentialServiceKey.read.out.model_json_schema()

        # Only expected fields are exposed on create
        assert set(create_fields.keys()) == {
            "label",
            "service_identity_id",
            "valid_from",
            "valid_to",
        }
        # Only label and service_identity_id are required
        assert set(create_schema.get("required", [])) == {"label", "service_identity_id"}
        # Digest should not be part of the create payload
        assert "digest" not in create_fields
        # Validity window fields are included in responses
        assert "valid_from" in read_schema.get("properties", {})
        assert "valid_to" in read_schema.get("properties", {})
        # Schemas still reference service_identity_id and exclude user_id
        assert "service_identity_id" in create_fields
        assert "user_id" not in create_fields
        assert "service_identity_id" in AdminRouter.schemas.CredentialServiceKey.read.out.model_fields
        assert "user_id" not in AdminRouter.schemas.CredentialServiceKey.read.out.model_fields


@pytest.mark.unit
class TestModelIntegration:
    """Test model interactions and edge cases."""

    def test_api_key_and_service_key_digest_compatibility(self):
        """Test that credential key tables use the same digest algorithm."""
        test_key = "test-key-123"

        api_key_digest = CredentialApiKey.digest_of(test_key)
        service_key_digest = CredentialServiceKey.digest_of(test_key)

        # Should produce same digest for same input
        assert api_key_digest == service_key_digest

    def test_client_id_regex_pattern(self):
        """Test the client ID regex pattern directly."""
        from tigrbl_auth.tables import _CLIENT_ID_RE

        valid_patterns = [
            "simple123",
            "test-client",
            "Client_ID",
            "UPPER-lower",
            "12345678",
            "a" * 64,
        ]

        invalid_patterns = [
            "short",
            "a" * 65,
            "has@symbol",
            "has spaces",
            "has.dots",
            "has/slash",
            "",
        ]

        for pattern in valid_patterns:
            assert _CLIENT_ID_RE.fullmatch(pattern), f"Should match: {pattern}"

        for pattern in invalid_patterns:
            assert not _CLIENT_ID_RE.fullmatch(pattern), f"Should not match: {pattern}"

    def test_service_basic_creation(self):
        """Test basic service creation without database."""
        service = ServiceIdentity(tenant_id=uuid.uuid4(), name="test-service", is_active=True)

        assert service.name == "test-service"
        assert service.is_active is True
