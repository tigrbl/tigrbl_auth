const SAFE_PUBLIC_HASH_PATHS = new Set([
  "#/",
  "#/callback",
  "#/consent",
  "#/forgot-password",
  "#/login",
  "#/mfa",
  "#/profile",
  "#/register",
  "#/reset-password",
  "#/terms",
  "#/verify-email",
]);

const BLOCKED_BROWSER_PATH_PREFIXES = ["/admin", "/rpc"];
const DEFAULT_CSRF_STORAGE_KEY = "tigrbl_auth_public_csrf";

const fallbackOrigin = (): string =>
  typeof window === "undefined" ? "http://localhost:3000" : window.location.origin;

const trimTrailingSlash = (value: string): string => value.replace(/\/+$/, "");

const toHashRoute = (value: string): string => {
  if (!value) {
    return "#/";
  }
  if (value.startsWith("#")) {
    return value;
  }
  if (value.startsWith("/")) {
    return `#${value}`;
  }
  return `#/${value.replace(/^#?\/?/, "")}`;
};

export const safePublicHashPaths = (): string[] => Array.from(SAFE_PUBLIC_HASH_PATHS);

export const sanitizePublicHashTarget = (
  candidate: string | null | undefined,
  fallback: string = "#/login",
): string => {
  const safeFallback = toHashRoute(fallback);
  if (!candidate) {
    return safeFallback;
  }

  if (/^https?:\/\//i.test(candidate)) {
    try {
      const url = new URL(candidate);
      if (url.origin === fallbackOrigin() && url.hash) {
        return sanitizePublicHashTarget(url.hash, safeFallback);
      }
    } catch {
      return safeFallback;
    }
    return safeFallback;
  }

  const hashRoute = toHashRoute(candidate);
  const [path, query = ""] = hashRoute.split("?");
  if (!SAFE_PUBLIC_HASH_PATHS.has(path)) {
    return safeFallback;
  }
  return query ? `${path}?${query}` : path;
};

export const isTrustedBrowserOrigin = (
  candidate: string,
  publicBaseUrl: string,
  appOrigin: string = fallbackOrigin(),
): boolean => {
  try {
    const origin = new URL(candidate).origin;
    const trustedOrigins = new Set([
      new URL(publicBaseUrl, appOrigin).origin,
      new URL(appOrigin).origin,
    ]);
    return trustedOrigins.has(origin);
  } catch {
    return false;
  }
};

export const resolveTrustedPublicEndpoint = (
  endpoint: string,
  action: string,
  publicBaseUrl: string,
): string => {
  const baseUrl = trimTrailingSlash(publicBaseUrl || fallbackOrigin());
  const resolved = new URL(endpoint, baseUrl);
  const trustedOrigin = new URL(baseUrl, fallbackOrigin()).origin;

  if (resolved.origin !== trustedOrigin) {
    throw new Error(`${action} is not available from the discovered tigrbl_auth endpoints.`);
  }

  if (BLOCKED_BROWSER_PATH_PREFIXES.some((prefix) => resolved.pathname.startsWith(prefix))) {
    throw new Error(`${action} is not available from the discovered tigrbl_auth endpoints.`);
  }

  return resolved.toString();
};

export const createCsrfToken = (): string => {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
};

export const getOrCreateCsrfToken = (
  storage?: Pick<Storage, "getItem" | "setItem"> | null,
  key: string = DEFAULT_CSRF_STORAGE_KEY,
): string => {
  const store = storage
    ?? (typeof sessionStorage === "undefined" ? null : sessionStorage);
  const existing = store?.getItem(key);
  if (existing) {
    return existing;
  }
  const created = createCsrfToken();
  store?.setItem(key, created);
  return created;
};

export const buildBrowserJsonRequestInit = (
  body: unknown,
  csrfToken: string,
): RequestInit => ({
  method: "POST",
  credentials: "include",
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken,
    "X-Requested-With": "XMLHttpRequest",
  },
  body: JSON.stringify(body),
});

export const buildPopupCallbackHash = (
  search: string | null | undefined,
): string | null => {
  if (!search) {
    return null;
  }
  const normalized = search.replace(/^\?/, "").trim();
  if (!normalized) {
    return null;
  }
  return `#/callback?${normalized}`;
};

export interface ConsentViewModel {
  approveTarget: string;
  cancelTarget: string;
  clientName: string;
  scopes: string[];
}

export const parseConsentViewModel = (
  hash: string,
  fallbackApproveTarget: string = "#/profile",
  fallbackCancelTarget: string = "#/login",
): ConsentViewModel => {
  const query = hash.includes("?") ? hash.slice(hash.indexOf("?") + 1) : "";
  const params = new URLSearchParams(query);
  const scopeText = params.get("scope") || "openid profile email";

  return {
    approveTarget: sanitizePublicHashTarget(params.get("continue"), fallbackApproveTarget),
    cancelTarget: sanitizePublicHashTarget(params.get("cancel"), fallbackCancelTarget),
    clientName: params.get("client_name") || "tigrbl_auth application",
    scopes: scopeText.split(/\s+/).filter(Boolean),
  };
};

