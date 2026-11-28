from tba_capability_identity_document import IdentityDocumentCapability
from tba_capability_possession_proof import PossessionProofCapability
from tba_capability_protected_envelope import ProtectedEnvelopeCapability
from tba_capability_workload_credential_brokering import WorkloadCredentialBrokeringCapability
from tba_capability_workload_identity import WorkloadIdentityCapability

class Delegate:
    def __getattr__(self,name): return lambda *args,**kwargs:(name,args,kwargs)

def test_artifact_capabilities_report_required_and_optional_operations()->None:
    delegate=Delegate()
    document=IdentityDocumentCapability(delegate,delegate)
    envelope=ProtectedEnvelopeCapability(delegate,delegate)
    proof=PossessionProofCapability(delegate,delegate,delegate)
    assert document.definition().capability_id=="identity-document.processing"
    assert "publish_identity_document" in document.capability_report()[
        "unavailable_optional_operations"
    ]
    assert set(envelope.operations())=={"protect_envelope","verify_envelope"}
    assert "issue_possession_proof" in proof.capability_report()["optional_operations"]

def test_workload_capabilities_are_protocol_neutral()->None:
    delegate=Delegate()
    workload=WorkloadIdentityCapability(delegate,delegate)
    broker=WorkloadCredentialBrokeringCapability(delegate,lambda request:True,delegate,delegate)
    assert workload.definition().capability_id=="workload-identity.credentials"
    assert "fetch_x509_svid" not in workload.operations()
    assert "obtain_workload_credential" in workload.operations()
    assert broker.definition().capability_id=="workload-credential.brokering"
    assert "watch_delegated_workload_credentials" in broker.capability_report()[
        "unavailable_optional_operations"
    ]