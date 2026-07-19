import pytest
from tigrbl_workload_protocol_spiffe_broker_api import CURRENT_VERSION as BROKER_VERSION, RPC_NAMES as BROKER_RPCS, BrokerApiService
from tigrbl_workload_protocol_spiffe_workload_api import FORBIDDEN_EXTENSION_RPCS, RPC_NAMES as WORKLOAD_RPCS, WorkloadApiService

def test_exact_spiffe_rpc_surfaces_do_not_invent_wit_or_cwt_methods() -> None:
    assert WORKLOAD_RPCS == {"FetchX509SVID", "FetchX509Bundles", "FetchJWTSVID", "FetchJWTBundles", "ValidateJWTSVID"}
    assert BROKER_RPCS == {"SubscribeToX509SVID", "SubscribeToX509Bundles", "FetchJWTSVID", "SubscribeToJWTBundles"}
    assert FORBIDDEN_EXTENSION_RPCS == {"FetchWITSVID", "FetchCWTSVID"}
    assert BROKER_VERSION.status == "Incubating"

def test_services_are_closed_and_broker_is_authorized() -> None:
    handlers = {name: (lambda request: request) for name in WORKLOAD_RPCS}
    assert WorkloadApiService(handlers).dispatch("FetchJWTSVID", "request") == "request"
    with pytest.raises(ValueError): WorkloadApiService({**handlers, "FetchWITSVID": lambda request: request})
    broker_handlers = {name: (lambda request: request) for name in BROKER_RPCS}
    broker = BrokerApiService(authorize=lambda actor: actor == "allowed", handlers=broker_handlers)
    with pytest.raises(PermissionError): broker.dispatch("denied", "FetchJWTSVID", "request")