import { API_BASE_URL, PRODUCT_API, SURFACE_PURPOSE } from "./services/backendSurface";

const workflows = [
  "Register OIDC/OAuth applications",
  "Manage redirect URIs, metadata, secrets, and JWKS",
  "Inspect tenant-backed federation discovery for apps",
];

export default function App() {
  return (
    <main style={{ minHeight: "100vh", padding: "3rem", fontFamily: "Aptos, Segoe UI, sans-serif", background: "#eef3ff", color: "#131f33" }}>
      <section style={{ maxWidth: "860px" }}>
        <p style={{ margin: 0, letterSpacing: "0.18em", textTransform: "uppercase", color: "#315ca6" }}>{PRODUCT_API}</p>
        <h1 style={{ fontSize: "clamp(2.4rem, 7vw, 5rem)", lineHeight: 0.95, margin: "0.7rem 0" }}>Developer Portal</h1>
        <p style={{ fontSize: "1.2rem", maxWidth: "680px" }}>{SURFACE_PURPOSE}</p>
        <p>
          API base: <code>{API_BASE_URL}</code>
        </p>
        <div style={{ display: "grid", gap: "1rem", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", marginTop: "2rem" }}>
          {workflows.map((workflow) => (
            <article key={workflow} style={{ border: "1px solid #aebfe5", borderRadius: "18px", padding: "1rem", background: "#fbfdff" }}>
              {workflow}
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
