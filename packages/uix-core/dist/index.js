var x = Object.defineProperty;
var E = (e, r, n) => r in e ? x(e, r, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[r] = n;
var u = (e, r, n) => E(e, typeof r != "symbol" ? r + "" : r, n);
import { createContext as T, useContext as P, useState as h, useEffect as R, useCallback as p } from "react";
import { jsx as t, Fragment as f, jsxs as i } from "react/jsx-runtime";
class M extends Error {
  constructor(n, a, l = null) {
    super(n);
    u(this, "status");
    u(this, "payload");
    this.name = "ApiError", this.status = a, this.payload = l;
  }
}
function y(e, r) {
  return e === r || e.startsWith(`${r}/`);
}
function D(e, r) {
  if (!e.startsWith("/"))
    throw new Error(`API paths must be absolute: ${e}`);
  if (r.forbiddenPathPrefixes.some((n) => y(e, n)))
    throw new Error(`Path is outside ${r.productApi}: ${e}`);
  if (!r.allowedPathPrefixes.some((n) => y(e, n)))
    throw new Error(`Path is not part of ${r.productApi}: ${e}`);
}
function U(e, r, n) {
  return D(r, n), new URL(r, `${e.replace(/\/+$/, "")}/`);
}
class O {
  constructor(r) {
    u(this, "baseUrl");
    u(this, "boundary");
    u(this, "fetcher");
    u(this, "headers");
    this.baseUrl = r.baseUrl.replace(/\/+$/, ""), this.boundary = r.boundary, this.fetcher = r.fetcher ?? globalThis.fetch.bind(globalThis), this.headers = r.headers ?? {};
  }
  async request(r, n = {}) {
    const a = this.boundary ? U(this.baseUrl, r, this.boundary) : new URL(r, `${this.baseUrl}/`), l = await this.fetcher(a, {
      method: n.method ?? "GET",
      headers: {
        ...this.headers,
        ...n.body === void 0 ? {} : { "content-type": "application/json" },
        ...n.headers
      },
      body: n.body === void 0 ? void 0 : JSON.stringify(n.body),
      signal: n.signal
    }), c = (l.headers.get("content-type") ?? "").includes("application/json") ? await l.json() : await l.text();
    if (!l.ok)
      throw new M(`Request failed with ${l.status}`, l.status, c);
    return c;
  }
}
function Q(e, r) {
  const n = new URLSearchParams();
  return e && n.set("cursor", e), r !== void 0 && n.set("limit", String(r)), n;
}
const w = T({
  loading: !1,
  session: null
}), Y = w.Provider;
function m() {
  return P(w);
}
function C(e, r) {
  const n = new Set(e);
  return r.every((a) => n.has(a));
}
function B(e, r) {
  const n = new Set(e);
  return r.some((a) => n.has(a));
}
function Z({
  children: e,
  fallback: r = null,
  permissions: n
}) {
  const { session: a } = m();
  return C((a == null ? void 0 : a.permissions) ?? [], n) ? /* @__PURE__ */ t(f, { children: e }) : /* @__PURE__ */ t(f, { children: r });
}
function N({ body: e, title: r }) {
  return /* @__PURE__ */ i("div", { className: "tigrbl-empty-state", children: [
    /* @__PURE__ */ t("h2", { children: r }),
    e && /* @__PURE__ */ t("p", { children: e })
  ] });
}
function K({
  children: e,
  fallback: r
}) {
  const { loading: n, session: a } = m();
  return n ? /* @__PURE__ */ t(N, { title: "Loading session", body: "Checking the current authentication state." }) : a != null && a.authenticated ? /* @__PURE__ */ t(f, { children: e }) : r ?? /* @__PURE__ */ t(N, { title: "Session required", body: "Sign in to continue." });
}
function X(e) {
  return e != null && e.authenticated ? e.username ?? e.email ?? e.subject ?? "Authenticated session" : "Unauthenticated";
}
function F({ message: e, title: r = "Something went wrong" }) {
  return /* @__PURE__ */ i("div", { className: "tigrbl-error-state", role: "alert", children: [
    /* @__PURE__ */ t("h2", { children: r }),
    /* @__PURE__ */ t("p", { children: e })
  ] });
}
function _({
  message: e,
  title: r = "Request failed"
}) {
  return e ? /* @__PURE__ */ t(F, { title: r, message: e }) : null;
}
function d({
  children: e,
  variant: r = "primary",
  ...n
}) {
  return /* @__PURE__ */ t("button", { ...n, className: `tigrbl-button tigrbl-button-${r} ${n.className ?? ""}`.trim(), children: e });
}
function ee({
  children: e,
  tone: r = "default",
  ...n
}) {
  return /* @__PURE__ */ t("section", { ...n, className: `tigrbl-card tigrbl-card-${r} ${n.className ?? ""}`.trim(), children: e });
}
function re({
  children: e,
  label: r,
  onCheckedChange: n,
  ...a
}) {
  return /* @__PURE__ */ i("label", { className: "tigrbl-checkbox", children: [
    /* @__PURE__ */ i("span", { className: "tigrbl-checkbox-box", children: [
      /* @__PURE__ */ t(
        "input",
        {
          ...a,
          type: "checkbox",
          onChange: (l) => n == null ? void 0 : n(l.target.checked)
        }
      ),
      /* @__PURE__ */ t("span", { "aria-hidden": "true", className: "tigrbl-checkbox-mark", children: "✓" })
    ] }),
    /* @__PURE__ */ t("span", { children: e ?? r })
  ] });
}
function k({
  children: e,
  onClose: r,
  open: n,
  title: a
}) {
  return n ? /* @__PURE__ */ t("div", { className: "tigrbl-modal-backdrop", role: "presentation", children: /* @__PURE__ */ i("section", { "aria-modal": "true", className: "tigrbl-modal", role: "dialog", children: [
    /* @__PURE__ */ i("header", { children: [
      /* @__PURE__ */ t("h2", { children: a }),
      /* @__PURE__ */ t(d, { onClick: r, type: "button", variant: "subtle", children: "Close" })
    ] }),
    e
  ] }) }) : null;
}
function te({
  body: e,
  confirmLabel: r = "Confirm",
  onCancel: n,
  onConfirm: a,
  open: l,
  title: s
}) {
  return /* @__PURE__ */ i(k, { onClose: n, open: l, title: s, children: [
    /* @__PURE__ */ t("p", { children: e }),
    /* @__PURE__ */ i("div", { className: "tigrbl-actions", children: [
      /* @__PURE__ */ t(d, { onClick: n, type: "button", variant: "subtle", children: "Cancel" }),
      /* @__PURE__ */ t(d, { onClick: a, type: "button", variant: "danger", children: r })
    ] })
  ] });
}
function ne({
  help: e,
  label: r,
  rows: n = 8,
  ...a
}) {
  return /* @__PURE__ */ i("label", { className: "tigrbl-field", children: [
    /* @__PURE__ */ t("span", { className: "tigrbl-field-label", children: r }),
    /* @__PURE__ */ t("textarea", { ...a, className: `tigrbl-code-field ${a.className ?? ""}`.trim(), rows: n }),
    e && /* @__PURE__ */ t("span", { className: "tigrbl-field-help", children: e })
  ] });
}
function ae({ text: e }) {
  async function r() {
    await navigator.clipboard.writeText(e);
  }
  return /* @__PURE__ */ t(d, { onClick: () => void r(), type: "button", variant: "subtle", children: "Copy" });
}
function le({
  action: e,
  children: r,
  title: n = "Danger zone"
}) {
  return /* @__PURE__ */ i("section", { className: "tigrbl-danger-zone", children: [
    /* @__PURE__ */ i("div", { children: [
      /* @__PURE__ */ t("h2", { children: n }),
      /* @__PURE__ */ t("div", { className: "tigrbl-danger-zone-body", children: r })
    ] }),
    e && /* @__PURE__ */ t("div", { className: "tigrbl-danger-zone-action", children: e })
  ] });
}
function j({
  columns: e,
  empty: r,
  getRowKey: n,
  items: a
}) {
  return a.length === 0 ? /* @__PURE__ */ t(f, { children: r ?? /* @__PURE__ */ t(N, { title: "No records", body: "There are no records to show yet." }) }) : /* @__PURE__ */ t("div", { className: "tigrbl-table-wrap", children: /* @__PURE__ */ i("table", { className: "tigrbl-table", children: [
    /* @__PURE__ */ t("thead", { children: /* @__PURE__ */ t("tr", { children: e.map((l) => /* @__PURE__ */ t("th", { children: l.header }, l.key)) }) }),
    /* @__PURE__ */ t("tbody", { children: a.map((l) => /* @__PURE__ */ t("tr", { children: e.map((s) => /* @__PURE__ */ t("td", { children: s.render(l) }, s.key)) }, n(l))) })
  ] }) });
}
function ie({ children: e, title: r }) {
  return /* @__PURE__ */ i("section", { className: "tigrbl-panel", children: [
    /* @__PURE__ */ t("h2", { children: r }),
    e
  ] });
}
function se({
  actions: e,
  children: r,
  description: n,
  onClose: a,
  open: l,
  title: s
}) {
  return l ? /* @__PURE__ */ t("div", { className: "tigrbl-drawer-backdrop", role: "presentation", children: /* @__PURE__ */ i("aside", { "aria-modal": "true", className: "tigrbl-drawer", role: "dialog", children: [
    /* @__PURE__ */ i("header", { className: "tigrbl-drawer-header", children: [
      /* @__PURE__ */ i("div", { children: [
        /* @__PURE__ */ t("h2", { children: s }),
        n && /* @__PURE__ */ t("p", { children: n })
      ] }),
      /* @__PURE__ */ t(d, { onClick: a, type: "button", variant: "subtle", children: "Close" })
    ] }),
    /* @__PURE__ */ t("div", { className: "tigrbl-drawer-body", children: r }),
    e && /* @__PURE__ */ t("footer", { className: "tigrbl-drawer-actions", children: e })
  ] }) }) : null;
}
function q({
  error: e,
  help: r,
  label: n,
  ...a
}) {
  return /* @__PURE__ */ i("label", { className: "tigrbl-field", children: [
    /* @__PURE__ */ i("span", { className: "tigrbl-field-label", children: [
      /* @__PURE__ */ t("span", { children: n }),
      e && /* @__PURE__ */ t(I, { children: e })
    ] }),
    /* @__PURE__ */ t("input", { ...a, "aria-invalid": e ? "true" : a["aria-invalid"] }),
    r && /* @__PURE__ */ t("small", { className: "tigrbl-field-help", children: r })
  ] });
}
function ce({ children: e }) {
  return /* @__PURE__ */ t("p", { className: "tigrbl-form-error", children: e });
}
function I({ children: e }) {
  return /* @__PURE__ */ t("span", { className: "tigrbl-validation-message", children: e });
}
function oe({
  children: e,
  label: r,
  ...n
}) {
  return /* @__PURE__ */ t("button", { ...n, "aria-label": r, className: `tigrbl-icon-button ${n.className ?? ""}`.trim(), title: r, children: e });
}
function v({ message: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ t("div", { className: `tigrbl-toast tigrbl-toast-${r}`, children: e });
}
function de({
  error: e,
  success: r
}) {
  return e ? /* @__PURE__ */ t(v, { message: e, tone: "danger" }) : r ? /* @__PURE__ */ t(v, { message: r, tone: "success" }) : null;
}
function ue(e) {
  return /* @__PURE__ */ t(q, { ...e });
}
function he({ value: e }) {
  return /* @__PURE__ */ t("pre", { className: "tigrbl-json", children: JSON.stringify(e, null, 2) });
}
function be({
  description: e,
  label: r,
  value: n,
  ...a
}) {
  return /* @__PURE__ */ i("article", { ...a, className: `tigrbl-metric-card ${a.className ?? ""}`.trim(), children: [
    /* @__PURE__ */ t("p", { className: "tigrbl-metric-card-label", children: r }),
    /* @__PURE__ */ t("strong", { className: "tigrbl-metric-card-value", children: n }),
    e && /* @__PURE__ */ t("p", { className: "tigrbl-metric-card-description", children: e })
  ] });
}
function S({
  children: e,
  description: r,
  onClose: n,
  open: a,
  title: l
}) {
  return /* @__PURE__ */ i(k, { onClose: n, open: a, title: l, children: [
    r && /* @__PURE__ */ t("p", { className: "tigrbl-dialog-description", children: r }),
    e
  ] });
}
function ge(e) {
  return /* @__PURE__ */ t(S, { ...e });
}
function me(e) {
  return /* @__PURE__ */ t(S, { ...e });
}
function fe({
  actions: e,
  columns: r,
  emptyBody: n,
  emptyTitle: a,
  getRowKey: l,
  items: s
}) {
  const c = e != null && e.length ? [
    ...r,
    {
      header: "Actions",
      key: "actions",
      render: (o) => /* @__PURE__ */ t("div", { className: "tigrbl-row-actions", children: e.map((b) => /* @__PURE__ */ t(
        "button",
        {
          className: `tigrbl-row-action tigrbl-row-action-${b.tone ?? "subtle"}`,
          onClick: () => b.onClick(o),
          type: "button",
          children: b.label
        },
        b.label
      )) })
    }
  ] : r;
  return /* @__PURE__ */ t(
    j,
    {
      columns: c,
      empty: /* @__PURE__ */ t(N, { title: a ?? "No resources", body: n ?? "Create a resource to begin." }),
      getRowKey: l,
      items: s
    }
  );
}
function Ne({
  actions: e,
  children: r,
  createLabel: n,
  description: a,
  onCreate: l,
  title: s
}) {
  return /* @__PURE__ */ i("div", { className: "tigrbl-resource-toolbar", children: [
    /* @__PURE__ */ i("div", { className: "tigrbl-resource-toolbar-copy", children: [
      s && /* @__PURE__ */ t("h2", { children: s }),
      a && /* @__PURE__ */ t("p", { children: a }),
      r
    ] }),
    /* @__PURE__ */ i("div", { className: "tigrbl-resource-toolbar-actions", children: [
      e,
      l && /* @__PURE__ */ t(d, { onClick: l, type: "button", children: n ?? "Create" })
    ] })
  ] });
}
function pe({ label: e, value: r }) {
  const [n, a] = h(!1);
  return /* @__PURE__ */ i("div", { className: "tigrbl-secret", children: [
    /* @__PURE__ */ t("span", { children: e }),
    /* @__PURE__ */ t("code", { children: n ? r : "••••••••••••" }),
    /* @__PURE__ */ t(d, { onClick: () => a((l) => !l), type: "button", variant: "subtle", children: n ? "Hide" : "Show" })
  ] });
}
function ye({
  help: e,
  label: r,
  options: n,
  ...a
}) {
  return /* @__PURE__ */ i("label", { className: "tigrbl-field", children: [
    /* @__PURE__ */ t("span", { className: "tigrbl-field-label", children: r }),
    /* @__PURE__ */ t("select", { ...a, children: n.map((l) => /* @__PURE__ */ t("option", { value: l.value, children: l.label }, l.value)) }),
    e && /* @__PURE__ */ t("span", { className: "tigrbl-field-help", children: e })
  ] });
}
function ve({
  children: e,
  icon: r,
  label: n,
  ...a
}) {
  return /* @__PURE__ */ i("button", { ...a, className: `tigrbl-social-button ${a.className ?? ""}`.trim(), type: a.type ?? "button", children: [
    r && /* @__PURE__ */ t("span", { "aria-hidden": "true", className: "tigrbl-social-button-icon", children: r }),
    /* @__PURE__ */ t("span", { children: e ?? `Continue with ${n}` })
  ] });
}
function we({ children: e, tone: r = "neutral" }) {
  return /* @__PURE__ */ t("span", { className: `tigrbl-badge tigrbl-badge-${r}`, children: e });
}
function Ce({
  children: e,
  loading: r = !1,
  loadingLabel: n = "Working...",
  ...a
}) {
  return /* @__PURE__ */ t(d, { ...a, disabled: r || a.disabled, type: a.type ?? "submit", children: r ? n : e });
}
function ke({ activeHref: e, items: r }) {
  return /* @__PURE__ */ t("nav", { className: "tigrbl-tabs", children: r.map((n) => /* @__PURE__ */ t("a", { "aria-current": e === n.href ? "page" : void 0, href: n.href, children: n.label }, n.href)) });
}
function Se({
  description: e,
  label: r,
  ...n
}) {
  return /* @__PURE__ */ i("label", { className: "tigrbl-toggle-field", children: [
    /* @__PURE__ */ i("span", { className: "tigrbl-toggle-copy", children: [
      /* @__PURE__ */ t("span", { className: "tigrbl-toggle-label", children: r }),
      e && /* @__PURE__ */ t("span", { className: "tigrbl-toggle-description", children: e })
    ] }),
    /* @__PURE__ */ i("span", { className: "tigrbl-toggle-control", children: [
      /* @__PURE__ */ t("input", { ...n, type: "checkbox" }),
      /* @__PURE__ */ t("span", { "aria-hidden": "true", className: "tigrbl-toggle-track", children: /* @__PURE__ */ t("span", { className: "tigrbl-toggle-thumb" }) })
    ] })
  ] });
}
function $e({ children: e }) {
  return /* @__PURE__ */ t("div", { className: "tigrbl-toolbar", children: e });
}
function Ae(e) {
  return /* @__PURE__ */ t("textarea", { ...e, className: `tigrbl-json-editor ${e.className ?? ""}`.trim(), spellCheck: !1 });
}
function xe({
  children: e,
  footer: r,
  ...n
}) {
  return /* @__PURE__ */ i("form", { ...n, className: `tigrbl-resource-form ${n.className ?? ""}`.trim(), children: [
    /* @__PURE__ */ t("div", { className: "tigrbl-resource-form-fields", children: e }),
    r && /* @__PURE__ */ t("footer", { children: r })
  ] });
}
function Ee(e) {
  const [r, n] = h(null), [a, l] = h(!1);
  async function s(...c) {
    n(null), l(!0);
    try {
      return await e(...c);
    } catch (o) {
      return n(o instanceof Error ? o.message : "Request failed"), null;
    } finally {
      l(!1);
    }
  }
  return { error: r, loading: a, run: s };
}
function Te(e, r = []) {
  const [n, a] = h({ data: null, error: null, loading: !0 });
  return R(() => {
    const l = new AbortController();
    return a((s) => ({ ...s, error: null, loading: !0 })), e(l.signal).then((s) => a({ data: s, error: null, loading: !1 })).catch((s) => {
      l.signal.aborted || a({ data: null, error: s instanceof Error ? s.message : "Request failed", loading: !1 });
    }), () => l.abort();
  }, r), n;
}
function Pe() {
  return m().session;
}
function Re(e, r = {}) {
  const [n, a] = h(null), [l, s] = h(!1), [c, o] = h(null), b = p(() => {
    a(null), o(null);
  }, []), $ = p(
    async (...A) => {
      a(null), o(null), s(!0);
      try {
        const g = await e(...A);
        return r.successMessage && o(
          typeof r.successMessage == "function" ? r.successMessage(g) : r.successMessage
        ), g;
      } catch (g) {
        return a(g instanceof Error ? g.message : "Request failed"), null;
      } finally {
        s(!1);
      }
    },
    [e, r.successMessage]
  );
  return { error: n, loading: l, reset: b, run: $, success: c };
}
function Me() {
  const { session: e } = m(), r = (e == null ? void 0 : e.permissions) ?? [];
  return {
    permissions: r,
    hasAny: (n) => B(r, n),
    hasEvery: (n) => C(r, n)
  };
}
function De() {
  const { session: e } = m();
  return {
    tenantId: (e == null ? void 0 : e.tenantId) ?? null,
    hasTenantContext: !!(e != null && e.tenantId)
  };
}
function L({
  activeHref: e,
  apiBaseUrl: r,
  items: n,
  productApi: a,
  title: l
}) {
  return /* @__PURE__ */ i("aside", { className: "tigrbl-sidebar", children: [
    /* @__PURE__ */ t("p", { className: "tigrbl-sidebar-product", children: a }),
    /* @__PURE__ */ t("h1", { children: l }),
    /* @__PURE__ */ t("nav", { children: n.map((s) => {
      const c = e === s.href || e.startsWith(`${s.href}/`);
      return /* @__PURE__ */ i("a", { "aria-current": c ? "page" : void 0, href: s.href, children: [
        /* @__PURE__ */ t("span", { children: s.label }),
        s.badge && /* @__PURE__ */ t("small", { children: s.badge })
      ] }, s.href);
    }) }),
    r && /* @__PURE__ */ i("p", { className: "tigrbl-sidebar-api", children: [
      "API: ",
      /* @__PURE__ */ t("code", { children: r })
    ] })
  ] });
}
function z({ onLogout: e, sessionLabel: r }) {
  return /* @__PURE__ */ i("header", { className: "tigrbl-topbar", children: [
    /* @__PURE__ */ t("span", { children: r ?? "No active session" }),
    e && /* @__PURE__ */ t(d, { onClick: e, type: "button", variant: "subtle", children: "Sign out" })
  ] });
}
function Ue({
  activeHref: e,
  apiBaseUrl: r,
  children: n,
  navigation: a,
  onLogout: l,
  productApi: s,
  sessionLabel: c,
  title: o
}) {
  return /* @__PURE__ */ i("main", { className: "tigrbl-shell", children: [
    /* @__PURE__ */ t(L, { activeHref: e, apiBaseUrl: r, items: a, productApi: s, title: o }),
    /* @__PURE__ */ i("section", { className: "tigrbl-shell-main", children: [
      /* @__PURE__ */ t(z, { onLogout: l, sessionLabel: c }),
      /* @__PURE__ */ t("div", { className: "tigrbl-shell-content", children: n })
    ] })
  ] });
}
function J({
  label: e = "Tigrbl Auth",
  logoLetter: r
}) {
  const n = r ?? (e.trim().charAt(0).toUpperCase() || "T");
  return /* @__PURE__ */ i("div", { className: "tigrbl-brand-mark", children: [
    /* @__PURE__ */ t("span", { className: "tigrbl-brand-mark-glyph", children: n }),
    /* @__PURE__ */ t("span", { className: "tigrbl-brand-mark-label", children: e })
  ] });
}
function W({
  actions: e,
  label: r = "Tigrbl Auth",
  logoLetter: n
}) {
  return /* @__PURE__ */ i("header", { className: "tigrbl-brand-header", children: [
    /* @__PURE__ */ t(J, { label: r, logoLetter: n }),
    e && /* @__PURE__ */ t("nav", { className: "tigrbl-brand-header-actions", children: e })
  ] });
}
function Be({
  children: e,
  footer: r,
  productApi: n,
  subtitle: a,
  title: l
}) {
  return /* @__PURE__ */ i("main", { className: "tigrbl-auth-shell", children: [
    /* @__PURE__ */ t(W, { label: "Tigrbl Auth" }),
    /* @__PURE__ */ i("section", { className: "tigrbl-auth-shell-content", children: [
      /* @__PURE__ */ i("div", { className: "tigrbl-auth-copy", children: [
        n && /* @__PURE__ */ t("p", { className: "tigrbl-eyebrow", children: n }),
        /* @__PURE__ */ t("h1", { children: l }),
        a && /* @__PURE__ */ t("p", { children: a })
      ] }),
      e
    ] }),
    /* @__PURE__ */ t("footer", { className: "tigrbl-auth-footer", children: r ?? /* @__PURE__ */ i("span", { children: [
      "© ",
      (/* @__PURE__ */ new Date()).getFullYear(),
      " Tigrbl Auth"
    ] }) })
  ] });
}
function Fe({ items: e }) {
  return /* @__PURE__ */ t("nav", { "aria-label": "Breadcrumbs", className: "tigrbl-breadcrumbs", children: e.map((r, n) => /* @__PURE__ */ t("a", { href: r.href, "aria-current": n === e.length - 1 ? "page" : void 0, children: r.label }, r.href)) });
}
function je({
  actions: e,
  description: r,
  title: n
}) {
  return /* @__PURE__ */ i("header", { className: "tigrbl-page-header", children: [
    /* @__PURE__ */ i("div", { children: [
      /* @__PURE__ */ t("h1", { children: n }),
      r && /* @__PURE__ */ t("p", { children: r })
    ] }),
    e && /* @__PURE__ */ t("div", { className: "tigrbl-page-actions", children: e })
  ] });
}
export {
  O as ApiClient,
  M as ApiError,
  _ as ApiErrorNotice,
  Ue as AppShell,
  Y as AuthProvider,
  Be as AuthShell,
  W as BrandHeader,
  J as BrandMark,
  Fe as Breadcrumbs,
  d as Button,
  ee as Card,
  re as Checkbox,
  ne as CodeField,
  te as ConfirmDialog,
  ae as CopyButton,
  ge as CreateResourceDialog,
  le as DangerZone,
  j as DataTable,
  se as DetailDrawer,
  ie as DetailPanel,
  me as EditResourceDialog,
  N as EmptyState,
  F as ErrorState,
  ce as FormError,
  q as FormField,
  oe as IconButton,
  de as InlineMutationResult,
  ue as Input,
  Ae as JsonEditor,
  he as JsonViewer,
  be as MetricCard,
  k as Modal,
  je as PageHeader,
  Z as PermissionGate,
  K as RequireAuth,
  xe as ResourceForm,
  fe as ResourceTable,
  Ne as ResourceToolbar,
  pe as SecretField,
  ye as SelectField,
  L as Sidebar,
  ve as SocialButton,
  we as StatusBadge,
  Ce as SubmitButton,
  ke as Tabs,
  v as Toast,
  Se as ToggleField,
  $e as Toolbar,
  z as Topbar,
  I as ValidationMessage,
  D as assertSurfacePath,
  U as createSurfaceUrl,
  X as describeSession,
  Q as encodeCursorParams,
  B as hasAnyPermission,
  C as hasEveryPermission,
  Ee as useApiMutation,
  Te as useApiQuery,
  m as useAuthContext,
  Pe as useCurrentUser,
  Re as useMutationState,
  Me as usePermissions,
  De as useTenantContext
};
