from __future__ import annotations

import asyncio
import base64
import json

import pytest

from tigrbl_auth import load_pqc_public_jwk, load_pqc_signing_jwk, sign_jws, verify_jws
from tigrbl_auth.jwtoken import JWTCoder
from tigrbl_auth.runtime_cfg import settings as facade_settings
from tigrbl_auth_protocol_oauth.standards._rfc9700.sender_constraints import discovery_policy_metadata
from tigrbl_identity_jose import key_management
from tigrbl_identity_jose.pqc import (
    ML_DSA_65_ALG,
    PQC_REQUIRED_DEPENDENCY,
    generate_pqc_signature_keypair,
    pqc_backend_report,
    pqc_public_jwk,
    pqc_signing_jwk,
    sign_pqc_payload,
    verify_pqc_signature,
)
from tigrbl_identity_runtime.deployment import resolve_deployment
from tigrbl_identity_runtime.settings import settings as runtime_settings


def _jwt_header(token: str) -> dict[str, object]:
    header_segment = token.split(".")[0]
    padded = header_segment + "=" * (-len(header_segment) % 4)
    return json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))


def test_pqc_signature_round_trip_uses_required_backend() -> None:
    report = pqc_backend_report()
    assert report["library"] == "pqcrypto"
    assert report["required_dependency"] == PQC_REQUIRED_DEPENDENCY
    assert report["available"] is True

    keypair = generate_pqc_signature_keypair()
    payload = b"tigrbl-auth-pqc-runtime"
    signature = sign_pqc_payload(payload, keypair.secret_key)

    assert keypair.algorithm == ML_DSA_65_ALG
    assert verify_pqc_signature(payload, signature, keypair.public_key)
    assert not verify_pqc_signature(b"tampered", signature, keypair.public_key)


def test_compact_jws_uses_ml_dsa_65_signature() -> None:
    keypair = generate_pqc_signature_keypair()
    signing_jwk = pqc_signing_jwk(keypair.secret_key, keypair.public_key, kid="pqc-jws-test")
    public_jwk = pqc_public_jwk(keypair.public_key, kid="pqc-jws-test")

    token = asyncio.run(sign_jws("payload", signing_jwk, alg=ML_DSA_65_ALG))

    assert _jwt_header(token)["alg"] == ML_DSA_65_ALG
    assert asyncio.run(verify_jws(token, public_jwk)) == "payload"

    tampered = token.rsplit(".", 1)[0] + ".AA"
    with pytest.raises(RuntimeError, match="invalid JWS signature"):
        asyncio.run(verify_jws(tampered, public_jwk))


def test_pqc_key_management_persists_signing_jwk_and_exports_public_jwk(tmp_path) -> None:
    key_path = tmp_path / "jwt_ml_dsa_65.json"

    created = key_management.generate_pqc_jwt_keypair(path=key_path)
    signing_jwk = key_management.load_pqc_signing_jwk(path=key_path)
    public_jwk = key_management.load_pqc_public_jwk(path=key_path)

    assert key_path.is_file()
    assert signing_jwk["kid"] == created["kid"]
    assert signing_jwk["alg"] == ML_DSA_65_ALG
    assert "d" in signing_jwk
    assert public_jwk["kid"] == signing_jwk["kid"]
    assert public_jwk["x"] == signing_jwk["x"]
    assert "d" not in public_jwk


def test_top_level_pqc_jwk_exports_share_runtime_key(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(key_management, "_DEFAULT_PQC_KEY_PATH", tmp_path / "jwt_ml_dsa_65.json")

    signing_jwk = load_pqc_signing_jwk()
    public_jwk = load_pqc_public_jwk()

    assert signing_jwk["alg"] == ML_DSA_65_ALG
    assert public_jwk["x"] == signing_jwk["x"]
    assert "d" not in public_jwk


def test_jwt_coder_signs_and_verifies_ml_dsa_65_when_configured(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(key_management, "_DEFAULT_PQC_KEY_PATH", tmp_path / "jwt_ml_dsa_65.json")
    monkeypatch.setattr(facade_settings, "jwt_signing_alg", ML_DSA_65_ALG)
    monkeypatch.setattr(facade_settings, "enable_pqc_jose", True)

    coder = JWTCoder.default()
    token = coder.sign(
        sub="subject-1",
        tid="tenant-1",
        issuer="https://issuer.example",
        audience="https://api.example",
    )

    assert _jwt_header(token)["alg"] == ML_DSA_65_ALG
    payload = coder.decode(
        token,
        issuer="https://issuer.example",
        audience="https://api.example",
        verify_revocation=False,
    )
    assert payload["sub"] == "subject-1"
    assert payload["tid"] == "tenant-1"
    assert payload["iss"] == "https://issuer.example"
    assert payload["aud"] == "https://api.example"


def test_oauth_metadata_advertises_ml_dsa_when_pqc_profile_enabled(monkeypatch) -> None:
    monkeypatch.setattr(runtime_settings, "enable_pqc_jose", True)
    monkeypatch.setattr(runtime_settings, "jwt_signing_alg", ML_DSA_65_ALG)
    monkeypatch.setattr(runtime_settings, "enable_rfc9068", True)

    metadata = discovery_policy_metadata(resolve_deployment(runtime_settings, profile="production"))

    assert ML_DSA_65_ALG in metadata["access_token_signing_alg_values_supported"]
