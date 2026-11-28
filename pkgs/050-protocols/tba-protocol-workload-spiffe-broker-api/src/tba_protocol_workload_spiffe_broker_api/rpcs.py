from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrokerRpcDefinition:
    name: str
    server_streaming: bool
    profile: str


RPC_DEFINITIONS = (
    BrokerRpcDefinition("SubscribeToX509SVID", True, "x509-svid"),
    BrokerRpcDefinition("SubscribeToX509Bundles", True, "x509-svid"),
    BrokerRpcDefinition("FetchJWTSVID", False, "jwt-svid"),
    BrokerRpcDefinition("SubscribeToJWTBundles", True, "jwt-svid"),
)
RPC_NAMES = frozenset(item.name for item in RPC_DEFINITIONS)
