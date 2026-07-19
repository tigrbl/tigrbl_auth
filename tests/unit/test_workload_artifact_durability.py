from tigrbl_identity_storage.tables import PossessionProofReplay, ProtectedArtifactReference, TABLE_MODELS, WorkloadCredentialEntitlement, WorkloadReferenceBinding
from tigrbl_token_durability import RUNTIME_OPERATION_BY_ALIAS as TOKEN_OPS
from tigrbl_workload_identity_durability import RUNTIME_OPERATION_BY_ALIAS as WORKLOAD_OPS

def test_new_tables_are_canonical_storage_models()->None:
    assert {WorkloadReferenceBinding,WorkloadCredentialEntitlement,ProtectedArtifactReference,PossessionProofReplay}.issubset(set(TABLE_MODELS))

def test_new_durability_aliases_are_carrier_neutral()->None:
    assert {"bind_workload_reference","grant_workload_credential_entitlement"}.issubset(WORKLOAD_OPS)
    assert {"register_protected_artifact_reference","reserve_possession_proof_replay"}.issubset(TOKEN_OPS)
    for operation in (*WORKLOAD_OPS.values(),*TOKEN_OPS.values()):
        assert operation.expose_routes is False
        assert operation.expose_rpc is False