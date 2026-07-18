export const SURFACE_LINKS = {
  publicUix: import.meta.env.VITE_TIGRBL_AUTH_PUBLIC_UIX_URL || "http://localhost:3010/#/login",
  platformAdminUix: import.meta.env.VITE_TIGRBL_AUTH_PLATFORM_ADMIN_UIX_URL || "http://localhost:3011/#/dashboard",
  tenantAdminUix: import.meta.env.VITE_TIGRBL_AUTH_TENANT_ADMIN_UIX_URL || "http://localhost:3012/#/dashboard",
  developerUix: import.meta.env.VITE_TIGRBL_AUTH_DEVELOPER_UIX_URL || "http://localhost:3013/#/dashboard",
  serviceAdminUix: import.meta.env.VITE_TIGRBL_AUTH_SERVICE_ADMIN_UIX_URL || "http://localhost:3014/#/dashboard",
  myAccountUix: import.meta.env.VITE_TIGRBL_AUTH_MY_ACCOUNT_UIX_URL || "http://localhost:3019/#/overview",
  publicApiDocs: import.meta.env.VITE_TIGRBL_AUTH_PUBLIC_API_DOCS_URL || "http://localhost:8013/docs",
  resourceValidationApiDocs: import.meta.env.VITE_TIGRBL_AUTH_RESOURCE_VALIDATION_API_DOCS_URL || "http://localhost:8014/docs",
  platformAdminApiDocs: import.meta.env.VITE_TIGRBL_AUTH_PLATFORM_ADMIN_API_DOCS_URL || "http://localhost:8015/docs",
  tenantAdminApiDocs: import.meta.env.VITE_TIGRBL_AUTH_TENANT_ADMIN_API_DOCS_URL || "http://localhost:8016/docs",
  developerApiDocs: import.meta.env.VITE_TIGRBL_AUTH_DEVELOPER_API_DOCS_URL || "http://localhost:8017/docs",
  serviceAdminApiDocs: import.meta.env.VITE_TIGRBL_AUTH_SERVICE_ADMIN_API_DOCS_URL || "http://localhost:8018/docs",
  myAccountApiDocs: import.meta.env.VITE_TIGRBL_AUTH_MY_ACCOUNT_API_DOCS_URL || "http://localhost:8019/docs"
};

export const BACKEND_APP = "composed local backend apps";
