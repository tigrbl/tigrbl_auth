"""Exercise deployable WIT issuance and delegated, replay-consuming WPT checks."""

import asyncio
from copy import deepcopy
from hashlib import sha256

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from httpx import ASGITransport, AsyncClient
import pytest
from tigrbl import TigrblApp

from tba_app_backend_wit_issuance import WitIssuerConfig, build_app as build_issuer
from tba_app_backend_wpt_verifier import (
    WptVerifierSettings,
    build_app as build_verifier,
)
from tba_concrete_jwt import decode_jwt_unverified
from tba_contracts_proof_of_possession import (
    ConfirmationKeyBinding,
    PossessionProofContext,
    PossessionProofIssuerPort,
    PossessionProofVerificationRequest,
)
from tba_primitives_identity import base64url_encode
from tba_profile_workload_credential_wimse_wit import issue_wit
from tba_profile_workload_proof_wimse_wpt import (
    WptProofIssuer,
    WptProofVerifier,
    issue_wpt,
    present_wit,
)
from tba_provider_jose_cryptography import JwsCryptographyProvider
from tba_provider_jose_cryptography.jws import sign_compact_jwt
from tba_provider_replay_memory import MemoryReplayCheckProvider
from tba_router_wpt_verification import build_wpt_verification_router
from tba_runtime_identity.composition.workload_identity import (
    WorkloadIdentityRuntimeConfig,
    build_workload_identity_composition,
)

NOW = 1_800_000_000
AUDIENCE = "https://resource.example.org/work"
SUBJECT = "wimse://example.org/workload"


def digest(value):
    return base64url_encode(sha256(value.encode("ascii")).digest())


def jwk(key):
    return {
        "kty": "OKP",
        "crv": "Ed25519",
        "alg": "EdDSA",
        "x": base64url_encode(
            key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        ),
    }


class RecordingReplayStore:
    def __init__(self):
        self.calls = 0
        self.store = MemoryReplayCheckProvider()

    def check_and_store(self, key, *, now, ttl_s):
        self.calls += 1
        return self.store.check_and_store(key, now=now, ttl_s=ttl_s)


@pytest.fixture
def material():
    issuer = Ed25519PrivateKey.generate()
    workload = Ed25519PrivateKey.generate()
    signer = JwsCryptographyProvider({"issuer": issuer, "workload": workload})
    confirmation = jwk(workload)
    wit = issue_wit(
        signer,
        subject=SUBJECT,
        confirmation_jwk=confirmation,
        issuer_key_reference="issuer",
        issuer_key_id="issuer",
        issuer_algorithm="EdDSA",
        issued_at=NOW,
        expires_at=NOW + 900,
        issuer="https://issuer.example.org",
    )
    return (
        signer,
        wit,
        confirmation,
        {"example.org": [{**jwk(issuer), "kid": "issuer"}]},
    )


def proof_body(material, **options):
    signer, wit, _, _ = material
    return {
        "workload_identity_token": wit,
        "workload_proof_token": issue_wpt(
            signer,
            wit,
            workload_key_reference="workload",
            audience=AUDIENCE,
            now=NOW,
            **options,
        ),
    }


async def authenticate(request):
    return {"Bearer recipient": "recipient", "Bearer outsider": "outsider"}.get(
        request.headers.get("authorization")
    )


async def authorize(principal):
    return principal == "recipient"


def remote_app(material, store, *, required=()):
    return build_verifier(
        WptVerifierSettings(AUDIENCE, material[3], required),
        replay_store=store,
        authenticate=authenticate,
        authorize_verification=authorize,
        clock=lambda: NOW,
    )


def client(app):
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="https://verifier.example.org"
    )


def test_carrier_neutral_issuer_round_trips_through_contract(material):
    signer, wit, confirmation, trust = material
    issuer: PossessionProofIssuerPort = WptProofIssuer(
        signer, wit, workload_key_reference="workload", clock=lambda: NOW
    )
    context = PossessionProofContext(
        audience=AUDIENCE,
        accompanying_token_digests={"txn-token": digest("transaction")},
    )
    proof = issuer.issue(context)
    other = issuer.issue(context)
    assert proof.proof_id != other.proof_id
    assert proof.context.credential_digest == digest(wit)
    assert proof.expires_at.timestamp() == NOW + 60
    claims = decode_jwt_unverified(proof.artifact).claims
    assert claims["tth"] == digest("transaction")
    verifier = WptProofVerifier(
        trust_by_domain=trust,
        replay_store=MemoryReplayCheckProvider(),
        clock=lambda: NOW,
    )
    request = PossessionProofVerificationRequest(
        proof, ConfirmationKeyBinding("jwk", confirmation), proof.context
    )
    assert verifier.verify(request).valid
    assert not verifier.verify(request).valid


