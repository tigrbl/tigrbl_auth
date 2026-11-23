from tba_capability_mcp_authorization import MCPGrantBinding

binding = MCPGrantBinding(
    grant_id="g-123",
    tenant_id="example-tenant",
    client_id="example-client",
    resource="https://example.com/mcp",
)
assert binding.tenant_id == "example-tenant"
