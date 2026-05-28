import type { ReactNode } from "react";
import { PRODUCT_API, PRODUCT_SURFACE } from "../defaults";

const tabs = [
  ["#/profile", "Profile"],
  ["#/security", "Security"],
  ["#/sessions", "Sessions"],
  ["#/apps", "Authorized Apps"]
];

export function Layout({
  children,
  currentHash
}: {
  children: ReactNode;
  currentHash: string;
}) {
  return (
    <main
      style={{
        background: "#f5f7f2",
        color: "#102620",
        fontFamily: "Aptos, Segoe UI, sans-serif",
        minHeight: "100vh"
      }}
    >
      <header style={{ borderBottom: "1px solid #c9d8d2", padding: "22px min(5vw, 42px)" }}>
        <p style={{ color: "#4f6d63", fontSize: "0.78rem", letterSpacing: "0.12em", margin: 0, textTransform: "uppercase" }}>
          {PRODUCT_SURFACE}
        </p>
        <h1 style={{ fontSize: "clamp(2rem, 5vw, 3.75rem)", letterSpacing: 0, lineHeight: 1, margin: "8px 0" }}>
          My Account
        </h1>
        <p style={{ color: "#4f6d63", margin: 0 }}>{PRODUCT_API}</p>
      </header>
      <nav
        aria-label="Account sections"
        style={{
          borderBottom: "1px solid #d8e2dd",
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          padding: "12px min(5vw, 42px)"
        }}
      >
        {tabs.map(([href, label]) => {
          const active = currentHash.startsWith(href);
          return (
            <a
              key={href}
              href={href}
              style={{
                background: active ? "#102620" : "#ffffff",
                border: "1px solid #b8cac3",
                borderRadius: "8px",
                color: active ? "#ffffff" : "#102620",
                padding: "9px 12px",
                textDecoration: "none"
              }}
            >
              {label}
            </a>
          );
        })}
      </nav>
      <div style={{ margin: "0 auto", maxWidth: "980px", padding: "20px min(5vw, 42px)" }}>{children}</div>
    </main>
  );
}
