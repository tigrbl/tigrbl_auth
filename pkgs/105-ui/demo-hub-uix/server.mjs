import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";

const port = Number(process.env.PORT || 80);
const root = "/usr/share/demo-hub";
const demoPassword = process.env.TIGRBL_AUTH_DEMO_ADMIN_PASSWORD || "AdminPass123!";

const bases = {
  public: process.env.TIGRBL_AUTH_PUBLIC_BACKEND_APP_BASE_URL || "http://host.docker.internal:8013",
  resourceValidation: process.env.TIGRBL_AUTH_RESOURCE_VALIDATION_BACKEND_APP_BASE_URL || "http://host.docker.internal:8014",
  platformAdmin: process.env.TIGRBL_AUTH_PLATFORM_ADMIN_BACKEND_APP_BASE_URL || "http://host.docker.internal:8015",
  tenantAdmin: process.env.TIGRBL_AUTH_TENANT_ADMIN_BACKEND_APP_BASE_URL || "http://host.docker.internal:8016",
  developer: process.env.TIGRBL_AUTH_DEVELOPER_BACKEND_APP_BASE_URL || "http://host.docker.internal:8017",
  serviceAdmin: process.env.TIGRBL_AUTH_SERVICE_ADMIN_BACKEND_APP_BASE_URL || "http://host.docker.internal:8018"
};

const adminKeys = {
  platformAdmin: process.env.TIGRBL_AUTH_PLATFORM_ADMIN_API_KEY || "dev-platform-admin-key",
  tenantAdmin: process.env.TIGRBL_AUTH_TENANT_ADMIN_API_KEY || "dev-tenant-admin-key",
  developer: process.env.TIGRBL_AUTH_DEVELOPER_API_KEY || "dev-developer-key",
  serviceAdmin: process.env.TIGRBL_AUTH_SERVICE_ADMIN_API_KEY || "dev-service-admin-key"
};

const demo = {
  realm: {
    slug: "acme",
    name: "Acme Realm",
    issuer_path: "/realms/acme",
    description: "Demo issuer namespace"
  },
  tenant: {
    slug: "acme-demo",
    name: "Acme Demo",
    email: "acme-demo@example.test"
  },
  user: {
    username: "alex-demo",
    email: "alex@acme.example",
    password: "AlexDemoPass123!",
    role: "tenant-admin"
  },
  app: {
    name: "Acme Dashboard",
    redirectUri: "http://127.0.0.1:5173/callback",
    scopes: "openid profile email offline_access"
  },
  service: {
    name: "Acme Worker"
  }
};

function jsonResponse(response, status, payload) {
  const body = JSON.stringify(payload);
  response.writeHead(status, {
    "content-type": "application/json",
    "content-length": Buffer.byteLength(body)
  });
  response.end(body);
}

function textSample(text) {
  return String(text || "").slice(0, 320);
}

function cookieFrom(headers) {
  return headers
    .getSetCookie?.()
    ?.map((value) => value.split(";")[0])
    .join("; ") || headers.get("set-cookie")?.split(";")[0] || "";
}

async function apiFetch(base, path, { method = "GET", body, cookie, apiKey } = {}) {
  const headers = {};
  if (body !== undefined) headers["content-type"] = "application/json";
  if (cookie) headers.cookie = cookie;
  if (apiKey) headers["x-api-key"] = apiKey;
  const response = await fetch(`${base}${path}`, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body)
  });
  const text = await response.text();
  let json = null;
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = null;
  }
  return {
    ok: response.ok,
    status: response.status,
    text,
    json,
    cookie: cookieFrom(response.headers)
  };
}

async function loginAdmin(base) {
  const login = await apiFetch(base, "/admin/auth/login", {
    method: "POST",
    body: { identifier: "admin", password: demoPassword }
  });
  if (!login.ok || !login.cookie) {
    throw new Error(`admin login failed ${login.status}: ${textSample(login.text)}`);
  }
  return login.cookie;
}

function result(id, ok, status, summary, evidence = {}) {
  return { id, ok, status, summary, evidence };
}