@pytest.mark.parametrize(
    "context",
    [
        PossessionProofContext(),
        PossessionProofContext(audience=AUDIENCE, credential_digest="wrong"),
        PossessionProofContext(audience=AUDIENCE, target_uri=AUDIENCE + "/other"),
        PossessionProofContext(audience=AUDIENCE, method="POST"),
    ],
)
def test_issuer_rejects_unfulfilled_context_bindings(material, context):
    with pytest.raises(ValueError):
        WptProofIssuer(
            material[0], material[1], workload_key_reference="workload"
        ).issue(context)


@pytest.mark.parametrize("lifetime", [0, -1, 301, True, 1.5])
def test_issuer_rejects_invalid_lifetimes(material, lifetime):
    with pytest.raises(ValueError, match="lifetime"):
        WptProofIssuer(
            material[0],
            material[1],
            workload_key_reference="workload",
            lifetime_seconds=lifetime,
        )


def test_issue_wpt_caps_expiry_and_rejects_expired_wit_and_wrong_key(material):
    signer, wit, _, _ = material
    proof = issue_wpt(
        signer, wit, workload_key_reference="workload", audience=AUDIENCE, now=NOW + 890
    )
    assert decode_jwt_unverified(proof).claims["exp"] == NOW + 900
    with pytest.raises(ValueError, match="expired"):
        issue_wpt(
            signer,
            wit,
            workload_key_reference="workload",
            audience=AUDIENCE,
            now=NOW + 900,
        )
    with pytest.raises(ValueError):
        issue_wpt(
            signer, wit, workload_key_reference="issuer", audience=AUDIENCE, now=NOW
        )


def test_http_presentation_keeps_transaction_binding(material):
    signer, wit, _, _ = material
    headers = present_wit(
        signer,
        wit,
        workload_key_reference="workload",
        target_uri=AUDIENCE + "?q=1#part",
        now=NOW,
        transaction_token="transaction",
    )
    claims = decode_jwt_unverified(headers["Authorization"].split()[1]).claims
    assert claims["aud"] == AUDIENCE
    assert claims["tth"] == digest(headers["Txn-Token"])


@pytest.mark.parametrize(
    "bindings",
    [{"Txn-Token": "x" * 43}, {"txn-token": "bad"}, {"authorization": "x" * 43}],
)
def test_issue_wpt_rejects_invalid_digest_inputs(material, bindings):
    with pytest.raises(ValueError, match="digest"):
        proof_body(material, accompanying_token_digests=bindings)


@pytest.mark.asyncio
async def test_wit_backend_enforces_enrollment_and_key_authorization(material):
    signer, _, confirmation, trust = material

    async def resolve(principal):
        return SUBJECT if principal == "recipient" else None

    async def authorize_key(principal, proposed):
        return principal == "recipient" and proposed == confirmation

    app = build_issuer(
        WitIssuerConfig(
            "example.org", "https://issuer.example.org", "issuer", "issuer", "EdDSA"
        ),
        signer=signer,
        authenticate=authenticate,
        resolve_identity=resolve,
        authorize_confirmation_key=authorize_key,
        clock=lambda: NOW,
    )
    async with client(app) as http:
        payload = {"confirmation_jwk": confirmation}
        assert (await http.post("/wit/issue", json=payload)).status_code == 401
        assert (
            await http.post(
                "/wit/issue", json=payload, headers={"Authorization": "Bearer outsider"}
            )
        ).status_code == 403
        denied = await http.post(
            "/wit/issue",
            json={"confirmation_jwk": trust["example.org"][0]},
            headers={"Authorization": "Bearer recipient"},
        )
        assert denied.status_code == 403
        issued = await http.post(
            "/wit/issue", json=payload, headers={"Authorization": "Bearer recipient"}
        )
    assert issued.status_code == 200, issued.text
    assert issued.headers["cache-control"] == "no-store"
    wit = issued.json()["workload_identity_token"]
    body = proof_body((signer, wit, confirmation, trust))
    async with client(remote_app(material, RecordingReplayStore())) as http:
        accepted = await http.post(
            "/wpt/verify", json=body, headers={"Authorization": "Bearer recipient"}
        )
    assert accepted.status_code == 200, accepted.text
    assert accepted.json()["subject"] == SUBJECT


