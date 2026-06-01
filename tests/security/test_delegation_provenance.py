import pytest

from tigrbl_auth.security.certification import (
    CertificationError,
    DelegationStep,
    assert_delegation_provenance,
)


def test_delegation_provenance_t0_contract_exports_chain_check() -> None:
    assert callable(assert_delegation_provenance)


def test_delegation_provenance_t1_accepts_bounded_attenuated_chain() -> None:
    chain = (
        DelegationStep("service-a", "user-1", frozenset({"read", "write"}), "proof-1"),
        DelegationStep("service-b", "service-a", frozenset({"read"}), "proof-2"),
    )

    assert_delegation_provenance(chain, max_depth=3, allowed_final_scopes=frozenset({"read"}))


@pytest.mark.parametrize(
    "chain,match",
    [
        ((DelegationStep("a", "user", frozenset({"admin"}), "proof"),), "scopes"),
        (
            (
                DelegationStep("a", "user", frozenset({"read"}), "proof"),
                DelegationStep("a", "a", frozenset({"read"}), "proof"),
            ),
            "cycle",
        ),
        ((DelegationStep("a", "user", frozenset({"read"}), ""),), "proof"),
    ],
)
def test_delegation_provenance_t2_rejects_unbounded_or_unproven_chains(
    chain: tuple[DelegationStep, ...],
    match: str,
) -> None:
    with pytest.raises(CertificationError, match=match):
        assert_delegation_provenance(chain, max_depth=3, allowed_final_scopes=frozenset({"read"}))
