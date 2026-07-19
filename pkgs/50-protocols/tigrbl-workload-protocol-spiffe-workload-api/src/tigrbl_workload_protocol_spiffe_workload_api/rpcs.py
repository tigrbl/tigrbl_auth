from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class RpcDefinition:
    name: str
    server_streaming: bool
    profile: str
RPC_DEFINITIONS = (
    RpcDefinition("FetchX509SVID", True, "x509-svid"),
    RpcDefinition("FetchX509Bundles", True, "x509-svid"),
    RpcDefinition("FetchJWTSVID", False, "jwt-svid"),
    RpcDefinition("FetchJWTBundles", True, "jwt-svid"),
    RpcDefinition("ValidateJWTSVID", False, "jwt-svid"),
)
RPC_NAMES = frozenset(item.name for item in RPC_DEFINITIONS)
FORBIDDEN_EXTENSION_RPCS = frozenset({"FetchWITSVID", "FetchCWTSVID"})