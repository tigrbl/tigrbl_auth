from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import replace

import cbor2
import pytest
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from tigrbl_auth_protocol_webauthn import (
    AuthenticationExpectation,
    AuthenticationVerificationError,
    AuthenticatorAssertionResponse,
    AuthenticatorAttestationResponse,
    PublicKeyCredential,
    RegistrationExpectation,
    RegistrationVerificationError,
    WebAuthnVersion,
    build_creation_options,
    build_request_options,
    features_for,
    verify_authentication_response,
    verify_registration_response,
)
from tigrbl_security_cose import decode_cose_key, verify_detached_signature


def _b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _client_data(
    kind: str, challenge: bytes, origin: str = "https://login.example"
) -> bytes:
    return json.dumps(
        {
            "type": kind,
            "challenge": _b64(challenge),
            "origin": origin,
            "crossOrigin": False,
        },
        separators=(",", ":"),
    ).encode()


def _key_material():
    private = ec.generate_private_key(ec.SECP256R1())
    numbers = private.public_key().public_numbers()
    cose = cbor2.dumps(
        {
            1: 2,
            3: -7,
            -1: 1,
            -2: numbers.x.to_bytes(32, "big"),
            -3: numbers.y.to_bytes(32, "big"),
        },
        canonical=True,
    )
    return private, cose


def _registration_fixture():
    private, cose = _key_material()
    challenge = b"r" * 32
    raw_id = b"credential-identifier"
    client = _client_data("webauthn.create", challenge)
    auth = (
        hashlib.sha256(b"login.example").digest()
        + bytes([0x45])
        + (0).to_bytes(4, "big")
        + (b"\x00" * 16)
        + len(raw_id).to_bytes(2, "big")
        + raw_id
        + cose
    )
    attestation = cbor2.dumps({"fmt": "none", "authData": auth, "attStmt": {}})
    response = PublicKeyCredential(
        id=_b64(raw_id),
        raw_id=raw_id,
        response=AuthenticatorAttestationResponse(client, attestation, ("internal",)),
    )
    expectation = RegistrationExpectation(
        ceremony_id="ceremony:registration",
        tenant_id="tenant:1",
        principal_id="principal:1",
        rp_id="login.example",
        origin="https://login.example",
        challenge=challenge,
        user_handle=b"user-handle",
        user_verification="required",
    )
    return private, response, expectation


def test_cose_key_and_detached_signature_are_strict():
    private, cose = _key_material()
    message = b"signed message"
    signature = private.sign(message, ec.ECDSA(hashes.SHA256()))
    assert decode_cose_key(cose)[3] == -7
    assert verify_detached_signature(
        public_key=cose, algorithm=-7, message=message, signature=signature
    )
    assert not verify_detached_signature(
        public_key=cose, algorithm=-7, message=message + b"!", signature=signature
    )
    with pytest.raises(ValueError, match="canonical"):
        decode_cose_key(cbor2.dumps({3: -7, 1: 2, -1: 1, -2: b"x" * 32, -3: b"y" * 32}))


def test_registration_and_authentication_complete_end_to_end():
    private, response, expectation = _registration_fixture()
    registration = verify_registration_response(response, expected=expectation)
    source = registration.credential
    assert source.external_id == response.raw_id
    assert source.backup_eligible is False
    assert source.binding.principal_id == "principal:1"

    challenge = b"a" * 32
    client = _client_data("webauthn.get", challenge)
    authenticator_data = (
        hashlib.sha256(b"login.example").digest()
        + bytes([0x05])
        + (1).to_bytes(4, "big")
    )
    signature = private.sign(
        authenticator_data + hashlib.sha256(client).digest(), ec.ECDSA(hashes.SHA256())
    )
    assertion = PublicKeyCredential(
        id=response.id,
        raw_id=response.raw_id,
        response=AuthenticatorAssertionResponse(
            client, authenticator_data, signature, b"user-handle"
        ),
    )
    verified = verify_authentication_response(
        assertion,
        expected=AuthenticationExpectation(
            ceremony_id="ceremony:authentication",
            rp_id="login.example",
            origin="https://login.example",
            challenge=challenge,
            credential=source,
            user_verification="required",
        ),
    )
    assert verified.principal_id == "principal:1"
    assert verified.sign_count == 1
    assert verified.evidence.user_verification.verified


def test_registration_rejects_origin_and_authentication_rejects_replay_counter():
    private, response, expectation = _registration_fixture()
    bad = replace(expectation, origin="https://evil.example")
    with pytest.raises(RegistrationVerificationError, match="origin"):
        verify_registration_response(response, expected=bad)

    source = verify_registration_response(response, expected=expectation).credential
    source = replace(source, sign_count=2)
    challenge = b"a" * 32
    client = _client_data("webauthn.get", challenge)
    authenticator_data = (
        hashlib.sha256(b"login.example").digest()
        + bytes([0x05])
        + (2).to_bytes(4, "big")
    )
    signature = private.sign(
        authenticator_data + hashlib.sha256(client).digest(), ec.ECDSA(hashes.SHA256())
    )
    assertion = PublicKeyCredential(
        id=response.id,
        raw_id=response.raw_id,
        response=AuthenticatorAssertionResponse(client, authenticator_data, signature),
    )
    with pytest.raises(AuthenticationVerificationError, match="counter"):
        verify_authentication_response(
            assertion,
            expected=AuthenticationExpectation(
                "ceremony:authentication",
                "login.example",
                "https://login.example",
                challenge,
                source,
            ),
        )


def test_options_and_level3_features_are_explicit():
    creation = build_creation_options(
        rp_id="login.example",
        rp_name="Example",
        user_handle=b"user",
        user_name="user@example.com",
        user_display_name="User",
    )
    request = build_request_options(rp_id="login.example")
    assert len(creation.challenge) == len(request.challenge) == 32
    assert "conditional-mediation" in features_for(WebAuthnVersion.LEVEL_3)
    assert "conditional-mediation" not in features_for(WebAuthnVersion.LEVEL_2)