async function stepPlatformProvisionTenant() {
  const cookie = await loginAdmin(bases.platformAdmin);
  const createdRealm = await apiFetch(bases.platformAdmin, "/admin/realm", {
    method: "POST",
    cookie,
    apiKey: adminKeys.platformAdmin,
    body: demo.realm
  });
  let realm = createdRealm.json;
  if (!createdRealm.ok && createdRealm.status !== 409) {
    return result("platform-provision-tenant", false, createdRealm.status, textSample(createdRealm.text), { response: createdRealm.json ?? createdRealm.text });
  }
  if (createdRealm.status === 409) {
    const listedRealms = await apiFetch(bases.platformAdmin, "/admin/realm", {
      cookie,
      apiKey: adminKeys.platformAdmin
    });
    const realmRows = Array.isArray(listedRealms.json) ? listedRealms.json : [];
    realm = realmRows.find((row) => row.slug === demo.realm.slug);
    if (!realm) {
      return result("platform-provision-tenant", false, listedRealms.status, textSample(listedRealms.text), listedRealms.json);
    }
  }
  const created = await apiFetch(bases.platformAdmin, `/admin/realm/${encodeURIComponent(realm.id)}/tenant`, {
    method: "POST",
    cookie,
    apiKey: adminKeys.platformAdmin,
    body: { ...demo.tenant, realm_id: realm.id }
  });
  if (created.ok) {
    return result("platform-provision-tenant", true, created.status, `realm and tenant provisioned: ${realm.slug}/${created.json?.slug}`, { realm, tenant: created.json });
  }
  if (created.status !== 409) {
    return result("platform-provision-tenant", false, created.status, textSample(created.text), { realm, response: created.json ?? created.text });
  }
  const listed = await apiFetch(bases.platformAdmin, `/admin/realm/${encodeURIComponent(realm.id)}/tenant`, {
    cookie,
    apiKey: adminKeys.platformAdmin
  });
  const rows = Array.isArray(listed.json) ? listed.json : [];
  const match = rows.find((row) => row.slug === demo.tenant.slug);
  return result("platform-provision-tenant", Boolean(match), listed.status, match ? `realm and tenant already provisioned: ${realm.slug}/${match.slug}` : textSample(listed.text), { realm, tenant: match ?? listed.json });
}

async function stepTenantManageIdentity() {
  const cookie = await loginAdmin(bases.tenantAdmin);
  const session = await apiFetch(bases.tenantAdmin, "/admin/auth/session", { cookie, apiKey: adminKeys.tenantAdmin });
  const tenantId = session.json?.tenant_id;
  if (!session.ok || !tenantId) {
    return result("tenant-manage-identity", false, session.status, `tenant admin session unavailable: ${textSample(session.text)}`, session.json);
  }
  const create = await apiFetch(bases.tenantAdmin, "/admin/identities", {
    method: "POST",
    cookie,
    apiKey: adminKeys.tenantAdmin,
    body: {
      tenant_id: tenantId,
      username: demo.user.username,
      email: demo.user.email,
      password: demo.user.password,
      is_admin: true,
      is_superuser: false,
      must_change_password: false
    }
  });
  if (create.ok) {
    return result("tenant-manage-identity", true, create.status, `identity provisioned: ${create.json?.email}`, create.json);
  }
  if (create.status !== 409) {
    return result("tenant-manage-identity", false, create.status, textSample(create.text), { response: create.json ?? create.text });
  }
  const listed = await apiFetch(bases.tenantAdmin, `/admin/identities?tenant_id=${tenantId}`, {
    cookie,
    apiKey: adminKeys.tenantAdmin
  });
  const rows = Array.isArray(listed.json) ? listed.json : [];
  const match = rows.find((row) => row.email === demo.user.email);
  return result("tenant-manage-identity", Boolean(match), listed.status, match ? `identity already provisioned: ${match.email}` : textSample(listed.text), match ?? listed.json);
}

async function stepDeveloperRegisterClient() {
  const response = await apiFetch(bases.developer, "/register", {
    method: "POST",
    body: {
      tenant_slug: "public",
      client_name: demo.app.name,
      redirect_uris: [demo.app.redirectUri],
      grant_types: ["authorization_code"],
      response_types: ["code"],
      scope: demo.app.scopes,
      token_endpoint_auth_method: "client_secret_basic"
    }
  });
  return result(
    "developer-register-client",
    response.ok,
    response.status,
    response.ok ? `client registered: ${response.json?.client_id}` : textSample(response.text),
    response.json ?? response.text
  );
}

