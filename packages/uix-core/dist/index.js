var y = Object.defineProperty;
var v = (e, r, t) => r in e ? y(e, r, { enumerable: !0, configurable: !0, writable: !0, value: t }) : e[r] = t;
var o = (e, r, t) => v(e, typeof r != "symbol" ? r + "" : r, t);
import { createContext as w, useContext as S, useState as b, useEffect as $ } from "react";
import { jsx as n, Fragment as m, jsxs as l } from "react/jsx-runtime";
class A extends Error {
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
function C(e, r) {
  if (!e.startsWith("/"))
    throw new Error(`API paths must be absolute: ${e}`);
  if (r.forbiddenPathPrefixes.some((t) => g(e, t)))
    throw new Error(`Path is outside ${r.productApi}: ${e}`);
  if (!r.allowedPathPrefixes.some((t) => g(e, t)))
    throw new Error(`Path is not part of ${r.productApi}: ${e}`);
}
function k(e, r, t) {
  return C(r, t), new URL(r, `${e.replace(/\/+$/, "")}/`);
}
class M {
  constructor(r) {
    o(this, "baseUrl");
    o(this, "boundary");
    o(this, "fetcher");
    o(this, "headers");
    this.baseUrl = r.baseUrl.replace(/\/+$/, ""), this.boundary = r.boundary, this.fetcher = r.fetcher ?? globalThis.fetch.bind(globalThis), this.headers = r.headers ?? {};
  }
  async request(r, t = {}) {
    const a = this.boundary ? k(this.baseUrl, r, this.boundary) : new URL(r, `${this.baseUrl}/`), i = await this.fetcher(a, {
      method: t.method ?? "GET",
      headers: {
        ...this.headers,
        ...t.body === void 0 ? {} : { "content-type": "application/json" },
        ...t.headers
      },
      body: t.body === void 0 ? void 0 : JSON.stringify(t.body),
      signal: t.signal
    }), s = (i.headers.get("content-type") ?? "").includes("application/json") ? await i.json() : await i.text();
    if (!i.ok)
      throw new A(`Request failed with ${i.status}`, i.status, s);
    return s;
  }
}
function D(e, r) {
  const t = new URLSearchParams();
  return e && t.set("cursor", e), r !== void 0 && t.set("limit", String(r)), t;
}
const N = w({
  loading: !1,
  session: null
}), J = N.Provider;
function u() {
  return S(N);
}
function p(e, r) {
  const t = new Set(e);
  return r.every((a) => t.has(a));
}
function x(e, r) {
  const t = new Set(e);
  return r.some((a) => t.has(a));
}
function L({
  children: e,
  fallback: r = null,
  permissions: t
}) {
  const { session: a } = u();
  return p((a == null ? void 0 : a.permissions) ?? [], t) ? /* @__PURE__ */ n(m, { children: e }) : /* @__PURE__ */ n(m, { children: r });
}
function f({ body: e, title: r }) {
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
  return t ? /* @__PURE__ */ n(f, { title: "Loading session", body: "Checking the current authentication state." }) : a != null && a.authenticated ? /* @__PURE__ */ n(m, { children: e }) : r ?? /* @__PURE__ */ n(f, { title: "Session required", body: "Sign in to continue." });
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
  title: c
}) {
  return /* @__PURE__ */ l(P, { onClose: t, open: i, title: c, children: [
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
  return a.length === 0 ? /* @__PURE__ */ n(m, { children: r ?? /* @__PURE__ */ n(f, { title: "No records", body: "There are no records to show yet." }) }) : /* @__PURE__ */ n("div", { className: "tigrbl-table-wrap", children: /* @__PURE__ */ l("table", { className: "tigrbl-table", children: [
    /* @__PURE__ */ n("thead", { children: /* @__PURE__ */ n("tr", { children: e.map((i) => /* @__PURE__ */ n("th", { children: i.header }, i.key)) }) }),
    /* @__PURE__ */ n("tbody", { children: a.map((i) => /* @__PURE__ */ n("tr", { children: e.map((c) => /* @__PURE__ */ n("td", { children: c.render(i) }, c.key)) }, t(i))) })
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
function re({
  description: e,
  label: r,
  value: t,
  ...a
}) {
  return /* @__PURE__ */ l("article", { ...a, className: `tigrbl-metric-card ${a.className ?? ""}`.trim(), children: [
    /* @__PURE__ */ n("p", { className: "tigrbl-metric-card-label", children: r }),
    /* @__PURE__ */ n("strong", { className: "tigrbl-metric-card-value", children: t }),
    e && /* @__PURE__ */ n("p", { className: "tigrbl-metric-card-description", children: e })
  ] });
}
function te({ label: e, value: r }) {
  const [t, a] = b(!1);
  return /* @__PURE__ */ l("div", { className: "tigrbl-secret", children: [
    /* @__PURE__ */ n("span", { children: e }),
    /* @__PURE__ */ n("code", { children: t ? r : "••••••••••••" }),
    /* @__PURE__ */ n(d, { onClick: () => a((i) => !i), type: "button", variant: "subtle", children: t ? "Hide" : "Show" })
  ] });
}
function ne({
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
function ae({ children: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ n("span", { className: `tigrbl-badge tigrbl-badge-${r}`, children: e });
}
function ie({
  children: e,
  loading: r = !1,
  loadingLabel: t = "Working...",
  ...a
}) {
  return /* @__PURE__ */ n(d, { ...a, disabled: r || a.disabled, type: a.type ?? "submit", children: r ? t : e });
}
function le({ activeHref: e, items: r }) {
  return /* @__PURE__ */ n("nav", { className: "tigrbl-tabs", children: r.map((t) => /* @__PURE__ */ n("a", { "aria-current": e === t.href ? "page" : void 0, href: t.href, children: t.label }, t.href)) });
}
function ce({ message: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ n("div", { className: `tigrbl-toast tigrbl-toast-${r}`, children: e });
}
function se({ children: e }) {
  return /* @__PURE__ */ n("div", { className: "tigrbl-toolbar", children: e });
}
function oe(e) {
  return /* @__PURE__ */ n("textarea", { ...e, className: `tigrbl-json-editor ${e.className ?? ""}`.trim(), spellCheck: !1 });
}
function de({
  children: e,
  footer: r,
  ...t
}) {
  return /* @__PURE__ */ l("form", { ...t, className: `tigrbl-resource-form ${t.className ?? ""}`.trim(), children: [
    /* @__PURE__ */ n("div", { className: "tigrbl-resource-form-fields", children: e }),
    r && /* @__PURE__ */ n("footer", { children: r })
  ] });
}
function ue(e) {
  const [r, t] = b(null), [a, i] = b(!1);
  async function c(...s) {
    t(null), i(!0);
    try {
      return await e(...s);
    } catch (h) {
      return t(h instanceof Error ? h.message : "Request failed"), null;
    } finally {
      i(!1);
    }
  }
  return { error: r, loading: a, run: c };
}
function he(e, r = []) {
  const [t, a] = b({ data: null, error: null, loading: !0 });
  return $(() => {
    const i = new AbortController();
    return a((c) => ({ ...c, error: null, loading: !0 })), e(i.signal).then((c) => a({ data: c, error: null, loading: !1 })).catch((c) => {
      i.signal.aborted || a({ data: null, error: c instanceof Error ? c.message : "Request failed", loading: !1 });
    }), () => i.abort();
  }, r), t;
}
function be() {
  return u().session;
}
function me() {
  const { session: e } = u(), r = (e == null ? void 0 : e.permissions) ?? [];
  return {
    permissions: r,
    hasAny: (t) => x(r, t),
    hasEvery: (t) => p(r, t)
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
    /* @__PURE__ */ n("nav", { children: t.map((c) => {
      const s = e === c.href || e.startsWith(`${c.href}/`);
      return /* @__PURE__ */ l("a", { "aria-current": s ? "page" : void 0, href: c.href, children: [
        /* @__PURE__ */ n("span", { children: c.label }),
        c.badge && /* @__PURE__ */ n("small", { children: c.badge })
      ] }, c.href);
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
function ge({
  activeHref: e,
  apiBaseUrl: r,
  children: t,
  navigation: a,
  onLogout: i,
  productApi: c,
  sessionLabel: s,
  title: h
}) {
  return /* @__PURE__ */ l("main", { className: "tigrbl-shell", children: [
    /* @__PURE__ */ n(U, { activeHref: e, apiBaseUrl: r, items: a, productApi: c, title: h }),
    /* @__PURE__ */ l("section", { className: "tigrbl-shell-main", children: [
      /* @__PURE__ */ n(B, { onLogout: i, sessionLabel: s }),
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
function Ne({
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
function ye({
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
  M as ApiClient,
  A as ApiError,
  ge as AppShell,
  J as AuthProvider,
  Ne as AuthShell,
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
  f as EmptyState,
  K as ErrorState,
  X as FormError,
  T as FormField,
  Z as IconButton,
  _ as Input,
  oe as JsonEditor,
  ee as JsonViewer,
  re as MetricCard,
  P as Modal,
  ye as PageHeader,
  L as PermissionGate,
  W as RequireAuth,
  de as ResourceForm,
  te as SecretField,
  U as Sidebar,
  ne as SocialButton,
  ae as StatusBadge,
  ie as SubmitButton,
  le as Tabs,
  ce as Toast,
  se as Toolbar,
  B as Topbar,
  E as ValidationMessage,
  C as assertSurfacePath,
  k as createSurfaceUrl,
  V as describeSession,
  D as encodeCursorParams,
  x as hasAnyPermission,
  p as hasEveryPermission,
  ue as useApiMutation,
  he as useApiQuery,
  u as useAuthContext,
  be as useCurrentUser,
  me as usePermissions,
  fe as useTenantContext
};
