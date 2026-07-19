import pytest

from tigrbl_claim_confirmation_concrete import ConfirmationClaim
from tigrbl_claim_cwt_confirmation_concrete import CwtConfirmationClaim
from tigrbl_claim_other_token_hashes_concrete import OtherTokenHashesClaim
from tigrbl_claim_transaction_token_hash_concrete import TransactionTokenHashClaim
from tigrbl_claim_workload_token_hash_concrete import WorkloadTokenHashClaim
from tigrbl_identity_core import ClaimNameKind

_DIGEST = "A" * 43


def test_wimse_hash_claims_are_independent_concrete_objects() -> None:
    wth = WorkloadTokenHashClaim(_DIGEST, required=True)
    tth = TransactionTokenHashClaim(_DIGEST)
    oth = OtherTokenHashesClaim({"X-Identity-Token": _DIGEST})

    assert wth.name == "wth"
    assert wth.required is True
    assert tth.name == "tth"
    assert oth.value == {"X-Identity-Token": _DIGEST}


@pytest.mark.parametrize(
    "claim_type",
    [WorkloadTokenHashClaim, TransactionTokenHashClaim],
)
def test_sha256_token_hash_claims_require_unpadded_base64url(claim_type) -> None:
    with pytest.raises(ValueError):
        claim_type("short")
    with pytest.raises(ValueError):
        claim_type("A" * 42 + "=")


def test_other_token_hashes_require_named_sha256_digests() -> None:
    with pytest.raises(ValueError):
        OtherTokenHashesClaim({})
    with pytest.raises(ValueError):
        OtherTokenHashesClaim({"": _DIGEST})
    with pytest.raises(ValueError):
        OtherTokenHashesClaim({"X-Token": "short"})


def test_jose_confirmation_supports_public_key_and_thumbprints() -> None:
    assert ConfirmationClaim({"jwk": {"kty": "EC", "crv": "P-256"}}).name == "cnf"
    assert ConfirmationClaim({"jkt": _DIGEST}).value == {"jkt": _DIGEST}
    assert ConfirmationClaim({"x5t#S256": _DIGEST}).name == "cnf"

    with pytest.raises(ValueError, match="private"):
        ConfirmationClaim({"jwk": {"kty": "EC", "d": "secret"}})
    with pytest.raises(ValueError, match="exactly one"):
        ConfirmationClaim({"jkt": _DIGEST, "x5t#S256": _DIGEST})


def test_cwt_confirmation_uses_integer_claim_and_method_labels() -> None:
    cose_key = CwtConfirmationClaim({1: {1: 2, -1: 1, -2: b"x", -3: b"y"}})
    encrypted_key = CwtConfirmationClaim({2: [b"protected", {}, b"ciphertext"]})
    kid = CwtConfirmationClaim({3: b"key-id"})
    thumbprint = CwtConfirmationClaim({5: b"cose-key-thumbprint"})

    assert cose_key.name == 8
    assert cose_key.name_kind is ClaimNameKind.INTEGER_LABEL
    assert encrypted_key.name == kid.name == thumbprint.name == 8


@pytest.mark.parametrize(
    "value",
    [
        {},
        {1: {}, 3: b"kid"},
        {1: b"not-a-map"},
        {2: b"not-a-cose-array"},
        {3: "not-bytes"},
        {5: b""},
        {99: b"unknown"},
    ],
)
def test_cwt_confirmation_rejects_invalid_methods(value) -> None:
    with pytest.raises(ValueError):
        CwtConfirmationClaim(value)