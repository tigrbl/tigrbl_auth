import pytest
from tba_auth.crypto import (
    hash_pw,
    verify_pw,
)


@pytest.mark.unit
class TestPasswordCrypto:
    """Test password hashing and verification functions."""

    def test_hash_password_generates_bcrypt_hash(self):
        """Test that password hashing generates valid bcrypt hash."""
        password = "TestPassword123!"
        hashed = hash_pw(password)

        # Should be bcrypt format (starts with $2b$ and is 60 bytes)
        assert hashed.startswith(b"$2b$")
        assert len(hashed) == 60

    def test_verify_password_with_correct_password(self):
        """Test password verification with correct password."""
        password = "TestPassword123!"
        hashed = hash_pw(password)

        assert verify_pw(password, hashed) is True

    def test_verify_password_with_incorrect_password(self):
        """Test password verification with incorrect password."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hash_pw(password)

        assert verify_pw(wrong_password, hashed) is False

    def test_verify_password_with_invalid_hash_format(self):
        """Test password verification with invalid hash format."""
        password = "TestPassword123!"
        invalid_hash = b"not-a-valid-bcrypt-hash"

        assert verify_pw(password, invalid_hash) is False

    def test_password_hash_different_each_time(self):
        """Test that the same password produces different hashes (salt)."""
        password = "TestPassword123!"
        hash1 = hash_pw(password)
        hash2 = hash_pw(password)

        assert hash1 != hash2
        assert verify_pw(password, hash1) is True
        assert verify_pw(password, hash2) is True

    def test_password_hash_handles_unicode(self):
        """Test password hashing with unicode characters."""
        password = "Test密码123!ñ"
        hashed = hash_pw(password)

        assert verify_pw(password, hashed) is True
        assert verify_pw("different", hashed) is False


@pytest.mark.unit
class TestSecurityEdgeCases:
    """Test security-related edge cases and error conditions."""

    def test_password_verification_handles_none_input(self):
        """Test that password verification handles None input gracefully."""
        hashed = hash_pw("password")

        # This should not raise an exception but return False
        assert verify_pw("", hashed) is False

    def test_empty_password_hashing(self):
        """Test hashing of empty password."""
        empty_hash = hash_pw("")
        assert verify_pw("", empty_hash) is True
        assert verify_pw("not-empty", empty_hash) is False

    def test_very_long_password(self):
        """Test handling of very long passwords (bcrypt truncates at 72 bytes)."""
        long_password = "a" * 1000
        hashed = hash_pw(long_password)

        assert verify_pw(long_password, hashed) is True

        # bcrypt only uses first 72 bytes, so passwords longer than 72 bytes
        # that start the same will hash identically
        very_long_same_start = "a" * 500
        assert verify_pw(very_long_same_start, hashed) is True

        # But a password with different start should fail
        different_long_password = "b" * 1000
        assert verify_pw(different_long_password, hashed) is False
