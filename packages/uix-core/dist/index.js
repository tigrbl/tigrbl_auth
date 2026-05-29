var N = Object.defineProperty;
var v = (e, r, t) => r in e ? N(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t;
var o = (e, r, t) => v(e, typeof r != "symbol" ? r + "" : r, t);
import { createContext as w, useContext as C, useState as b, useEffect as S } from "react";
import { jsx as n, Fragment as f, jsxs as s } from "react/jsx-runtime";
class P extends Error {
  constructor(t, a, i = null) {
    super(t);
    o(this, "status");
    o(this, "payload");
    this.name = "ApiError", this.status = a, this.payload = i;
  }
}
function m(e, r) {
  return e === r || e.startsWith(`${r}/`);
}
function $(e, r) {
  if (!e.startsWith("/"))
    throw new Error(`API paths must be absolute: ${e}`);
  if (r.forbiddenPathPrefixes.some((t) => m(e, t)))
    throw new Error(`Path is outside ${r.productApi}: ${e}`);
  if (!r.allowedPathPrefixes.some((t) => m(e, t)))
    throw new Error(`Path is not part of ${r.productApi}: ${e}`);
}
function A(e, r, t) {
  return $(r, t), new URL(r, `${e.replace(/\/+$/, "")}/`);
}
class q {
  constructor(r) {
    o(this, "baseUrl");
    o(this, "boundary");
    o(this, "fetcher");
    o(this, "headers");
    this.baseUrl = r.baseUrl.replace(/\/+$/, ""), this.boundary = r.boundary, this.fetcher = r.fetcher ?? globalThis.fetch.bind(globalThis), this.headers = r.headers ?? {};
  }
  async request(r, t = {}) {
    const a = this.boundary ? A(this.baseUrl, r, this.boundary) : new URL(r, `${this.baseUrl}/`), i = await this.fetcher(a, {
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
      throw new P(`Request failed with ${i.status}`, i.status, c);
    return c;
  }
}
function B(e, r) {
  const t = new URLSearchParams();
  return e && t.set("cursor", e), r !== void 0 && t.set("limit", String(r)), t;
}
const p = w({
  loading: !1,
  session: null
}), I = p.Provider;
function d() {
  return C(p);
}
function y(e, r) {
  const t = new Set(e);
  return r.every((a) => t.has(a));
}
function E(e, r) {
  const t = new Set(e);
  return r.some((a) => t.has(a));
}
function F({
  children: e,
  fallback: r = null,
  permissions: t
}) {
  const { session: a } = d();
  return y((a == null ? void 0 : a.permissions) ?? [], t) ? /* @__PURE__ */ n(f, { children: e }) : /* @__PURE__ */ n(f, { children: r });
}
function g({ body: e, title: r }) {
  return /* @__PURE__ */ s("div", { className: "tigrbl-empty-state", children: [
    /* @__PURE__ */ n("h2", { children: r }),
    e && /* @__PURE__ */ n("p", { children: e })
  ] });
}
function J({
  children: e,
  fallback: r
}) {
  const { loading: t, session: a } = d();
  return t ? /* @__PURE__ */ n(g, { title: "Loading session", body: "Checking the current authentication state." }) : a != null && a.authenticated ? /* @__PURE__ */ n(f, { children: e }) : r ?? /* @__PURE__ */ n(g, { title: "Session required", body: "Sign in to continue." });
}
function L(e) {
  return e != null && e.authenticated ? e.username ?? e.email ?? e.subject ?? "Authenticated session" : "Unauthenticated";
}
function u({
  children: e,
  variant: r = "primary",
  ...t
}) {
  return /* @__PURE__ */ n("button", { ...t, className: `tigrbl-button tigrbl-button-${r} ${t.className ?? ""}`.trim(), children: e });
}
function x({
  children: e,
  onClose: r,
  open: t,
  title: a
}) {
  return t ? /* @__PURE__ */ n("div", { className: "tigrbl-modal-backdrop", role: "presentation", children: /* @__PURE__ */ s("section", { "aria-modal": "true", className: "tigrbl-modal", role: "dialog", children: [
    /* @__PURE__ */ s("header", { children: [
      /* @__PURE__ */ n("h2", { children: a }),
      /* @__PURE__ */ n(u, { onClick: r, type: "button", variant: "subtle", children: "Close" })
    ] }),
    e
  ] }) }) : null;
}
function D({
  body: e,
  confirmLabel: r = "Confirm",
  onCancel: t,
  onConfirm: a,
  open: i,
  title: l
}) {
  return /* @__PURE__ */ s(x, { onClose: t, open: i, title: l, children: [
    /* @__PURE__ */ n("p", { children: e }),
    /* @__PURE__ */ s("div", { className: "tigrbl-actions", children: [
      /* @__PURE__ */ n(u, { onClick: t, type: "button", variant: "subtle", children: "Cancel" }),
      /* @__PURE__ */ n(u, { onClick: a, type: "button", variant: "danger", children: r })
    ] })
  ] });
}
function W({ text: e }) {
  async function r() {
    await navigator.clipboard.writeText(e);
  }
  return /* @__PURE__ */ n(u, { onClick: () => void r(), type: "button", variant: "subtle", children: "Copy" });
}
function G({
  columns: e,
  empty: r,
  getRowKey: t,
  items: a
}) {
  return a.length === 0 ? /* @__PURE__ */ n(f, { children: r ?? /* @__PURE__ */ n(g, { title: "No records", body: "There are no records to show yet." }) }) : /* @__PURE__ */ n("div", { className: "tigrbl-table-wrap", children: /* @__PURE__ */ s("table", { className: "tigrbl-table", children: [
    /* @__PURE__ */ n("thead", { children: /* @__PURE__ */ n("tr", { children: e.map((i) => /* @__PURE__ */ n("th", { children: i.header }, i.key)) }) }),
    /* @__PURE__ */ n("tbody", { children: a.map((i) => /* @__PURE__ */ n("tr", { children: e.map((l) => /* @__PURE__ */ n("td", { children: l.render(i) }, l.key)) }, t(i))) })
  ] }) });
}
function M({ children: e, title: r }) {
  return /* @__PURE__ */ s("section", { className: "tigrbl-panel", children: [
    /* @__PURE__ */ n("h2", { children: r }),
    e
  ] });
}
function O({ message: e, title: r = "Something went wrong" }) {
  return /* @__PURE__ */ s("div", { className: "tigrbl-error-state", role: "alert", children: [
    /* @__PURE__ */ n("h2", { children: r }),
    /* @__PURE__ */ n("p", { children: e })
  ] });
}
function V({
  help: e,
  label: r,
  ...t
}) {
  return /* @__PURE__ */ s("label", { className: "tigrbl-field", children: [
    /* @__PURE__ */ n("span", { children: r }),
    /* @__PURE__ */ n("input", { ...t }),
    e && /* @__PURE__ */ n("small", { children: e })
  ] });
}
function H({
  children: e,
  label: r,
  ...t
}) {
  return /* @__PURE__ */ n("button", { ...t, "aria-label": r, className: `tigrbl-icon-button ${t.className ?? ""}`.trim(), title: r, children: e });
}
function Q({ value: e }) {
  return /* @__PURE__ */ n("pre", { className: "tigrbl-json", children: JSON.stringify(e, null, 2) });
}
function z({ label: e, value: r }) {
  const [t, a] = b(!1);
  return /* @__PURE__ */ s("div", { className: "tigrbl-secret", children: [
    /* @__PURE__ */ n("span", { children: e }),
    /* @__PURE__ */ n("code", { children: t ? r : "••••••••••••" }),
    /* @__PURE__ */ n(u, { onClick: () => a((i) => !i), type: "button", variant: "subtle", children: t ? "Hide" : "Show" })
  ] });
}
function K({ children: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ n("span", { className: `tigrbl-badge tigrbl-badge-${r}`, children: e });
}
function X({ activeHref: e, items: r }) {
  return /* @__PURE__ */ n("nav", { className: "tigrbl-tabs", children: r.map((t) => /* @__PURE__ */ n("a", { "aria-current": e === t.href ? "page" : void 0, href: t.href, children: t.label }, t.href)) });
}
function Y({ message: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ n("div", { className: `tigrbl-toast tigrbl-toast-${r}`, children: e });
}
function Z({ children: e }) {
  return /* @__PURE__ */ n("div", { className: "tigrbl-toolbar", children: e });
}
function _(e) {
  return /* @__PURE__ */ n("textarea", { ...e, className: `tigrbl-json-editor ${e.className ?? ""}`.trim(), spellCheck: !1 });
}
function ee({
  children: e,
  footer: r,
  ...t
}) {
  return /* @__PURE__ */ s("form", { ...t, className: `tigrbl-resource-form ${t.className ?? ""}`.trim(), children: [
    /* @__PURE__ */ n("div", { className: "tigrbl-resource-form-fields", children: e }),
    r && /* @__PURE__ */ n("footer", { children: r })
  ] });
}
function re(e) {
  const [r, t] = b(null), [a, i] = b(!1);
  async function l(...c) {
    t(null), i(!0);
    try {
      return await e(...c);
    } catch (h) {
      return t(h instanceof Error ? h.message : "Request failed"), null;
    } finally {
      i(!1);
    }
  }
  return { error: r, loading: a, run: l };
}
function te(e, r = []) {
  const [t, a] = b({ data: null, error: null, loading: !0 });
  return S(() => {
    const i = new AbortController();
    return a((l) => ({ ...l, error: null, loading: !0 })), e(i.signal).then((l) => a({ data: l, error: null, loading: !1 })).catch((l) => {
      i.signal.aborted || a({ data: null, error: l instanceof Error ? l.message : "Request failed", loading: !1 });
    }), () => i.abort();
  }, r), t;
}
function ne() {
  return d().session;
}
function ae() {
  const { session: e } = d(), r = (e == null ? void 0 : e.permissions) ?? [];
  return {
    permissions: r,
    hasAny: (t) => E(r, t),
    hasEvery: (t) => y(r, t)
  };
}
function ie() {
  const { session: e } = d();
  return {
    tenantId: (e == null ? void 0 : e.tenantId) ?? null,
    hasTenantContext: !!(e != null && e.tenantId)
  };
}
function T({
  activeHref: e,
  apiBaseUrl: r,
  items: t,
  productApi: a,
  title: i
}) {
  return /* @__PURE__ */ s("aside", { className: "tigrbl-sidebar", children: [
    /* @__PURE__ */ n("p", { className: "tigrbl-sidebar-product", children: a }),
    /* @__PURE__ */ n("h1", { children: i }),
    /* @__PURE__ */ n("nav", { children: t.map((l) => {
      const c = e === l.href || e.startsWith(`${l.href}/`);
      return /* @__PURE__ */ s("a", { "aria-current": c ? "page" : void 0, href: l.href, children: [
        /* @__PURE__ */ n("span", { children: l.label }),
        l.badge && /* @__PURE__ */ n("small", { children: l.badge })
      ] }, l.href);
    }) }),
    r && /* @__PURE__ */ s("p", { className: "tigrbl-sidebar-api", children: [
      "API: ",
      /* @__PURE__ */ n("code", { children: r })
    ] })
  ] });
}
function k({ onLogout: e, sessionLabel: r }) {
  return /* @__PURE__ */ s("header", { className: "tigrbl-topbar", children: [
    /* @__PURE__ */ n("span", { children: r ?? "No active session" }),
    e && /* @__PURE__ */ n(u, { onClick: e, type: "button", variant: "subtle", children: "Sign out" })
  ] });
}
function le({
  activeHref: e,
  apiBaseUrl: r,
  children: t,
  navigation: a,
  onLogout: i,
  productApi: l,
  sessionLabel: c,
  title: h
}) {
  return /* @__PURE__ */ s("main", { className: "tigrbl-shell", children: [
    /* @__PURE__ */ n(T, { activeHref: e, apiBaseUrl: r, items: a, productApi: l, title: h }),
    /* @__PURE__ */ s("section", { className: "tigrbl-shell-main", children: [
      /* @__PURE__ */ n(k, { onLogout: i, sessionLabel: c }),
      /* @__PURE__ */ n("div", { className: "tigrbl-shell-content", children: t })
    ] })
  ] });
}
function se({ items: e }) {
  return /* @__PURE__ */ n("nav", { "aria-label": "Breadcrumbs", className: "tigrbl-breadcrumbs", children: e.map((r, t) => /* @__PURE__ */ n("a", { href: r.href, "aria-current": t === e.length - 1 ? "page" : void 0, children: r.label }, r.href)) });
}
function ce({
  actions: e,
  description: r,
  title: t
}) {
  return /* @__PURE__ */ s("header", { className: "tigrbl-page-header", children: [
    /* @__PURE__ */ s("div", { children: [
      /* @__PURE__ */ n("h1", { children: t }),
      r && /* @__PURE__ */ n("p", { children: r })
    ] }),
    e && /* @__PURE__ */ n("div", { className: "tigrbl-page-actions", children: e })
  ] });
}
export {
  q as ApiClient,
  P as ApiError,
  le as AppShell,
  I as AuthProvider,
  se as Breadcrumbs,
  u as Button,
  D as ConfirmDialog,
  W as CopyButton,
  G as DataTable,
  M as DetailPanel,
  g as EmptyState,
  O as ErrorState,
  V as FormField,
  H as IconButton,
  _ as JsonEditor,
  Q as JsonViewer,
  x as Modal,
  ce as PageHeader,
  F as PermissionGate,
  J as RequireAuth,
  ee as ResourceForm,
  z as SecretField,
  T as Sidebar,
  K as StatusBadge,
  X as Tabs,
  Y as Toast,
  Z as Toolbar,
  k as Topbar,
  $ as assertSurfacePath,
  A as createSurfaceUrl,
  L as describeSession,
  B as encodeCursorParams,
  E as hasAnyPermission,
  y as hasEveryPermission,
  re as useApiMutation,
  te as useApiQuery,
  d as useAuthContext,
  ne as useCurrentUser,
  ae as usePermissions,
  ie as useTenantContext
};