async function stepPublicAuthenticateUser(context) {
  const response = await apiFetch(bases.public, "/login", {
    method: "POST",
    body: { identifier: "admin", password: demoPassword }
  });
  if (response.ok && response.cookie) {
    context.publicCookie = response.cookie;
  }
  return result(
    "public-authenticate-user",
    response.ok && Boolean(response.cookie),
    response.status,
    response.ok ? "public issuer session established" : textSample(response.text),
    response.json ?? response.text
  );
}

async function stepAccountReviewConsents(context) {
  if (!context.publicCookie) {
    await stepPublicAuthenticateUser(context);
  }
  const response = await apiFetch(bases.public, "/account/profile", {
    cookie: context.publicCookie
  });
  return result(
    "account-review-consents",
    response.ok,
    response.status,
    response.ok ? `account profile loaded: ${response.json?.email}` : textSample(response.text),
    response.json ?? response.text
  );
}

async function stepServiceConfigureWorkload() {
  const response = await apiFetch(bases.serviceAdmin, "/service", {
    apiKey: adminKeys.serviceAdmin
  });
  return result(
    "service-configure-workload",
    response.ok,
    response.status,
    response.ok ? "service-admin workload surface reachable" : textSample(response.text),
    response.json ?? response.text
  );
}

async function stepResourceValidateToken() {
  const response = await apiFetch(bases.resourceValidation, "/.well-known/jwks.json");
  const keys = Array.isArray(response.json?.keys) ? response.json.keys.length : 0;
  return result(
    "resource-validate-token",
    response.ok && keys > 0,
    response.status,
    response.ok ? `JWKS available with ${keys} key(s)` : textSample(response.text),
    response.json ?? response.text
  );
}

const stepRunners = {
  "platform-provision-tenant": stepPlatformProvisionTenant,
  "tenant-manage-identity": stepTenantManageIdentity,
  "developer-register-client": stepDeveloperRegisterClient,
  "public-authenticate-user": stepPublicAuthenticateUser,
  "account-review-consents": stepAccountReviewConsents,
  "service-configure-workload": stepServiceConfigureWorkload,
  "resource-validate-token": stepResourceValidateToken
};

async function runStep(stepId, context = {}) {
  const runner = stepRunners[stepId];
  if (!runner) {
    return result(stepId, false, 404, `unknown demo step: ${stepId}`);
  }
  try {
    return await runner(context);
  } catch (error) {
    return result(stepId, false, undefined, error instanceof Error ? error.message : "demo step failed");
  }
}

async function runAll() {
  const context = {};
  const ordered = Object.keys(stepRunners);
  const results = [];
  for (const stepId of ordered) {
    const stepResult = await runStep(stepId, context);
    results.push(stepResult);
    if (!stepResult.ok) break;
  }
  return {
    ok: results.length === ordered.length && results.every((item) => item.ok),
    results
  };
}

async function serveStatic(request, response) {
  const url = new URL(request.url || "/", "http://localhost");
  const rawPath = url.pathname === "/" ? "/index.html" : url.pathname;
  const normalized = normalize(rawPath).replace(/^(\.\.[/\\])+/, "");
  let filePath = join(root, normalized);
  try {
    const content = await readFile(filePath);
    const type = {
      ".html": "text/html; charset=utf-8",
      ".js": "text/javascript; charset=utf-8",
      ".css": "text/css; charset=utf-8",
      ".svg": "image/svg+xml"
    }[extname(filePath)] || "application/octet-stream";
    response.writeHead(200, { "content-type": type });
    response.end(content);
  } catch {
    filePath = join(root, "index.html");
    const content = await readFile(filePath);
    response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    response.end(content);
  }
}

createServer(async (request, response) => {
  const url = new URL(request.url || "/", "http://localhost");
  if (request.method === "POST" && url.pathname === "/demo-api/run-all") {
    jsonResponse(response, 200, await runAll());
    return;
  }
  const stepMatch = url.pathname.match(/^\/demo-api\/steps\/([^/]+)$/);
  if (request.method === "POST" && stepMatch) {
    jsonResponse(response, 200, await runStep(decodeURIComponent(stepMatch[1]), {}));
    return;
  }
  await serveStatic(request, response);
}).listen(port, "0.0.0.0");
