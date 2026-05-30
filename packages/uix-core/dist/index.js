var y = Object.defineProperty;
var v = (e, r, t) => r in e ? y(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t;
var o = (e, r, t) => v(e, typeof r != "symbol" ? r + "" : r, t);
import { createContext as w, useContext as S, useState as b, useEffect as A } from "react";
import { jsx as n, Fragment as f, jsxs as l } from "react/jsx-runtime";
class $ extends Error {
  constructor(t, a, i = null) {
    super(t);
    o(this, "status");
    o(this, "payload");
    this.name = "ApiError", this.status = a, this.payload = i;
  }
}
function g(e, r) {
  return e === r || e.startsWith(`${r}/`);
}
function k(e, r) {
  if (!e.startsWith("/"))
    throw new Error(`API paths must be absolute: ${e}`);
  if (r.forbiddenPathPrefixes.some((t) => g(e, t)))
    throw new Error(`Path is outside ${r.productApi}: ${e}`);
  if (!r.allowedPathPrefixes.some((t) => g(e, t)))
    throw new Error(`Path is not part of ${r.productApi}: ${e}`);
}
function x(e, r, t) {
  return k(r, t), new URL(r, `${e.replace(/\/+$/, "")}/`);
}
class D {
  constructor(r) {
    o(this, "baseUrl");
    o(this, "boundary");
    o(this, "fetcher");
    o(this, "headers");
    this.baseUrl = r.baseUrl.replace(/\/+$/, ""), this.boundary = r.boundary, this.fetcher = r.fetcher ?? globalThis.fetch.bind(globalThis), this.headers = r.headers ?? {};
  }
  async request(r, t = {}) {
    const a = this.boundary ? x(this.baseUrl, r, this.boundary) : new URL(r, `${this.baseUrl}/`), i = await this.fetcher(a, {
      method: t.method ?? "GET",
      headers: {
        ...this.headers,
        ...t.body === void 0 ? {} : { "content-type": "application/json" },
        ...t.headers
      },
      body: t.body === void 0 ? void 0 : JSON.stringify(t.body),
      signal: t.signal
    }), c = (i.headers.get("content-type") ?? "").includes("application/json") ? await i.json() : await i.text();
    if (!i.ok)
      throw new $(`Request failed with ${i.status}`, i.status, c);
    return c;
  }
}
function J(e, r) {
  const t = new URLSearchParams();
  return e && t.set("cursor", e), r !== void 0 && t.set("limit", String(r)), t;
}
const p = w({
  loading: !1,
  session: null
}), L = p.Provider;
function u() {
  return S(p);
}
function N(e, r) {
  const t = new Set(e);
  return r.every((a) => t.has(a));
}
function C(e, r) {
  const t = new Set(e);
  return r.some((a) => t.has(a));
}
function M({
  children: e,
  fallback: r = null,
  permissions: t
}) {
  const { session: a } = u();
  return N((a == null ? void 0 : a.permissions) ?? [], t) ? /* @__PURE__ */ n(f, { children: e }) : /* @__PURE__ */ n(f, { children: r });
}
function m({ body: e, title: r }) {
  return /* @__PURE__ */ l("div", { className: "tigrbl-empty-state", children: [
    /* @__PURE__ */ n("h2", { children: r }),
    e && /* @__PURE__ */ n("p", { children: e })
  ] });
}
function W({
  children: e,
  fallback: r
}) {
  const { loading: t, session: a } = u();
  return t ? /* @__PURE__ */ n(m, { title: "Loading session", body: "Checking the current authentication state." }) : a != null && a.authenticated ? /* @__PURE__ */ n(f, { children: e }) : r ?? /* @__PURE__ */ n(m, { title: "Session required", body: "Sign in to continue." });
}
function V(e) {
  return e != null && e.authenticated ? e.username ?? e.email ?? e.subject ?? "Authenticated session" : "Unauthenticated";
}
function d({
  children: e,
  variant: r = "primary",
  ...t
}) {
  return /* @__PURE__ */ n("button", { ...t, className: `tigrbl-button tigrbl-button-${r} ${t.className ?? ""}`.trim(), children: e });
}
function G({
  children: e,
  tone: r = "default",
  ...t
}) {
  return /* @__PURE__ */ n("section", { ...t, className: `tigrbl-card tigrbl-card-${r} ${t.className ?? ""}`.trim(), children: e });
}
function H({
  children: e,
  label: r,
  onCheckedChange: t,
  ...a
}) {
  return /* @__PURE__ */ l("label", { className: "tigrbl-checkbox", children: [
    /* @__PURE__ */ l("span", { className: "tigrbl-checkbox-box", children: [
      /* @__PURE__ */ n(
        "input",
        {
          ...a,
          type: "checkbox",
          onChange: (i) => t == null ? void 0 : t(i.target.checked)
        }
      ),
      /* @__PURE__ */ n("span", { "aria-hidden": "true", className: "tigrbl-checkbox-mark", children: "✓" })
    ] }),
    /* @__PURE__ */ n("span", { children: e ?? r })
  ] });
}
function P({
  children: e,
  onClose: r,
  open: t,
  title: a
}) {
  return t ? /* @__PURE__ */ n("div", { className: "tigrbl-modal-backdrop", role: "presentation", children: /* @__PURE__ */ l("section", { "aria-modal": "true", className: "tigrbl-modal", role: "dialog", children: [
    /* @__PURE__ */ l("header", { children: [
      /* @__PURE__ */ n("h2", { children: a }),
      /* @__PURE__ */ n(d, { onClick: r, type: "button", variant: "subtle", children: "Close" })
    ] }),
    e
  ] }) }) : null;
}
function O({
  body: e,
  confirmLabel: r = "Confirm",
  onCancel: t,
  onConfirm: a,
  open: i,
  title: s
}) {
  return /* @__PURE__ */ l(P, { onClose: t, open: i, title: s, children: [
    /* @__PURE__ */ n("p", { children: e }),
    /* @__PURE__ */ l("div", { className: "tigrbl-actions", children: [
      /* @__PURE__ */ n(d, { onClick: t, type: "button", variant: "subtle", children: "Cancel" }),
      /* @__PURE__ */ n(d, { onClick: a, type: "button", variant: "danger", children: r })
    ] })
  ] });
}
function Q({ text: e }) {
  async function r() {
    await navigator.clipboard.writeText(e);
  }
  return /* @__PURE__ */ n(d, { onClick: () => void r(), type: "button", variant: "subtle", children: "Copy" });
}
function Y({
  columns: e,
  empty: r,
  getRowKey: t,
  items: a
}) {
  return a.length === 0 ? /* @__PURE__ */ n(f, { children: r ?? /* @__PURE__ */ n(m, { title: "No records", body: "There are no records to show yet." }) }) : /* @__PURE__ */ n("div", { className: "tigrbl-table-wrap", children: /* @__PURE__ */ l("table", { className: "tigrbl-table", children: [
    /* @__PURE__ */ n("thead", { children: /* @__PURE__ */ n("tr", { children: e.map((i) => /* @__PURE__ */ n("th", { children: i.header }, i.key)) }) }),
    /* @__PURE__ */ n("tbody", { children: a.map((i) => /* @__PURE__ */ n("tr", { children: e.map((s) => /* @__PURE__ */ n("td", { children: s.render(i) }, s.key)) }, t(i))) })
  ] }) });
}
function z({ children: e, title: r }) {
  return /* @__PURE__ */ l("section", { className: "tigrbl-panel", children: [
    /* @__PURE__ */ n("h2", { children: r }),
    e
  ] });
}
function K({ message: e, title: r = "Something went wrong" }) {
  return /* @__PURE__ */ l("div", { className: "tigrbl-error-state", role: "alert", children: [
    /* @__PURE__ */ n("h2", { children: r }),
    /* @__PURE__ */ n("p", { children: e })
  ] });
}
function T({
  error: e,
  help: r,
  label: t,
  ...a
}) {
  return /* @__PURE__ */ l("label", { className: "tigrbl-field", children: [
    /* @__PURE__ */ l("span", { className: "tigrbl-field-label", children: [
      /* @__PURE__ */ n("span", { children: t }),
      e && /* @__PURE__ */ n(E, { children: e })
    ] }),
    /* @__PURE__ */ n("input", { ...a, "aria-invalid": e ? "true" : a["aria-invalid"] }),
    r && /* @__PURE__ */ n("small", { className: "tigrbl-field-help", children: r })
  ] });
}
function X({ children: e }) {
  return /* @__PURE__ */ n("p", { className: "tigrbl-form-error", children: e });
}
function E({ children: e }) {
  return /* @__PURE__ */ n("span", { className: "tigrbl-validation-message", children: e });
}
function Z({
  children: e,
  label: r,
  ...t
}) {
  return /* @__PURE__ */ n("button", { ...t, "aria-label": r, className: `tigrbl-icon-button ${t.className ?? ""}`.trim(), title: r, children: e });
}
function _(e) {
  return /* @__PURE__ */ n(T, { ...e });
}
function ee({ value: e }) {
  return /* @__PURE__ */ n("pre", { className: "tigrbl-json", children: JSON.stringify(e, null, 2) });
}
function re({ label: e, value: r }) {
  const [t, a] = b(!1);
  return /* @__PURE__ */ l("div", { className: "tigrbl-secret", children: [
    /* @__PURE__ */ n("span", { children: e }),
    /* @__PURE__ */ n("code", { children: t ? r : "••••••••••••" }),
    /* @__PURE__ */ n(d, { onClick: () => a((i) => !i), type: "button", variant: "subtle", children: t ? "Hide" : "Show" })
  ] });
}
function te({
  children: e,
  icon: r,
  label: t,
  ...a
}) {
  return /* @__PURE__ */ l("button", { ...a, className: `tigrbl-social-button ${a.className ?? ""}`.trim(), type: a.type ?? "button", children: [
    r && /* @__PURE__ */ n("span", { "aria-hidden": "true", className: "tigrbl-social-button-icon", children: r }),
    /* @__PURE__ */ n("span", { children: e ?? `Continue with ${t}` })
  ] });
}
function ne({ children: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ n("span", { className: `tigrbl-badge tigrbl-badge-${r}`, children: e });
}
function ae({
  children: e,
  loading: r = !1,
  loadingLabel: t = "Working...",
  ...a
}) {
  return /* @__PURE__ */ n(d, { ...a, disabled: r || a.disabled, type: a.type ?? "submit", children: r ? t : e });
}
function ie({ activeHref: e, items: r }) {
  return /* @__PURE__ */ n("nav", { className: "tigrbl-tabs", children: r.map((t) => /* @__PURE__ */ n("a", { "aria-current": e === t.href ? "page" : void 0, href: t.href, children: t.label }, t.href)) });
}
function le({ message: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ n("div", { className: `tigrbl-toast tigrbl-toast-${r}`, children: e });
}
function se({ children: e }) {
  return /* @__PURE__ */ n("div", { className: "tigrbl-toolbar", children: e });
}
function ce(e) {
  return /* @__PURE__ */ n("textarea", { ...e, className: `tigrbl-json-editor ${e.className ?? ""}`.trim(), spellCheck: !1 });
}
function oe({
  children: e,
  footer: r,
  ...t
}) {
  return /* @__PURE__ */ l("form", { ...t, className: `tigrbl-resource-form ${t.className ?? ""}`.trim(), children: [
    /* @__PURE__ */ n("div", { className: "tigrbl-resource-form-fields", children: e }),
    r && /* @__PURE__ */ n("footer", { children: r })
  ] });
}
function de(e) {
  const [r, t] = b(null), [a, i] = b(!1);
  async function s(...c) {
    t(null), i(!0);
    try {
      return await e(...c);
    } catch (h) {
      return t(h instanceof Error ? h.message : "Request failed"), null;
    } finally {
      i(!1);
    }
  }
  return { error: r, loading: a, run: s };
}
function ue(e, r = []) {
  const [t, a] = b({ data: null, error: null, loading: !0 });
  return A(() => {
    const i = new AbortController();
    return a((s) => ({ ...s, error: null, loading: !0 })), e(i.signal).then((s) => a({ data: s, error: null, loading: !1 })).catch((s) => {
      i.signal.aborted || a({ data: null, error: s instanceof Error ? s.message : "Request failed", loading: !1 });
    }), () => i.abort();
  }, r), t;
}
function he() {
  return u().session;
}
function be() {
  const { session: e } = u(), r = (e == null ? void 0 : e.permissions) ?? [];
  return {
    permissions: r,
    hasAny: (t) => C(r, t),
    hasEvery: (t) => N(r, t)
  };
}
function fe() {
  const { session: e } = u();
  return {
    tenantId: (e == null ? void 0 : e.tenantId) ?? null,
    hasTenantContext: !!(e != null && e.tenantId)
  };
}
function U({
  activeHref: e,
  apiBaseUrl: r,
  items: t,
  productApi: a,
  title: i
}) {
  return /* @__PURE__ */ l("aside", { className: "tigrbl-sidebar", children: [
    /* @__PURE__ */ n("p", { className: "tigrbl-sidebar-product", children: a }),
    /* @__PURE__ */ n("h1", { children: i }),
    /* @__PURE__ */ n("nav", { children: t.map((s) => {
      const c = e === s.href || e.startsWith(`${s.href}/`);
      return /* @__PURE__ */ l("a", { "aria-current": c ? "page" : void 0, href: s.href, children: [
        /* @__PURE__ */ n("span", { children: s.label }),
        s.badge && /* @__PURE__ */ n("small", { children: s.badge })
      ] }, s.href);
    }) }),
    r && /* @__PURE__ */ l("p", { className: "tigrbl-sidebar-api", children: [
      "API: ",
      /* @__PURE__ */ n("code", { children: r })
    ] })
  ] });
}
function B({ onLogout: e, sessionLabel: r }) {
  return /* @__PURE__ */ l("header", { className: "tigrbl-topbar", children: [
    /* @__PURE__ */ n("span", { children: r ?? "No active session" }),
    e && /* @__PURE__ */ n(d, { onClick: e, type: "button", variant: "subtle", children: "Sign out" })
  ] });
}
function me({
  activeHref: e,
  apiBaseUrl: r,
  children: t,
  navigation: a,
  onLogout: i,
  productApi: s,
  sessionLabel: c,
  title: h
}) {
  return /* @__PURE__ */ l("main", { className: "tigrbl-shell", children: [
    /* @__PURE__ */ n(U, { activeHref: e, apiBaseUrl: r, items: a, productApi: s, title: h }),
    /* @__PURE__ */ l("section", { className: "tigrbl-shell-main", children: [
      /* @__PURE__ */ n(B, { onLogout: i, sessionLabel: c }),
      /* @__PURE__ */ n("div", { className: "tigrbl-shell-content", children: t })
    ] })
  ] });
}
function j({
  label: e = "Tigrbl Auth",
  logoLetter: r
}) {
  const t = r ?? (e.trim().charAt(0).toUpperCase() || "T");
  return /* @__PURE__ */ l("div", { className: "tigrbl-brand-mark", children: [
    /* @__PURE__ */ n("span", { className: "tigrbl-brand-mark-glyph", children: t }),
    /* @__PURE__ */ n("span", { className: "tigrbl-brand-mark-label", children: e })
  ] });
}
function R({
  actions: e,
  label: r = "Tigrbl Auth",
  logoLetter: t
}) {
  return /* @__PURE__ */ l("header", { className: "tigrbl-brand-header", children: [
    /* @__PURE__ */ n(j, { label: r, logoLetter: t }),
    e && /* @__PURE__ */ n("nav", { className: "tigrbl-brand-header-actions", children: e })
  ] });
}
function ge({
  children: e,
  footer: r,
  productApi: t,
  subtitle: a,
  title: i
}) {
  return /* @__PURE__ */ l("main", { className: "tigrbl-auth-shell", children: [
    /* @__PURE__ */ n(R, { label: "Tigrbl Auth" }),
    /* @__PURE__ */ l("section", { className: "tigrbl-auth-shell-content", children: [
      /* @__PURE__ */ l("div", { className: "tigrbl-auth-copy", children: [
        t && /* @__PURE__ */ n("p", { className: "tigrbl-eyebrow", children: t }),
        /* @__PURE__ */ n("h1", { children: i }),
        a && /* @__PURE__ */ n("p", { children: a })
      ] }),
      e
    ] }),
    /* @__PURE__ */ n("footer", { className: "tigrbl-auth-footer", children: r ?? /* @__PURE__ */ l("span", { children: [
      "© ",
      (/* @__PURE__ */ new Date()).getFullYear(),
      " Tigrbl Auth"
    ] }) })
  ] });
}
function pe({ items: e }) {
  return /* @__PURE__ */ n("nav", { "aria-label": "Breadcrumbs", className: "tigrbl-breadcrumbs", children: e.map((r, t) => /* @__PURE__ */ n("a", { href: r.href, "aria-current": t === e.length - 1 ? "page" : void 0, children: r.label }, r.href)) });
}
function Ne({
  actions: e,
  description: r,
  title: t
}) {
  return /* @__PURE__ */ l("header", { className: "tigrbl-page-header", children: [
    /* @__PURE__ */ l("div", { children: [
      /* @__PURE__ */ n("h1", { children: t }),
      r && /* @__PURE__ */ n("p", { children: r })
    ] }),
    e && /* @__PURE__ */ n("div", { className: "tigrbl-page-actions", children: e })
  ] });
}
export {
  D as ApiClient,
  $ as ApiError,
  me as AppShell,
  L as AuthProvider,
  ge as AuthShell,
  R as BrandHeader,
  j as BrandMark,
  pe as Breadcrumbs,
  d as Button,
  G as Card,
  H as Checkbox,
  O as ConfirmDialog,
  Q as CopyButton,
  Y as DataTable,
  z as DetailPanel,
  m as EmptyState,
  K as ErrorState,
  X as FormError,
  T as FormField,
  Z as IconButton,
  _ as Input,
  ce as JsonEditor,
  ee as JsonViewer,
  P as Modal,
  Ne as PageHeader,
  M as PermissionGate,
  W as RequireAuth,
  oe as ResourceForm,
  re as SecretField,
  U as Sidebar,
  te as SocialButton,
  ne as StatusBadge,
  ae as SubmitButton,
  ie as Tabs,
  le as Toast,
  se as Toolbar,
  B as Topbar,
  E as ValidationMessage,
  k as assertSurfacePath,
  x as createSurfaceUrl,
  V as describeSession,
  J as encodeCursorParams,
  C as hasAnyPermission,
  N as hasEveryPermission,
  de as useApiMutation,
  ue as useApiQuery,
  u as useAuthContext,
  he as useCurrentUser,
  be as usePermissions,
  fe as useTenantContext
};
