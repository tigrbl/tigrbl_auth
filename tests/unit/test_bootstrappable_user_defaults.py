from __future__ import annotations

from tigrbl_auth.services.key_management import verify_pw
from tigrbl_auth.tables import User
from tigrbl_identity_storage.tables.user import DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD


def test_user_is_bootstrappable_with_default_superuser_row() -> None:
    assert hasattr(User, "ensure_bootstrapped")

    row = User.DEFAULT_ROWS[0]
    assert row["username"] == "admin"
    assert row["email"] == "admin@example.com"
    assert row["is_admin"] is True
    assert row["is_superuser"] is True
    assert row["must_change_password"] is True
    assert verify_pw(DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD, row["password_hash"])
