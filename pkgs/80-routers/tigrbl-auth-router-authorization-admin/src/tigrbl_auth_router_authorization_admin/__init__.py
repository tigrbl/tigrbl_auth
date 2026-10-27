CUSTOMER_ROUTES = ("/v1/tenants/{tenant_id}/members", "/v1/tenants/{tenant_id}/authorization/groups", "/v1/tenants/{tenant_id}/authorization/roles", "/v1/tenants/{tenant_id}/authorization/grants", "/v1/tenants/{tenant_id}/authorization/effective-access", "/v1/tenants/{tenant_id}/access-reviews")
INTERNAL_ROUTES = ("/v1/platform/authority/people", "/v1/platform/authority/grants", "/v1/platform/authority/policies", "/v1/platform/authority/decisions", "/v1/platform/authority/break-glass")

def assert_tenant_scope(actor_tenant_id: str, route_tenant_id: str) -> None:
    if actor_tenant_id != route_tenant_id:
        raise PermissionError("cross-tenant administration denied")

__all__ = ["CUSTOMER_ROUTES", "INTERNAL_ROUTES", "assert_tenant_scope"]