@pytest.mark.asyncio
async def test_remote_verification_authenticates_caller_before_consuming_proof(
    material,
):
    store = RecordingReplayStore()
    body = proof_body(material)
    async with client(remote_app(material, store)) as http:
        assert (await http.post("/wpt/verify", json=body)).status_code == 401
        assert (
            await http.post(
                "/wpt/verify", json=body, headers={"Authorization": "Bearer outsider"}
            )
        ).status_code == 403
        assert store.calls == 0
        accepted = await http.post(
            "/wpt/verify", json=body, headers={"Authorization": "Bearer recipient"}
        )
        replayed = await http.post(
            "/wpt/verify", json=body, headers={"Authorization": "Bearer recipient"}
        )
    assert accepted.status_code == 200, accepted.text
    assert accepted.json() == {
        "valid": True,
        "subject": SUBJECT,
        "audience": AUDIENCE,
        "proof_id": decode_jwt_unverified(body["workload_proof_token"]).claims["jti"],
        "expires_at": NOW + 60,
    }
    assert replayed.status_code == 401
    assert store.calls == 2  # Exactly one check per authorized verification attempt.
    assert (
        accepted.headers["cache-control"]
        == replayed.headers["cache-control"]
        == "no-store"
    )
    assert body["workload_proof_token"] not in accepted.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mutation",
    ["audience", "proof_signature", "wit_signature", "expiry", "wit_binding"],
)
async def test_remote_rejects_invalid_proofs_without_consuming_replay(
    material, mutation
):
    body = proof_body(material)
    signer = material[0]
    if mutation in {"proof_signature", "wit_signature"}:
        field = (
            "workload_proof_token"
            if mutation == "proof_signature"
            else "workload_identity_token"
        )
        parts = body[field].split(".")
        parts[2] = ("A" if parts[2][0] != "A" else "B") + parts[2][1:]
        body[field] = ".".join(parts)
    else:
        claims = dict(decode_jwt_unverified(body["workload_proof_token"]).claims)
        claims.update(
            {"aud": AUDIENCE + "/other"}
            if mutation == "audience"
            else {"exp": NOW}
            if mutation == "expiry"
            else {"wth": digest("different-wit")}
        )
        body["workload_proof_token"] = sign_compact_jwt(
            signer,
            claims,
            headers={"typ": "wpt+jwt", "alg": "EdDSA"},
            key_reference="workload",
        )
    store = RecordingReplayStore()
    async with client(remote_app(material, store)) as http:
        rejected = await http.post(
            "/wpt/verify", json=body, headers={"Authorization": "Bearer recipient"}
        )
    assert rejected.status_code == 401, rejected.text
    assert store.calls == 0


@pytest.mark.asyncio
async def test_remote_trust_is_configured_and_not_taken_from_submission(material):
    store = RecordingReplayStore()
    wrong = deepcopy(material[3])
    wrong["example.org"][0].update(jwk(Ed25519PrivateKey.generate()))
    app = build_verifier(
        WptVerifierSettings(AUDIENCE, wrong),
        replay_store=store,
        authenticate=authenticate,
        authorize_verification=authorize,
        clock=lambda: NOW,
    )
    async with client(app) as http:
        response = await http.post(
            "/wpt/verify",
            json=proof_body(material),
            headers={"Authorization": "Bearer recipient"},
        )
    assert response.status_code == 401
    assert store.calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("malformed", ["not-a-jwt", "a.b.c", "é", ".", ".."])
