"""Exercise issuance through Tigrbl and verification through runtime composition."""

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from time import time

import pytest
from cryptography import x509
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.x509.oid import NameOID
from httpx import ASGITransport, AsyncClient
from tigrbl import TigrblApp

from tba_app_backend_wic_ca import WicCaSettings, build_app
from tba_concrete_jwt import decode_jwt_unverified
from tba_contracts_proof_of_possession import (
    ConfirmationKeyBinding,
    PossessionProof,
    PossessionProofContext,
    PossessionProofVerificationRequest,
)
from tba_primitives_identity import base64url_encode
from tba_profile_workload_proof_wimse_wpt import present_wit
from tba_provider_jose_cryptography import JwsCryptographyProvider
from tba_provider_replay_memory import MemoryReplayCheckProvider
from tba_router_wit_issuance import build_wit_issuance_router
from tba_runtime_identity.composition.workload_identity import (
    WorkloadIdentityRuntimeConfig,
    build_workload_identity_composition,
)
from tba_runtime_identity.workload.wit_token_service import (
    WitIssuerConfig,
    WitTokenService,
)

IDENTITY = "wimse://example.org/workload"
AUDIENCE = "https://service.example.org/work"


async def authenticate(request):
    if request.headers.get("authorization") == "Enrollment fixture":
        return "workload"
    return None


async def resolve_identity(principal):
    if principal == "workload":
        return IDENTITY
    return None


def jwk(key):
    public = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return {
        "kty": "OKP",
        "crv": "Ed25519",
        "alg": "EdDSA",
        "x": base64url_encode(public),
    }


@pytest.mark.asyncio
async def test_wic_ca_signs_only_the_enrolled_identity(tmp_path):
    key = Ed25519PrivateKey.generate()
    workload_key = Ed25519PrivateKey.generate()
    now = datetime.now(timezone.utc)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Test CA")])
    ca = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(days=1))
        .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
        .sign(key, None)
    )
    cert_path = tmp_path / "ca.pem"
    key_path = tmp_path / "key.pem"
    cert_path.write_bytes(ca.public_bytes(Encoding.PEM))
    key_path.write_bytes(
        key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
    )
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(x509.Name([]))
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.UniformResourceIdentifier("wimse://example.org/admin")]
            ),
            critical=True,
        )
        .sign(workload_key, None)
    )
    app = build_app(
        WicCaSettings("example.org", cert_path, key_path),
        authenticate=authenticate,
        resolve_identity=resolve_identity,
    )
    body = {"csr_pem": csr.public_bytes(Encoding.PEM).decode()}
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://ca.example.org"
    ) as client:
        assert (await client.post("/wic/issue", json=body)).status_code == 401
        response = await client.post(
            "/wic/issue", headers={"Authorization": "Enrollment fixture"}, json=body
        )
        invalid = await client.post(
            "/wic/issue",
            headers={"Authorization": "Enrollment fixture"},
            json={"csr_pem": "-----BEGIN CERTIFICATE REQUEST-----\nbad"},
        )
        assert invalid.status_code == 400
    assert response.status_code == 200, response.text
    assert response.headers["cache-control"] == "no-store"
    certificate = x509.load_pem_x509_certificate(
        response.json()["certificate_pem"].encode()
    )
    certificate.verify_directly_issued_by(ca)
    san = certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    assert san.value.get_values_for_type(x509.UniformResourceIdentifier) == [IDENTITY]
    assert (
        certificate.public_key().public_bytes_raw()
        == workload_key.public_key().public_bytes_raw()
    )
    assert not certificate.extensions.get_extension_for_class(
        x509.BasicConstraints
    ).value.ca


@pytest.mark.asyncio
async def test_wit_router_and_runtime_wpt_share_replay_protection():
    workload_key = Ed25519PrivateKey.generate()
    issuer_key = Ed25519PrivateKey.generate()
    confirmation = {**jwk(workload_key), "key_ops": ["verify"]}
    signer = JwsCryptographyProvider({"issuer": issuer_key, "workload": workload_key})

    async def authorize_key(principal, proposed):
        return principal == "workload" and proposed == confirmation

    service = WitTokenService(
        signer,
        WitIssuerConfig(
            "example.org", "https://identity.example.org", "issuer", "issuer", "EdDSA"
        ),
        resolve_identity=resolve_identity,
        authorize_confirmation_key=authorize_key,
    )
    app = TigrblApp()
    app.include_router(
        build_wit_issuance_router(service=service, authenticate=authenticate)
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="https://identity.example.org"
    ) as client:
        headers = {"Authorization": "Enrollment fixture"}
        rejected = await client.post(
            "/wit/issue", headers=headers, json={"confirmation_jwk": jwk(issuer_key)}
        )
        assert rejected.status_code == 403
        issued = await client.post(
            "/wit/issue", headers=headers, json={"confirmation_jwk": confirmation}
        )
    assert issued.status_code == 200, issued.text
    assert issued.headers["cache-control"] == "no-store"
    wit = issued.json()["workload_identity_token"]
    composition = build_workload_identity_composition(
        WorkloadIdentityRuntimeConfig(enable_wimse_wit=True, enable_wimse_wpt=True),
        dependencies={
            "credential_provider": object(),
            "credential_verifier": object(),
            "wit_trust_by_domain": {
                "example.org": [{**jwk(issuer_key), "kid": "issuer"}]
            },
            "wpt_replay_store": MemoryReplayCheckProvider(),
        },
    )
    verifier = composition.dependencies["wimse_wpt_verifier"]
    headers = present_wit(
        signer,
        wit,
        workload_key_reference="workload",
        target_uri=AUDIENCE,
        now=int(time()),
    )
    proof = headers["Authorization"].split(" ", 1)[1]
    claims = decode_jwt_unverified(proof).claims
    context = PossessionProofContext(
        audience=AUDIENCE,
        credential_digest=base64url_encode(sha256(wit.encode("ascii")).digest()),
    )
    request = PossessionProofVerificationRequest(
        PossessionProof(
            claims["jti"],
            proof,
            datetime.fromtimestamp(claims["exp"], timezone.utc),
            context,
        ),
        ConfirmationKeyBinding("jwk", confirmation),
        context,
    )
    with pytest.raises(ValueError, match="audience"):
        verifier.authenticate_request(headers.items(), audience=AUDIENCE + "/other")
    authenticated = verifier.authenticate_request(headers.items(), audience=AUDIENCE)
    assert authenticated.claims["sub"] == IDENTITY
    assert authenticated.claims["iss"] == "https://identity.example.org"
    assert not verifier.verify(request).valid
    headers = present_wit(
        signer,
        wit,
        workload_key_reference="workload",
        target_uri=AUDIENCE,
        now=int(time()),
    )
    proof = headers["Authorization"].split(" ", 1)[1]
    claims = decode_jwt_unverified(proof).claims
    request = PossessionProofVerificationRequest(
        PossessionProof(
            claims["jti"],
            proof,
            datetime.fromtimestamp(claims["exp"], timezone.utc),
            context,
        ),
        ConfirmationKeyBinding("jwk", confirmation),
        context,
    )
    assert verifier.verify(request).valid
    with pytest.raises(ValueError, match="replay"):
        verifier.authenticate_request(headers.items(), audience=AUDIENCE)
