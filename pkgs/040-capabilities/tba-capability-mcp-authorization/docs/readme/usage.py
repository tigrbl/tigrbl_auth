from collections.abc import Callable

from tba_capability_mcp_authorization import (
    MCPAuthorizationCapability,
    MCPGrantBinding,
    MCPResourceCheck,
    MCPPrincipal,
)


async def authorize_read(
    capability: MCPAuthorizationCapability,
    verified_binding: MCPGrantBinding,
    verified_token_scopes: frozenset[str],
    can_read_resource: MCPResourceCheck,
) -> MCPPrincipal | None:
    return await capability.authorize_tool(
        verified_binding,
        verified_token_scopes,
        required_scopes={"journal:read"},
        check_resource=can_read_resource,
    )


assert isinstance(authorize_read, Callable)