@pytest.mark.parametrize("field", ["workload_identity_token", "workload_proof_token"])
async def test_remote_rejects_malformed_token_encodings(material, malformed, field):
    body = {**proof_body(material), field: malformed}
    store = RecordingReplayStore()
    async with client(remote_app(material, store)) as http:
        response = await http.post(
            "/wpt/verify", json=body, headers={"Authorization": "Bearer recipient"}
        )
    assert response.status_code == 401
    assert store.calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "bad",
    [
        {"audience": "https://attacker.example.org"},
        {"trust_by_domain": {}},
        {"token_headers": [{"name": "Authorization", "value": "replacement"}]},
        {"token_headers": [{"name": "Txn-Token", "value": "bad\nheader"}]},
        {"workload_proof_token": "x" * 16385},
    ],
)
async def test_remote_rejects_caller_policy_overrides_and_malformed_input(
    material, bad
):
    store = RecordingReplayStore()
    async with client(remote_app(material, store)) as http:
        response = await http.post(
            "/wpt/verify",
            json={**proof_body(material), **bad},
            headers={"Authorization": "Bearer recipient"},
        )
        malformed = await http.post(
            "/wpt/verify", content=b"{", headers={"Authorization": "Bearer recipient"}
        )
    assert response.status_code == malformed.status_code == 400
    assert store.calls == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("supplied", ["missing", "substituted", "duplicate", "correct"])
async def test_remote_requires_exact_transaction_and_other_token_bindings(
    material, supplied
):
    body = proof_body(
        material,
        accompanying_token_digests={
            "txn-token": digest("transaction"),
            "x-access-token": digest("access"),
        },
    )
    headers = [
        {"name": "Txn-Token", "value": "transaction"},
        {"name": "X-Access-Token", "value": "access"},
    ]
    if supplied == "missing":
        headers.pop()
    elif supplied == "substituted":
        headers[0]["value"] = "replacement"
    elif supplied == "duplicate":
        headers.append(dict(headers[0]))
    body["token_headers"] = headers
    store = RecordingReplayStore()
    async with client(
        remote_app(material, store, required=("txn-token", "x-access-token"))
    ) as http:
        response = await http.post(
            "/wpt/verify", json=body, headers={"Authorization": "Bearer recipient"}
        )
    assert response.status_code == (200 if supplied == "correct" else 401), (
        response.text
    )
    assert store.calls == (1 if supplied == "correct" else 0)


@pytest.mark.asyncio
async def test_required_binding_cannot_be_omitted_from_both_proof_and_request(material):
    async with client(
        remote_app(material, RecordingReplayStore(), required=("x-access-token",))
    ) as http:
        response = await http.post(
            "/wpt/verify",
            json=proof_body(material),
            headers={"Authorization": "Bearer recipient"},
        )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_two_verifier_instances_share_atomic_replay_state(material):
    store = RecordingReplayStore()
    body = proof_body(material)
    async with (
        client(remote_app(material, store)) as left,
        client(remote_app(material, store)) as right,
    ):
        results = await asyncio.gather(
            *[
                http.post(
                    "/wpt/verify",
                    json=body,
                    headers={"Authorization": "Bearer recipient"},
                )
                for http in (left, right)
            ]
        )
    assert sorted(result.status_code for result in results) == [200, 401]


@pytest.mark.asyncio
async def test_router_mounts_independently(material):
    app = TigrblApp()
    app.include_router(
        build_wpt_verification_router(
            verifier=WptProofVerifier(
                trust_by_domain=material[3],
                replay_store=RecordingReplayStore(),
                clock=lambda: NOW,
            ),
            audience=AUDIENCE,
            authenticate=authenticate,
            authorize_verification=authorize,
        )
    )
    async with client(app) as http:
        response = await http.post(
            "/wpt/verify",
            json=proof_body(material),
            headers={"Authorization": "Bearer recipient"},
        )
    assert response.status_code == 200


def test_runtime_wires_optional_issuer_and_rejects_partial_configuration(material):
    dependencies = {
        "credential_provider": object(),
        "credential_verifier": object(),
        "wit_trust_by_domain": material[3],
        "wpt_replay_store": RecordingReplayStore(),
        "wpt_signer": material[0],
        "wpt_wit": material[1],
        "wpt_workload_key_reference": "workload",
    }
    config = WorkloadIdentityRuntimeConfig(enable_wimse_wit=True, enable_wimse_wpt=True)
    composition = build_workload_identity_composition(config, dependencies=dependencies)
    assert isinstance(composition.dependencies["wimse_wpt_issuer"], WptProofIssuer)
    dependencies.pop("wpt_wit")
    with pytest.raises(ValueError, match="missing WPT issuer"):
        build_workload_identity_composition(config, dependencies=dependencies)
