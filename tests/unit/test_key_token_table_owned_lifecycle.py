from __future__ import annotations

from tigrbl_identity_storage.tables import (
    CryptoKey,
    CryptoKeyVersion,
    KeyAttestationEvidence,
    KeyEnvelope,
    PrincipalKeyBinding,
    RevokedToken,
    TokenRecord,
)
from tigrbl_identity_storage.tables._security_ctx import (
    JWT_CODER_CTX,
    KEY_PROVIDER_CTX,
    SIGNER_CTX,
    VERIFIER_CTX,
    stash_security_providers,
)
from tigrbl_identity_jose import materialize_public_key_record
from tigrbl_identity_storage_runtime import normalize_key_usage_values


def test_key_tables_are_storage_owned_and_exported() -> None:
    key_columns = CryptoKey.__table__.columns

    assert CryptoKey.__tablename__ == "crypto_keys"
    assert "key_usages" in key_columns
    assert "key_profiles" not in key_columns
    assert CryptoKeyVersion.__tablename__ == "crypto_key_versions"
    assert PrincipalKeyBinding.__tablename__ == "principal_key_bindings"
    assert KeyEnvelope.__tablename__ == "key_envelopes"
    assert KeyAttestationEvidence.__tablename__ == "key_attestation_evidence"
    assert callable(CryptoKey.handlers.update.core)
    assert not hasattr(CryptoKey, "sign")
    assert not hasattr(CryptoKey, "verify")
    assert not hasattr(CryptoKey, "publish_jwks")
    assert callable(CryptoKeyVersion.handlers.create.core)


def test_key_usage_defaults_and_narrows_allowed_ops() -> None:
    assert normalize_key_usage_values(
        {"key_kind": "symmetric", "key_usages": ["kek"]}
    ) == {
        "key_kind": "symmetric",
        "key_usages": ["kek"],
        "allowed_ops": ["wrap_key", "unwrap_key"],
    }
    assert normalize_key_usage_values(
        {"key_kind": "symmetric", "key_usages": ["kek"], "allowed_ops": ["wrap_key"]}
    ) == {
        "key_kind": "symmetric",
        "key_usages": ["kek"],
        "allowed_ops": ["wrap_key"],
    }


def test_key_material_scrubbers_remove_private_fields() -> None:
    payload = {
        "kid": "kid-1",
        "provider_key_ref": "secret-ref",
        "public_material": {"kid": "kid-1", "kty": "PQC", "x": "pub", "d": "priv"},
    }

    assert materialize_public_key_record(payload) == {
        "kid": "kid-1",
        "public_material": {"kid": "kid-1", "kty": "PQC", "x": "pub"},
    }
    assert materialize_public_key_record(payload) == {
        "kid": "kid-1",
        "public_material": {"kid": "kid-1", "kty": "PQC", "x": "pub"},
    }


def test_token_records_track_signing_key_provenance() -> None:
    columns = TokenRecord.__table__.columns

    assert "jti" in columns
    assert "kid" in columns
    assert "key_version" in columns
    assert "token_status" in columns
    assert "refresh_family_id" in RevokedToken.__table__.columns


def test_security_provider_context_helper_uses_stable_keys() -> None:
    ctx = {}
    provider = object()
    signer = object()
    verifier = object()
    coder = object()

    stash_security_providers(ctx, key_provider=provider, signer=signer, verifier=verifier, jwt_coder=coder)

    assert ctx[KEY_PROVIDER_CTX] is provider
    assert ctx[SIGNER_CTX] is signer
    assert ctx[VERIFIER_CTX] is verifier
    assert ctx[JWT_CODER_CTX] is coder
