import type { ReactNode } from "react";
import { API_BASE_URL, PRODUCT_API, SURFACE_PURPOSE } from "../services/backendSurface";
import type { AdminSession } from "../types";
import { Button } from "./UI";

const nav = [
  ["#/tenants", "Tenants"],
  ["#/identities", "Identities"],
  ["#/audit", "Audit"]
];

export function Layout({
  currentHash,
  session,
  onLogout,
  children
}: {
  currentHash: string;
  session: AdminSession | null;
  onLogout: () => void;
  children: ReactNode;
}) {
  return (
    <main style={{ minHeight: "100vh", background: "#f7f8f5", color: "#17211d", fontFamily: "Aptos, Segoe UI, sans-serif" }}>
      <aside
        style={{
          borderRight: "1px solid #d9e1dc",
          bottom: 0,
          left: 0,
          padding: "22px 18px",
          position: "fixed",
          top: 0,
          width: "260px"
        }}
      >
        <p style={{ color: "#4b6a5f", fontSize: "0.72rem", letterSpacing: "0.12em", margin: 0, textTransform: "uppercase" }}>{PRODUCT_API}</p>
        <h1 style={{ fontSize: "1.45rem", lineHeight: 1.1, margin: "10px 0 8px" }}>Platform Admin</h1>
        <p style={{ color: "#4b5f58", fontSize: "0.9rem", margin: "0 0 18px" }}>{SURFACE_PURPOSE}</p>
        <nav style={{ display: "grid", gap: "8px", marginTop: "20px" }}>
          {nav.map(([href, label]) => {
            const active = currentHash.startsWith(href);
            return (
              <a
                key={href}
                href={href}
                style={{
                  background: active ? "#14342b" : "transparent",
                  borderRadius: "6px",
                  color: active ? "#ffffff" : "#20362f",
                  padding: "9px 10px",
                  textDecoration: "none"
                }}
              >
                {label}
              </a>
            );
          })}
        </nav>
        <div style={{ borderTop: "1px solid #d9e1dc", bottom: "18px", left: "18px", paddingTop: "14px", position: "absolute", right: "18px" }}>
          <p style={{ color: "#60766e", fontSize: "0.78rem", margin: "0 0 8px" }}>API: <code>{API_BASE_URL}</code></p>
          {session?.authenticated ? (
            <>
              <p style={{ fontSize: "0.88rem", margin: "0 0 10px" }}>{session.username || session.email}</p>
              <Button variant="subtle" onClick={onLogout}>Sign out</Button>
            </>
          ) : (
            <p style={{ color: "#8f1f2d", fontSize: "0.88rem", margin: 0 }}>Admin session required</p>
          )}
        </div>
      </aside>
      <section style={{ marginLeft: "260px", padding: "28px", minHeight: "100vh" }}>
        <div style={{ margin: "0 auto", maxWidth: "1120px" }}>{children}</div>
      </section>
    </main>
  );
}
