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
from tigrbl_identity_storage.tables.crypto_key import scrub_key_material
from tigrbl_identity_storage.tables.crypto_key_version import scrub_key_version_material


def test_key_tables_are_storage_owned_and_exported() -> None:
    assert CryptoKey.__tablename__ == "crypto_keys"
    assert CryptoKeyVersion.__tablename__ == "crypto_key_versions"
    assert PrincipalKeyBinding.__tablename__ == "principal_key_bindings"
    assert KeyEnvelope.__tablename__ == "key_envelopes"
    assert KeyAttestationEvidence.__tablename__ == "key_attestation_evidence"
    assert callable(CryptoKey.rotate_record)
    assert not hasattr(CryptoKey, "sign")
    assert not hasattr(CryptoKey, "verify")
    assert not hasattr(CryptoKey, "publish_jwks")
    assert callable(CryptoKeyVersion.create_version)


def test_key_material_scrubbers_remove_private_fields() -> None:
    payload = {
        "kid": "kid-1",
        "provider_key_ref": "secret-ref",
        "public_material": {"kid": "kid-1", "kty": "PQC", "x": "pub", "d": "priv"},
    }

    assert scrub_key_material(payload) == {
        "kid": "kid-1",
        "public_material": {"kid": "kid-1", "kty": "PQC", "x": "pub"},
    }
    assert scrub_key_version_material(payload) == {
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
