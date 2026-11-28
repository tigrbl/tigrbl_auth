from __future__ import annotations

from tba_runtime_identity_administration.bootstrap import DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD
from tba_storage_core.tables import User
from tba_provider_secret_hashing_bcrypt import BcryptSecretHasher


def test_user_storage_does_not_materialize_a_bootstrap_secret() -> None:
    assert not hasattr(User, "DEFAULT_ROWS")
    assert not hasattr(User, "ensure_bootstrapped")

    encoded = BcryptSecretHasher().hash_secret(
        DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD
    ).encoded
    assert BcryptSecretHasher().verify_secret(
        DEFAULT_BOOTSTRAP_SUPERUSER_PASSWORD, encoded
    ).verified
