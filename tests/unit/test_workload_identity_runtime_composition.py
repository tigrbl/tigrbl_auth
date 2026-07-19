import pytest
from tigrbl_identity_runtime.composition.workload_identity import WorkloadIdentityRuntimeConfig, build_workload_identity_composition

def deps(): return {"credential_provider": object(), "credential_verifier": object()}

def test_experimental_and_incubating_profiles_default_off() -> None:
    result = build_workload_identity_composition(WorkloadIdentityRuntimeConfig(), dependencies={})
    assert result.active_profiles == ()

def test_wit_svid_requires_wit_wpt_and_exact_revisions() -> None:
    with pytest.raises(ValueError): build_workload_identity_composition(WorkloadIdentityRuntimeConfig(enable_spiffe_wit_svid=True), dependencies=deps())
    config = WorkloadIdentityRuntimeConfig(enable_wimse_wit=True, enable_wimse_wpt=True, enable_spiffe_wit_svid=True)
    assert build_workload_identity_composition(config, dependencies=deps()).active_profiles == ("wit", "wpt", "wit-svid")

def test_broker_fails_closed_without_endpoint_and_authorization() -> None:
    with pytest.raises(ValueError): build_workload_identity_composition(WorkloadIdentityRuntimeConfig(enable_spiffe_broker_api=True), dependencies=deps())
    config = WorkloadIdentityRuntimeConfig(enable_spiffe_broker_api=True, broker_endpoint="unix:///broker.sock", broker_authorized_principals=("broker",))
    assert "spiffe-broker-api" in build_workload_identity_composition(config, dependencies=deps()).active_profiles